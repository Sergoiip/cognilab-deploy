#!/usr/bin/env python3
"""Cuestionario interactivo para armar el manifiesto de un cliente.

Pensado para correr EN VIVO junto al cliente (fase 1, ficha de ingreso), o a mano por Sergio
después de leer las respuestas de la encuesta web (`bootstrap/encuesta.html`).

Lee los módulos y paquetes reales del repo (nunca una lista hardcodeada aparte), así que
siempre refleja lo que de verdad existe hoy.

Uso:
    tools/encuesta_manifiesto.py [--salida manifiestos/cliente-X.yaml]
"""
import argparse
import pathlib
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent


def cargar_modulos():
    mods = {}
    for f in sorted(REPO.glob("modulos/*/*/modulo.yaml")):
        m = yaml.safe_load(f.read_text(encoding="utf-8"))
        mods[m["id"]] = m
    return mods


def cargar_paquetes():
    paq = {}
    for f in sorted((REPO / "paquetes").glob("*.yaml")):
        p = yaml.safe_load(f.read_text(encoding="utf-8"))
        paq[f.stem] = p
    return paq


def preguntar(texto, por_defecto=None, opciones=None):
    sufijo = f" [{por_defecto}]" if por_defecto else ""
    if opciones:
        print(f"  Opciones: {', '.join(opciones)}")
    while True:
        r = input(f"{texto}{sufijo}: ").strip()
        if not r and por_defecto is not None:
            r = por_defecto
        if not opciones or r in opciones:
            return r
        print(f"  (responde una de: {', '.join(opciones)})")


def preguntar_si_no(texto, por_defecto=True):
    d = "s" if por_defecto else "n"
    r = input(f"{texto} (s/n) [{d}]: ").strip().lower()
    if not r:
        r = d
    return r == "s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida")
    a = ap.parse_args()

    mods = cargar_modulos()
    paquetes = cargar_paquetes()

    print("== Encuesta de ingreso — manifiesto del cliente ==\n")

    cliente = preguntar("Nombre del cliente (para el archivo, sin datos sensibles)", "[cliente]")

    paquete = preguntar("Paquete", "esencial", list(paquetes.keys()))
    pq = paquetes[paquete]

    escala = preguntar("Escala (1 individuo / 2 negocio / 3 equipo)", "1", ["1", "2", "3"])

    print(f"\nMódulos obligatorios del paquete {pq['paquete']}: {', '.join(pq.get('obligatorios', []))}")
    elegir_n = pq.get("principal", {}).get("elegir", 0)
    entre = pq.get("principal", {}).get("entre", [])
    elegidos = []
    if elegir_n and entre:
        print(f"\nElige {elegir_n} módulo(s) principal(es) entre:")
        for mid in entre:
            nombre = mods.get(mid, {}).get("nombre", "?")
            print(f"  {mid}: {nombre}")
        while len(elegidos) < elegir_n:
            r = preguntar(f"  Módulo {len(elegidos) + 1}/{elegir_n} (id)", opciones=entre)
            if r not in elegidos:
                elegidos.append(r)

    ids_modulos = list(dict.fromkeys(pq.get("obligatorios", []) + elegidos))
    modulos_manifiesto = [{"id": mid, "escala": int(escala)} for mid in ids_modulos]

    vault = preguntar("Ruta de la bóveda en el equipo del cliente", "~/Documents/Obsidian/Bóveda-cliente")

    acompanamiento = preguntar(
        "Nivel de acompañamiento: 'tecnico' (quiere dominar su agente) o 'integral' (resultados sin tecnicismo)",
        "tecnico", ["tecnico", "integral"],
    )

    print("\n-- Nombre y personalidad del agente (opcional; Enter para omitir) --")
    nombre_agente = input("  Nombre con el que se dirigirá a su agente: ").strip()
    personalidad = input("  Personalidad (texto libre corto, ej. 'cálido, directo, sin jerga'): ").strip()

    print("\n-- Herramientas --")
    ya_sabe = preguntar_si_no("¿El cliente ya sabe qué apps usar (modo 'cliente')? Si no, se le asigna un perfil ('asignar')", False)
    modo = "cliente" if ya_sabe else "asignar"
    ya_usa_raw = input("  Apps que ya usa (ids del catálogo, separadas por coma, Enter si ninguna): ").strip()
    ya_usa = [x.strip() for x in ya_usa_raw.split(",") if x.strip()]
    cuentas_raw = input("  Cuentas que el cliente va a crear a mano (ej. telegram, whatsapp-business, google-drive): ").strip()
    cuentas = [x.strip() for x in cuentas_raw.split(",") if x.strip()] or ["telegram"]

    man = {
        "cliente": cliente,
        "paquete": paquete,
        "acompanamiento": acompanamiento,
        "vault": vault,
        "modulos": modulos_manifiesto,
        "herramientas": {
            "modo": modo,
            "perfil": "auto",
            "ya_usa": ya_usa,
            "extras": [],
            "excluir": [],
            "cuentas": cuentas,
        },
    }
    if nombre_agente or personalidad:
        man["agente"] = {}
        if nombre_agente:
            man["agente"]["nombre"] = nombre_agente
        if personalidad:
            man["agente"]["personalidad"] = personalidad

    texto = yaml.safe_dump(man, allow_unicode=True, sort_keys=False)
    print("\n== Manifiesto generado ==\n")
    print(texto)

    salida = a.salida or f"manifiestos/{cliente.lower().replace(' ', '-')}.yaml"
    if preguntar_si_no(f"\n¿Guardar en {salida}?", True):
        ruta = REPO / salida if not pathlib.Path(salida).is_absolute() else pathlib.Path(salida)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        if ruta.exists():
            print(f"AVISO: {ruta} ya existe, no se sobrescribe. Guarda a mano si quieres reemplazarlo.", file=sys.stderr)
        else:
            ruta.write_text(texto, encoding="utf-8")
            print(f"Guardado en {ruta}")
    else:
        print("No se guardó nada; copia el texto de arriba a mano si lo necesitas.")


if __name__ == "__main__":
    main()
