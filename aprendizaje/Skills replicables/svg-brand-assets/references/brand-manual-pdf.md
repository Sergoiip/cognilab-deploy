# The brand guide as a designed PDF

The guide is the artifact that outlives the session. Written as markdown it is
a reference; rendered as a PDF it is the thing a designer, a printer or a client
actually looks at — and it is a different deliverable with its own failure
modes.

Route the build itself through `{{PIPELINE_PDF}}` (HTML + CSS →
headless Chromium). This file covers only what is specific to a brand guide.

## Make the document apply its own rules

A brand guide that describes the identity without obeying it is a brochure.
The check is simple and worth stating in the source, because it changes what
goes on each page:

| The guide states | The PDF therefore |
| --- | --- |
| the background is near-black | **is** near-black, verified by pixel |
| contrast minimum is 4.5:1 | **prints the measured ratio**, not the declared one |
| mark X is illegible below N px | **shows N px failing**, at real size |
| no 3D gloss / no neon | has none |

Verifying the palette is a strong final check, because the hexes are known:

```python
cols = collections.Counter(im.getpixel((x, y)) for y in range(0, H, 3)
                           for x in range(0, W, 3))
for nombre, hexa in PALETA.items():
    n = cols.get(rgb(hexa), 0)
    assert n > 30, f"{nombre} {hexa} no aparece en el render"
assert cols.most_common(1)[0][0] == rgb(PALETA["fondo"])
```

If a declared hex is absent from its own guide, the stylesheet and the palette
have drifted — and that check costs one image pass.

## Contrast: measure the render, never the hex

This is the single most transferable lesson, and it is the one that changes
outcomes. Computing WCAG contrast from the hex **overstates the real ratio**,
because it assumes pure ink and pure ground:

| | Calculated from hex | Measured on the render |
| --- | --- | --- |
| light-violet footer ink, small type | 6.67:1 | **2.47:1** |

The mechanism is antialiasing. Small type (6.8 pt at 150 dpi) has a glyph core
that never reaches the nominal color — it composites toward the background. The
WCAG formula has no term for that. Two more contributors: page-wide `text-shadow`
on body copy, and a radial vignette that darkens the ground exactly where the
text block ends.

Sample p20 for the background (low tail, inside the ground, letters excluded)
and p99.5 for the text (high tail, inside the glyph core, halo excluded). p95 is
the glow, not the letter.

**Sanity check before quoting any ratio:** the lightest text on the page must
measure well above 120/255. If it does not, you are sampling the halo and every
number is invented.

## Sweep the page; do not hardcode sample boxes

The first version of the checker named fixed rectangles for each text zone. It
reported three zones below 4.5:1 on a page that measured 4.59:1 minimum, i.e. it
pointed at empty regions and read the ground as text. It nearly caused a
"correction" to colors that were already correct.

```python
# measure every horizontal band that actually contains ink
filas = []
for y in range(0, H - paso, paso):
    vals = sorted(_lum(im.getpixel((x, yy)))
                  for yy in range(y, y + paso)
                  for x in range(int(.06*W), int(.94*W)))
    fondo, texto = vals[int(len(vals)*.20)], vals[int(len(vals)*.995)]
    if texto < 40:          # no glyph here: nothing to measure
        continue
    filas.append(((texto+5)/(fondo+5), texto, fondo, y/H))
```

Sweeping cannot measure the wrong place, because there is no place to name. The
cutoff discards empty bands rather than reporting them as failures — and it
has to be set above card borders, not above zero. A 1px dark-teal card border
on a near-black ground yields a p99.5 of ~40, which at a cutoff of 40
survives the filter and reports a fabricated 4.26:1 on a band containing no
text at all. The nucleus of even 6.4 pt type clears 60. So:

```python
if texto < 60:      # below this you are reading a border, not a glyph
    continue
```

Then fix the *cause* named in the failure — a footer that fails may need a
lighter ink, or the vignette darkening that corner may need reducing. Raising
the ink when the vignette is the cause fixes nothing.

## Texture has a ceiling, and the user will find it

A brand guide renders its own aesthetic, which means it inherits the exact
failure the aesthetic warns about. The recurring one: **scanlines strong enough
to read as a second tone across the page.** At 7.5% they stop being texture and
become a screen door laid over the text — the page looks like a dirty print, and
the guide that argues for legibility is the least legible artifact in the folder.

1.2% with a 1px-on/5px-off period is the working value: the texture is present
at 100% zoom and invisible at reading size. Measure it rather than trusting the
number:

```python
# amplitude of the background's vertical variation
vals = [lum(im.getpixel((x, y))) for y in range(int(.30*H), int(.45*H))]
amplitud = (max(vals) - min(vals)) / 255   # ~0.7% is right; ~3% is a screen door
```

Record the limit and its test in the guide itself, so the next revision does not
rediscover it: **if the lines are still visible after you delete the text, they
are too strong.** That sentence is worth more than the hex value.

The same ceiling applies to any decorative layer added to the page. Each one is
a contrast cost — add it, re-measure, and if a band drops below the minimum, the
layer goes.

## Inline SVG loses its dimensions and its background

Embedding an exported logo in the guide has two silent losses:

```python
s = re.sub(r'\s(width|height)="[\d.]+"', "", s, count=2)   # fixed size -> overflows
s = re.sub(r'\s*<rect[^>]*fill="{{COLOR_FONDO}}"[^>]*/>', "", s, count=1)  # page paints it
```

Without the first, a lockup's nominal fixed size (e.g. `1200×512`) overflows its container and
pushes the following text off the page. Without the second, the mark carries its
own opaque ground and shows as a black block.

```css
.card svg { display: block; width: 100%; height: auto; }
```

This is the same silent-drop family as the rsvg failures in
`rsvg-silent-failures.md`, arriving from the opposite direction.

## Report the numbers, not adjectives

The guide's whole value is that its claims are checkable. The PDF inherits that:
print the ratio table with the measured values, list the real minimum sizes with
the failing one marked, and state in the source that the values are computed at
generation time from the real background. "Professional" is not a claim anyone
can check; `4.58:1 worst band over 34 measured bands` is.

## Regenerate, and let the generator refuse

Keep the PDF generated, like the marks — a generator script beside the markdown,
gated on the contrast sweep so an unmeasured edit cannot ship:

```
marca/
  MANUAL-DE-MARCA.md      the reference: edited, versioned
  generar_manual_pdf.py   the artifact: measured, gated
  Manual de marca.pdf     generated
```

State the split in the markdown so nobody edits the PDF. The generator raising
on a low band is the mechanism that keeps the two honest.