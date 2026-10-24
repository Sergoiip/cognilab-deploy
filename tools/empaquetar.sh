#!/usr/bin/env bash
# Genera un paquete .tar.gz del repo con su sha256, para clientes sin cuenta de GitHub.
#   tools/empaquetar.sh [carpeta_salida]      (por defecto ~/Documents/cognilab-deploy-paquetes)
# Solo incluye lo que git versiona (nunca manifiestos de clientes ni archivos locales) y corre el verificador antes.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$HOME/Documents/cognilab-deploy-paquetes}"
cd "$REPO"
[[ -z "$(git status --porcelain)" ]] || { echo "ERROR: hay cambios sin commit; confirma y vuelve a correr." >&2; exit 1; }
PY=python3; python3 -c 'import yaml' 2>/dev/null || { [[ -x "$HOME/.hermes/cache/scratch/gh/v/bin/python" ]] && PY="$HOME/.hermes/cache/scratch/gh/v/bin/python"; }
"$PY" tools/verificar.py | head -1
"$PY" tools/verificar.py >/dev/null || { echo "ERROR: el verificador falló; no se empaqueta." >&2; exit 1; }
V="$(git describe --tags --always)"
N="cognilab-deploy-$V"
mkdir -p "$OUT"
git archive --format=tar.gz --prefix="$N/" -o "$OUT/$N.tar.gz" HEAD
( cd "$OUT" && sha256sum "$N.tar.gz" > "$N.tar.gz.sha256" )
echo "Paquete: $OUT/$N.tar.gz"
echo "Hash:    $(cut -d' ' -f1 "$OUT/$N.tar.gz.sha256")"
echo "Entrega ambos archivos por enlace temporal. El cliente verifica con: sha256sum -c $N.tar.gz.sha256"
