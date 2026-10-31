#!/usr/bin/env python3
"""Propone qué perfiles de Hermes crear para un cliente con más de una persona, a partir de
`personas:` y `tipo:` del manifiesto — por ROL, nunca por nombre propio (el manifiesto no
lleva nombres propios de clientes, ver `criterios/`).

Patrón (ver `bootstrap/CONFIGURACION-DUAL-MAQUINA.md` → "Cuando el cliente es más de una
persona"):
  - Un perfil por cada persona con `usa_pc: true`.
  - Un perfil compartido adicional ("agencia"/"negocio") cuando `tipo: negocio` y hay más de
    una persona con `usa_pc: true` — el que redacta hacia clientes externos con las
    directrices conjuntas de todos.

Solo PROPONE — no crea perfiles en ninguna máquina. Ese paso es aparte, igual que
`roster_sugerido.py`.

Uso:
    tools/perfiles_equipo.py manifiesto.yaml
"""
import argparse
import pathlib
import re

import yaml


def slug(texto: str) -> str:
    s = texto.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "persona"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifiesto")
    a = ap.parse_args()

    man = yaml.safe_load(pathlib.Path(a.manifiesto).read_text(encoding="utf-8")) or {}
    tipo = man.get("tipo", "negocio")
    personas = [p for p in (man.get("personas") or []) if p.get("usa_pc")]

    if not personas:
        print("El manifiesto no trae 'personas' con usa_pc: true — nada que proponer.")
        return

    print(f"Tipo de cliente: {tipo} · personas con equipo propio: {len(personas)}")
    print()

    vistos = {}
    for p in personas:
        base = slug(p.get("rol", "persona"))
        n = vistos.get(base, 0)
        vistos[base] = n + 1
        rol_id = base if n == 0 else f"{base}-{n+1}"
        print(f"- Perfil personal: hermes profile create {rol_id}")
        print(f"    rol: {p.get('rol')}  (sin nombre propio — el manifiesto no lo trae)")

    if tipo == "negocio" and len(personas) > 1:
        print()
        print("- Perfil compartido: hermes profile create agencia")
        print("    Redacta hacia clientes externos con las directrices conjuntas de todos los")
        print("    perfiles personales de arriba. No sustituye a ninguno.")
    elif tipo == "negocio" and len(personas) == 1:
        print()
        print("(Una sola persona con equipo propio — no hace falta un perfil compartido aparte,")
        print(" su propio perfil ya hace las dos funciones.)")


if __name__ == "__main__":
    main()
