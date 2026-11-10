#!/usr/bin/env python3
"""Faro «Respaldo de la Flota» (Fénix · sector mantenimiento).
Copia cada noche lo que hace falta para reconstruir la Flota si algo se daña: configuración,
instrucciones (SOUL), memoria, faros y credenciales de cada perfil, y los tableros del Kanban
(copia consistente con la API de respaldo de SQLite). No copia el historial de conversaciones
(state.db) por su tamaño. Guarda los últimos N días en ~/.hermes/backups/fenix/ con permisos 600.
Solo habla si algo falla.

Uso: respaldo_flota.py [--dias 7]"""
import argparse, datetime, glob, os, sqlite3, sys, tarfile, tempfile, shutil

ap = argparse.ArgumentParser()
ap.add_argument("--dias", type=int, default=7)
a = ap.parse_args()
H = os.path.expanduser("~/.hermes")
DEST = os.path.join(H, "backups", "fenix")
os.makedirs(DEST, mode=0o700, exist_ok=True)
os.chmod(os.path.join(H, "backups"), 0o700); os.chmod(DEST, 0o700)
hoy = datetime.date.today().isoformat()
salida = os.path.join(DEST, f"flota-{hoy}.tgz")
errores = []
PIEZAS = ["config.yaml", "SOUL.md", ".env", "auth.json", "memories", "cron/jobs.json", "scripts", "profile.yaml"]
with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
    homes = {"default": H} | {os.path.basename(p): p for p in glob.glob(f"{H}/profiles/*") if os.path.isdir(p)}
    for nombre, home in homes.items():
        for pieza in PIEZAS:
            src = os.path.join(home, pieza)
            dst = os.path.join(tmp, "perfiles", nombre, pieza)
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.lock"))
                elif os.path.isfile(src):
                    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
            except Exception as e:
                errores.append(f"{nombre}/{pieza}: {e}")
    dbs = {"default": f"{H}/kanban.db"} | {p.split("/")[-2]: p for p in glob.glob(f"{H}/kanban/boards/*/kanban.db")}
    for slug, db in dbs.items():
        if not os.path.exists(db):
            continue
        dst = os.path.join(tmp, "kanban", slug, "kanban.db"); os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            s = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=30); d = sqlite3.connect(dst)
            s.backup(d); d.close(); s.close()
            bj = os.path.join(os.path.dirname(db), "board.json")
            if os.path.exists(bj):
                shutil.copy2(bj, os.path.dirname(dst))
        except Exception as e:
            errores.append(f"kanban {slug}: {e}")
    try:
        with tarfile.open(salida + ".tmp", "w:gz") as tf:
            tf.add(tmp, arcname=f"flota-{hoy}")
        os.replace(salida + ".tmp", salida); os.chmod(salida, 0o600)
    except Exception as e:
        errores.append(f"empaquetar: {e}")
viejos = sorted(glob.glob(os.path.join(DEST, "flota-*.tgz")))[:-a.dias]
for v in viejos:
    os.remove(v)
if errores:
    print("🔥 Fénix: el respaldo de la Flota tuvo problemas\n" + "\n".join("• " + e for e in errores[:10]))
