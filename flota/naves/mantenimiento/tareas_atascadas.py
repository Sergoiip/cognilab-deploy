#!/usr/bin/env python3
"""Faro «Tareas atascadas» (Sísifo · sector mantenimiento).
Avisa las misiones que se atascan: bloqueadas hace días, que se bloquean una y otra vez,
que fallaron seguidas o que llevan demasiado tiempo corriendo. Si no hay nada, calla.

Uso: tareas_atascadas.py [--dias 3] [--horas-corriendo 6]"""
import argparse, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_comun"))
from agora import tableros, filas, hace, codigo

ap = argparse.ArgumentParser()
ap.add_argument("--dias", type=float, default=3)
ap.add_argument("--horas-corriendo", type=float, default=6)
a = ap.parse_args()
ahora = time.time()
avisos = []
for slug, db in tableros().items():
    for t in filas(db, "select id,title,status,assignee,created_at,started_at,consecutive_failures,"
                       "block_recurrences,last_failure_error from tasks where status in ('blocked','running','ready','triage')"):
        razones = []
        ev = filas(db, "select max(created_at) m from task_events where task_id=? and kind='blocked'", (t["id"],))
        desde = ev[0]["m"] if ev and ev[0]["m"] else t["created_at"]
        if t["status"] == "blocked" and t["assignee"] and desde and ahora - desde > a.dias * 86400:
            razones.append(f"bloqueada hace {hace(desde)}")
        if (t["block_recurrences"] or 0) >= 2:
            razones.append(f"se ha bloqueado {t['block_recurrences']} veces")
        if (t["consecutive_failures"] or 0) >= 2:
            razones.append(f"{t['consecutive_failures']} fallos seguidos")
        if t["status"] == "running" and t["started_at"] and ahora - t["started_at"] > a.horas_corriendo * 3600:
            razones.append(f"corriendo hace {hace(t['started_at'])}")
        if t["status"] == "triage":
            razones.append("en triage (el despachador no supo qué hacer con ella)")
        if razones:
            err = f"\n    Último error: {t['last_failure_error'][:140]}" if t["last_failure_error"] else ""
            avisos.append(f"[{codigo(slug, t['id'])}] {t['title'][:70]}\n    {', '.join(razones)} · {t['assignee'] or 'sin asignar'}{err}")
if avisos:
    print("🪨 Tareas atascadas\n" + "\n".join(avisos) +
          "\n\nDile a ARG.OS «suelta 3», «re-especifica 3» o «archiva 3» (con el número).")
