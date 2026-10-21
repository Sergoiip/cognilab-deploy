#!/usr/bin/env bash
# Deja un PC listo según el manifiesto del cliente. Idempotente: se puede repetir sin romper nada.
#   bootstrap/instala.sh manifiestos/cliente.yaml [--dry-run] [--sin-apps]
# Instala los módulos pedidos (más E2, siempre) y las aplicaciones que el manifiesto resuelve.
set -euo pipefail

MANIFIESTO=""; DRY=0; SIN_APPS=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --sin-apps) SIN_APPS=1 ;;
    *) MANIFIESTO="$a" ;;
  esac
done
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HH="${HERMES_HOME:-$HOME/.hermes}"
DEST="$HH/skills/cognilab-deploy"

die() { echo "ERROR: $*" >&2; exit 1; }
run() { if [[ $DRY -eq 1 ]]; then echo "  [dry-run] $*"; else eval "$@"; fi; }

[[ -n "$MANIFIESTO" && -f "$MANIFIESTO" ]] || die "uso: instala.sh <manifiesto.yaml> [--dry-run] [--sin-apps]"

echo "== 1/5 Preflight"
PY=""
for c in /usr/bin/python3 python3 "$HH/hermes-agent/venv/bin/python"; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import yaml' 2>/dev/null; then PY="$c"; break; fi
done
[[ -n "$PY" ]] || die "no encuentro un Python con PyYAML (pacman: python-yaml · apt: python3-yaml · dnf: python3-pyyaml)"
PM=""
for c in pacman apt-get dnf; do command -v "$c" >/dev/null 2>&1 && { PM="$c"; break; }; done
[[ "$PM" == "apt-get" ]] && PM="apt"
[[ -n "$PM" ]] || die "gestor de paquetes no soportado (solo pacman, apt, dnf)"
echo "  SO: $(uname -sr) · gestor: $PM · Hermes en: $HH · disco libre: $(df -h "$HOME" | awk 'NR==2{print $4}')"

echo "== 2/5 Resolver módulos del manifiesto"
RESUELTO="$("$PY" - "$MANIFIESTO" "$REPO" <<'PY'
import sys, yaml, pathlib
man = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
repo = pathlib.Path(sys.argv[2])
por_id = {}
for f in repo.glob("modulos/*/*/modulo.yaml"):
    m = yaml.safe_load(f.read_text(encoding="utf-8")); por_id[m["id"]] = (m["slug"], f.parent)
ids = [x["id"] for x in man.get("modulos", [])] + ["E2"]
vistos = []
for i in ids:
    if i not in por_id:
        sys.exit(f"módulo desconocido en el manifiesto: {i}")
    if i not in vistos:
        vistos.append(i); print(f"{i}|{por_id[i][0]}|{por_id[i][1]}")
PY
)" || die "manifiesto inválido (ver mensaje arriba)"
mapfile -t SLUGS <<<"$RESUELTO"
for l in "${SLUGS[@]}"; do echo "  - ${l%%|*}"; done

echo "== 3/5 Instalar skills en $DEST"
run "mkdir -p '$DEST'"
for l in "${SLUGS[@]}"; do
  IFS='|' read -r id slug src <<<"$l"
  run "rm -rf '$DEST/$slug' && cp -r '$src' '$DEST/$slug'"
done

echo "== 4/5 Aplicaciones"
if [[ $SIN_APPS -eq 1 ]]; then
  echo "  (omitido por --sin-apps)"
else
  PLAN="$("$PY" "$REPO/tools/stack.py" plan "$MANIFIESTO" --pm "$PM")" || die "no se pudo resolver el stack"
  VAULT="$("$PY" -c 'import sys,yaml,os;print(os.path.expanduser(yaml.safe_load(open(sys.argv[1])).get("vault","")))' "$MANIFIESTO")"
  MANUALES=()
  while IFS='|' read -r tipo a b; do
    case "$tipo" in
      INFO) echo "  $a" ;;
      SKIP) echo "  = $a ($b)" ;;
      HERMES)
        if [[ -d "$HH" ]]; then echo "  = hermes (ya instalado)"; else
          echo "  + hermes (instalador oficial)"
          run "T=\$(mktemp) && curl -fsSL '$a' -o \"\$T\" && bash \"\$T\" && rm -f \"\$T\""
        fi ;;
      PKG)
        echo "  + paquetes: $a"
        case "$PM" in
          pacman) run "sudo pacman -S --needed --noconfirm $a" ;;
          apt)    run "sudo apt-get install -y $a" ;;
          dnf)    run "sudo dnf install -y $a" ;;
        esac ;;
      FLATPAK) echo "  + flatpak: $a"; run "flatpak install -y flathub '$a'" ;;
      PIP)
        echo "  + pip (venv propio): $a"
        run "python3 -m venv '$HH/venvs/cognilab' && '$HH/venvs/cognilab/bin/pip' install -q $a" ;;
      PLUGINS)
        if [[ -z "$VAULT" ]]; then MANUALES+=("Plugins de Obsidian ($a): el manifiesto no trae 'vault:'")
        else
          echo "  + plugins de Obsidian en $VAULT: $a"
          if [[ $DRY -eq 1 ]]; then "$PY" "$REPO/tools/stack.py" plugins "$MANIFIESTO" --vault "$VAULT" --dry-run | sed 's/^/    /'
          else "$PY" "$REPO/tools/stack.py" plugins "$MANIFIESTO" --vault "$VAULT" | sed 's/^/    /'; fi
        fi ;;
      MANUAL) MANUALES+=("$a") ;;
    esac
  done <<<"$PLAN"
  if [[ ${#MANUALES[@]} -gt 0 ]]; then echo "  A mano (no se pueden automatizar):"; for m in "${MANUALES[@]}"; do echo "    [ ] $m"; done; fi
fi

echo "== 5/5 Registrar versión instalada"
VER="$(git -C "$REPO" describe --tags --always 2>/dev/null || echo sin-git)"
run "cp '$MANIFIESTO' '$DEST/MANIFIESTO.yaml' && printf '%s\n' '$VER' > '$DEST/VERSION'"
echo "Listo. Versión del repo: $VER. Anótala en Cadence junto al cliente."
[[ $DRY -eq 1 ]] && echo "(dry-run: no se escribió nada)"
exit 0
