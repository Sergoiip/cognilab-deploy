#!/usr/bin/env python3
"""Crea el espacio de trabajo por cliente (patrón ICM) a partir de un manifiesto.
  python3 tools/espacio.py crear manifiestos/cliente-X.yaml --destino DIR [--dry-run] [--forzar]
  python3 tools/espacio.py estado DIR
Nunca sobrescribe un archivo existente salvo con --forzar."""
import sys, argparse, datetime, pathlib, shutil, subprocess, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
ETAPAS = [("01-diagnostico-y-base", "etapa-1.md.tpl"), ("02-construccion", "etapa-2.md.tpl"), ("03-consolidacion", "etapa-3.md.tpl")]
REFS = [("fichas/ingreso.md", "ingreso.md"), ("fichas/cierre.md", "cierre.md"), ("criterios/CRITERIOS-DE-HECHO.md", "CRITERIOS-DE-HECHO.md"), ("escalas.md", "escalas.md")]


def version():
    try:
        return subprocess.run(["git", "-C", str(ROOT), "describe", "--tags", "--always"], capture_output=True, text=True).stdout.strip() or "sin-git"
    except Exception:
        return "sin-git"


def llenar(txt, vals):
    for k, v in vals.items():
        txt = txt.replace("{{" + k + "}}", str(v))
    return txt


def crear(a):
    man = yaml.safe_load(open(a.manifiesto, encoding="utf-8"))
    mods = man.get("modulos", [])
    escalas = [m.get("escala", 1) for m in mods] or [1]
    vals = {
        "CLIENTE": man.get("cliente", "[cliente]"), "PAQUETE": man.get("paquete", "[paquete]"),
        "ESCALA": max(escalas), "VERSION": version(), "FECHA": datetime.date.today().isoformat(),
        "MODULOS": "\n".join(f"- {m['id']} (escala {m.get('escala', 1)})" for m in mods) or "- (ninguno)",
    }
    dest = pathlib.Path(a.destino).expanduser()
    plan = [("CLAUDE.md", (ROOT / "icm/CLAUDE.md.tpl"), True), ("CONTEXT.md", (ROOT / "icm/CONTEXT.md.tpl"), True)]
    for carpeta, tpl in ETAPAS:
        plan.append((f"etapas/{carpeta}/CONTEXT.md", ROOT / "icm" / tpl, True))
    for src, nombre in REFS:
        plan.append((f"referencias/{nombre}", ROOT / src, False))
    creados, saltados = [], []
    for rel, src, es_tpl in plan:
        out = dest / rel
        if out.exists() and not a.forzar:
            saltados.append(rel); continue
        creados.append(rel)
        if not a.dry_run:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(llenar(src.read_text(encoding="utf-8"), vals) if es_tpl else src.read_text(encoding="utf-8"), encoding="utf-8")
    for carpeta, _ in ETAPAS:
        k = dest / "etapas" / carpeta / "output" / ".gitkeep"
        if not k.exists() and not a.dry_run:
            k.parent.mkdir(parents=True, exist_ok=True); k.touch()
    pref = "[dry-run] " if a.dry_run else ""
    for r in creados: print(f"  {pref}+ {r}")
    for r in saltados: print(f"  = {r} (ya existe, se respeta)")
    print(f"Espacio en {dest}")


def estado(a):
    d = pathlib.Path(a.dir).expanduser() / "etapas"
    if not d.is_dir():
        sys.exit("no encuentro etapas/ en esa carpeta")
    siguiente = None
    for carpeta, _ in ETAPAS:
        out = d / carpeta / "output"
        arch = sorted(p.name for p in out.glob("*") if p.name != ".gitkeep") if out.is_dir() else []
        acept = [x for x in arch if x.startswith("aceptacion-hito")]
        marca = "aceptada" if acept else ("en curso" if arch else "sin empezar")
        print(f"{carpeta}: {marca} · {len(arch)} archivo(s)")
        for x in arch: print(f"    - {x}")
        if not acept and siguiente is None: siguiente = carpeta
    print("Sigue:", siguiente or "todas las etapas aceptadas")


p = argparse.ArgumentParser()
s = p.add_subparsers(dest="cmd", required=True)
c = s.add_parser("crear"); c.add_argument("manifiesto"); c.add_argument("--destino", required=True)
c.add_argument("--dry-run", action="store_true"); c.add_argument("--forzar", action="store_true"); c.set_defaults(f=crear)
e = s.add_parser("estado"); e.add_argument("dir"); e.set_defaults(f=estado)
a = p.parse_args(); a.f(a)
