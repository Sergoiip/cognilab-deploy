# Deriving a palette from existing artwork — and gating it

How to build a palette from marks that already exist, without inheriting the
artwork's glow as a stroke color, and how to keep the palette honest with a
gate the generator enforces.

## The trap: most-saturated pixel is not a usable color

Sampling "the most saturated pixel in each hue family" from a mark built with
gradients and glow returns a value that is real and visible in the PNG — and
unusable as a line color. That pixel lives *inside* a highlight. A 3px stroke
in that color renders as a thin, dark, low-contrast line, because the glow it
came from is a wide bloom a thin stroke never reproduces.

What such a sample typically gives you against a near-black background
(`{{COLOR_FONDO}}`):

| Family | Use | Contrast | Verdict |
| --- | --- | --- | --- |
| blue | lines | 4.39:1 | fails 4.5:1 |
| violet | fill | 3.33:1 | fails, badly |
| cyan | accent | 9.16:1 | fine |
| magenta | accent | 5.40:1 | fine |

Both failures shipped in a first build before anything checked.

**The distinction that resolves it:** a gradient serves *glow*; a stroke serves
*line*. Different jobs need different values from the same family. Derive them
separately.

## Fix by walking up, not by switching palette

Keep the hue family and raise its value until it clears the minimum:

```python
def hx(rgb): return "#%02x%02x%02x" % tuple(min(255, int(round(v))) for v in rgb)

base = rgb(P["linea_muestreada"])   # the sampled color
for k in range(100, 200):            # walk up
    h = hx(tuple(c * k / 100 for c in base))
    if contrast(h, P["fondo"]) >= {{CONTRASTE_MINIMO}}:
        break                         # e.g. 4.39:1 -> 4.52:1, visibly the same hue
```

Swapping in a different family instead — or borrowing a color from a swatch
that "looked right" — breaks the mark↔guide relationship without a reason
anyone can state later.

## Tints over a dark background are not lighter colors

`fill-opacity="0.30"` over a near-black ground composites to about **1.2:1** —
effectively black. The same color at 85 % opacity still measures ~2.6:1.

Decide what a fill is for before tuning it:

- **decorative** — interior texture, depth cue. Make it opaque and simple.
- **informational** — it encodes something. Then it must pass as a solid.

Compute the composite rather than eyeballing it:

```python
def composite(fg, bg, alpha):
    f, b = rgb(fg), rgb(bg)
    return hx(tuple(f[i]*alpha + b[i]*(1-alpha) for i in range(3)))
```

## Embedding the gate

Run it inside the generator so a palette edit cannot ship unchecked:

```python
def test_contraste(P, minimo={{CONTRASTE_MINIMO}}, exempt=()):
    # _lum / cr as in SKILL.md step 8
    lineas = {k: v for k, v in P.items() if k != "fondo" and k not in exempt}
    fallas = [(n, h, cr(h, P["fondo"])) for n, h in lineas.items()
              if cr(h, P["fondo"]) < minimo]
    if fallas:
        raise RuntimeError(
            "contraste bajo el mínimo: "
            + "; ".join(f"{n} {h} = {v:.2f}:1" for n, h, v in fallas)
            + ". Subí el color o cambiá su uso; no lo bajes de saturación.")
```

Keep the exempt list small and justified (decorative fills made opaque on
purpose). Each entry is a decision someone can be wrong about — comment it.

## Audit the whole palette, not the delta

A guide can state a minimum and still ship marks that violate it: the guide and
the artifact are separate claims. When adopting or re-deriving a palette, check
**every** line color, including ones considered settled, and report
pre-existing failures as defects in the shipped asset.

## Record the values in the guide

Keep a table of each palette color, its value and its computed contrast
against its own background, with a "was → now" note for anything walked up, so
a later session can see what changed and why. A near-black background makes
most saturated colors pass; **re-run the gate if the background changes** — the
numbers do not transfer.
