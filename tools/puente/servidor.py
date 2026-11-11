#!/usr/bin/env python3
"""Puente de mando de la Flota: una vista en vivo (localhost, solo lectura) de cómo está trabajando todo.

Lee lo que ya existe en la máquina, sin tocar nada:
  · el manifiesto del cliente (estaciones, coordinador, naves y sus nombres),
  · los faros de cada perfil (cron/jobs.json y su última salida),
  · el Ágora (todos los tableros vivos del Kanban),
  · el historial de cada perfil (state.db: quién está trabajando ahora y el consumo del día),
  · el gateway, los servicios de usuario, la corriente y el último respaldo.

Uso:  servidor.py <manifiesto.yaml> [--puerto 7171]
Se ata a localhost (loopback): no queda expuesto a la red. Si el manifiesto no trae «alias», muestra nombres funcionales."""
import argparse, datetime as dt, glob, json, os, re, sqlite3, subprocess, sys, threading, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import yaml

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
FLOTA = RAIZ / "flota"
sys.path.insert(0, str(FLOTA / "naves" / "_comun"))
from agora import tableros, filas  # noqa: E402
import avance as AV  # noqa: E402

H = Path(os.path.expanduser("~/.hermes"))
PREFIJO = "Flota · "
ZONA = dt.timezone(dt.timedelta(hours=-5))


def home_de(perfil):
    return H if perfil == "default" else H / "profiles" / perfil


def ts(v):
    """ISO o epoch → epoch (float) o None."""
    if v in (None, ""):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return dt.datetime.fromisoformat(str(v)).timestamp()
    except Exception:
        return None


