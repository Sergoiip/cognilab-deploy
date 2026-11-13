#!/usr/bin/env bash
# Deja un PC listo según el manifiesto del cliente. Idempotente: se puede repetir sin romper nada.
#   bootstrap/instala.sh --base [--dry-run]                       (1.º: sin manifiesto)
#   bootstrap/instala.sh manifiestos/cliente.yaml [--dry-run] [--sin-apps] [--si] [--espacio]
# Desde 0.28.0 el manifiesto se arma DURANTE la instalación: --base deja el agente con la skill
# cd-manifiesto-en-vivo, el Hermes del cliente hace las preguntas y luego corre este script
# con el manifiesto que resultó (bootstrap/skill-manifiesto/SKILL.md).
# Las apps son OPCIONALES: sin --si pregunta cuáles instalar (sin terminal, no instala ninguna).
# Instala los módulos pedidos (más E2, siempre) y las aplicaciones que el manifiesto resuelve.
set -euo pipefail

MANIFIESTO=""; DRY=0; SIN_APPS=0; SI=0; BASE=0; ESPACIO=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --sin-apps) SIN_APPS=1 ;;
    --si) SI=1 ;;
    --base) BASE=1 ;;
    --espacio) ESPACIO=1 ;;
    *) MANIFIESTO="$a" ;;
  esac
done
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HH="${HERMES_HOME:-$HOME/.hermes}"
DEST="$HH/skills/cognilab-deploy"
REPL="$HH/skills/cognilab-replicables"   # skills de aprendizaje/Skills replicables que piden los módulos activos
MANUALES=()

die() { echo "ERROR: $*" >&2; exit 1; }
run() { if [[ $DRY -eq 1 ]]; then echo "  [dry-run] $*"; else eval "$@"; fi; }

if [[ $BASE -eq 0 ]]; then
  [[ -n "$MANIFIESTO" && -f "$MANIFIESTO" ]] || die "uso: instala.sh --base  |  instala.sh <manifiesto.yaml> [--dry-run] [--sin-apps]"
fi
instalar_todos_los_modulos() {   # desde 0.29.0: los 22 módulos viajan siempre; el manifiesto solo marca cuáles están activos
  for d in "$REPO"/modulos/*/cd-*/; do
    d="${d%/}"; run "rm -rf '$DEST/$(basename "$d")' && cp -r '$d' '$DEST/$(basename "$d")'"
  done
  echo "  $(ls -d "$REPO"/modulos/*/cd-*/ | wc -l) módulos instalados"
}
instalar_skill_manifiesto() {
  run "mkdir -p '$DEST/cd-manifiesto-en-vivo' && sed 's#~/cognilab-deploy#$REPO#g' '$REPO/bootstrap/skill-manifiesto/SKILL.md' > '$DEST/cd-manifiesto-en-vivo/SKILL.md'"
}

echo "== 1/$([[ $BASE -eq 1 ]] && echo 3 || echo 7) Preflight"
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

if [[ $BASE -eq 1 ]]; then
  echo "== 2/3 Base: todos los módulos + manifiesto en vivo en $DEST (ninguno activo todavía)"
  run "mkdir -p '$DEST'"
  instalar_todos_los_modulos
  instalar_skill_manifiesto
  run ": > '$DEST/ACTIVOS'"
  echo "== 3/3 Registrar versión"
  VER="$(git -C "$REPO" describe --tags --always 2>/dev/null || echo sin-git)"
  run "printf '%s\n' '$VER' > '$DEST/VERSION'"
  echo "Base lista (versión $VER). Siguiente paso: abre Hermes en este equipo y escribe"
  echo "  «Arma mi manifiesto de CogniLab»"
  echo "Hermes hará las preguntas en ventanas de respuesta y terminará la instalación con tu aprobación."
  [[ $DRY -eq 1 ]] && echo "(dry-run: no se escribió nada)"
  exit 0
fi

echo "== 2/7 Resolver módulos del manifiesto"
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

