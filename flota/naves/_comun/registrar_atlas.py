#!/usr/bin/env python3
"""Registra una actividad en Atlas (ATLAS.SYS) con la misma forma que escribe el plugin (src/crm/servicio.ts):
<carpeta Atlas>/CRM/Actividades/AAAA-MM/<fecha>-<usuario>-<sufijo>.md con atlas_type: actividad, vinculada con
`atlas_sobre` a las fichas de Cadence (empresa o contacto). La nota queda en la bóveda (respaldo con su git).

Uso: registrar_atlas.py --titulo "..." --sobre "<cliente>" --nota-archivo resumen.md \
        [--clase nota] [--siguiente "acción" --fecha AAAA-MM-DD] [--usuario promempteo] [--boveda ...]
Imprime la ruta de la nota creada. Si ya existe una actividad con el mismo título ese día, no la duplica.
"""
import argparse, os, re, sys, time, datetime as dt
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--titulo", required=True)
ap.add_argument("--sobre", action="append", default=[])
ap.add_argument("--con", action="append", default=[])
ap.add_argument("--clase", default="nota", choices=["nota", "reunion", "llamada", "correo", "tarea"])
ap.add_argument("--nota-archivo")
ap.add_argument("--siguiente")
ap.add_argument("--fecha")
ap.add_argument("--usuario", default="promempteo")
ap.add_argument("--boveda", default=os.path.expanduser("~/Documents/Obsidian/Bóveda de Operaciones"))
a = ap.parse_args()

ATLAS = Path(a.boveda) / "04 - Infraestructura" / "ATLAS.SYS"
if not ATLAS.is_dir():
    sys.exit(f"✗ No encuentro Atlas en {ATLAS}")
hoy = dt.date.today().isoformat()
if a.siguiente and (not a.fecha or a.fecha < hoy):
    sys.exit("✗ La siguiente acción necesita una fecha de hoy en adelante (regla de Atlas).")
cad = Path(a.boveda) / "04 - Infraestructura" / "Cadence"
for s in a.sobre:
    if not any((cad / sub / f"{s}.md").exists() for sub in ("Companies", "Contacts", "Clients", "Projects", "Pipeline")):
        print(f"⚠ «{s}» no es una ficha de Cadence; el vínculo quedará como texto.", file=sys.stderr)

carpeta = ATLAS / "CRM" / "Actividades" / hoy[:7]
carpeta.mkdir(parents=True, exist_ok=True)
for p in carpeta.glob(f"{hoy}-*.md"):
    if f'atlas_titulo: "{a.titulo}"' in p.read_text(encoding="utf-8", errors="replace")[:600]:
        print(p); sys.exit(0)

# el autor debe existir como miembro del equipo de Atlas
m = ATLAS / "Equipo" / f"{a.usuario}.md"
if not m.exists():
    m.write_text(f'---\natlas_type: miembro\natlas_handle: "{a.usuario}"\natlas_nombre: "{a.usuario.capitalize()}"\n'
                 f'atlas_activo: true\natlas_modificado: "{dt.datetime.now().astimezone().isoformat(timespec="seconds")}"\n---\n\n'
                 f"# {a.usuario.capitalize()}\n\nAgente de la Flota (Estación Negocio). Registra los pulsos semanales de los clientes.\n", encoding="utf-8")

ms = int(time.time() * 1000)
def b36(n):
    s = "0123456789abcdefghijklmnopqrstuvwxyz"; o = ""
    while n: n, r = divmod(n, 36); o = s[r] + o
    return o or "0"
id_ = f"{a.usuario}-{b36(ms)}"
q = lambda s: '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
lineas = ["---", "atlas_type: actividad", f"atlas_id: {q(id_)}", f"atlas_titulo: {q(a.titulo)}", f"atlas_clase: {a.clase}",
          f"atlas_cuando: {hoy}", "atlas_con:" + ("" if a.con else " []"), *[f'  - "[[{c}]]"' for c in a.con],
          "atlas_sobre:" + ("" if a.sobre else " []"), *[f'  - "[[{s}]]"' for s in a.sobre]]
if a.siguiente:
    lineas += [f"atlas_siguiente_accion: {q(a.siguiente)}", f"atlas_siguiente_fecha: {a.fecha}"]
lineas += [f"atlas_autor: {q(a.usuario)}", "atlas_fuente: agente", "---", ""]
cuerpo = Path(a.nota_archivo).read_text(encoding="utf-8") if a.nota_archivo else ""
ruta = carpeta / f"{hoy}-{a.usuario}-{id_.split('-')[-1]}.md"
ruta.write_text("\n".join(lineas) + f"\n# {a.titulo}\n\n{cuerpo.strip()}\n", encoding="utf-8")
print(ruta)
