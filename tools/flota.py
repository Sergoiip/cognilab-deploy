#!/usr/bin/env python3
"""La Flota desde la terminal.

  python3 tools/flota.py estado  manifiestos/cliente-X.yaml      cobertura por sector (con las dos lentes)
  python3 tools/flota.py aplicar manifiestos/cliente-X.yaml      muestra lo que haría (no toca nada)
  python3 tools/flota.py aplicar manifiestos/cliente-X.yaml --si lo hace

`aplicar` es idempotente: describe las estaciones que existen, crea las que faltan (sin copiar
credenciales: eso pasa por el responsable), genera el envoltorio de cada nave en el directorio de
scripts del perfil y da de alta su faro si no existe uno con el mismo nombre. Solo corre con --si en
la máquina que declara el manifiesto."""
import sys, os, json, socket, pathlib, argparse, subprocess, shlex, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
FLOTA = ROOT / "flota"
HERMES = os.environ.get("HERMES_BIN", "hermes")
PREFIJO = "Flota · "


# ---------- catálogo ----------
def cargar_catalogo():
    sect = yaml.safe_load((FLOTA / "sectores.yaml").read_text(encoding="utf-8"))["sectores"]
    naves = {}
    for f in FLOTA.glob("naves/*/*.yaml"):
        n = yaml.safe_load(f.read_text(encoding="utf-8"))
        n["_dir"] = f.parent
        naves[n["id"]] = n
    est = {f.stem: yaml.safe_load(f.read_text(encoding="utf-8")) for f in FLOTA.glob("estaciones/*.yaml")}
    return sect, naves, est


def cargar(man_path):
    man = yaml.safe_load(pathlib.Path(man_path).read_text(encoding="utf-8"))
    plano = yaml.safe_load((FLOTA / "planos" / f"{man['plano']}.yaml").read_text(encoding="utf-8"))
    return man, plano


def home_de(perfil):
    base = pathlib.Path.home() / ".hermes"
    return base if perfil == "default" else base / "profiles" / perfil


def jobs_de(perfil):
    jp = home_de(perfil) / "cron" / "jobs.json"
    if not jp.exists():
        return {}
    d = json.loads(jp.read_text(encoding="utf-8"))
    return {j["id"]: j for j in (d["jobs"] if isinstance(d, dict) else d)}


def resolver(valor, man):
    """'{crm.raiz}' -> man['crm']['raiz']"""
    if isinstance(valor, str) and valor.startswith("{") and valor.endswith("}"):
        cur = man
        for k in valor[1:-1].split("."):
            cur = cur[k]
        return str(pathlib.Path(cur).expanduser())
    return str(valor)


def estacion_de_nave(nave, man):
    for e in man["estaciones"]:
        if e["tipo"] == nave.get("la_ejecuta", "negocio"):
            return e
    return man["estaciones"][0]


