#!/usr/bin/env python3
"""Faro «aviso de pulsos» (Estación Negocio): cuando un pulso semanal de cliente termina o se traba, se lo cuenta al
responsable por el canal de la estación, una sola vez por pulso. En silencio si no hay nada nuevo.
Uso: aviso_pulsos.py [prefijo del título, por defecto «Pulso semanal ·»]"""
import json, os, sqlite3, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_comun"))
from agora import tableros, filas, codigo

PREF = sys.argv[1] if len(sys.argv) > 1 else "Pulso semanal ·"
H = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
ESTADO = H / "cache" / "flota-pulsos-avisados.json"
vistos = set(json.loads(ESTADO.read_text())) if ESTADO.exists() else set()
desde = time.time() - 8 * 86400
salida = []
for slug, db in tableros().items():
    try:
        for t in filas(db, "select id,title,status,completed_at,created_at,result,last_failure_error from tasks where title like ? and created_at>=?", (PREF + "%", desde)):
            if t["status"] not in ("done", "blocked", "triage"):
                continue
            clave = f"{t['id']}:{t['status']}"
            if clave in vistos:
                continue
            run = filas(db, "select summary,metadata,outcome from task_runs where task_id=? order by id desc limit 1", (t["id"],))
            r = run[0] if run else {}
            meta = {}
            try: meta = json.loads(r.get("metadata") or "{}") or {}
            except Exception: pass
            nombre = t["title"].replace(PREF, "").strip()
            if t["status"] == "done":
                res = (r.get("summary") or t["result"] or "Terminó sin resumen.").strip()
                pal = meta.get("palancas") or []
                linea = f"📊 Pulso · {nombre}\n{res}"
                if pal and not any(p[:25] in res for p in pal):
                    linea += "\nPalancas: " + " · ".join(pal[:3])
                if meta.get("atlas"):
                    linea += f"\nEn Atlas: {Path(meta['atlas']).name}"
            else:
                linea = f"⚠️ El pulso de {nombre} se trabó [{codigo(slug, t['id'])}]: {(t['last_failure_error'] or r.get('summary') or 'sin detalle')[:300]}\nDile a ARG.OS «¿qué pasa con el {codigo(slug, t['id'])}?»."
            salida.append(linea); vistos.add(clave)
    except Exception as e:
        salida.append(f"⚠️ No pude leer el tablero {slug}: {e}")
if salida:
    print("\n\n".join(salida))
    ESTADO.parent.mkdir(parents=True, exist_ok=True)
    ESTADO.write_text(json.dumps(sorted(vistos)))
