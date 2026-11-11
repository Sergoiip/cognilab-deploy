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


# ---- Códigos cortos para responder desde el teléfono («aprueba 7» en vez de «aprueba t_9951119d») ----
# Registro persistente: ~/.hermes/state/agora_codigos.json  {"7": {"tablero": slug, "id": "t_…", "asignado": ts}}
# Un número se recicla solo cuando su tarea ya está terminada o archivada y lleva 3 días sin mostrarse.
# Para traducir una respuesta: python3 flota/naves/_comun/agora.py 7  → imprime «tablero id».
_REG = os.path.expanduser("~/.hermes/state/agora_codigos.json")

def _cargar():
    import json
    try:
        return json.load(open(_REG))
    except Exception:
        return {}

def _guardar(reg):
    import json
    os.makedirs(os.path.dirname(_REG), exist_ok=True)
    tmp = _REG + ".tmp"
    json.dump(reg, open(tmp, "w"), ensure_ascii=False, indent=1)
    os.replace(tmp, _REG)

def _libre(reg, n):
    e = reg.get(str(n))
    if not e:
        return True
    if time.time() - e.get("asignado", 0) < 3 * 86400:
        return False
    db = tableros().get(e.get("tablero"))
    st = filas(db, "select status from tasks where id=?", (e["id"],)) if db else []
    return not st or st[0]["status"] in ("done", "archived")

def codigo(slug, tid):
    """Número corto y estable para la tarea (slug, tid)."""
    reg = _cargar()
    for k, e in reg.items():
        if e.get("id") == tid and e.get("tablero") == slug:
            e["asignado"] = time.time(); _guardar(reg); return k
    n = 1
    while not _libre(reg, n):
        n += 1
    reg[str(n)] = {"tablero": slug, "id": tid, "asignado": time.time()}
    _guardar(reg)
    return str(n)

def codigo_de_id(tid):
    """Igual que codigo(), buscando en qué tablero vive la tarea."""
    for slug, db in tableros().items():
        if filas(db, "select 1 from tasks where id=?", (tid,)):
            return codigo(slug, tid)
    return tid

def con_codigos(texto):
    """Reemplaza cada t_xxxxxxxx de un texto por su código corto entre corchetes."""
    import re
    return re.sub(r"\bt_[0-9a-f]{8}\b", lambda m: f"[{codigo_de_id(m.group(0))}]", texto)

if __name__ == "__main__":
    import sys
    reg = _cargar()
    for k in sys.argv[1:]:
        e = reg.get(k.strip("[]#"))
        print(f"{e['tablero']} {e['id']}" if e else f"? {k}")