# ---------- estado ----------
def estado(args):
    sect, naves, _ = cargar_catalogo()
    man, plano = cargar(args.manifiesto)
    problemas, por_sector = [], {k: [] for k in sect}
    jobs_all = {}
    for e in man["estaciones"]:
        jobs_all.update(jobs_de(e["perfil_hermes"]))
    por_nombre = {j.get("name"): j for j in jobs_all.values()}

    def st_de(j):
        if j is None:
            return "no existe"
        s = "activo" if j.get("enabled", True) and j.get("state") != "paused" else "pausado"
        if j.get("last_status") == "error":
            s += " · último run con error"
        return s

    for cid, f in (man.get("faros") or {}).items():
        if f["sector"] not in sect:
            problemas.append(f"faro {cid}: sector '{f['sector']}' no existe")
            continue
        por_sector[f["sector"]].append((st_de(jobs_all.get(cid)), f["nombre"]))
    for item in man.get("naves") or []:
        n = naves.get(item["id"])
        if not n:
            problemas.append(f"nave '{item['id']}' no está en el catálogo")
            continue
        j = por_nombre.get(PREFIJO + n["nombre_visible"])
        por_sector[n["sector"]].append((st_de(j) if j else "sin instalar (corre `aplicar`)", n["nombre_visible"] + " ⛵"))
    for item in man.get("naves_locales") or []:
        if item.get("sector") in por_sector:
            por_sector[item["sector"]].append((item.get("estado", "pendiente"), item["nombre_visible"] + " (local)"))

    print(f"Flota «{man['cliente']}» · plano {plano['id']} ({plano['estado']}) · lentes: {' + '.join(plano['lentes'])}")
    print("Estaciones: " + ", ".join(f"{e['nombre_visible']} ({e['tipo']}, perfil {e['perfil_hermes']})" for e in man["estaciones"]))
    huecos = []
    for k, s in sect.items():
        lente = []
        if "pkm" in plano["lentes"] and s.get("pkm"):
            lente.append(f"PKM: {s['pkm']}")
        if "apqc" in plano["lentes"] and s.get("apqc"):
            lente.append("APQC " + ", ".join(x.split()[0] for x in s["apqc"]))
        if not lente:
            continue
        items = por_sector[k]
        activos = [i for i in items if i[0].startswith("activo")]
        marca = "✅" if activos else ("🟡" if items else "⬜")
        if not activos and k in plano.get("cobertura_minima", []):
            huecos.append(s["nombre"])
        print(f"\n{marca} {s['nombre']}  [{' · '.join(lente)}]" + ("  (transversal)" if s["tipo"] == "transversal" else ""))
        for st, nombre in items:
            print(f"    - {nombre} — {st}")
        if not items:
            print("    (nada lo vigila)")
    print("\nSin cobertura activa: " + (", ".join(huecos) if huecos else "ninguno"))
    print("⛵ = nave del catálogo del Astillero")
    for p in problemas:
        print("PROBLEMA", p)
    return 1 if problemas else 0


# ---------- aplicar ----------
def run(cmd, si, pasos):
    pasos.append(" ".join(shlex.quote(c) for c in cmd))
    if not si:
        return True, ""
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def perfiles_existentes():
    base = pathlib.Path.home() / ".hermes" / "profiles"
    return {"default"} | ({p.name for p in base.iterdir() if p.is_dir()} if base.exists() else set())


def descripcion(e, ficha, man):
    sectores = man.get("_sectores_activos", [])
    return (f"{e['nombre_visible']} · Estación {e['tipo'].capitalize()} de la Flota «{man['cliente']}» "
            f"(plano {man['plano']}). {e.get('mision') or ficha['mision']} "
            f"Capitán: {e.get('capitan') or man.get('capitan')}."
            + (f" Sectores que cubre: {', '.join(sectores)}." if sectores else ""))


def envoltorio(nave, args_resueltos):
    script = (nave["_dir"] / nave["script"]).resolve()
    return f'''#!/usr/bin/env python3
"""Faro de la Flota: {nave['nombre_visible']} (generado por tools/flota.py aplicar; no editar a mano).
La lógica vive en el Astillero: {script}
Salida vacía = silencio."""
import subprocess, sys, pathlib
NAVE = pathlib.Path({str(script)!r})
ARGS = {args_resueltos!r}
if not NAVE.exists():
    print(f"⚠️ Faro «{nave['nombre_visible']}»: no encuentro la nave en {{NAVE}}")
    sys.exit(0)
r = subprocess.run([sys.executable, str(NAVE), *ARGS], capture_output=True, text=True, timeout=120)
if r.returncode != 0:
    print(f"⚠️ Faro «{nave['nombre_visible']}» falló:\\n{{r.stderr[-800:]}}")
else:
    sys.stdout.write(r.stdout)
'''


