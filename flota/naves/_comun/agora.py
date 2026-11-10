#!/usr/bin/env python3
"""Utilidades compartidas por los faros del Ágora (Kanban de Hermes). Solo lectura."""
import glob, os, sqlite3, time

def tableros():
    """{slug: ruta_db} de los tableros vivos de la máquina (incluye el por defecto; salta archivados y vacíos)."""
    import json
    base = os.path.expanduser("~/.hermes")
    cands = {"default": f"{base}/kanban.db"}
    for d in sorted(glob.glob(f"{base}/kanban/boards/*/kanban.db")):
        slug = d.split("/")[-2]
        bj = os.path.join(os.path.dirname(d), "board.json")
        try:
            if os.path.exists(bj) and json.load(open(bj)).get("archived"):
                continue
        except Exception:
            pass
        if not slug.startswith("_"):
            cands[slug] = d
    out = {}
    for slug, db in cands.items():
        if os.path.exists(db) and filas(db, "select 1 from sqlite_master where type='table' and name='tasks'"):
            out[slug] = db
    return out

def filas(db, sql, args=()):
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=10)
    c.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in c.execute(sql, args)]
    finally:
        c.close()

def hace(ts):
    if not ts:
        return "?"
    d = (time.time() - ts) / 86400
    return f"{int(d)} d" if d >= 1 else f"{int(d * 24)} h"
