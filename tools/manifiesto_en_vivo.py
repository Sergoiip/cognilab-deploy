#!/usr/bin/env python3
"""Manifiesto en vivo: el Hermes del cliente arma el manifiesto DURANTE la instalación.

Desde 0.28.0 el manifiesto ya no se llena antes (encuesta). Se instala la base
(`bootstrap/instala.sh --base`), y el propio Hermes del cliente le hace las preguntas con sus
ventanas de respuesta (herramienta clarify). Este script le da al agente los datos REALES del
repo y escribe el YAML, para que nadie copie listas a mano ni escriba YAML a ojo.

Uso:
    manifiesto_en_vivo.py opciones                 # JSON: paquetes y módulos tal como están en el repo
    manifiesto_en_vivo.py guardar respuestas.json [--salida manifiestos/cliente-x.yaml]
                                                   # valida y escribe el manifiesto

respuestas.json (lo arma el agente con lo que contestó el cliente):
{
  "cliente": "nombre corto", "paquete": "esencial" | "ecosistema",
  "escala": 1 | 2 | 3, "modulos": ["B1", ...],          # principal(es), sin los obligatorios
  "vault": "~/Documents/Obsidian/Mi-boveda",
  "acompanamiento": "tecnico" | "integral",
  "agente": {"nombre": "...", "personalidad": "..."},   # opcional
  "herramientas": {"modo": "asignar" | "cliente", "ya_usa": [], "cuentas": ["telegram"]},
  "ritmo": {...}                                        # opcional, ver bootstrap/ORGANIZACION-TEMPORAL.md
}
"""
import json
import pathlib
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
ALIAS = {"integral": "ecosistema"}   # nombre anterior del paquete


def modulos():
    out = {}
    for f in sorted(REPO.glob("modulos/*/*/modulo.yaml")):
        m = yaml.safe_load(f.read_text(encoding="utf-8"))
        out[m["id"]] = {"nombre": m.get("nombre", ""), "escalas": m.get("escalas", []),
                        "hecho": (m.get("hecho") or [])[:2]}
    return out


def paquetes():
    out = {}
    for f in sorted((REPO / "paquetes").glob("*.yaml")):
        p = yaml.safe_load(f.read_text(encoding="utf-8"))
        out[f.stem] = {k: p.get(k) for k in ("paquete", "duracion_meses", "duracion_max_meses", "frentes",
                                              "entregables", "empieza_con", "obligatorios", "incluye", "no_incluye")}
        out[f.stem]["elegir"] = (p.get("principal") or {}).get("elegir")   # None = a medida
        out[f.stem]["entre"] = (p.get("principal") or p.get("a_medida") or {}).get("entre", [])
    return out


def guardar(resp_path, salida=None):
    r = json.loads(pathlib.Path(resp_path).read_text(encoding="utf-8"))
    mods, pqs = modulos(), paquetes()
    errores = []
    paquete = ALIAS.get(str(r.get("paquete", "")).lower(), str(r.get("paquete", "")).lower())
    if paquete not in pqs:
        errores.append(f"paquete desconocido: {r.get('paquete')} (hay: {', '.join(pqs)})")
    escala = int(r.get("escala", 1))
    if escala not in (1, 2, 3):
        errores.append("escala debe ser 1, 2 o 3")
    elegidos = [m for m in r.get("modulos", []) if m]
    for m in elegidos:
        if m not in mods:
            errores.append(f"módulo desconocido: {m}")
    if paquete in pqs:
        pq = pqs[paquete]
        fuera = [m for m in elegidos if m not in pq["entre"] and m not in (pq["obligatorios"] or [])]
        if fuera:
            errores.append(f"{pq['paquete']} no ofrece: {', '.join(fuera)}")
        principales = [m for m in elegidos if m not in (pq["obligatorios"] or [])]
        if pq["elegir"] and len(principales) != pq["elegir"]:
            errores.append(f"{pq['paquete']} lleva exactamente {pq['elegir']} frente(s); llegaron {len(principales)}")
    if not r.get("vault"):
        errores.append("falta vault (ruta de la bóveda)")
    if r.get("acompanamiento", "tecnico") not in ("tecnico", "integral"):
        errores.append("acompanamiento debe ser tecnico o integral")
    if errores:
        print("NO SE GUARDÓ. Corregir con el cliente:", *[f"  - {e}" for e in errores], sep="\n", file=sys.stderr)
        return 1

    ids = list(dict.fromkeys((pqs[paquete]["obligatorios"] or []) + elegidos))
    h = r.get("herramientas") or {}
    man = {
        "cliente": r.get("cliente") or "[cliente]",
        "paquete": paquete,
        "acompanamiento": r.get("acompanamiento", "tecnico"),
        "vault": r["vault"],
        "origen_manifiesto": "en-vivo",   # armado por el Hermes del cliente durante la instalación
        "modulos": [{"id": m, "escala": escala} for m in ids],
        "herramientas": {"modo": h.get("modo", "asignar"), "perfil": "auto", "ya_usa": h.get("ya_usa", []),
                         "extras": [], "excluir": [], "cuentas": h.get("cuentas") or ["telegram"]},
    }
    ag = {k: v for k, v in (r.get("agente") or {}).items() if k in ("nombre", "personalidad") and v}
    if ag:
        man["agente"] = ag
    if r.get("ritmo"):
        man["ritmo"] = r["ritmo"]
    slug = "".join(c if c.isalnum() else "-" for c in man["cliente"].lower()).strip("-") or "cliente"
    destino = pathlib.Path(salida) if salida else REPO / "manifiestos" / f"cliente-{slug}.yaml"
    if not destino.is_absolute():
        destino = REPO / destino
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(yaml.safe_dump(man, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(destino)
    return 0


def main():
    a = sys.argv[1:]
    if a[:1] == ["opciones"]:
        print(json.dumps({"paquetes": paquetes(), "modulos": modulos()}, ensure_ascii=False, indent=1))
        return 0
    if a[:1] == ["guardar"] and len(a) >= 2:
        sal = a[a.index("--salida") + 1] if "--salida" in a else None
        return guardar(a[1], sal)
    print(__doc__, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
