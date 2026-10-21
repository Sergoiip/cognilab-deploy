#!/usr/bin/env bash
# Deja un PC listo según el manifiesto del cliente. Idempotente: se puede repetir sin romper nada.
#   bootstrap/instala.sh manifiestos/cliente.yaml [--dry-run]
# Instala SOLO los módulos que el manifiesto pide (más E2 Entrega verificada, siempre).
set -euo pipefail

MANIFIESTO="${1:-}"; DRY=0; [[ "${2:-}" == "--dry-run" ]] && DRY=1
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HH="${HERMES_HOME:-$HOME/.hermes}"
DEST="$HH/skills/cognilab-deploy"

die() { echo "ERROR: $*" >&2; exit 1; }
run() { if [[ $DRY -eq 1 ]]; then echo "  [dry-run] $*"; else eval "$@"; fi; }

[[ -n "$MANIFIESTO" && -f "$MANIFIESTO" ]] || die "uso: instala.sh <manifiesto.yaml> [--dry-run]"

echo "== 1/4 Preflight"
PY=""
for c in /usr/bin/python3 python3 "$HH/hermes-agent/venv/bin/python"; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import yaml' 2>/dev/null; then PY="$c"; break; fi
done
[[ -n "$PY" ]] || die "no encuentro un Python con PyYAML (instala python-yaml)"
[[ -d "$HH" ]] || die "no existe $HH: instala Hermes primero"
echo "  SO: $(uname -sr) · Hermes en: $HH · disco libre: $(df -h "$HH" | awk 'NR==2{print $4}')"

echo "== 2/4 Resolver módulos del manifiesto"
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
for l in "${SLUGS[@]}"; do echo "  - ${l%%|*}  ${l#*|}" | cut -d'|' -f1; done

echo "== 3/4 Instalar skills en $DEST"
run "mkdir -p '$DEST'"
for l in "${SLUGS[@]}"; do
  IFS='|' read -r id slug src <<<"$l"
  run "rm -rf '$DEST/$slug' && cp -r '$src' '$DEST/$slug'"
done

echo "== 4/4 Registrar versión instalada"
VER="$(git -C "$REPO" describe --tags --always 2>/dev/null || echo sin-git)"
run "cp '$MANIFIESTO' '$DEST/MANIFIESTO.yaml' && printf '%s\n' '$VER' > '$DEST/VERSION'"
echo "Listo. Versión del repo: $VER. Anótala en Cadence junto al cliente."
[[ $DRY -eq 1 ]] && echo "(dry-run: no se escribió nada)"
exit 0