echo "== 3/7 Estructura de la bóveda (se refleja de inmediato)"
if [[ $DRY -eq 1 ]]; then
  "$PY" "$REPO/tools/scaffold_vault.py" "$MANIFIESTO" --dry-run
else
  "$PY" "$REPO/tools/scaffold_vault.py" "$MANIFIESTO"
fi

echo "== 4/7 Instalar módulos en $DEST"
run "mkdir -p '$DEST'"
instalar_todos_los_modulos
ACT=""; for l in "${SLUGS[@]}"; do ACT+="${l%%|*} "; done
echo "  activos según el manifiesto: $ACT"
run "printf '%s\n' $ACT > '$DEST/ACTIVOS'"
instalar_skill_manifiesto   # para ajustar el manifiesto después (p. ej. tras la sesión de mapeo)

echo "== Personalizar agente (nombre y personalidad)"
if [[ $DRY -eq 1 ]]; then
  "$PY" "$REPO/tools/personalizar_agente.py" "$MANIFIESTO" "$HH" --dry-run
else
  "$PY" "$REPO/tools/personalizar_agente.py" "$MANIFIESTO" "$HH"
fi

echo "== 5/7 Aplicaciones"
if [[ $SIN_APPS -eq 1 ]]; then
  echo "  (omitido por --sin-apps)"
else
  LISTA="$("$PY" "$REPO/tools/stack.py" lista "$MANIFIESTO" --pm "$PM")" || die "no se pudo resolver el stack"
  EXCL=""
  echo "  Propuesta (todo opcional):"
  echo "$LISTA" | awk -F'|' '$1=="INFO"{print "  "$2} $1=="APP"{n++; printf "   %2d) %-44s %s [%s]\n", n, $3, $4, $5}'
  if [[ $DRY -eq 0 && $SI -eq 0 ]]; then
    if [[ -t 0 ]]; then
      read -r -p "  Enter = instalar todas · números separados por coma = QUITAR esas · n = ninguna: " R
      case "$R" in
        "") ;;
        n|N) EXCL="$(echo "$LISTA" | awk -F'|' '$1=="APP"{printf "%s%s", s, $2; s=","}')" ;;
        *) EXCL="$(echo "$LISTA" | awk -F'|' -v q="$R" 'BEGIN{n=split(q,a,","); for(i=1;i<=n;i++) m[a[i]+0]=1} $1=="APP"{k++; if(k in m){printf "%s%s", s, $2; s=","}}')" ;;
      esac
    else
      echo "  Sin terminal y sin --si: no se instala ninguna app (usa --si para aceptar la propuesta)."
      EXCL="$(echo "$LISTA" | awk -F'|' '$1=="APP"{printf "%s%s", s, $2; s=","}')"
    fi
  fi
  PLAN="$("$PY" "$REPO/tools/stack.py" plan "$MANIFIESTO" --pm "$PM" --excluir "$EXCL")" || die "no se pudo resolver el stack"
  VAULT="$("$PY" -c 'import sys,yaml,os;print(os.path.expanduser(yaml.safe_load(open(sys.argv[1])).get("vault","")))' "$MANIFIESTO")"
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
          if [[ $DRY -eq 1 ]]; then "$PY" "$REPO/tools/stack.py" plugins "$MANIFIESTO" --vault "$VAULT" --excluir "$EXCL" --dry-run | sed 's/^/    /'
          else "$PY" "$REPO/tools/stack.py" plugins "$MANIFIESTO" --vault "$VAULT" --excluir "$EXCL" | sed 's/^/    /'; fi
        fi ;;
      MANUAL) MANUALES+=("$a") ;;
    esac
  done <<<"$PLAN"
fi