def aplicar(args):
    sect, naves, est = cargar_catalogo()
    man, plano = cargar(args.manifiesto)
    si = args.si
    pasos, avisos, fallos = [], [], []
    host = socket.gethostname()
    if si and man.get("maquina") not in (host, "cualquiera"):
        print(f"✋ El manifiesto es para la máquina «{man.get('maquina')}» y esta es «{host}». No aplico nada.")
        return 1
    man["_sectores_activos"] = sorted({naves[i["id"]]["sector"] for i in man.get("naves") or [] if i["id"] in naves}
                                      | {f["sector"] for f in (man.get("faros") or {}).values()})
    existentes = perfiles_existentes()

    # 1. estaciones
    for e in man["estaciones"]:
        ficha = est.get(e["tipo"])
        if not ficha:
            fallos.append(f"estación {e['id']}: tipo '{e['tipo']}' no existe en flota/estaciones/")
            continue
        desc = descripcion(e, ficha, man)
        if e["perfil_hermes"] not in existentes:
            ok, out = run([HERMES, "profile", "create", e["perfil_hermes"], "--clone", "--description", desc], si, pasos)
            avisos.append(f"estación {e['id']}: perfil «{e['perfil_hermes']}» creado SIN credenciales. "
                          f"El responsable conecta su proveedor (`hermes -p {e['perfil_hermes']} auth`) antes de usarlo.")
        else:
            ok, out = run([HERMES, "profile", "describe", e["perfil_hermes"], "--text", desc], si, pasos)
        if not ok:
            fallos.append(f"estación {e['id']}: {out[-300:]}")

    # 2. naves
    for item in man.get("naves") or []:
        n = naves.get(item["id"])
        if not n:
            fallos.append(f"nave '{item['id']}' no está en el catálogo")
            continue
        if n.get("estado_ficha") == "borrador":
            avisos.append(f"nave {n['id']}: ficha en borrador, no se instala")
            continue
        if not n.get("script"):
            avisos.append(f"nave {n['id']}: no tiene script; por ahora solo las naves con script se instalan solas")
            continue
        e = estacion_de_nave(n, man)
        perfil = e["perfil_hermes"]
        try:
            a = [resolver(x, man) for x in n.get("argumentos", [])]
        except KeyError as k:
            fallos.append(f"nave {n['id']}: el manifiesto no define {k}")
            continue
        for fr in item.get("frentes") or []:
            a += [n["por_frente"], fr]
        dest = home_de(perfil) / "scripts" / f"flota_{n['id'].replace('-', '_')}.py"
        pasos.append(f"escribir {dest}")
        if si:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(envoltorio(n, a), encoding="utf-8")
        nombre = PREFIJO + n["nombre_visible"]
        sched = item.get("faro") or n["disparador"]["faro"]
        existe = next((j for j in jobs_de(perfil).values() if j.get("name") == nombre), None)
        if existe:
            pasos.append(f"faro «{nombre}» ya existe ({existe['id']}); se deja como está")
            continue
        cmd = [HERMES] + (["-p", perfil] if perfil != "default" else []) + [
            "cron", "create", sched, "--name", nombre, "--script", dest.name, "--no-agent",
            "--deliver", man["entrega"], "--timezone", man.get("zona", "America/Bogota"), "--catch-up", "on"]  # un aviso tarde > un aviso perdido
        ok, out = run(cmd, si, pasos)
        if not ok:
            fallos.append(f"nave {n['id']}: {out[-300:]}")

    print(("APLICADO" if si else "SIMULACIÓN (agrega --si para hacerlo)") + f" · Flota «{man['cliente']}» · máquina {host}")
    for p in pasos:
        print("  →", p)
    for a in avisos:
        print("  ⚠", a)
    for f in fallos:
        print("  ✗", f)
    return 1 if fallos else 0


