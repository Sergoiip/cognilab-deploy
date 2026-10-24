#!/usr/bin/env bash
# Inventario de solo lectura del equipo del cliente. Corre CON PERMISO. No envía nada a ningún lado.
#   tools/inventario.sh > inventario.yaml
# No lee archivos personales, solo versiones, recursos y qué herramientas del catálogo hay.
set -u
has() { command -v "$1" >/dev/null 2>&1 && echo true || echo false; }
PM=none; for c in pacman apt-get dnf; do command -v $c >/dev/null 2>&1 && { PM=$c; break; }; done
[ "$PM" = apt-get ] && PM=apt
. /etc/os-release 2>/dev/null
SUDO=false; if sudo -n true 2>/dev/null; then SUDO=true; elif id -nG 2>/dev/null | grep -qwE 'sudo|wheel'; then SUDO=probable; fi
GPU=$(lspci 2>/dev/null | grep -iE 'vga|3d' | head -1 | sed 's/.*: //' | tr -d '"')
cat <<YAML
so: "$(uname -s) ${PRETTY_NAME:-}"
kernel: "$(uname -r)"
gestor_paquetes: $PM
soportado_por_instalador: $([ "$PM" != none ] && echo true || echo false)
ram_gb: $(awk '/MemTotal/{printf "%.0f", $2/1048576}' /proc/meminfo 2>/dev/null || echo null)
disco_libre_home: "$(df -h "$HOME" | awk 'NR==2{print $4}')"
gpu: "${GPU:-desconocida}"
admin: $SUDO
herramientas:
  hermes: $(has hermes)
  obsidian: $(has obsidian)
  git: $(has git)
  gh: $(has gh)
  ffmpeg: $(has ffmpeg)
  pandoc: $(has pandoc)
  syncthing: $(has syncthing)
  rclone: $(has rclone)
  obs-studio: $(has obs)
  kdenlive: $(has kdenlive)
  inkscape: $(has inkscape)
  gimp: $(has gimp)
  libreoffice: $(has libreoffice)
  faster-whisper: $(python3 -c 'import faster_whisper' 2>/dev/null && echo true || echo false)
YAML
