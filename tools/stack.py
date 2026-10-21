#!/usr/bin/env python3
"""Resuelve qué apps instalar para un manifiesto y instala los plugins de Obsidian.
  stack.py plan    MANIFIESTO --pm pacman|apt|dnf          -> acciones, una por línea
  stack.py plugins MANIFIESTO --vault RUTA [--dry-run]     -> plugins verificados por sha256
Solo requiere PyYAML."""
import sys, json, hashlib, shutil, argparse, pathlib, urllib.request, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAT = yaml.safe_load((ROOT/"stack/catalogo.yaml").read_text(encoding="utf-8"))


def resolver(man):
    mods = man.get("modulos", []) or []
    esc = max([m.get("escala", 1) for m in mods] or [1])
    h = man.get("herramientas", {}) or {}
    modo = h.get("modo", "asignar")          # asignar: el cliente no sabe qué usar -> se le da el perfil
    perfil = h.get("perfil", "auto")
    if perfil == "auto":
        perfil = {1: "ligero", 2: "negocio", 3: "equipo"}[min(esc, 3)]
    P = CAT["perfiles"]
    orden, p = [], perfil
    while p:
        orden.insert(0, p)
        p = P[p].get("hereda")
    apps = []

    def add(a):
        if a not in apps:
            apps.append(a)

    if modo == "asignar":
        for p in orden:
            for a in P[p]["apps"]:
                add(a)
    for m in mods:
        for a in CAT["por_modulo"].get(m["id"], []):
            add(a)
        for e, lst in CAT.get("por_modulo_desde_escala", {}).get(m["id"], {}).items():
            if m.get("escala", 1) >= int(e):
                for a in lst:
                    add(a)
    for a in h.get("extras", []) or []:
        add(a)
    excluir = set(h.get("excluir", []) or []) | set(h.get("ya_usa", []) or [])
    desconocidas = [a for a in apps if a not in CAT["apps"]]
    return perfil, esc, modo, [a for a in apps if a not in excluir], excluir, h.get("cuentas", []) or [], desconocidas


def cmd_plan(a):
    man = yaml.safe_load(open(a.manifiesto, encoding="utf-8"))
    perfil, esc, modo, apps, excl, cuentas, desc = resolver(man)
    if desc:
        sys.exit(f"app desconocida en el catálogo: {desc}")
    print(f"INFO|perfil={perfil} escala={esc} modo={modo}")
    pk, fp, pip, plug = [], [], [], []
    for x in apps:
        d = CAT["apps"][x]
        t = d["tipo"]
        if t == "hermes":
            print("HERMES|" + d["url"])
        elif t == "obsidian-plugin":
            plug.append(x)
        elif t == "pip":
            pip.append(d["paquete"])
        elif t == "sistema":
            if shutil.which(d["bin"]):
                print(f"SKIP|{x}|ya instalado")
                continue
            n = d["pm"].get(a.pm)
            if not n:
                print(f"MANUAL|{d['nombre']}: sin paquete para {a.pm}, instalar a mano")
                continue
            (fp if n.startswith("flatpak:") else pk).append(n.split(":", 1)[-1])
    if pk:
        print(f"PKG|{' '.join(pk)}")
    for f in fp:
        print(f"FLATPAK|{f}")
    if pip:
        print(f"PIP|{' '.join(pip)}")
    if plug:
        print(f"PLUGINS|{','.join(plug)}")
    for e in sorted(excl):
        print(f"SKIP|{e}|el cliente ya lo usa o se excluyó")
    for c in cuentas:
        print(f"MANUAL|Cuenta: {CAT['cuentas_manuales'].get(c, c)}")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cmd_plugins(a):
    man = yaml.safe_load(open(a.manifiesto, encoding="utf-8"))
    apps = resolver(man)[3]
    ids = [x for x in apps if CAT["apps"][x]["tipo"] == "obsidian-plugin"]
    vault = pathlib.Path(a.vault).expanduser()
    if not ids:
        print("sin plugins que instalar")
        return
    if not vault.is_dir():
        if a.dry_run:
            print(f"(la bóveda {vault} se crearía)")
        else:
            vault.mkdir(parents=True, exist_ok=True)
    cp = vault/".obsidian"/"community-plugins.json"
    activos = json.loads(cp.read_text()) if cp.exists() else []
    for x in ids:
        d = CAT["apps"][x]
        dest = vault/".obsidian"/"plugins"/x
        print(f"- {x} {d['version']} ({d['licencia']})")
        if a.dry_run:
            continue
        buf = {}
        for f, esperado in d["sha256"].items():
            u = f"https://github.com/{d['repo']}/releases/download/{d['version']}/{f}"
            b = urllib.request.urlopen(u, timeout=60).read()
            if sha(b) != esperado:
                sys.exit(f"HASH DISTINTO en {x}/{f}: no se instala (esperado {esperado[:12]}, llegó {sha(b)[:12]})")
            buf[f] = b
        dest.mkdir(parents=True, exist_ok=True)
        for f, b in buf.items():
            (dest/f).write_bytes(b)
        tpl = CAT["plantillas"].get(x)
        if tpl and not (dest/"data.json").exists():
            shutil.copy(ROOT/tpl, dest/"data.json")
            print(f"  plantilla de {x} copiada (data.json)")
        if x not in activos:
            activos.append(x)
    if not a.dry_run:
        if cp.exists():
            shutil.copy(cp, str(cp) + ".bak-cognilab")
        cp.parent.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(activos, indent=2))
        print("community-plugins.json actualizado. En Obsidian: Ajustes > Complementos de la comunidad > desactivar modo restringido (una vez).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="c", required=True)
    p = sp.add_parser("plan"); p.add_argument("manifiesto"); p.add_argument("--pm", default="pacman"); p.set_defaults(f=cmd_plan)
    q = sp.add_parser("plugins"); q.add_argument("manifiesto"); q.add_argument("--vault", required=True)
    q.add_argument("--dry-run", action="store_true"); q.set_defaults(f=cmd_plugins)
    a = ap.parse_args()
    a.f(a)
