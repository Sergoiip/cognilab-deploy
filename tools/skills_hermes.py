#!/usr/bin/env python3
"""Skills de Hermes que piden los módulos (`requiere_skills_hermes`): de dónde sale cada una.

  tools/skills_hermes.py auditar
      Recorre TODOS los módulos y clasifica cada skill: REPO (aprendizaje/Skills replicables),
      HERMES (viene con Hermes), HUB (stack/skills_hermes.yaml) o NO-VIAJA. Sale con 1 si hay
      alguna NO-VIAJA. Última línea: «N skills · N NO-VIAJA».

  tools/skills_hermes.py plan <ID> [<ID> ...] --hermes-home <ruta> --destino <ruta>
      Para los módulos dados (los ACTIVOS), una línea por skill, para bootstrap/instala.sh:
        YA|nombre|ruta            ya está instalada en el Hermes del equipo (no se toca)
        REPO|nombre|carpeta       copiar desde el repo a <destino>/<nombre>
        HERMES|nombre|            viene con Hermes; se siembra al abrir Hermes
        HUB|nombre|identificador  hermes skills install <identificador> --yes
        FALTA|nombre|módulos      no se encuentra en ningún lado (lista «a mano»)
"""
import argparse
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPL = ROOT / "aprendizaje" / "Skills replicables"


def requeridas():
    """{skill: [ids de módulo]} leído en vivo de modulos/*/*/modulo.yaml."""
    out = {}
    for f in sorted(ROOT.glob("modulos/*/*/modulo.yaml")):
        m = yaml.safe_load(f.read_text(encoding="utf-8"))
        for s in m.get("requiere_skills_hermes") or []:
            out.setdefault(s, []).append(m["id"])
    return out


def fuentes():
    cfg = yaml.safe_load((ROOT / "stack" / "skills_hermes.yaml").read_text(encoding="utf-8")) or {}
    return set(cfg.get("incluidas_en_hermes") or []), dict(cfg.get("hub") or {})


def nombre_de(skill_md):
    m = re.search(r"^name:\s*(\S+)", skill_md.read_text(encoding="utf-8", errors="ignore"), re.M)
    return m.group(1).strip("'\"") if m else skill_md.parent.name


def clasificar(nombre, incluidas, hub):
    sk = REPL / nombre / "SKILL.md"
    if sk.is_file():
        if nombre_de(sk) != nombre:
            sys.exit(f"{sk.relative_to(ROOT)}: el name: del frontmatter no coincide con la carpeta")
        return "REPO", str(sk.parent)
    if nombre in incluidas:
        return "HERMES", ""
    if nombre in hub:
        return "HUB", hub[nombre]
    return "NO-VIAJA", ""


def instaladas(hermes_home, destino):
    """{nombre: ruta} de las skills ya presentes en el Hermes del equipo, salvo las que este
    instalador puso en <destino> (esas se actualizan siempre desde el repo)."""
    base = pathlib.Path(hermes_home).expanduser() / "skills"
    dest = pathlib.Path(destino).expanduser().resolve()
    out = {}
    if base.is_dir():
        for sk in base.rglob("SKILL.md"):
            if dest in sk.resolve().parents:
                continue
            out.setdefault(nombre_de(sk), str(sk.parent))
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auditar")
    p = sub.add_parser("plan")
    p.add_argument("ids", nargs="+")
    p.add_argument("--hermes-home", required=True)
    p.add_argument("--destino", required=True)
    a = ap.parse_args()

    req = requeridas()
    incluidas, hub = fuentes()

    if a.cmd == "auditar":
        malas = 0
        for s in sorted(req):
            tipo, det = clasificar(s, incluidas, hub)
            malas += tipo == "NO-VIAJA"
            det = pathlib.Path(det).relative_to(ROOT) if tipo == "REPO" else det
            print(f"{tipo:<9} {s:<45} {','.join(sorted(req[s])):<12} {det}")
        print(f"{len(req)} skills · {malas} NO-VIAJA")
        sys.exit(1 if malas else 0)

    ya = instaladas(a.hermes_home, a.destino)
    vistas = []
    for s in sorted(req):
        mods = [m for m in req[s] if m in a.ids]
        if not mods or s in vistas:
            continue
        vistas.append(s)
        tipo, det = clasificar(s, incluidas, hub)
        if s in ya:
            print(f"YA|{s}|{ya[s]}")
        elif tipo == "NO-VIAJA":
            print(f"FALTA|{s}|{','.join(mods)}")
        else:
            print(f"{tipo}|{s}|{det}")


if __name__ == "__main__":
    main()
