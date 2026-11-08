#!/usr/bin/env python3
"""
Structural verification of a brand lockup SVG.

    python3 verificar_lockup.py svg/lockup.svg [otro.svg ...] [--id-wordmark wordmark]

Checks the SVG SOURCE, not the rendered pixels. That distinction is the whole
point: rsvg fails silently, and pixel metrics against a branded background
return healthy values for an empty render. See
references/rsvg-silent-failures.md.

Checks:
  - a viewBox exists
  - the root <svg> width is an integer (decimals make rsvg drop groups)
  - inside the wordmark group: #<path> >= #glyphs, and no glyph starts
    outside the viewBox
  - every <g transform="..."> contains drawable geometry

Exit 0 = structurally sound. Exit 1 = at least one check failed.
"""
import argparse
import re
import sys


def verificar(path, id_wordmark="wordmark"):
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    fallos = []

    vb = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"', s)
    if not vb:
        return ["no se encontró viewBox: el archivo no es un SVG renderizable"]
    vb_w = float(vb.group(1))

    # Root width must be an integer. Decimals make rsvg drop transformed groups.
    m = re.search(r'<svg[^>]*\bwidth="([\d.]+)"', s)
    if m and "." in m.group(1):
        fallos.append(
            f'el width de la raíz es decimal ("{m.group(1)}"): rsvg descarta '
            f"los grupos con transform. Usar entero y dejar el decimal solo "
            f"en el viewBox.")

    # Wordmark checks, only when there is one.
    marca = f'id="{id_wordmark}"'
    if marca in s:
        inicio = s.rfind("<g", 0, s.find(marca))
        wm = s[inicio if inicio >= 0 else s.find(marca):]
        glifos = len(re.findall(r'scale\([\d.]+', wm))
        paths = wm.count("<path")
        if glifos == 0:
            fallos.append("el wordmark no tiene glifos")
        elif paths < glifos:
            fallos.append(
                f"{glifos} glifos pero solo {paths} <path>: el atributo d se "
                f"está emitiendo sin envolver en <path d=\"...\"> y el "
                f"renderizador lo descarta en silencio.")
        xs = [float(x) for x in
              re.findall(r'translate\(([\d.]+)[\s,]+[-\d.]+\)\s*scale', wm)]
        if xs and max(xs) >= vb_w:
            fallos.append(
                f"el último glifo arranca en x={max(xs)} pero el viewBox "
                f"termina en {vb_w}: el texto se sale del lienzo.")

    # Every element carrying a transform must contain drawable geometry.
    for g in re.finditer(r'<g\b[^>]*transform="([^"]+)"[^>]*>(.*?)</g>', s, re.S):
        transform, cuerpo = g.group(1), g.group(2)
        if not re.search(r'<(path|circle|rect|polygon|polyline|ellipse|line|use|g)\b',
                         cuerpo):
            fallos.append(
                f'un <g transform="{transform}"> no contiene geometría: el '
                f"contenido es texto, no un elemento dibujable.")

    return fallos


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", nargs="+", help="lockup SVG(s) a verificar")
    ap.add_argument("--id-wordmark", default="wordmark",
                    help='id del <g> que contiene los glifos (default: "wordmark")')
    a = ap.parse_args()

    rc = 0
    for path in a.svg:
        try:
            fallos = verificar(path, a.id_wordmark)
        except OSError as e:
            fallos = [f"no se pudo leer: {e}"]
        if fallos:
            rc = 1
            print(f"✗ {path}")
            for f in fallos:
                print(f"    {f}")
        else:
            print(f"✓ {path} — estructura correcta")
    return rc


if __name__ == "__main__":
    sys.exit(main())
