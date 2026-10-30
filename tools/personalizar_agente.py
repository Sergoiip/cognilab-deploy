#!/usr/bin/env python3
"""Escribe/actualiza el bloque de identidad del agente (nombre + personalidad) en SOUL.md
a partir de los campos opcionales `agente.nombre` / `agente.personalidad` del manifiesto.

No reemplaza el SOUL.md completo: inserta un bloque marcado al inicio del archivo (idempotente,
se puede correr varias veces sin duplicar) y deja el resto del SOUL.md (el que trae Hermes por
defecto, o el que el cliente ya tenga) intacto debajo.

Uso:
    personalizar_agente.py <manifiesto.yaml> <hermes_home> [--dry-run]

Sale en silencio (sin tocar nada) si el manifiesto no trae `agente.nombre` ni
`agente.personalidad`.
"""
import sys
import pathlib
import yaml

INICIO = "<!-- COGNILAB:AGENTE:INICIO -->"
FIN = "<!-- COGNILAB:AGENTE:FIN -->"


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) != 2:
        print("uso: personalizar_agente.py <manifiesto.yaml> <hermes_home> [--dry-run]", file=sys.stderr)
        return 1
    manifiesto_path, hermes_home = pathlib.Path(args[0]), pathlib.Path(args[1])

    man = yaml.safe_load(manifiesto_path.read_text(encoding="utf-8")) or {}
    agente = man.get("agente") or {}
    nombre = (agente.get("nombre") or "").strip()
    personalidad = (agente.get("personalidad") or "").strip()

    if not nombre and not personalidad:
        print("  (sin agente.nombre/agente.personalidad en el manifiesto; SOUL.md no se toca)")
        return 0

    bloque_lineas = [INICIO]
    if nombre:
        bloque_lineas.append(f"Nombre: {nombre}.")
    if personalidad:
        bloque_lineas.append(f"Personalidad: {personalidad}.")
    bloque_lineas.append(FIN)
    bloque = "\n".join(bloque_lineas) + "\n"

    soul_path = hermes_home / "SOUL.md"
    existente = soul_path.read_text(encoding="utf-8") if soul_path.exists() else ""

    if INICIO in existente and FIN in existente:
        pre, resto = existente.split(INICIO, 1)
        _, post = resto.split(FIN, 1)
        nuevo = pre + bloque.rstrip("\n") + post
        accion = "actualizado"
    else:
        nuevo = bloque + ("\n" + existente if existente else "")
        accion = "insertado"

    if dry:
        print(f"  [dry-run] SOUL.md: bloque de agente {accion} (nombre='{nombre}' personalidad='{personalidad}')")
        return 0

    if soul_path.exists():
        backup = soul_path.with_suffix(soul_path.suffix + ".bak")
        backup.write_text(existente, encoding="utf-8")

    soul_path.parent.mkdir(parents=True, exist_ok=True)
    soul_path.write_text(nuevo, encoding="utf-8")
    print(f"  + SOUL.md: bloque de agente {accion} (nombre='{nombre}' personalidad='{personalidad}')")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