if [[ $ESPACIO -eq 1 ]]; then
  echo "== 5b Espacio de trabajo (patrón ICM)"
  EV="$("$PY" -c 'import sys,yaml,os;print(os.path.expanduser(yaml.safe_load(open(sys.argv[1])).get("vault","")))' "$MANIFIESTO")"
  if [[ -z "$EV" ]]; then echo "  (omitido: el manifiesto no trae 'vault:')"
  else
    EDRY=""; [[ $DRY -eq 1 ]] && EDRY="--dry-run"
    "$PY" "$REPO/tools/espacio.py" crear "$MANIFIESTO" --destino "$EV/Espacio CogniLab" $EDRY | sed 's/^/  /'
  fi
fi


# Composio va primero en la lista «a mano»: es prioridad del setup (bootstrap/COMPOSIO.md).
if grep -q "connect.composio.dev" "$HH/config.yaml" 2>/dev/null; then echo "  = Composio ya está configurado en este perfil (probar con 'hermes mcp test composio')"; else
MANUALES=("PRIORIDAD · Conectar Composio: el cliente corre 'hermes mcp add composio --url https://connect.composio.dev/mcp --auth header' con su clave y autoriza sus cuentas desde el chat (bootstrap/COMPOSIO.md)" ${MANUALES[@]+"${MANUALES[@]}"})
fi
# Toda instalación con canal de mensajería deja pendiente la transcripción con Groq (después del gateway).
if "$PY" -c 'import sys,yaml;c=(yaml.safe_load(open(sys.argv[1])).get("herramientas") or {}).get("cuentas") or [];sys.exit(0 if any(x in str(c).lower() for x in ("telegram","whatsapp","discord","signal")) else 1)' "$MANIFIESTO"; then
  MANUALES+=("Después de configurar el gateway: activar la transcripción de audios con Groq (bootstrap/TRANSCRIPCION-GROQ.md; la clave la guarda el cliente)")
fi

echo "== 6/7 Skills de Hermes que piden los módulos activos"
# Fuente de cada una: aprendizaje/Skills replicables (se copia), Hermes (ya viene) o el hub
# (stack/skills_hermes.yaml). Las que no se encuentran pasan a la lista «a mano».
PLAN_SK="$("$PY" "$REPO/tools/skills_hermes.py" plan $ACT --hermes-home "$HH" --destino "$REPL")" || die "no se pudo resolver las skills de Hermes"
HAY_HERMES=0; command -v hermes >/dev/null 2>&1 && HAY_HERMES=1
while IFS='|' read -r tipo nombre det; do
  case "$tipo" in
    YA)     echo "  = $nombre (ya instalada en $det)" ;;
    REPO)   echo "  + $nombre (del repo)"
            run "mkdir -p '$REPL' && rm -rf '$REPL/$nombre' && cp -r '$det' '$REPL/$nombre'" ;;
    HERMES) echo "  = $nombre (viene con Hermes; se siembra al abrir Hermes)" ;;
    HUB)    if [[ $HAY_HERMES -eq 1 ]]; then echo "  + $nombre (hub: $det)"
              run "HERMES_HOME='$HH' hermes skills install '$det' --yes" || MANUALES+=("Skill $nombre: falló 'hermes skills install $det --yes'; repetirlo a mano")
            else MANUALES+=("Skill $nombre: instalar Hermes y luego 'hermes skills install $det --yes'"); fi ;;
    FALTA)  MANUALES+=("Skill $nombre (módulos $det): no está en el repo, ni en Hermes, ni en el hub") ;;
  esac
done <<<"$PLAN_SK"
if [[ ${#MANUALES[@]} -gt 0 ]]; then echo "  A mano (no se pueden automatizar):"; for m in "${MANUALES[@]}"; do echo "    [ ] $m"; done; fi

echo "== 7/7 Registrar versión instalada"
VER="$(git -C "$REPO" describe --tags --always 2>/dev/null || echo sin-git)"
run "cp '$MANIFIESTO' '$DEST/MANIFIESTO.yaml' && printf '%s\n' '$VER' > '$DEST/VERSION'"
echo "Listo. Versión del repo: $VER. Anótala en Cadence junto al cliente."
[[ $DRY -eq 1 ]] && echo "(dry-run: no se escribió nada)"
exit 0
