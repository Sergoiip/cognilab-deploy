#!/usr/bin/env python3
"""Propone el roster de empleados-agente (Bots de Hermes) para un cliente, a partir de su
manifiesto — y, si se da, de la identidad que dejó en su radiografía (narrativa/lore,
motivación, estética).

Solo PROPONE — no crea perfiles de Hermes todavía. Eso es un paso aparte, deliberado: crear
perfiles es tocar la máquina del cliente, no algo para automatizar a ciegas antes de que Sergio
confirme el roster con él.

Uso:
    tools/roster_sugerido.py <manifiesto.yaml> [--radiografia <radiografia.yaml>]
"""
import argparse
import pathlib

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifiesto")
    ap.add_argument("--radiografia")
    a = ap.parse_args()

    man = yaml.safe_load(pathlib.Path(a.manifiesto).read_text(encoding="utf-8")) or {}
    ids_cliente = {m["id"] for m in (man.get("modulos") or [])}
    cliente = man.get("cliente", "[cliente]")

    cat = yaml.safe_load((REPO / "stack" / "roles-agentes.yaml").read_text(encoding="utf-8"))

    identidad = {}
    if a.radiografia:
        rad = yaml.safe_load(pathlib.Path(a.radiografia).read_text(encoding="utf-8")) or {}
        identidad = rad.get("identidad_agentes", {}) or {}

    print(f"Roster sugerido para {cliente} (módulos del manifiesto: {', '.join(sorted(ids_cliente)) or 'ninguno'})")
    print()

    propuestos = []
    for rol_id, rol in cat["roles"].items():
        activa = set(rol.get("activa_con", []))
        tambien = set(rol.get("tambien_si", []))
        if activa & ids_cliente:
            razon = sorted(activa & ids_cliente)
            extra = sorted(tambien & ids_cliente)
            propuestos.append((rol_id, rol, razon, extra))

    if not propuestos:
        print("Ningún rol de la línea base se activa con este manifiesto — todavía no hay módulos de los bloques C/D que los disparen.")
        return

    for rol_id, rol, razon, extra in propuestos:
        print(f"## {rol['nombre']}  (perfil sugerido: {rol_id})")
        print(f"   Activado por: {', '.join(razon)}" + (f" · también cubre: {', '.join(extra)}" if extra else ""))
        print(f"   Título: {rol['titulo_base']}")
        print(f"   Descripción base: {rol['descripcion_base']}")
        print(f"   Skills sugeridas: {', '.join(rol.get('skills_sugeridas', []))}")
        if identidad.get("narrativa_lore") or identidad.get("motivacion") or identidad.get("estetica_favorita"):
            print("   Flavor de este cliente (de su radiografía, para el SOUL.md del Bot):")
            if identidad.get("narrativa_lore"):
                print(f"     - Narrativa/lore: {identidad['narrativa_lore']}")
            if identidad.get("motivacion"):
                print(f"     - Motivación real: {identidad['motivacion']}")
            if identidad.get("estetica_favorita"):
                print(f"     - Estética favorita: {identidad['estetica_favorita']}")
        else:
            print("   (sin identidad_agentes capturada todavía en la radiografía — Bot genérico hasta que se llene)")
        print(f"   Crear con: hermes profile create {rol_id}-{cliente.lower().replace(' ', '-')}")
        print()


if __name__ == "__main__":
    main()
