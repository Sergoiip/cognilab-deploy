#!/usr/bin/env python3
"""Vista de una Flota: cobertura por sector, con las dos lentes (PKM y APQC).

Uso:  python3 tools/flota.py estado manifiestos/cliente-X.yaml [--jobs ~/.hermes/cron/jobs.json]

Cruza el manifiesto con el estado real de los crons de Hermes en la máquina
(activo / pausado / no existe) y marca los sectores sin cobertura activa."""
import sys, json, pathlib, argparse, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
FLOTA = ROOT / "flota"


def cargar_catalogo():
    sect = yaml.safe_load((FLOTA / "sectores.yaml").read_text(encoding="utf-8"))["sectores"]
    naves = {}
    for f in FLOTA.glob("naves/*/*.yaml"):
        n = yaml.safe_load(f.read_text(encoding="utf-8"))
        naves[n["id"]] = n
    return sect, naves


def estado(args):
    sect, naves = cargar_catalogo()
    man = yaml.safe_load(pathlib.Path(args.manifiesto).read_text(encoding="utf-8"))
    plano = yaml.safe_load((FLOTA / "planos" / f"{man['plano']}.yaml").read_text(encoding="utf-8"))
    jobs = {}
    jp = pathlib.Path(args.jobs).expanduser()
    if jp.exists():
        d = json.loads(jp.read_text(encoding="utf-8"))
        for j in (d["jobs"] if isinstance(d, dict) else d):
            jobs[j["id"]] = j
    problemas = []
    por_sector = {k: [] for k in sect}
    for cid, f in (man.get("faros") or {}).items():
        s = f["sector"]
        if s not in sect:
            problemas.append(f"faro {cid}: sector '{s}' no existe")
            continue
        j = jobs.get(cid)
        st = "no existe" if j is None else ("activo" if j.get("enabled", True) and j.get("state") != "paused" else "pausado")
        if j is not None and j.get("last_status") == "error":
            st += " · último run con error"
        if f.get("nave") and f["nave"] not in naves:
            problemas.append(f"faro {cid}: nave '{f['nave']}' no está en el catálogo")
        por_sector[s].append((st, f["nombre"]))
    for n in man.get("naves_pendientes") or []:
        if n not in naves:
            problemas.append(f"nave pendiente '{n}' no está en el catálogo")
        else:
            por_sector[naves[n]["sector"]].append(("pendiente", naves[n]["nombre_visible"]))

    print(f"Flota «{man['cliente']}» · plano {plano['id']} ({plano['estado']}) · lentes: {' + '.join(plano['lentes'])}")
    print(f"Estaciones: " + ", ".join(f"{e['nombre_visible']} ({e['tipo']}, perfil {e['perfil_hermes']})" for e in man["estaciones"]))
    huecos = []
    for k, s in sect.items():
        lente = []
        if "pkm" in plano["lentes"] and s.get("pkm"):
            lente.append(f"PKM: {s['pkm']}")
        if "apqc" in plano["lentes"] and s.get("apqc"):
            lente.append("APQC " + ", ".join(x.split()[0] for x in s["apqc"]))
        if not lente:
            continue                       # sector fuera de las lentes del plano
        items = por_sector[k]
        activos = [i for i in items if i[0].startswith("activo")]
        marca = "✅" if activos else ("🟡" if items else "⬜")
        if not activos and k in plano.get("cobertura_minima", []):
            huecos.append(s["nombre"])
        print(f"\n{marca} {s['nombre']}  [{' · '.join(lente)}]" + ("  (transversal)" if s["tipo"] == "transversal" else ""))
        for st, nombre in items:
            print(f"    - {nombre} — {st}")
        if not items:
            print("    (nada lo vigila)")
    print("\nSin cobertura activa: " + (", ".join(huecos) if huecos else "ninguno"))
    for p in problemas:
        print("PROBLEMA", p)
    return 1 if problemas else 0


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
e = sub.add_parser("estado")
e.add_argument("manifiesto")
e.add_argument("--jobs", default="~/.hermes/cron/jobs.json")
a = ap.parse_args()
sys.exit(estado(a))
