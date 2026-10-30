#!/usr/bin/env python3
"""Refleja el manifiesto en la bóveda del cliente de inmediato: crea la bóveda si falta, escribe
una nota de bienvenida personalizada (nombre del cliente, agente, módulos elegidos, nivel de
acompañamiento) y crea las carpetas base que los módulos elegidos ya necesitan de verdad.

Idempotente: se puede correr muchas veces (cada vez que el manifiesto cambie durante la semana
de Radiografía) sin duplicar nada — la nota de bienvenida se regenera completa, las carpetas que
ya existen no se tocan.

NO inventa estructura de entidades (clientes, leads, etc.) que todavía no esté definida en el
repo — solo crea lo que ya tiene una ruta real conocida (ver mapeo abajo). El resto de la
estructura por entidad se define en vivo con el cliente (A2, paso 1 del método).

Uso:
    tools/scaffold_vault.py <manifiesto.yaml> [--dry-run]
"""
import argparse
import datetime
import pathlib
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent

# Carpetas con ruta REAL ya definida en este repo (no inventadas), por módulo elegido.
# A2 a escala >=2 instala Lab Cadence, que lee `expensesFolder` = Cadence/Gastos por defecto
# (ver stack/vendor/lab-cadence/CAMBIOS.md). A3 instala TaskNotes, que lee TaskNotes/Tasks/, y
# el ritmo diario vive en daily/ (ver note-taking/obsidian-vault-canvas-and-roadmaps).
CARPETAS_POR_MODULO = {
    ("A2", 2): ["Cadence/Gastos"],
    ("A2", 3): ["Cadence/Gastos"],
    ("A3", 1): ["TaskNotes/Tasks", "daily"],
    ("A3", 2): ["TaskNotes/Tasks", "daily"],
    ("A3", 3): ["TaskNotes/Tasks", "daily"],
}


def cargar_modulos():
    mods = {}
    for f in sorted(REPO.glob("modulos/*/*/modulo.yaml")):
        m = yaml.safe_load(f.read_text(encoding="utf-8"))
        mods[m["id"]] = m["nombre"]
    return mods


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifiesto")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    man = yaml.safe_load(pathlib.Path(a.manifiesto).read_text(encoding="utf-8")) or {}
    vault = pathlib.Path(man.get("vault", "")).expanduser()
    if not vault:
        sys.exit("el manifiesto no trae 'vault:'")

    nombres_modulo = cargar_modulos()
    cliente = man.get("cliente", "[cliente]")
    paquete = man.get("paquete", "?")
    acompanamiento = man.get("acompanamiento", "(sin definir)")
    agente = man.get("agente", {}) or {}
    modulos = man.get("modulos", []) or []

    carpetas = ["Cadence", "TaskNotes"]  # base, siempre (lo usa casi cualquier módulo)
    for m in modulos:
        for c in CARPETAS_POR_MODULO.get((m["id"], m.get("escala", 1)), []):
            if c not in carpetas:
                carpetas.append(c)

    print(f"Bóveda: {vault}")
    print(f"Carpetas a asegurar: {', '.join(carpetas)}")

    bienvenida = []
    bienvenida.append(f"# Bienvenido/a, {cliente}")
    bienvenida.append("")
    bienvenida.append(f"> Generado y actualizado automáticamente desde tu manifiesto — última sincronía: {datetime.date.today().isoformat()}.")
    bienvenida.append("")
    if agente.get("nombre") or agente.get("personalidad"):
        bienvenida.append("## Tu agente")
        if agente.get("nombre"):
            bienvenida.append(f"- Nombre: **{agente['nombre']}**")
        if agente.get("personalidad"):
            bienvenida.append(f"- Personalidad: {agente['personalidad']}")
        bienvenida.append("")
    bienvenida.append(f"## Tu paquete: {paquete} · acompañamiento {acompanamiento}")
    bienvenida.append("")
    bienvenida.append("## Módulos de este manifiesto")
    if modulos:
        for m in modulos:
            nombre = nombres_modulo.get(m["id"], m["id"])
            bienvenida.append(f"- [ ] {m['id']} — {nombre} (escala {m.get('escala', 1)})")
    else:
        bienvenida.append("_(todavía no hay módulos confirmados — se afinan durante la semana de Radiografía)_")
    bienvenida.append("")
    bienvenida.append("Esta nota se regenera completa cada vez que el manifiesto cambia — no editarla a mano, los cambios se pierden en la próxima sincronía.")
    texto = "\n".join(bienvenida) + "\n"

    if a.dry_run:
        print(f"[dry-run] se crearía/actualizaría {vault / '00 - Bienvenida.md'}")
        for c in carpetas:
            print(f"[dry-run] se asegurría carpeta {vault / c}")
        return

    vault.mkdir(parents=True, exist_ok=True)
    for c in carpetas:
        (vault / c).mkdir(parents=True, exist_ok=True)
    (vault / "00 - Bienvenida.md").write_text(texto, encoding="utf-8")
    print(f"+ {vault / '00 - Bienvenida.md'} escrita")
    print("+ carpetas asegradas:", ", ".join(str(vault / c) for c in carpetas))


if __name__ == "__main__":
    main()
