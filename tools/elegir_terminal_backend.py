#!/usr/bin/env python3
"""Alterna terminal.backend del SERVIDOR (el dueño del perfil) entre `ssh` (apuntando a un
equipo secundario, si responde) y `local` (en el servidor mismo) — pensado para correr como
cron cada pocos minutos.

Corre EN el servidor (donde vive el perfil/memoria), nunca en el equipo secundario. Solo decide
dónde arrancan las tareas de terminal NUEVAS a partir de ahora — una tarea que ya estaba
corriendo en una máquina no "migra" sola si esa máquina se apaga a mitad de camino.

IMPORTANTE — verificar antes de usar en producción: la documentación pública de Hermes confirma
`TERMINAL_SSH_HOST` y `TERMINAL_SSH_USER` como variables de entorno obligatorias para el backend
`ssh`, pero no el nombre exacto de la clave equivalente en `config.yaml` (si existe una,
`terminal.ssh_host`/`terminal.ssh_user` es la mejor suposición, no un hecho confirmado). Probar
`hermes config set terminal.backend ssh` seguido de un comando de terminal real antes de confiar
este script a un cliente — si el host/usuario no toman por config, hay que exportarlos como
variables de entorno del proceso del gateway en su lugar (unit systemd: `Environment=`).

Uso:
    tools/elegir_terminal_backend.py --host <usuario@ip-secundaria> [--timeout 3]

Pensado para un cron tipo:
    tools/elegir_terminal_backend.py --host dani@100.x.y.z
cada 5 minutos, en el servidor.
"""
import argparse
import subprocess
import sys


def secundaria_responde(host: str, timeout: int) -> bool:
    try:
        r = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "BatchMode=yes", host, "true"],
            capture_output=True, timeout=timeout + 2,
        )
        return r.returncode == 0
    except Exception:
        return False


def hermes_config_set(clave: str, valor: str, dry_run: bool) -> bool:
    if dry_run:
        print(f"[dry-run] hermes config set {clave} {valor}")
        return True
    r = subprocess.run(["hermes", "config", "set", clave, valor], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"AVISO: 'hermes config set {clave} {valor}' falló: {r.stderr.strip()}", file=sys.stderr)
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True, help="usuario@ip-tailscale del equipo secundario")
    ap.add_argument("--timeout", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true", help="no toca config.yaml, solo imprime lo que haría")
    a = ap.parse_args()

    usuario, _, ip = a.host.partition("@")
    if not ip:
        sys.exit("--host debe ser usuario@ip")

    if secundaria_responde(a.host, a.timeout):
        print(f"{a.host} responde — terminal.backend = ssh")
        hermes_config_set("terminal.backend", "ssh", a.dry_run)
        hermes_config_set("terminal.ssh_host", ip, a.dry_run)
        hermes_config_set("terminal.ssh_user", usuario, a.dry_run)
    else:
        print(f"{a.host} no responde — terminal.backend = local (servidor)")
        hermes_config_set("terminal.backend", "local", a.dry_run)


if __name__ == "__main__":
    main()