# ---------- mision ----------
def mision(args):
    tipos = yaml.safe_load((FLOTA / "misiones" / "tipos.yaml").read_text(encoding="utf-8"))["tipos"]
    plantillas = {yaml.safe_load(f.read_text(encoding="utf-8"))["id"]: f for f in FLOTA.glob("misiones/*/*.yaml")}
    if args.plantilla not in plantillas:
        print(f"✗ No existe la plantilla '{args.plantilla}'. Hay: {', '.join(sorted(plantillas))}")
        return 1
    p = yaml.safe_load(plantillas[args.plantilla].read_text(encoding="utf-8"))
    t = tipos[p["tipo"]]
    man, _ = cargar(args.manifiesto)
    vars_ = dict(kv.split("=", 1) for kv in args.var)
    vars_.setdefault("cliente", args.cliente or man["cliente"])
    try:
        cuerpo = p["cuerpo"].format(**vars_)
        registro = p["registro"].format(**vars_)
    except KeyError as k:
        print(f"✗ Falta la variable {k}. Pásala con --var {k.args[0]}=...")
        return 1
    if t["ejecuta"] != "agente":
        print(f"✗ Una misión de tipo «{t['nombre']}» no se asigna a una estación (la ejecuta el capitán).")
        return 1
    est = next((e for e in man["estaciones"] if e["tipo"] == p["la_ejecuta"]), man["estaciones"][0])
    nuc = yaml.safe_load((FLOTA / "nucleo.yaml").read_text(encoding="utf-8"))
    no_hace = list(p.get("no_hace", [])) + nuc["codigo_de_navegacion"]
    titulo = f"{p['nombre_visible']} · {vars_['cliente']}" + (f" · {vars_['periodo']}" if "periodo" in vars_ else "")
    body = (f"MISIÓN ({t['nombre']}) · plantilla {p['id']} · sector {p['sector']}\n\n{cuerpo}\n"
            f"CRITERIO DE HECHO:\n" + "\n".join(f"- {h}" for h in p["hecho"]) +
            f"\n\nNO HACE:\n" + "\n".join(f"- {x}" for x in no_hace) +
            f"\n\nREGISTRO: {registro}\nREVISIÓN: {t['criterio_revision']}\n"
            + ("CIERRE: termina con kanban_complete y la ruta del borrador en metadata. NO pidas revisión: "
               "la aprobación es la tarjeta hija «⛔ Visto bueno», que solo cierra el capitán.\n" if t["revision"] == "capitan" else ""))
    clave = f"{p['id']}-{vars_['cliente']}-{vars_.get('periodo', '')}".lower().replace(" ", "-")
    board = args.board or man.get("tablero")
    base = [HERMES, "kanban"] + (["--board", board] if board else [])
    tmp = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / f"mision-{clave}.md"
    tmp.write_text(body, encoding="utf-8")
    cmd = base + ["create", titulo, "--body-file", str(tmp), "--assignee", est["perfil_hermes"],
                  "--tenant", vars_["cliente"], "--idempotency-key", clave, "--json"]
    for s in p.get("skills") or []:
        cmd += ["--skill", s]
    if t["modo"] == "goal":
        cmd += ["--goal"]
    if not args.si:
        print("SIMULACIÓN (agrega --si para crearla)\n  →", " ".join(shlex.quote(c) for c in cmd))
        if t["revision"] == "capitan":
            print(f"  → y la puerta del capitán: «⛔ Visto bueno · {titulo}» sin asignar, hija de la misión")
        print("\n--- cuerpo ---\n" + body)
        return 0
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("✗", (r.stdout + r.stderr)[-500:])
        return 1
    tid = json.loads(r.stdout[r.stdout.index("{"):])["id"]
    print(f"✓ misión {tid} asignada a {est['perfil_hermes']}")
    if t["revision"] == "capitan":
        r2 = subprocess.run(base + ["create", f"⛔ Visto bueno · {titulo}", "--body",
                            f"COMPUERTA HUMANA — NO ASIGNAR. {man.get('capitan')} revisa el resultado de {tid} y decide si se envía.",
                            "--parent", tid, "--tenant", vars_["cliente"], "--idempotency-key", clave + "-visto-bueno", "--json"],
                            capture_output=True, text=True)
        print("✓ puerta del capitán creada" if r2.returncode == 0 else "✗ puerta: " + (r2.stdout + r2.stderr)[-300:])
    return 0


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
e = sub.add_parser("estado")
e.add_argument("manifiesto")
p = sub.add_parser("aplicar")
p.add_argument("manifiesto")
p.add_argument("--si", action="store_true")
m = sub.add_parser("mision")
m.add_argument("plantilla")
m.add_argument("manifiesto")
m.add_argument("--cliente")
m.add_argument("--var", action="append", default=[], help="clave=valor para la plantilla (repetible)")
m.add_argument("--board")
m.add_argument("--si", action="store_true")
a = ap.parse_args()
sys.exit({"estado": estado, "aplicar": aplicar, "mision": mision}[a.cmd](a))
