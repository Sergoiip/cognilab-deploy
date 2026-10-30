#!/usr/bin/env python3
"""Marca qué cliente está en su semana de Radiografía (Fase 0), para que el cron de guía diaria
sepa de qué cliente hablar sin que haya que repetírselo cada día.

Guarda el estado FUERA del repo (nunca en git): `~/.hermes/cache/radiografia-activa.json`.
Solo un cliente activo a la vez (operación de una sola persona).

Uso:
    tools/radiografia_activa.py start <cliente> <ruta-radiografia.yaml> [--repo <ruta-repo>]
    tools/radiografia_activa.py status
    tools/radiografia_activa.py parar
"""
import argparse
import datetime
import json
import pathlib
import sys

ESTADO = pathlib.Path.home() / ".hermes" / "cache" / "radiografia-activa.json"


def start(a):
    ESTADO.parent.mkdir(parents=True, exist_ok=True)
    estado = {
        "cliente": a.cliente,
        "radiografia_yaml": str(pathlib.Path(a.radiografia_yaml).expanduser()),
        "repo": str(pathlib.Path(a.repo).expanduser()) if a.repo else str(pathlib.Path(__file__).resolve().parent.parent),
        "fecha_inicio": datetime.date.today().isoformat(),
    }
    ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Radiografía activa: {a.cliente} desde {estado['fecha_inicio']}. Reanuda el cron 'Radiografía — guía diaria' ahora.")


def status(a):
    if not ESTADO.exists():
        print("Sin radiografía activa.")
        return
    estado = json.loads(ESTADO.read_text(encoding="utf-8"))
    inicio = datetime.date.fromisoformat(estado["fecha_inicio"])
    habiles = 0
    d = inicio
    hoy = datetime.date.today()
    while d <= hoy:
        if d.weekday() < 5:
            habiles += 1
        d += datetime.timedelta(days=1)
    print(json.dumps(estado, ensure_ascii=False, indent=2))
    print(f"Día hábil de la semana: {habiles} (1 a 5 según fases/0-radiografia.md)")


def parar(a):
    if ESTADO.exists():
        ESTADO.unlink()
        print("Radiografía activa borrada. Pausa el cron 'Radiografía — guía diaria' si no hay otro cliente en camino.")
    else:
        print("No había ninguna activa.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="accion", required=True)

    p_start = sub.add_parser("start")
    p_start.add_argument("cliente")
    p_start.add_argument("radiografia_yaml")
    p_start.add_argument("--repo")
    p_start.set_defaults(fn=start)

    p_status = sub.add_parser("status")
    p_status.set_defaults(fn=status)

    p_parar = sub.add_parser("parar")
    p_parar.set_defaults(fn=parar)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
