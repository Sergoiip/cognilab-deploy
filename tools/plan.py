#!/usr/bin/env python3
"""De la Radiografía al manifiesto.
  plan.py radiografia.yaml [--inventario inventario.yaml] [--salida manifiestos/cliente-X.yaml]
Propone módulos, escala por módulo y modo de herramientas, y EXPLICA cada decisión.
Es una propuesta: Sergio revisa y ajusta antes de aprobar. Solo requiere PyYAML."""
import sys, argparse, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
OBLIGATORIOS = ["A1", "E1", "E2", "E3"]


def cargar(p):
    return yaml.safe_load(pathlib.Path(p).read_text(encoding="utf-8")) or {}


def escala_de(uso):
    """Regla de escalas.md (umbrales en BORRADOR): personas y costo de falla."""
    p = int(uso.get("personas", 1)); c = uso.get("costo_falla", "bajo")
    if p >= 6 or (p >= 3 and c == "alto"): return 3
    if p >= 2 or c in ("medio", "alto"): return 2
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ficha"); ap.add_argument("--inventario"); ap.add_argument("--salida")
    a = ap.parse_args()
    f = cargar(a.ficha); inv = cargar(a.inventario) if a.inventario else {}
    mapa = cargar(ROOT / "criterios/dolor-a-modulo.yaml")
    paquete = f.get("paquete_objetivo", "integral")
    pk = cargar(ROOT / f"paquetes/{'esencial' if paquete in ('esencial','piloto') else 'integral'}.yaml")
    avisos, razones, score = [], [], {}

    for d in f.get("dolores", []):
        ev = [e for e in d.get("evidencias", []) if str(e).strip()]
        if len(ev) < 3:
            avisos.append(f"Dolor {d.get('id')} ({d.get('categoria')}): {len(ev)} evidencias, se piden 3. NO entra al plan."); continue
        mods = mapa.get(d.get("categoria"))
        if not mods:
            avisos.append(f"Dolor {d.get('id')}: categoría «{d.get('categoria')}» no está en criterios/dolor-a-modulo.yaml. Decidir a mano."); continue
        for i, m in enumerate(mods):
            w = int(d.get("prioridad", 1)) * (2 if i == 0 else 1)
            score[m] = score.get(m, 0) + w
            razones.append(f"{m} ← dolor {d['id']} «{d.get('descripcion','')}» (prio {d.get('prioridad',1)}, {'principal' if i==0 else 'alterno'})")

    ranking = sorted((m for m in score if m not in OBLIGATORIOS), key=lambda m: -score[m])
    if paquete == "piloto":
        elegidos = ranking[:1]; nota = "Piloto: un solo entregable (el de mayor puntaje)."
    elif paquete == "esencial":
        ligeros = set(pk.get("ligero", {}).get("entre_PROPUESTA", []))
        princ = ranking[:1]
        lig = next((m for m in ranking[1:] if m in ligeros), None)
        elegidos = princ + ([lig] if lig else [])
        nota = "Esencial: 1 principal + 1 ligero (la lista de ligeros es PROPUESTA, la define Sergio)."
        if not lig: avisos.append("Esencial: ningún dolor lleva a un módulo ligero; elegir el segundo a mano.")
    else:
        elegidos = ranking; nota = "Integral: a medida; el tope es el tiempo (90 días), no el número de módulos."

    modulos = [{"id": m, "escala": 2} for m in OBLIGATORIOS[:1]]
    uso = f.get("uso_modulos", {}) or {}
    for m in OBLIGATORIOS[:1] + elegidos + OBLIGATORIOS[1:]:
        if m not in uso and m not in OBLIGATORIOS:
            avisos.append(f"{m}: falta uso_modulos (personas y costo de falla). Escala provisional 2.")
    modulos = []
    for m in dict.fromkeys(OBLIGATORIOS[:1] + elegidos + OBLIGATORIOS[1:]):
        modulos.append({"id": m, "escala": escala_de(uso[m]) if m in uso else 2})

    h = f.get("herramientas_actuales", {}) or {}
    modo = h.get("modo", "asignar")
    man_h = {"modo": modo, "perfil": "auto", "ya_usa": h.get("ya_usa", []), "extras": [], "excluir": [],
             "cuentas": f.get("cuentas_que_crea_el_cliente", [])}
    if h.get("otras"):
        avisos.append(f"Usa herramientas fuera del catálogo ({', '.join(map(str,h['otras']))}): no se instala nada para esa función; decidir si se migra o se integra.")

    if inv:
        if not inv.get("soportado_por_instalador", True):
            avisos.append(f"SO «{inv.get('so')}»: el instalador cubre pacman, apt y dnf. Todo es manual; no prometer instalación automática.")
        if inv.get("admin") is False:
            avisos.append("Sin permisos de administrador: las apps del sistema piden sudo; usar --sin-apps o pedir acceso.")
        if inv.get("ram_gb") and inv["ram_gb"] < 8:
            avisos.append(f"RAM {inv['ram_gb']} GB: IA local no recomendada; considerar nube y decidirlo con el cliente.")
        ya = [k for k, v in (inv.get("herramientas") or {}).items() if v]
        if ya and modo == "asignar":
            avisos.append("Ya hay en el equipo: " + ", ".join(ya) + ". Confirmar si pasan a `ya_usa`.")

    man = {"cliente": f.get("cliente", "[cliente]"), "paquete": "esencial" if paquete == "piloto" else paquete,
           "vault": f.get("vault", "~/Documents/Obsidian/Bóveda-cliente"), "modulos": modulos, "herramientas": man_h}
    salida = yaml.safe_dump(man, allow_unicode=True, sort_keys=False, default_flow_style=None)
    if a.salida:
        pathlib.Path(a.salida).write_text("# BORRADOR generado por tools/plan.py — revisar antes de aprobar\n" + salida, encoding="utf-8")
        print(f"manifiesto → {a.salida}")
    else:
        print(salida)
    print("— Por qué —", nota, *razones, sep="\n  ")
    if score: print("— Puntaje —", ", ".join(f"{m}={score[m]}" for m in sorted(score, key=lambda x: -score[x])))
    if avisos: print("— Avisos —", *avisos, sep="\n  ! ")


if __name__ == "__main__":
    main()
