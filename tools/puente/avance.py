#!/usr/bin/env python3
"""Puente de mando · «Avance»: la evidencia de que la Flota trabaja y avanza (solo lectura).

  pulso(dias)            cuándo estuvo la máquina encendida, dormida o apagada, y qué tareas corrieron tarde
  areas(flota, naves)    por cada uno de los 9 sectores: tareas automáticas, sus corridas y las misiones
  proyectos(flota)       proyectos por fases (tabla del README) o por tablero
  indicadores(...)       los indicadores de las fichas que ya se pueden medir
  modelo(...)            el modelo de la nota contra lo instalado
"""
import datetime as dt, glob, json, os, re, subprocess, time
from pathlib import Path
from agora import tableros, filas

H = Path(os.path.expanduser("~/.hermes"))


def home_de(perfil):
    return H if perfil == "default" else H / "profiles" / perfil


def _j(cmd, timeout=20):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception:
        return ""


# ───────────── pulso 24/7 ─────────────
def pulso(dias=7):
    ahora = time.time(); desde = ahora - dias * 86400
    boots = []
    try:
        for b in json.loads(_j(["journalctl", "--list-boots", "--no-pager", "-o", "json"]) or "[]"):
            ini, fin = b["first_entry"] / 1e6, b["last_entry"] / 1e6
            if fin >= desde:
                boots.append([max(ini, desde), fin])
    except Exception:
        pass
    if boots:
        boots[-1][1] = ahora  # el arranque actual sigue vivo
    # suspensiones (entrada/salida) en el registro del kernel
    sus, abierto = [], None
    for linea in _j(["journalctl", "--since", f"-{dias}d", "--no-pager", "-o", "short-unix", "_TRANSPORT=kernel",
                     "-g", "PM: suspend (entry|exit)"], 40).splitlines():
        m = re.match(r"(\d+\.\d+) .*PM: suspend (entry|exit)", linea)
        if not m:
            continue
        t = float(m.group(1))
        if m.group(2) == "entry":
            abierto = t
        elif abierto:
            sus.append([abierto, t]); abierto = None
    # línea de tiempo en tramos de 5 min: apagado por defecto, encendido si hay un arranque, dormido si hay suspensión
    paso = 300; n = int((ahora - desde) // paso) + 1
    est = ["apagado"] * n
    def marcar(a, b, v):
        for k in range(max(0, int((a - desde) // paso)), min(n, int((b - desde) // paso) + 1)):
            est[k] = v
    for a, b in boots:
        marcar(a, b, "encendido")
    for a, b in sus:
        if b >= desde:
            marcar(max(a, desde), b, "dormido")
    seg = []
    for k, v in enumerate(est):
        t0 = desde + k * paso
        if seg and seg[-1]["tipo"] == v:
            seg[-1]["fin"] = min(ahora, t0 + paso)
        else:
            seg.append({"tipo": v, "ini": t0, "fin": min(ahora, t0 + paso)})
    tot = {k: round(sum(s["fin"] - s["ini"] for s in seg if s["tipo"] == k) / 3600, 1) for k in ("encendido", "dormido", "apagado")}
    # tareas que corrieron tarde: salidas en los primeros 10 min de un arranque o de un regreso de suspensión
    retornos = [b[0] for b in boots] + [s[1] for s in sus]
    tarde = []
    for home, perfil in ((H, "default"), *[(Path(p), Path(p).name) for p in glob.glob(str(H / "profiles" / "*"))]):
        jobs = {j["id"]: j for j in (_leer(home / "cron" / "jobs.json") or {}).get("jobs", [])}
        for f in glob.glob(str(home / "cron" / "output" / "*" / "*.md")):
            jid = f.split("/")[-2]; j = jobs.get(jid)
            if not j or str(j.get("schedule_display", "")).startswith(("every", "once")):
                continue
            t = _ts_salida(f)
            if t and t >= desde and any(0 <= t - r <= 600 for r in retornos):
                tarde.append({"id": jid, "perfil": perfil, "nombre": j["name"], "ts": t})
    servicios = {}
    for s in ("hermes-gateway", "flota-despierta", "cogsmos-puente"):
        v = _j(["systemctl", "--user", "show", f"{s}.service", "-p", "ActiveState", "-p", "ActiveEnterTimestamp"])
        d = dict(l.split("=", 1) for l in v.splitlines() if "=" in l)
        servicios[s] = {"estado": d.get("ActiveState"), "desde": d.get("ActiveEnterTimestamp")}
    return {"desde": desde, "hasta": ahora, "segmentos": seg, "horas": tot,
            "tarde": sorted(tarde, key=lambda x: -x["ts"])[:20], "servicios": servicios}


def _leer(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def _ts_salida(f):
    m = re.search(r"(\d{4}-\d\d-\d\d)_(\d\d)-(\d\d)-(\d\d)\.md$", f)
    if not m:
        return None
    return dt.datetime.strptime(" ".join(m.groups()), "%Y-%m-%d %H %M %S").timestamp()


def _estado_salida(f):
    try:
        cab = Path(f).read_text(encoding="utf-8", errors="replace")[:800]
    except Exception:
        return "?"
    m = re.search(r"\*\*Status:\*\*\s*([^\n]+)", cab)
    if m:
        return "silencio" if m.group(1).lower().startswith("silent") else ("fallo" if re.search(r"(?i)error|fail", m.group(1)) else "aviso")
    return "fallo" if re.search(r"(?i)\*\*(error|failed)", cab) else "aviso"


# ───────────── misiones (con su área) ─────────────
RE_AREA = re.compile(r"· sector ([a-z]+)\b")


def misiones():
    out = []
    for slug, db in tableros().items():
        try:
            for t in filas(db, "select id,title,status,assignee,coalesce(body,'') body,created_at,completed_at from tasks where status!='archived'"):
                m = RE_AREA.search(t["body"][:400])
                out.append({**{k: t[k] for k in ("id", "title", "status", "assignee", "created_at", "completed_at")},
                            "tablero": slug, "area": m.group(1) if m else None})
        except Exception:
            pass
    return out


# ───────────── áreas ─────────────
_JOBS = None
def _ids_mismo_faro(n):
    """(perfil, id) del faro y de sus copias anteriores con el mismo nombre en otros perfiles (historia antes del traslado)."""
    global _JOBS
    if _JOBS is None or time.time() - _JOBS[0] > 60:
        todos = []
        for home, perfil in ((H, "default"), *[(Path(p), Path(p).name) for p in glob.glob(str(H / "profiles" / "*"))]):
            for j in (_leer(home / "cron" / "jobs.json") or {}).get("jobs", []):
                todos.append((perfil, j["id"], j["name"]))
        _JOBS = (time.time(), todos)
    nombre = next((x[2] for x in _JOBS[1] if x[1] == n["id"]), None)
    return {(p, i) for p, i, nm in _JOBS[1] if i == n["id"] or (nombre and nm == nombre)}

def areas(flota, naves, dias=7):
    desde = time.time() - dias * 86400
    mis = misiones()
    res = {}
    for clave, s in flota.sectores.items():
        ns = [n for n in naves if n["sector"] == clave]
        corridas = {"aviso": 0, "silencio": 0, "fallo": 0}
        ultimo = None
        for n in ns:
            for f in [g for jid in _ids_mismo_faro(n) for g in glob.glob(str(home_de(jid[0]) / "cron" / "output" / jid[1] / "*.md"))]:
                t = _ts_salida(f)
                if t and t >= desde:
                    corridas[_estado_salida(f)] = corridas.get(_estado_salida(f), 0) + 1
                    if _estado_salida(f) == "aviso":
                        ultimo = max(ultimo or 0, t)
        ms = [m for m in mis if m["area"] == clave]
        res[clave] = {
            "nombre": s.get("nombre", clave), "lente": s.get("lente") or s.get("lentes"),
            "naves": [{"id": n["id"], "perfil": n["perfil"], "alias": n["alias"], "nombre": n["nombre"], "estado": n["estado"]} for n in ns],
            "activas": sum(1 for n in ns if n["estado"] != "pausada"),
            "corridas": corridas, "ultimo_aviso": ultimo,
            "misiones": {"abiertas": sum(1 for m in ms if m["status"] in ("todo", "ready", "running", "blocked", "review", "triage")),
                         "en_curso": sum(1 for m in ms if m["status"] == "running"),
                         "bloqueadas": sum(1 for m in ms if m["status"] == "blocked"),
                         "hechas": sum(1 for m in ms if m["status"] == "done" and (m["completed_at"] or 0) >= desde),
                         "lista": [{"id": m["id"], "tablero": m["tablero"], "titulo": m["title"], "estado": m["status"]}
                                   for m in sorted(ms, key=lambda x: (x["status"] != "running", x["status"] == "done", -(x["created_at"] or 0)))[:6]]},
        }
    sin = [m for m in mis if not m["area"]]
    res["_sin_area"] = {"abiertas": sum(1 for m in sin if m["status"] not in ("done",)),
                        "hechas": sum(1 for m in sin if m["status"] == "done" and (m["completed_at"] or 0) >= desde),
                        "total": len(mis), "con_area": len(mis) - len(sin)}
    return res


# ───────────── proyectos ─────────────
def proyectos(flota):
    out = []
    dbs = tableros()
    for p in flota.man.get("proyectos") or []:
        db = dbs.get(p.get("tablero"))
        if not db:
            continue
        ts = {t["id"]: t for t in filas(db, "select id,title,status,assignee,started_at,completed_at,created_at from tasks where status!='archived'")}
        fases = []
        if p.get("readme") and Path(p["readme"]).exists():
            for linea in Path(p["readme"]).read_text(encoding="utf-8").splitlines():
                m = re.match(r"\|\s*([A-Z]\w*)\s*\|\s*`(t_[0-9a-f]+)`\s*\|\s*`(t_[0-9a-f]+)`\s*\|", linea)
                if m:
                    f, c = ts.get(m.group(2)), ts.get(m.group(3))
                    fases.append({"fase": m.group(1),
                                  "tarjeta": {"id": m.group(2), "titulo": f and f["title"], "estado": f and f["status"], "inicio": f and f["started_at"], "fin": f and f["completed_at"]},
                                  "compuerta": {"id": m.group(3), "titulo": c and c["title"], "estado": c and c["status"]}})
        cerradas = sum(1 for f in fases if f["compuerta"]["estado"] == "done")
        actual = next((f for f in fases if f["compuerta"]["estado"] != "done"), None)
        otros = [t for i, t in ts.items() if not any(i in (f["tarjeta"]["id"], f["compuerta"]["id"]) for f in fases)]
        estados = {}
        for t in ts.values():
            estados[t["status"]] = estados.get(t["status"], 0) + 1
        out.append({"nombre": p["nombre"], "tablero": p["tablero"], "fases": fases, "cerradas": cerradas, "actual": actual,
                    "estados": estados, "total": len(ts),
                    "paralelas": [{"id": t["id"], "titulo": t["title"], "estado": t["status"]} for t in otros if t["status"] != "done"][:6],
                    "recientes": [{"id": t["id"], "titulo": t["title"], "fin": t["completed_at"]}
                                  for t in sorted(ts.values(), key=lambda x: -(x["completed_at"] or 0)) if t["status"] == "done"][:4]})
    return out


# ───────────── indicadores medibles ─────────────
def indicadores(flota, naves, agora_):
    ahora = time.time(); out = []
    instaladas = {}
    for item in flota.man.get("naves") or []:
        n = flota.catalogo.get(item["id"])
        if n:
            instaladas.setdefault(item["id"], {"ficha": n, "alias": item.get("alias")})
    for nid, x in instaladas.items():
        f = x["ficha"]; valor = None; nota = None
        if nid == "respaldo-flota":
            dias = sorted({re.search(r"flota-(\d{4}-\d\d-\d\d)", p).group(1) for p in glob.glob(str(H / "backups" / "fenix" / "flota-*.tgz"))}, reverse=True)
            racha, d = 0, dt.date.today()
            for _ in range(60):
                if d.isoformat() in dias:
                    racha += 1; d -= dt.timedelta(days=1)
                else:
                    break
            valor = f"{racha} día{'s' if racha != 1 else ''} seguidos"; nota = "se guardan los últimos 7"
        elif nid == "esperando-ok":
            esp = agora_["espera"]
            if esp:
                mx = max(ahora - (t["creada"] or ahora) for t in esp) / 3600
                valor = f"{len(esp)} esperando · la más vieja {mx:.0f} h"
            else:
                valor = "nada esperando"
        elif nid == "tareas-atascadas":
            at = agora_["atascadas"]
            if at:
                prom = sum(ahora - (t["inicio"] or t["creada"] or ahora) for t in at) / len(at) / 86400
                valor = f"{len(at)} atascadas · {prom:.1f} días en promedio"
            else:
                valor = "ninguna atascada"
        elif nid == "lanzar-mision":
            prog = [i for i in flota.man.get("naves") or [] if i["id"] == "lanzar-mision"]
            valor = f"{len(prog)} programada{'s' if len(prog) != 1 else ''}"
        out.append({"id": nid, "alias": x["alias"], "nombre": f.get("nombre_visible"), "indicador": f.get("indicador"),
                    "valor": valor, "nota": nota, "medido": valor is not None})
    return out


# ───────────── el modelo de la nota contra lo instalado ─────────────
def modelo(flota, naves, est_list, ind, ar, personajes):
    items = []
    def it(grupo, nombre, ok, detalle):
        items.append({"grupo": grupo, "nombre": nombre, "estado": ok, "detalle": detalle})
    sect = [k for k in flota.sectores]
    cub = [k for k in sect if ar.get(k, {}).get("activas")]
    it("Estructura", "9 sectores (PKM + APQC)", "ok" if len(cub) == len(sect) else "parcial", f"{len(cub)} de {len(sect)} con tareas automáticas activas")
    tipos = {e["tipo"] for e in est_list}
    for t, nom in (("persona", "Estación Persona"), ("negocio", "Estación Negocio"), ("servicio", "Estación Servicio")):
        e = next((x for x in est_list if x["tipo"] == t), None)
        if e:
            it("Estaciones", nom, "ok", f"{e['nombre']} · perfil {e['perfil']} · bot {'conectado' if e['bot'] == 'connected' else 'sin conectar'}")
        else:
            res = next((r for r in flota.man.get("reserva") or [] if "estación" in (r.get("funcion") or "")), None)
            it("Estaciones", nom, "pendiente", f"en reserva: {res['alias']}" if res else "no existe")
    co = next((x for x in est_list if x["coordinador"]), None)
    it("Estaciones", "Coordinador", "ok" if co else "pendiente", f"{co['nombre']} recibe, decide y reparte" if co else "sin coordinador")
    cat = len(flota.catalogo); inst = len({i["id"] for i in flota.man.get("naves") or []})
    it("Naves", "Catálogo del Astillero", "ok", f"{inst} de {cat} naves del catálogo instaladas")
    act = sum(1 for n in naves if n["estado"] != "pausada")
    it("Naves", "Tareas automáticas", "ok", f"{act} activas · {sum(1 for n in naves if n['estado'] == 'pausada')} pausadas · {sum(1 for n in naves if n['estado'] == 'fallo')} con falla")
    res = flota.man.get("reserva") or []
    it("Naves", "Naves en reserva", "parcial" if res else "ok", f"{len(res)} con nombre, sin tarea: " + ", ".join(r["alias"] for r in res))
    tipos_y = Path(__file__).resolve().parent.parent.parent / "flota" / "misiones" / "tipos.yaml"
    n_tipos = len(re.findall(r"^  [a-z_]+:\s*$", tipos_y.read_text(encoding="utf-8"), re.M)) if tipos_y.exists() else 0
    sa = ar.get("_sin_area", {})
    it("Misiones", "Tipos de misión con rúbrica", "ok" if n_tipos else "pendiente", f"{n_tipos} tipos definidos en tipos.yaml")
    pct = round(100 * sa.get("con_area", 0) / max(1, sa.get("total", 1)))
    it("Misiones", "Misiones con área", "ok" if pct >= 90 else "parcial", f"{sa.get('con_area', 0)} de {sa.get('total', 0)} ({pct} %)")
    it("Misiones", "Revisión automática (NémesIA)", "parcial", "va como rúbrica dentro de cada misión; falta calibrarla con resultados reales")
    med = sum(1 for i in ind if i["medido"])
    it("Medición", "Indicadores de las naves", "parcial" if med < len(ind) else "ok", f"{med} de {len(ind)} indicadores medidos")
    it("Medición", "Pulso 24/7", "ok", "encendido, dormido y apagado de los últimos 7 días")
    mn = any(re.search(r"(?i)memoria|mnemo", n["nombre"]) for n in naves if n["estado"] != "pausada")
    it("Memoria", "Mnemosync · wiki de memoria", "ok" if mn else "pendiente", "se sincroniza cada noche" if mn else "se corre a mano")
    it("Memoria", "Fénix · respaldo", "ok" if any(i["id"] == "respaldo-flota" and i["medido"] for i in ind) else "pendiente",
       next((i["valor"] for i in ind if i["id"] == "respaldo-flota"), "sin respaldo"))
    total_p = len(est_list) + len([n for n in naves if n["alias"]])
    it("Identidad", "Personajes (retratos)", "ok" if personajes and len(personajes) >= total_p else ("parcial" if personajes else "pendiente"),
       f"{len(personajes)} de {total_p} con retrato")
    return items
