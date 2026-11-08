#!/usr/bin/env python3
"""
Verify a RENDERED lockup by measuring it, not by calculating it.

    python3 verificar_alineacion.py png/lockup.png --split 560 --tolerancia 8 [--fondo '#RRGGBB']

Complements verificar_lockup.py, which checks the SVG source. This one checks
the PNG that actually ships, which is where alignment errors survive every
structural test.

WHY MEASUREMENT AND NOT ARITHMETIC
Three independent calculations are wrong in ways invisible in the numbers:

  · A group scaled to ESC inside a WxH viewBox has its optical center at
    H*ESC/2, not at the canvas center. It needs (H - H*ESC)/2 to compensate.
  · Accented capitals break the cap-height assumption. A word with an accented
    capital measures taller than one without, at the same body size, so a
    single cap constant is wrong by tens of pixels.
  · Text width is not 0.6 * font_size. The estimate runs long, and the error
    is the width of the entire trailing margin.

All three produce a file that renders, exits 0, and looks almost right.

If --fondo is omitted, the background color is read from the top-left pixel.

Exit 0 = within tolerance. Exit 1 = misaligned or uneven margins.
Requires: magick (ImageMagick 7).
"""
import argparse
import subprocess
import sys


def _magick(*args):
    r = subprocess.run(["magick", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "magick falló")
    return r.stdout.strip()


def color_esquina(png):
    """Background color sampled from the top-left pixel."""
    return _magick(png, "-format", "%[pixel:p{0,0}]", "info:")


def centro_vertical(png, x0, x1, H):
    """Optical center of the ink inside the horizontal slice [x0, x1)."""
    out = _magick(png, "-crop", f"{x1 - x0}x{H}+{x0}+0", "+repage",
                  "-fuzz", "6%", "-trim", "-format", "%h %Y", "info:")
    hh, yy = (int(v) for v in out.split())
    if hh == 0:
        raise RuntimeError(f"la franja x=[{x0},{x1}) está vacía: nada dibujado")
    return yy + hh / 2


def margenes(png, fondo):
    """(izq, der, arr, aba) of the drawn content, in px."""
    out = _magick(png, "-bordercolor", fondo, "-border", "1", "-fuzz", "6%",
                  "-trim", "-format", "%w %h %X %Y", "info:")
    bw, bh, bx, by = (int(v) for v in out.split())
    bx, by = bx - 1, by - 1          # compensate the 1px border
    W = int(_magick(png, "-format", "%w", "info:"))
    H = int(_magick(png, "-format", "%h", "info:"))
    return bx, W - bx - bw, by, H - by - bh


def verificar(png, split, tol, tol_margen, fondo):
    H = int(_magick(png, "-format", "%h", "info:"))
    W = int(_magick(png, "-format", "%w", "info:"))
    if not 0 < split < W:
        return [f"--split={split} fuera del ancho de la imagen ({W}px)"]
    fondo = fondo or color_esquina(png)
    fallos = []

    try:
        c_sim = centro_vertical(png, 0, split, H)
        c_txt = centro_vertical(png, split, W, H)
        des = abs(c_sim - c_txt)
        if des > tol:
            fallos.append(
                f"texto descentrado {des:.0f}px respecto al símbolo "
                f"(símbolo en {c_sim:.0f}, texto en {c_txt:.0f}; tolerancia "
                f"{tol}). Subí o bajá la línea base del texto.")
    except RuntimeError as e:
        return [str(e)]

    izq, der, arr, aba = margenes(png, fondo)
    if abs(izq - der) > tol_margen:
        fallos.append(
            f"márgenes horizontales desiguales: {izq} izq contra {der} der. "
            f"El ancho del viewBox no corresponde al largo de este texto.")
    if abs(arr - aba) > tol_margen:
        fallos.append(
            f"márgenes verticales desiguales: {arr} arriba contra {aba} abajo. "
            f"El conjunto flota en el lienzo.")
    return fallos


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("png", nargs="+")
    ap.add_argument("--split", type=int, required=True,
                    help="x en px donde termina el símbolo y empieza el texto")
    ap.add_argument("--tolerancia", type=float, default=8.0,
                    help="desalineación vertical máxima admitida, px")
    ap.add_argument("--tol-margen", type=float, default=20.0,
                    help="diferencia máxima entre márgenes opuestos, px")
    ap.add_argument("--fondo", default=None,
                    help="color de fondo para el trim (default: píxel superior izquierdo)")
    a = ap.parse_args()

    rc = 0
    for png in a.png:
        try:
            fallos = verificar(png, a.split, a.tolerancia, a.tol_margen, a.fondo)
        except (RuntimeError, ValueError, FileNotFoundError) as e:
            fallos = [str(e)]
        if fallos:
            rc = 1
            print(f"✗ {png}")
            for f in fallos:
                print(f"    {f}")
        else:
            print(f"✓ {png} — alineado y con márgenes parejos")
    return rc


if __name__ == "__main__":
    sys.exit(main())
