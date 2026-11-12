#!/usr/bin/env python3
"""Contexto de un cliente para el pulso semanal (solo lectura). Reúne en un solo texto lo que la misión necesita
contrastar: su proyecto en Cadence, lo que cambió en su carpeta, sus tareas en Atlas (TaskNotes), sus actividades
de Atlas, el pulso anterior y sus tarjetas en el Ágora. No resume ni opina: entrega los datos con su ruta.

Uso: contexto_cliente.py --cliente "<cliente>" --proyecto "<nota del proyecto en Cadence>" \
        --carpeta "<carpeta del cliente en Cadence>" --sobre "<cliente>" [--sobre ...] [--boveda ...] [--dias 7]
"""
import argparse, glob, os, re, sqlite3, sys, time, datetime as dt
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--cliente", required=True)
ap.add_argument("--proyecto", required=True)
ap.add_argument("--carpeta", required=True)
ap.add_argument("--sobre", action="append", default=[])
ap.add_argument("--boveda", default=os.path.expanduser("~/Documents/Obsidian/Bóveda de Operaciones"))
ap.add_argument("--dias", type=int, default=7)
a = ap.parse_args()
B = Path(a.boveda); INF = B / "04 - Infraestructura"
desde = time.time() - a.dias * 86400
claves = [s.lower() for s in [a.cliente, *a.sobre] if s] + [w.lower() for w in re.findall(r"[A-ZÁÉÍÓÚ][\wáéíóú]{3,}", a.cliente)]
def menciona(txt):
    t = txt.lower(); return any(k in t for k in claves)
def fm(texto):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", texto, re.S)
    if not m: return {}, texto
    d = {}
    for linea in m.group(1).splitlines():
        mm = re.match(r"([A-Za-z_]+):\s*(.*)", linea)
        if mm: d[mm.group(1)] = mm.group(2).strip().strip('"')
    return d, m.group(2)
def fecha(ts): return dt.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
def leer(p, n=None):
    try: t = Path(p).read_text(encoding="utf-8", errors="replace")
    except Exception: return ""
    return t if n is None else "\n".join(t.splitlines()[-n:])

print(f"# Contexto · {a.cliente} · {dt.date.today().isoformat()} (últimos {a.dias} días)\n")

# 1. Proyecto en Cadence
pp = INF / "Cadence" / "Projects" / f"{a.proyecto}.md"
print(f"## 1. Proyecto en Cadence\nRuta: `{pp}`")
if pp.exists():
    d, cuerpo = fm(leer(pp))
    print("Estado: " + ", ".join(f"{k}={d[k]}" for k in ("status", "priority", "started", "due") if k in d))
    print("\n" + cuerpo.strip()[:6000])
else:
    print("[no existe la nota del proyecto]")

# 2. Carpeta del cliente: lo que cambió y sus documentos vivos
C = Path(a.carpeta)
print(f"\n## 2. Carpeta del cliente\nRuta: `{C}`")
cambios = sorted([p for p in C.rglob("*") if p.is_file() and p.stat().st_mtime >= desde and "/_archivo/" not in str(p)],
                 key=lambda p: -p.stat().st_mtime)
print(f"Cambió en {a.dias} días: {len(cambios)} archivo(s)")
for p in cambios[:25]:
    print(f"- {fecha(p.stat().st_mtime)} · `{p.relative_to(C)}`")
vivos = [p for p in sorted(C.glob("*.md")) if re.search(r"(?i)bit[aá]cora|pendientes|requerimientos|plan|roadmap|objetivos|alcance", p.name)]
for p in vivos:
    t = leer(p)
    corto = len(t.splitlines()) <= 120
    print(f"\n### {p.name} · modificado {fecha(p.stat().st_mtime)}" + ("" if corto else " · (últimas 60 líneas)"))
    print((t if corto else leer(p, 60)).strip()[:5000])
canvas = sorted(C.glob("*.canvas"))
if canvas:
    print("\nLienzos: " + ", ".join(f"`{c.name}` ({fecha(c.stat().st_mtime)})" for c in canvas))

# 3. Tareas en Atlas (TaskNotes)
T = INF / "TaskNotes" / "Tasks"
print(f"\n## 3. Tareas en Atlas (TaskNotes)\nRuta: `{T}`")
filas = []
for p in sorted(T.glob("*.md")):
    t = leer(p); d, cuerpo = fm(t)
    if menciona(p.stem) or menciona(t[:3000]):
        filas.append((d.get("status", "?"), d.get("priority", ""), d.get("due", "") or d.get("scheduled", ""), p.stem, p.stat().st_mtime))
orden = {"in-progress": 0, "open": 1, "none": 2, "done": 3}
for s, pr, due, nom, mt in sorted(filas, key=lambda x: (orden.get(x[0], 2), x[2] or "9")):
    print(f"- [{s}] {nom}" + (f" · prioridad {pr}" if pr and pr != "none" else "") + (f" · fecha {due}" if due else "") + f" · tocada {fecha(mt)}")
if not filas:
    print("- (ninguna tarea menciona al cliente)")

# 4. Actividades de Atlas sobre el cliente (incluye pulsos anteriores)
A = INF / "ATLAS.SYS" / "CRM" / "Actividades"
print(f"\n## 4. Actividades en Atlas sobre el cliente\nRuta: `{A}`")
acts = []
for p in A.rglob("*.md"):
    d, cuerpo = fm(leer(p))
    sobre = " ".join(re.findall(r"\[\[([^\]]+)\]\]", leer(p)[:1500]))
    if d.get("atlas_type") == "actividad" and (menciona(sobre) or menciona(d.get("atlas_titulo", ""))):
        acts.append((d.get("atlas_cuando", ""), d.get("atlas_titulo", p.stem), p, cuerpo))
acts.sort(key=lambda x: x[0], reverse=True)
for cu, ti, p, cuerpo in acts[:8]:
    print(f"- {cu} · {ti} · `{p.name}`")
prev = next((x for x in acts if x[1].startswith("Pulso semanal")), None)
if prev:
    print(f"\n### Pulso anterior ({prev[0]})\n{prev[3].strip()[:4000]}")
else:
    print("\n(Es el primer pulso de este cliente.)")

# 5. Ágora: tarjetas del cliente
print("\n## 5. Tarjetas en el Ágora")
dbs = [Path.home() / ".hermes" / "kanban.db"] + [Path(x) for x in glob.glob(str(Path.home() / ".hermes" / "kanban" / "boards" / "*" / "kanban.db"))]
n = 0
for db in dbs:
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        for tid, ti, st, asg, ten, fin in con.execute("select id,title,status,assignee,tenant,completed_at from tasks where status!='archived'"):
            if (ten and menciona(ten)) or menciona(ti or ""):
                if st == "done" and (fin or 0) < desde:
                    continue
                n += 1; print(f"- [{st}] {ti} · {tid} · tablero {db.parent.name if db.parent.name != '.hermes' else 'default'}" + (f" · {asg}" if asg else ""))
    except Exception:
        pass
if not n:
    print("- (ninguna abierta ni terminada en el periodo)")
