#!/usr/bin/env python3
"""Verifica el repo y su sincronía con el entregable en Cadence.
Uso:  python3 tools/verificar.py            revisa
      python3 tools/verificar.py --sellar   registra que el repo quedó alineado con el entregable actual
Sale con código 1 si hay errores. Las advertencias no bloquean."""
import sys, re, json, hashlib, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAD = pathlib.Path("/home/sergoip/Documents/Obsidian/Bóveda de Operaciones/Cadence/Services/Paquete Del caos al sistema en 90 días.md")
SELLO = ROOT / "SYNC.json"
err, warn, sin_var = [], [], []

mods = []
for f in sorted(ROOT.glob("modulos/*/*/modulo.yaml")):
    m = yaml.safe_load(f.read_text(encoding="utf-8"))
    d = f.parent
    mods.append(m)
    for k in ("id", "nombre", "slug", "bloque", "hecho", "estado", "escalas", "cadence_ref"):
        if k not in m:
            err.append(f"{m.get('id', d.name)}: falta '{k}' en modulo.yaml")
    sk = d / "SKILL.md"
    if not sk.exists():
        err.append(f"{m['id']}: falta SKILL.md"); continue
    nm = re.search(r"^name:\s*(\S+)", sk.read_text(encoding="utf-8"), re.M)
    if not nm or nm.group(1) != d.name or m["slug"] != d.name:
        err.append(f"{m['id']}: carpeta, slug y name deben coincidir ({d.name})")
    for e in m.get("escalas", []):
        if not (d / "variantes" / f"{e}.md").exists():
            err.append(f"{m['id']}: falta variantes/{e}.md")
    if len(m.get("hecho", [])) < 2:
        err.append(f"{m['id']}: criterio de hecho con menos de 2 puntos")
    if "POR DESARROLLAR" in (d / "variantes" / "1-individuo.md").read_text(encoding="utf-8"):
        sin_var.append(m["id"])
    if m["estado"] == "esqueleto-sin-fuente":
        warn.append(f"{m['id']}: sin meta-skill de origen")

if sin_var:
    warn.append(f"{len(sin_var)} de {len(mods)} módulos con variantes sin desarrollar: {', '.join(sorted(sin_var))}")
ids = [m["id"] for m in mods]
if len(ids) != len(set(ids)):
    err.append("ids duplicados")

# Reglas de contenido: sin precios, sin datos de clientes, sin rastros de otros clientes
PROHIBIDO = [(r"\$\s?\d[\d.,]*", "precio"), (r"\bCOP\b", "moneda"),
             (r"(?i)\bdosis\b|\bocean\b|\bshaco\b|dosiscreativa", "rastro de otro cliente"),
             (r"(?i)Sebasti[aá]n Rada|Felipe Quintero|Alejandro L[oó]pez|Laura Valencia|Susana L[oó]pez|Yuliana",
              "nombre de cliente"),
             (r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "IP")]
for p in ROOT.rglob("*"):
    if p.is_file() and p.suffix in (".md", ".yaml", ".sh", ".py", ".js", ".css", ".json") and ".git" not in p.parts and p.name != "verificar.py":
        t = p.read_text(encoding="utf-8", errors="ignore")
        for rx, what in PROHIBIDO:
            if what in ("precio", "moneda") and p.suffix in (".sh", ".py", ".js", ".css", ".json"):
                continue
            if what == "IP" and p.suffix in (".js", ".css", ".json"):
                continue
            if re.search(rx, t):
                err.append(f"{p.relative_to(ROOT)}: contiene {what}")


# Stack: el catálogo debe ser coherente con los módulos y con los perfiles
CATF = ROOT / "stack" / "catalogo.yaml"
if CATF.exists():
    cat = yaml.safe_load(CATF.read_text(encoding="utf-8"))
    apps = cat["apps"]
    ids_mod = {m["id"] for m in mods}
    refs = set()
    for pf in cat["perfiles"].values():
        refs |= set(pf["apps"])
    for mid, lst in cat["por_modulo"].items():
        refs |= set(lst)
        if mid not in ids_mod:
            err.append(f"stack: por_modulo usa el módulo {mid}, que no existe")
    for mid, d in cat.get("por_modulo_desde_escala", {}).items():
        for lst in d.values():
            refs |= set(lst)
    for r in sorted(refs - set(apps)):
        err.append(f"stack: '{r}' está referenciada pero no existe en apps")
    for k, a in apps.items():
        if a["tipo"] == "obsidian-plugin":
            if set(a.get("sha256", {})) != {"main.js", "manifest.json", "styles.css"}:
                err.append(f"stack: {k} sin sha256 completo")
            if a.get("fuente") == "vendor":
                for f, esperado in a["sha256"].items():
                    fp = ROOT / a["ruta"] / f
                    if not fp.exists() or hashlib.sha256(fp.read_bytes()).hexdigest() != esperado:
                        err.append(f"stack: {k}/{f} no coincide con su sha256 del catálogo")
                if not (ROOT / a["ruta"] / "LICENSE").exists():
                    err.append(f"stack: {k} vendorizado sin LICENSE")
            if not a.get("licencia"):
                err.append(f"stack: {k} sin licencia declarada")
        if a["tipo"] == "sistema" and not {"pacman", "apt"} <= set(a["pm"]):
            warn.append(f"stack: {k} sin paquete para apt/pacman")
        if not a.get("opcional"):
            warn.append(f"stack: {k} no está marcada opcional")
    for x in cat["plantillas"].values():
        t = (ROOT / x).read_text(encoding="utf-8")
        if re.search(r'"cadenceApiToken":\s*"[^"]+"', t):
            err.append(f"{x}: trae un token")
    warn.append("stack: nombres de paquete verificados solo en pacman; apt y dnf sin probar en equipo real")
else:
    err.append("falta stack/catalogo.yaml")

# Sincronía con Cadence
if CAD.exists():
    txt = CAD.read_text(encoding="utf-8")
    h = hashlib.sha256(txt.encode()).hexdigest()
    cad_ms = set(re.findall(r"\((MS-\d+)\)", txt))
    repo_ms = {m["ms"] for m in mods if m.get("ms")}
    for x in sorted(cad_ms - repo_ms):
        err.append(f"Cadence menciona {x} y ningún módulo la implementa")
    for x in sorted(repo_ms - cad_ms):
        warn.append(f"El repo usa {x} pero el menú de Cadence no la menciona")
    n_menu = len(re.findall(r"^- \*\*", txt.split("## Menú de entregables")[1].split("## Dos paquetes")[0], re.M))
    if n_menu != len(mods):
        warn.append(f"Cadence lista {n_menu} entregables y el repo tiene {len(mods)} módulos: revisar")
    if "--sellar" in sys.argv:
        SELLO.write_text(json.dumps({"cadence_sha256": h, "modulos": len(mods)}, indent=2), encoding="utf-8")
        print("sellado:", h[:12])
    elif SELLO.exists():
        if json.loads(SELLO.read_text())["cadence_sha256"] != h:
            warn.append("El entregable de Cadence cambió desde el último sello: revisar y volver a sellar")
    else:
        warn.append("Repo sin sellar contra Cadence")
else:
    warn.append("No encuentro la nota de Cadence; sincronía no verificada")

print(f"{len(mods)} módulos · {len(err)} errores · {len(warn)} advertencias")
for e in err: print("ERROR ", e)
for w in warn: print("aviso ", w)
sys.exit(1 if err else 0)
