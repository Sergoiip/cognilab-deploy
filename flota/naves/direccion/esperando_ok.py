#!/usr/bin/env python3
"""Faro «Esperando tu OK» (Eos · sector dirección): el centro de aprobaciones del Ágora.
Junta en un solo aviso lo que necesita al capitán: misiones que nacieron bloqueadas
(modo manual), vistos buenos listos para revisar y lo que se terminó desde el último aviso.
Si no hay nada, calla.

Uso: esperando_ok.py [--horas 24]"""
import argparse, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_comun"))
from agora import tableros, filas, hace, codigo

ap = argparse.ArgumentParser()
ap.add_argument("--horas", type=float, default=24)
a = ap.parse_args()
desde = time.time() - a.horas * 3600
soltar, vistos, revision, hechas = [], [], [], []
for slug, db in tableros().items():
    for t in filas(db, "select id,title,status,assignee,created_by,created_at,completed_at,result from tasks "
                       "where status in ('blocked','todo','ready','review','done')"):
        if t["status"] == "blocked" and t["assignee"] and t["created_by"] == "flota":
            soltar.append(f"  [{codigo(slug, t['id'])}] {t['title'][:70]} → {t['assignee']} (espera hace {hace(t['created_at'])})")
        elif t["title"].startswith("⛔") and not t["assignee"] and t["status"] in ("ready", "todo"):
            padres = filas(db, "select p.status s from task_links l join tasks p on p.id=l.parent_id where l.child_id=?", (t["id"],))
            if padres and all(p["s"] == "done" for p in padres):
                vistos.append(f"  [{codigo(slug, t['id'])}] {t['title'][2:].strip()[:72]}")
        elif t["status"] == "review":
            revision.append(f"  [{codigo(slug, t['id'])}] {t['title'][:70]} ({t['assignee'] or 'sin asignar'})")
        elif t["status"] == "done" and t["assignee"] and (t["completed_at"] or 0) > desde:
            res = (t["result"] or "").strip().replace("\n", " ")
            hechas.append(f"  • {t['title'][:60]} ({t['assignee']})" + (f"\n    {res[:150]}" if res else ""))
bloques = []
if soltar:
    bloques.append("🔓 Para soltar (nacieron bloqueadas, modo manual):\n" + "\n".join(soltar))
if vistos:
    bloques.append("⛔ Vistos buenos listos para que revises:\n" + "\n".join(vistos))
if revision:
    bloques.append("🔎 En revisión:\n" + "\n".join(revision))
if hechas:
    bloques.append(f"✅ Terminadas en las últimas {int(a.horas)} h:\n" + "\n".join(hechas))
if bloques:
    print("🌅 Ágora · esperando tu OK\n\n" + "\n\n".join(bloques) +
          ("\n\nRespóndele a ARG.OS con el número: «suelta 3», «aprueba 3» o «descarta 3»." if (soltar or vistos or revision) else ""))