def leer_json(p, defecto=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return defecto


# ───────────────────────── catálogo y manifiesto ─────────────────────────
class Flota:
    def __init__(self, manifiesto):
        self.ruta = Path(manifiesto).resolve()
        self.cargar()

    def cargar(self):
        self.man = yaml.safe_load(self.ruta.read_text(encoding="utf-8"))
        sec = (yaml.safe_load((FLOTA / "sectores.yaml").read_text(encoding="utf-8")) or {}).get("sectores", {}) \
            if (FLOTA / "sectores.yaml").exists() else {}
        self.sectores = sec if isinstance(sec, dict) else {s["id"]: s for s in sec}
        self.catalogo = {}
        for f in glob.glob(str(FLOTA / "naves" / "*" / "*.yaml")):
            d = yaml.safe_load(Path(f).read_text(encoding="utf-8")) or {}
            if d.get("id"):
                self.catalogo[d["id"]] = d
        self.estaciones = self.man.get("estaciones", [])
        self.coord = self.man.get("coordinador")
        self.mtime = self.ruta.stat().st_mtime

    def refrescar(self):
        if self.ruta.stat().st_mtime != self.mtime:
            self.cargar()

    def estacion_de_nave(self, nave):
        if nave.get("la_ejecuta") == "coordinador":
            for e in self.estaciones:
                if e["id"] == self.coord:
                    return e
        for e in self.estaciones:
            if e.get("tipo") == nave.get("la_ejecuta"):
                return e
        return None

    def ficha_de_job(self, perfil, job):
        """Devuelve (alias, nombre, sector, en_manifiesto) para un faro."""
        f = (self.man.get("faros") or {}).get(job["id"])
        if f:
            return f.get("alias"), f.get("nombre") or job["name"], f.get("sector"), True
        if job["name"].startswith(PREFIJO):
            nombre = job["name"][len(PREFIJO):]
            for item in self.man.get("naves") or []:
                n = self.catalogo.get(item["id"])
                if not n:
                    continue
                est = self.estacion_de_nave(n)
                if est and est["perfil_hermes"] == perfil and (item.get("nombre") or n.get("nombre_visible")) == nombre:
                    return item.get("alias"), nombre, n.get("sector"), True
            return None, nombre, None, False
        return None, job["name"], None, False


# ───────────────────────── lectura del estado ─────────────────────────
def servicios():
    out = {}
    for s in ("hermes-gateway", "flota-despierta", "cogsmos-puente"):
        try:
            r = subprocess.run(["systemctl", "--user", "is-active", f"{s}.service"], capture_output=True, text=True, timeout=5)
            out[s] = r.stdout.strip() or "desconocido"
        except Exception:
            out[s] = "desconocido"
    return out


def energia():
    base = Path("/sys/class/power_supply")
    ac = bat = None
    for p in base.glob("*"):
        try:
            t = (p / "type").read_text().strip()
            if t == "Mains":
                ac = (p / "online").read_text().strip() == "1"
            elif t == "Battery":
                bat = int((p / "capacity").read_text().strip())
        except Exception:
            pass
    return {"corriente": ac, "bateria": bat}


def respaldo():
    fs = sorted(glob.glob(str(H / "backups" / "fenix" / "flota-*.tgz")))
    if not fs:
        return None
    f = Path(fs[-1])
    return {"archivo": f.name, "bytes": f.stat().st_size, "ts": f.stat().st_mtime, "copias": len(fs)}


def actividad_perfil(perfil, hoy0):
    db = home_de(perfil) / "state.db"
    res = {"sesiones_hoy": 0, "tokens_hoy": 0, "costo_hoy": 0.0, "activas": []}
    if not db.exists():
        return res
    try:
        r = filas(str(db), "select count(*) n, coalesce(sum(input_tokens+output_tokens),0) t, coalesce(sum(estimated_cost_usd),0) c "
                           "from sessions where started_at >= ?", (hoy0,))
        if r:
            res.update(sesiones_hoy=r[0]["n"], tokens_hoy=int(r[0]["t"] or 0), costo_hoy=round(float(r[0]["c"] or 0), 3))
        ahora = time.time()
        for s in filas(str(db), "select id, source, coalesce(title,'') title, last_activity_at, started_at, "
                                "coalesce(last_activity_description,'') que from sessions "
                                "where ended_at is null and last_activity_at > ? and source != 'subagent' "
                                "order by last_activity_at desc limit 6", (ahora - 180,)):
            res["activas"].append({"fuente": s["source"], "titulo": s["title"][:90], "que": s["que"][:120],
                                   "desde": s["started_at"], "ultimo": s["last_activity_at"]})
    except Exception as e:
        res["error"] = str(e)[:120]
    return res


def ultima_salida(perfil, job_id):
    d = home_de(perfil) / "cron" / "output" / job_id
    fs = sorted(d.glob("*.md")) if d.exists() else []
    return fs


def estado_naves(flota, actividad):
    naves = []
    for e in flota.estaciones:
        perfil = e["perfil_hermes"]
        jobs = (leer_json(home_de(perfil) / "cron" / "jobs.json", {}) or {}).get("jobs", [])
        corriendo = {a["titulo"].split(" · ")[0] for a in actividad.get(perfil, {}).get("activas", []) if a["fuente"] == "cron"}
        for j in jobs:
            activo = j.get("enabled", True) and j.get("state") != "paused"
            alias, nombre, sector, en_man = flota.ficha_de_job(perfil, j)
            if not activo and not en_man:
                continue  # copias viejas pausadas: no son parte de la flota
            ult = ts(j.get("last_run_at"))
            fallo = bool(j.get("last_error") or j.get("last_delivery_error") or (j.get("failure_streak") or 0) > 0
                         or (j.get("last_status") or "") in ("error", "failed"))
            if not activo:
                st = "pausada"
            elif j["name"] in corriendo:
                st = "corriendo"
            elif fallo:
                st = "fallo"
            else:
                st = "activa"
            sal = ultima_salida(perfil, j["id"])
            silencio = None
            if sal:
                cab = sal[-1].read_text(encoding="utf-8", errors="replace")[:600]
                silencio = "silent" in cab.lower()
            naves.append({
                "id": j["id"], "perfil": perfil, "estacion": e["id"], "alias": alias, "nombre": nombre,
                "sector": sector, "horario": j.get("schedule_display"), "estado": st,
                "ultimo": ult, "ultimo_estado": j.get("last_status"), "proximo": ts(j.get("next_run_at")),
                "error": (j.get("last_error") or j.get("last_delivery_error") or "")[:240],
                "sin_modelo": bool(j.get("no_agent")), "repeticiones": (j.get("repeat") or {}).get("times"),
                "ultimo_silencio": silencio,
            })
    return naves


def reserva(flota):
    """Naves con nombre en el glosario/manifiesto que aún no tienen faro (declaradas en `reserva:` del manifiesto)."""
    return flota.man.get("reserva") or []


def estado_agora(flota):
    est_por_perfil = {e["perfil_hermes"]: e["id"] for e in flota.estaciones}
    tareas, conteo, por_tablero, eventos = [], {}, {}, []
    ahora = time.time()
    for slug, db in tableros().items():
        try:
            ts_ = filas(db, "select id,title,status,assignee,created_by,created_at,started_at,completed_at,"
                            "consecutive_failures,block_recurrences from tasks where status != 'archived'")
        except Exception:
            continue
        pt = {}
        for t in ts_:
            conteo[t["status"]] = conteo.get(t["status"], 0) + 1
            pt[t["status"]] = pt.get(t["status"], 0) + 1
            if t["status"] in ("running", "ready", "blocked", "review", "triage") or \
               (t["status"] == "done" and (t["completed_at"] or 0) > ahora - 86400 and t["assignee"]):
                tareas.append({
                    "id": t["id"], "tablero": slug, "titulo": t["title"], "estado": t["status"],
                    "asignada": t["assignee"], "estacion": est_por_perfil.get(t["assignee"] or ""),
                    "creada": t["created_at"], "inicio": t["started_at"], "fin": t["completed_at"],
                    "creada_por": t["created_by"], "fallos": t["consecutive_failures"] or 0,
                    "rebloqueos": t["block_recurrences"] or 0,
                })
        por_tablero[slug] = pt
        try:
            for ev in filas(db, "select e.kind, e.created_at, e.task_id, coalesce(t.title,'') title, t.assignee "
                                "from task_events e left join tasks t on t.id=e.task_id "
                                "where e.kind in ('created','claimed','completed','blocked','unblocked','assigned','promoted',"
                                "'spawned','worker_result','reclaimed','archived','commented') "
                                "order by e.created_at desc limit 25"):
                eventos.append({"tipo": "tarea", "clase": ev["kind"], "ts": ev["created_at"], "tablero": slug,
                                "id": ev["task_id"], "titulo": ev["title"][:90], "asignada": ev["assignee"]})
        except Exception:
            pass
    # «Esperando tu OK» y «Atascadas» con las mismas reglas que Eos y Sísifo
    espera, atascadas = [], []
    for t in tareas:
        if t["estado"] == "blocked" and t["asignada"] and t["creada_por"] == "flota":
            espera.append({**t, "motivo": "para soltar"})
        elif t["estado"] == "review":
            espera.append({**t, "motivo": "en revisión"})
        elif t["titulo"].startswith("⛔") and not t["asignada"] and t["estado"] == "ready":
            espera.append({**t, "motivo": "visto bueno"})
        razones = []
        if t["estado"] == "blocked" and t["asignada"] and (t["creada"] or ahora) < ahora - 3 * 86400:
            razones.append("bloqueada > 3 d")
        if t["rebloqueos"] >= 2:
            razones.append(f"{t['rebloqueos']} rebloqueos")
        if t["fallos"] >= 2:
            razones.append(f"{t['fallos']} fallos")
        if t["estado"] == "running" and t["inicio"] and ahora - t["inicio"] > 6 * 3600:
            razones.append("corriendo > 6 h")
        if t["estado"] == "triage":
            razones.append("en triage")
        if razones:
            atascadas.append({**t, "motivo": ", ".join(razones)})
    eventos.sort(key=lambda x: x["ts"] or 0, reverse=True)
    return {"conteo": conteo, "tableros": por_tablero, "tareas": tareas, "espera": espera,
            "atascadas": atascadas, "eventos": eventos[:40]}


def clave_personaje(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def personajes_dir(flota):
    d = flota.man.get("personajes")
    return Path(os.path.expanduser(d)) if d and Path(os.path.expanduser(d)).is_dir() else None


def personajes(flota):
    """{clave: url} de los retratos disponibles (clave = alias o nombre de la estación, sin tildes)."""
    d = personajes_dir(flota)
    if not d:
        return {}
    out = {}
    for f in sorted(d.iterdir()):
        if re.fullmatch(r"[a-z0-9_-]+\.(png|jpg|webp)", f.name):
            out[f.name.rsplit(".", 1)[0]] = f"/personajes/{f.name}"
    return out


def instantanea(flota):
    flota.refrescar()
    hoy0 = dt.datetime.now(ZONA).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    gw = leer_json(H / "gateway_state.json", {}) or {}
    plats = {k: (v or {}).get("state") for k, v in (gw.get("platforms") or {}).items()}
    actividad = {e["perfil_hermes"]: actividad_perfil(e["perfil_hermes"], hoy0) for e in flota.estaciones}
    naves = estado_naves(flota, actividad)
    agora = estado_agora(flota)
    estaciones = []
    for e in flota.estaciones:
        p = e["perfil_hermes"]
        clave = "telegram" if p == "default" else f"{p}:telegram"
        estaciones.append({
            "id": e["id"], "perfil": p, "nombre": e.get("nombre_visible", p), "tipo": e.get("tipo"),
            "coordinador": e["id"] == flota.coord, "bot": plats.get(clave),
            "servida": p in (gw.get("served_profiles") or []), "actividad": actividad[p],
            "misiones": {s: sum(1 for t in agora["tareas"] if t["asignada"] == p and t["estado"] == s)
                         for s in ("running", "ready", "blocked", "review")},
        })
    # bitácora: eventos del Ágora + corridas de faros de las últimas 24 h
    bit = list(agora["eventos"])
    for n in naves:
        if n["ultimo"] and n["ultimo"] > time.time() - 86400:
            bit.append({"tipo": "faro", "clase": "fallo" if n["estado"] == "fallo" else ("silencio" if n["ultimo_silencio"] else "aviso"),
                        "ts": n["ultimo"], "titulo": n["alias"] or n["nombre"], "nombre": n["nombre"],
                        "estacion": n["estacion"], "id": n["id"], "perfil": n["perfil"], "sin_modelo": n["sin_modelo"]})
    bit.sort(key=lambda x: x["ts"] or 0, reverse=True)
    return {
        "ahora": time.time(), "cliente": flota.man.get("cliente"), "capitan": flota.man.get("capitan"),
        "lore": any(n.get("alias") for n in naves),
        "estaciones": estaciones, "naves": naves, "reserva": reserva(flota),
        "sectores": {k: v.get("nombre", k) for k, v in flota.sectores.items()},
        "personajes": personajes(flota),
        "agora": {k: agora[k] for k in ("conteo", "tableros", "tareas", "espera", "atascadas")},
        "bitacora": bit[:45],
        "sistema": {"gateway": gw.get("gateway_state") or gw.get("state"), "plataformas": plats,
                    "servicios": servicios(), "energia": energia(), "respaldo": respaldo()},
    }


def detalle_nave(flota, perfil, jid):
    if perfil not in {e["perfil_hermes"] for e in flota.estaciones} or not re.fullmatch(r"[0-9a-f]{12}", jid or ""):
        return None
    jobs = (leer_json(home_de(perfil) / "cron" / "jobs.json", {}) or {}).get("jobs", [])
    j = next((x for x in jobs if x["id"] == jid), None)
    if not j:
        return None
    alias, nombre, sector, _ = flota.ficha_de_job(perfil, j)
    sal = ultima_salida(perfil, jid)
    historial = []
    for f in sal[-8:]:
        cab = f.read_text(encoding="utf-8", errors="replace")[:800]
        m = re.search(r"\*\*Status:\*\*\s*([^\n]+)", cab)
        if m:
            e = m.group(1).strip()
            e = "en silencio" if e.lower().startswith("silent") else e[:40]
        else:
            e = "falló" if re.search(r"(?i)\*\*(error|failed)", cab) else "avisó"
        historial.append({"archivo": f.name, "estado": e})
    texto = ""
    if sal:
        texto = sal[-1].read_text(encoding="utf-8", errors="replace")
        texto = texto[:6000] + ("\n…" if len(texto) > 6000 else "")
    return {"id": jid, "perfil": perfil, "alias": alias, "nombre": nombre, "nombre_cron": j["name"],
            "sector": sector, "horario": j.get("schedule_display"), "zona": j.get("timezone"),
            "sin_modelo": bool(j.get("no_agent")), "script": j.get("script"), "skills": j.get("skills") or [],
            "entrega": j.get("deliver"), "estado": j.get("state"), "activo": j.get("enabled", True) and j.get("state") != "paused",
            "ultimo": ts(j.get("last_run_at")), "ultimo_estado": j.get("last_status"), "proximo": ts(j.get("next_run_at")),
            "error": j.get("last_error") or j.get("last_delivery_error"), "racha_fallos": j.get("failure_streak"),
            "instrucciones": (j.get("prompt") or "")[:1500], "historial": list(reversed(historial)), "ultima_salida": texto}


def detalle_tarea(tablero, tid):
    dbs = tableros()
    if tablero not in dbs or not re.fullmatch(r"t_[0-9a-f]{6,}", tid or ""):
        return None
    db = dbs[tablero]
    t = filas(db, "select * from tasks where id=?", (tid,))
    if not t:
        return None
    t = t[0]
    ev = filas(db, "select kind, created_at, substr(coalesce(payload,''),1,300) payload from task_events where task_id=? order by id desc limit 20", (tid,))
    com = []
    try:
        com = filas(db, "select author, body, created_at from task_comments where task_id=? order by created_at desc limit 5", (tid,))
    except Exception:
        pass
    return {"id": tid, "tablero": tablero, "titulo": t.get("title"), "estado": t.get("status"), "asignada": t.get("assignee"),
            "cuerpo": (t.get("body") or "")[:5000], "resultado": (t.get("result") or "")[:1500],
            "creada": t.get("created_at"), "inicio": t.get("started_at"), "fin": t.get("completed_at"),
            "eventos": ev, "comentarios": [{**c, "body": (c.get("body") or "")[:800]} for c in com]}


# ───────────────────────── servidor ─────────────────────────
class Puente(BaseHTTPRequestHandler):
    flota = None
    cache = {"t": 0, "d": None}
    cache_av = {"t": 0, "d": None}
    candado = threading.Lock()

    def log_message(self, *a):
        pass

    def enviar(self, codigo, cuerpo, tipo="application/json; charset=utf-8"):
        b = cuerpo if isinstance(cuerpo, bytes) else json.dumps(cuerpo, ensure_ascii=False, default=str).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            paginas = {"/": "mapa.html", "/index.html": "mapa.html", "/mapa": "mapa.html",
                       "/flujo": "flujo.html", "/resumen": "resumen.html", "/avance": "avance.html"}
            if u.path in paginas:
                return self.enviar(200, (AQUI / paginas[u.path]).read_bytes(), "text/html; charset=utf-8")
            if u.path in ("/comun.css", "/comun.js", "/piel.css"):
                tipo = "text/css; charset=utf-8" if u.path.endswith(".css") else "text/javascript; charset=utf-8"
                return self.enviar(200, (AQUI / u.path[1:]).read_bytes(), tipo)
            if u.path.startswith("/fuentes/") or u.path == "/isotipo.svg":
                nombre = u.path.rsplit("/", 1)[-1]
                f = (AQUI / "fuentes" / nombre) if u.path.startswith("/fuentes/") else AQUI / "isotipo.svg"
                if re.fullmatch(r"[A-Za-z0-9_.-]+\.(ttf|svg)", nombre) and f.is_file():
                    tipo = "font/ttf" if nombre.endswith(".ttf") else "image/svg+xml"
                    return self.enviar(200, f.read_bytes(), tipo)
                return self.enviar(404, {"error": "no encontrado"})
            if u.path == "/api/estado":
                with self.candado:
                    if time.time() - self.cache["t"] > 3 or self.cache["d"] is None:
                        self.cache["d"] = instantanea(self.flota)
                        self.cache["t"] = time.time()
                    return self.enviar(200, self.cache["d"])
            if u.path == "/api/avance":
                with self.candado:
                    if time.time() - self.cache_av["t"] > 60 or self.cache_av["d"] is None:
                        base = instantanea(self.flota)
                        ar = AV.areas(self.flota, base["naves"])
                        ind = AV.indicadores(self.flota, base["naves"], estado_agora(self.flota))
                        self.cache_av["d"] = {"ahora": time.time(), "pulso": AV.pulso(), "areas": ar, "proyectos": AV.proyectos(self.flota),
                                              "indicadores": ind, "personajes": base["personajes"],
                                              "modelo": AV.modelo(self.flota, base["naves"], base["estaciones"], ind, ar, base["personajes"])}
                        self.cache_av["t"] = time.time()
                    return self.enviar(200, self.cache_av["d"])
            if u.path.startswith("/personajes/"):
                nombre = u.path.rsplit("/", 1)[-1]; d = personajes_dir(self.flota)
                f = d / nombre if d else None
                if f and re.fullmatch(r"[a-z0-9_-]+\.(png|jpg|webp)", nombre) and f.is_file():
                    return self.enviar(200, f.read_bytes(), "image/" + ("jpeg" if nombre.endswith(".jpg") else nombre.rsplit(".", 1)[1]))
                return self.enviar(404, {"error": "no encontrado"})
            if u.path == "/api/nave":
                d = detalle_nave(self.flota, q.get("perfil"), q.get("id"))
                return self.enviar(200 if d else 404, d or {"error": "no encontrada"})
            if u.path == "/api/tarea":
                d = detalle_tarea(q.get("tablero"), q.get("id"))
                return self.enviar(200 if d else 404, d or {"error": "no encontrada"})
            return self.enviar(404, {"error": "ruta desconocida"})
        except Exception as e:
            return self.enviar(500, {"error": str(e)[:300]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifiesto")
    ap.add_argument("--puerto", type=int, default=7171)
    ap.add_argument("--una-vez", action="store_true", help="imprime la instantánea y sale (para probar)")
    a = ap.parse_args()
    Puente.flota = Flota(a.manifiesto)
    if a.una_vez:
        print(json.dumps(instantanea(Puente.flota), ensure_ascii=False, default=str, indent=1))
        return
    srv = ThreadingHTTPServer(("localhost", a.puerto), Puente)  # AF_INET → loopback IPv4
    print(f"Puente de mando en http://localhost:{a.puerto}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
