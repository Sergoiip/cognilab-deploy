#!/usr/bin/env python3
"""Genera stack/catalogo.yaml y la plantilla del CRM. Se corre una vez; después se edita el YAML a mano."""
import json, yaml, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = "/home/sergoip/Documents/Obsidian/Bóveda de Operaciones/.obsidian/plugins/cadence-planner/data.json"
HASHES = "/home/sergoip/.hermes/cache/scratch/plug/hashes.json"

(ROOT/"stack/plantillas/cadence-crm").mkdir(parents=True, exist_ok=True)
d = json.load(open(SRC))
d["cadenceApiToken"] = ""
d["cadenceApiUrl"] = ""
json.dump(d, open(ROOT/"stack/plantillas/cadence-crm/data.json", "w"), ensure_ascii=False, indent=1)

h = json.load(open(HASHES))
PL = {pid: {"nombre": pid, "tipo": "obsidian-plugin", "repo": v["repo"], "version": v["version"],
            "licencia": v["licencia"], "sha256": v["sha256"]} for pid, v in h.items()}

def S(n, b, pm, para):
    return {"nombre": n, "tipo": "sistema", "bin": b, "pm": pm, "verificado": ["pacman"], "para": para}

cat = {
 "_nota": "Todo es gratis. Los plugins se bajan del release oficial y se verifican por sha256 (no se redistribuyen aquí). 'verificado' = gestores donde confirmé el nombre del paquete.",
 "apps": {
  "hermes": {"nombre": "Hermes Agent", "tipo": "hermes", "costo": "gratis",
             "url": "https://hermes-agent.nousresearch.com/install.sh", "para": "agente de IA"},
  "obsidian": S("Obsidian", "obsidian", {"pacman": "obsidian", "apt": "flatpak:md.obsidian.Obsidian", "dnf": "flatpak:md.obsidian.Obsidian"}, "bóveda / second brain"),
  "git": S("Git", "git", {"pacman": "git", "apt": "git", "dnf": "git"}, "versionar la bóveda"),
  "gh": S("GitHub CLI", "gh", {"pacman": "github-cli", "apt": "gh", "dnf": "gh"}, "respaldo en GitHub"),
  "ffmpeg": S("FFmpeg", "ffmpeg", {"pacman": "ffmpeg", "apt": "ffmpeg", "dnf": "ffmpeg-free"}, "audio y video"),
  "pandoc": S("Pandoc", "pandoc", {"pacman": "pandoc-cli", "apt": "pandoc", "dnf": "pandoc"}, "documentos"),
  "syncthing": S("Syncthing", "syncthing", {"pacman": "syncthing", "apt": "syncthing", "dnf": "syncthing"}, "sincronizar equipos sin nube"),
  "rclone": S("rclone", "rclone", {"pacman": "rclone", "apt": "rclone", "dnf": "rclone"}, "espejo con Drive u otra nube"),
  "obs-studio": S("OBS Studio", "obs", {"pacman": "obs-studio", "apt": "obs-studio"}, "captura multipista"),
  "kdenlive": S("Kdenlive", "kdenlive", {"pacman": "kdenlive", "apt": "kdenlive", "dnf": "kdenlive"}, "edición de video"),
  "inkscape": S("Inkscape", "inkscape", {"pacman": "inkscape", "apt": "inkscape", "dnf": "inkscape"}, "logos y vectores"),
  "gimp": S("GIMP", "gimp", {"pacman": "gimp", "apt": "gimp", "dnf": "gimp"}, "retoque de fotos"),
  "libreoffice": S("LibreOffice", "libreoffice", {"pacman": "libreoffice-fresh", "apt": "libreoffice", "dnf": "libreoffice"}, "cotizaciones y cuentas de cobro"),
  "faster-whisper": {"nombre": "Transcripción local (faster-whisper)", "tipo": "pip", "paquete": "faster-whisper", "para": "captura por voz"},
  **PL},
 "perfiles": {
  "ligero": {"escala": 1, "descripcion": "Individuo. Lo mínimo que funciona: bóveda + agente + respaldo.",
             "apps": ["hermes", "obsidian", "git", "gh", "obsidian-git", "templater-obsidian"]},
  "negocio": {"escala": 2, "descripcion": "1 a 5 personas. Suma tareas, CRM y sincronización.", "hereda": "ligero",
              "apps": ["tasknotes", "cadence-planner", "syncthing", "pandoc", "ffmpeg"]},
  "equipo": {"escala": 3, "descripcion": "Varios roles. Suma espejo en nube y mapas.", "hereda": "negocio",
             "apps": ["rclone", "obsidian-excalidraw-plugin"]}},
 "por_modulo": {"A2": ["obsidian", "obsidian-git", "templater-obsidian"], "A3": ["tasknotes"], "A5": ["rclone", "syncthing"],
  "B1": ["hermes"], "B2": ["hermes"], "B3": ["faster-whisper", "ffmpeg"], "B4": ["gh"], "B5": ["obsidian-excalidraw-plugin"],
  "C1": ["inkscape", "gimp"], "C2": ["pandoc", "libreoffice"], "C3": ["pandoc"], "C6": ["ffmpeg", "kdenlive"],
  "D1": ["obs-studio"], "D2": ["kdenlive", "ffmpeg"]},
 "por_modulo_desde_escala": {"A2": {"2": ["cadence-planner"]}},
 "plantillas": {"cadence-planner": "stack/plantillas/cadence-crm/data.json"},
 "cuentas_manuales": {
  "telegram": "Cuenta o bot de Telegram (BotFather). Gratis.",
  "whatsapp-business": "WhatsApp Business: la app es gratis; la API oficial tiene costo.",
  "discord": "Servidor de Discord del cliente. Gratis.",
  "google-drive": "Cuenta de Google del cliente (15 GB gratis)."}}
yaml.safe_dump(cat, open(ROOT/"stack/catalogo.yaml", "w"), allow_unicode=True, sort_keys=False)
print(len(cat["apps"]), "apps; plantilla CRM", (ROOT/"stack/plantillas/cadence-crm/data.json").stat().st_size, "bytes")
