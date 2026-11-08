---
name: svg-brand-assets
description: "Use when generating logos, brand marks, or SVG lockups. Builds marks as scripted vector geometry, gates them numerically (geometry, contrast, structure, alignment) and rasterizes them without rsvg's silent failures."
version: 1.0.0
license: MIT
platforms: [linux]
metadata:
  tags: [svg, brand, logo, rsvg, fonttools, harfbuzz, lockup, rasterize, brand-guide]
  category: creative
---

# SVG brand assets — generate, verify, rasterize

## Parámetros a configurar

| Placeholder | Qué poner | Ejemplo genérico |
| --- | --- | --- |
| `{{NOMBRE_MARCA}}` | Name of the brand/product the mark is for | `Acme Studio` |
| `{{DIR_MARCA}}` | Folder that holds the brand's assets, generators and guide | `./marca/` |
| `{{DIR_NOTAS}}` | Root of the owner's notes/docs (decision records, brand notes, prior writing) | `./notas/` |
| `{{RAICES_BUSQUEDA}}` | Directories to search for existing marks before designing | `./proyectos ./documentos` |
| `{{URL_PUBLICADA}}` | Live page/channel where the current mark is served | `https://example.com` |
| `{{NOTA_DE_PAUSA}}` | Filename pattern of the pause/resume note for a multi-session exploration | `CONTINUAR-*.md` |
| `{{PALETA}}` | Dict of named brand colors (line colors + background) as the generator constant | `{"fondo": "#0b0b10", "linea": "#..."}` |
| `{{COLOR_FONDO}}` | Background color the marks and the guide are measured against | `#0b0b10` |
| `{{CONTRASTE_MINIMO}}` | Minimum contrast ratio the guide mandates for line colors / text | `4.5` |
| `{{FUENTE_WORDMARK}}` | Path to the licensed font file used for the wordmark | `./fuentes/Familia-Bold.ttf` |
| `{{TAMANOS_DESPLIEGUE}}` | Real deployment sizes to check legibility at | `16 24 32 64 128 512` |
| `{{PYTHON_CON_DEPS}}` | Interpreter/venv that has fontTools, PIL, numpy, shapely | `./.venv/bin/python` |
| `{{PIPELINE_PDF}}` | Your HTML+CSS → headless Chromium PDF workflow/skill | `designed-pdf-deliverables` |
| `{{LIBRERIA_REGLAS_LOGO}}` | Shared rulebook of logo design patterns used across concepts | a `design_patterns.md` file |
| `{{TEXTURA_PRESENTACION}}` | Name of the textured/material variant used for video & channel art | `material`, `crt`, `glass` |
| `{{DIR_CLIENTE}}` | Project folder of a third-party client (mockup deliveries) | `./clientes/<cliente>/` |
| `{{TELEFONO_CONTACTO}}` | Placeholder shown on mockups until the client's real contact is known | `+00 000 000 0000` |

## Propósito

Build a logo / brand mark / wordmark / lockup as **vector geometry produced by a
script**, prove it is correct with numeric gates, and export it to PNG/WebP at
every size it ships — plus the brand guide that documents it.

The hard part is not the design. It is that **rsvg fails silently**: it drops
elements, returns a correctly-sized PNG of the wrong content, exits 0, and warns
about nothing. And the second hard part is that a mark can pass every gate and
still be the wrong mark (built from a description, built on the wrong source
file, or in the wrong half of the client's style). Everything below exists
because those happened.

## Cuándo usar

- Redesigning, modernizing, or creating a logo, brand mark, or lockup
- Producing logo/icon/symbol SVG plus PNG exports at several sizes
- Composing a symbol with a wordmark into a horizontal or stacked lockup
- Debugging a render where "it exported fine" but the PNG is missing part
- Auditing an existing mark against a brand guide's rules (contrast, aesthetic)
- Building a concept library of many logo options, animating an approved mark,
  producing social covers or a designed brand-guide PDF from the identity

Not for: UI icon sets, architecture/infra diagrams, infographics, or one-off
HTML artifacts.

## Entradas

- The current mark(s), if any — and, ideally, the live URL where it is served
- Written decision records: brand note, guide, spec (`{{DIR_NOTAS}}`)
- The client's own liked references (3–6 screenshots/links/named brands) for
  any open concept
- Palette (`{{PALETA}}`), background (`{{COLOR_FONDO}}`), contrast minimum
  (`{{CONTRASTE_MINIMO}}`), licensed font (`{{FUENTE_WORDMARK}}`)
- Target media and their real sizes (`{{TAMANOS_DESPLIEGUE}}`)

## Pasos

### 1. Find what already exists before designing

The identity is usually spread across several places with no canonical copy.
Search the asset directories, the CSS of generated documents, and whatever
governs the channel/brand.

**Check for a pause/resume note first.** A multi-session exploration is often
tracked in a note (`{{NOTA_DE_PAUSA}}`) with: state at pause, directions
rejected (with the reason, so they are not re-proposed), the confirmed
direction, and the exact next step.

```bash
find {{DIR_MARCA}} -iname '{{NOTA_DE_PAUSA}}' -o -iname '*retomar*' -o -iname '*resume*'
find {{RAICES_BUSQUEDA}} -type f \
  \( -iname '*logo*' -o -iname '*brand*' -o -iname '*marca*' -o -iname '*identidad*' \) \
  2>/dev/null | head -40
```

If the note exists it is authoritative over re-deriving the brief — read it
fully before asking anything it already answers, and update it in place.

**Confirm WHICH file is the live one before drawing anything.** Asset folders
hold several generations side by side (old mark, current mark, favicon,
wordmark, emblem); picking by filename or mtime yields a complete, confident,
wrong deliverable. In order of strength:

1. Fetch the published asset and hash it against local candidates:
   ```bash
   curl -s -o "$TMPDIR/live" '<asset-url-from-{{URL_PUBLICADA}}>'
   sha256sum "$TMPDIR/live" {{DIR_MARCA}}/candidato*.png
   ```
2. Extract the asset URLs the live page serves (markdown images, CSS `url()`,
   `<link rel=icon>`) and match them by dimensions and filename family. Two
   different families served/stored side by side means **two marks**, not one.

When the user names a live URL or channel, go there before reading a local
file. A search that returns several plausible marks has not disambiguated
anything — hash or ask. Ten minutes of confirmation is cheap; a full identity
rebuilt on the wrong mark costs the whole session.

**Ask whether there is more than one brand.** A product mark and a parent
mark can deliberately share palette and typeface but never a symbol. If a
brand is later retired, remove it *completely* (grep the whole project, not
only the generator).

#### Look at the mark. Never build one from a description of it.

A vision model's prose about a logo is not the logo. Drawing geometry from that
text produces an invented mark wearing an existing name — and **no gate
catches it**: the SVG is valid, the palette passes, the guide documents it. It
surfaces only when the owner opens the real file.

- Open the source with a vision tool and treat its answer as a **hypothesis**.
- **Enumerate what is in the mark** and get it confirmed: number of rings,
  branches/limbs, filled vs outlined parts, where the text sits, flat vs
  gradient type. One missing limb is a different mark.
- Show the reconstruction beside the source. Unconfirmed reconstructions are
  labeled as guesses in the generator's docstring.
- When geometry must be faithful, **measure pixels** (mask → polar unwrap →
  IoU), see `references/reference-to-flat-logo.md`.

Corollary: the structural recipes in steps 4–5 apply **only when you are
choosing the geometry**. Reproducing an existing mark means reproducing its
subject; "prefer hub-and-spoke" applied to a mark depicting a specific object
turns it into a network graph — clean and categorically wrong.

#### Search the notes, not just the files

A decision record often fixes palette, claim and aesthetic limits, and states
what is still open (maybe only the logo). It is authoritative over colors
sampled from artwork.

```bash
grep -ril 'logo\|identidad\|marca\|brand\|paleta\|palette' {{DIR_NOTAS}} --include='*.md'
```

- **Two palettes in circulation** (note says one set of values, artwork on disk
  carries a near-identical but different set): the written decision wins — it
  was a decision; the artwork is residue. Record the conflict as an open item.
- **Same rule for TEXT.** Manifesto, tagline, voice section: never generate
  from scratch. Mine the owner's own prior writing in `{{DIR_NOTAS}}`, quote/
  adapt it as the candidate, and ask for confirmation. Brand text must read as
  written by the person whose brand it is.

### 2. Preserve the metaphor, replace the execution

"Modernize" keeps what the mark *means* and changes how it is drawn;
"redesign" changes the meaning too. Preserve when the metaphor carries
recognition and the complaint is execution (heavy effects, dated finish,
unreadable at size). Replace only when the metaphor itself says the wrong thing.

High-distance, low-loss execution changes **for a flat/minimal brief** (confirm
the client's references skew that way first — for a glossy/gradient brief the
list inverts):

- drop 3D finish (bevels, extrusion, gloss, inner highlights)
- stroke instead of fill — survives small sizes where gradients turn to mud
- re-cut proportions per medium (business card ≠ favicon)

Justify each change from a rule the project already committed to, not from
taste. Keep old files in a clearly named `referencia/` subfolder as provenance.

### 3. A brand-new symbol — ground it before drawing it

With no predecessor, the risk flips: inventing a "new" mark that is actually a
famous one. Primitive shapes have a small, already-claimed vocabulary (ring +
node = spinner, sphere + orbit = generic atom/chat icon, tapered curved stroke
= swoosh, faceted polyhedron = crypto icon). This recurs across unrelated style
briefs — it is the method, not bad luck.

**A mood word names a range, not a point.** "Modern", "clean", "tech" can mean
flat-matte-minimal to one client and saturated glossy dimensional gradients to
another. A mark that passed every check was rejected three rounds in a row as
"generic" because the whole direction was the wrong half of the client's word.
**Ask for 3–6 concrete liked references before the first full round.**

Then:

1. **Research real current marks in the requested style** (case studies,
   curated roundups, named logos). Extract the concrete technique ("one clean
   base shape + one deliberate cutout"), write it down as a reusable reference
   doc, then apply it.
2. **Stress-test adversarially, by name.** Not "does this look good?" but
   "does this resemble a known logo or stock icon — spinner, chat/atom icon,
   swoosh, crypto diamond, bird/wing, waveform, checkmark, scan frame, Olympic
   rings?" See `references/generic-icon-traps.md`.
3. **AI raster generators are mood-board tools, never the logo.** They render
   bloom and photoreal shading that is not vector and dies at favicon size.
   Free tiers are often single-shot. If the agent's image tool was just
   enabled, it may need a new session (or a gateway restart) to register;
   fall back to calling the provider API directly with credentials already
   configured in the environment rather than declaring it unavailable.
4. **After a few grounded, self-critiqued rounds still miss, stop generating
   blind.** Name the failed pattern each time and offer real next steps (a
   vector tool, a human designer, a sketch or named references to clone the
   execution level from).

**Radial 3-arm grammar reads as generic atom/science** no matter the colors or
curvature. When flagged 3+ times, change the topology, not the polish.

### 4. "Many options" means many FORMS, in vector

When asked for multiple versions or a library, explore FORM: several concepts
(current mark re-expressed + genuinely new metaphors), each in one ink and in
one shared material recipe, on one comparison board. Do **not** answer with an
interactive 3D/WebGL lab of one shape in several materials — that is not
exploring the logo, and a live 3D canvas is not a logo. Procedure, file
contract, checker, subagent fan-out and board:
`references/logo-exploration-library.md`.

### 5. When hand-coded SVG hits its ceiling — validate in 3D, deliver flat

If rounds keep being rejected as "too flat / flimsy" and the diagnosis is
technique, rebuild the geometry as a real 3D surface to **validate** form,
occlusion and material — but the deliverable stays a flat SVG that *suggests*
depth. "A logo is flat but can give an impression of depth; that is a render,
not a logo."

1. Parametrize curves + width profiles; build an SDF; measure crossings; mesh;
   render headless (Cycles) — full recipe in
   `references/3d-brand-mark-workflow.md`.
2. Project validated curves orthographically to 2D.
3. Flat SVG with per-region gradients that follow the form, occlusion via draw
   order, highlights on a consistent light side, soft offset shadows.
4. A central nucleus is drawn **last**, and arms bow outward to leave a real
   void — see `references/flat-logo-visible-nucleus.md`.

### 6. One geometry, one variant per medium

| variant | medium | treatment |
| --- | --- | --- |
| flat | documents, web, print, PDF | one color, no effects, light and dark |
| `{{TEXTURA_PRESENTACION}}` | video, channel art, bumpers | the medium's own aesthetic |

Share coordinates, vary only the paint. The exported SVG is an **artifact**:
parameters live in the script (nodes, radii, angles, colors, proportions); any
edit goes in the script and re-runs.

```python
CENTRO = (256.0, 256.0)
RAMAS = [(-104, 118, 17, [(-26, 74, 10)]), (-28, 96, 13, []), ...]
```

If the brand folder already has a generator (HarfBuzz shaping + fontTools
outlines + measured layout), **import its functions** for a new variant and
only add the new paint/layer on top.

### 7. Verify geometry numerically, before rendering

A render cannot tell you whether two edges mathematically intersect. Assert it
and refuse to export on failure.

```python
def test_cruces(aristas, key=lambda p: (round(p[0], 2), round(p[1], 2))):
    def ccw(a, b, p):
        return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])
    def hit(p1, p2, p3, p4):
        d1, d2 = ccw(p3, p4, p1), ccw(p3, p4, p2)
        d3, d4 = ccw(p1, p2, p3), ccw(p1, p2, p4)
        return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))
    cruces = []
    for i in range(len(aristas)):
        for j in range(i + 1, len(aristas)):
            a, b = aristas[i]; c, d = aristas[j]
            if key(a) in (key(c), key(d)) or key(b) in (key(c), key(d)):
                continue          # shared endpoint = convergence, not a crossing
            if hit(a, b, c, d):
                cruces.append((aristas[i], aristas[j]))
    return cruces
```

Normalize endpoints to 2-tuples before comparing — comparing `(x, y, r)`
against `(x, y)` makes every pair look like a crossing.

Also assert: node separation `dist(c1,c2) - (r1+r2) > 0`; optical centering
from a bbox **including radii**; exact symmetry angles, or a comment that the
asymmetry is deliberate.

**Woven / interlocking marks:** a spiral cloned and rotated by 360/N keeps
constant angular separation and provably never crosses its copies — prove it
with a closest-approach scan before rendering, then switch to closed-form
shapes (circle–circle intersection) and alternate over/under with one clipped
corrective patch per pair. See `references/real-occlusion-weaving.md`.

**Network marks:** a ring of N equal nodes reads as a star badge; a hub with
unequal branch lengths reads organic and is crossing-free by construction.
Keep one dominant hub. Node/synapse language: `references/node-graph-marks.md`.

### 8. Gate the palette's contrast in the generator

The most saturated pixel of a gradient is its **glow**, not a line color.
Promoted to a stroke it passes a swatch and fails on screen (two such colors
measured 4.39:1 and 3.33:1 against a mandated 4.5:1 and shipped, because
nothing checked).

```python
def _lum(h):
    h = h.lstrip('#'); c = []
    for i in (0, 2, 4):
        v = int(h[i:i+2], 16) / 255
        c.append(v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4)
    return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]

def cr(fg, bg):
    a, b = sorted((_lum(fg), _lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)

def test_contraste(P, lineas, minimo={{CONTRASTE_MINIMO}}):
    fallas = [(n, P[n], cr(P[n], P["fondo"])) for n in lineas
              if cr(P[n], P["fondo"]) < minimo]
    if fallas:
        raise RuntimeError("contraste bajo el mínimo: " + "; ".join(
            f"{n} {h} = {v:.2f}:1" for n, h, v in fallas))
```

Fix by **walking the same hue upward** until it passes (keeps the family), not
by switching palette. A tint (`fill-opacity` 0.3 over near-black ≈ 1.2:1) is not
a lighter color: a fill is either decorative (make it opaque) or informational
(must pass as a solid). Audit what already shipped, not only the delta. Full
detail: `references/color-contrast-gate.md`. Moodboard-derived palettes come
from measured pixels, never from the board's title:
`references/moodboard-palette-extraction.md`.

### 9. Wordmark as outlines — never `<text>`

`<text>` depends on the font being installed where the file opens; elsewhere it
silently substitutes. Outlines are autonomous.

```python
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

fuente = TTFont("{{FUENTE_WORDMARK}}")
gs, upem = fuente.getGlyphSet(), fuente["head"].unitsPerEm
pen = SVGPathPen(gs)
gs[nombre_glifo].draw(TransformPen(pen, (esc, 0, 0, -esc, x, y)))  # mirror y + scale
d = pen.getCommands()
svg_glifo = f'<path d="{d}"/>'   # ALWAYS wrap — bare commands are text, dropped silently
```

Three individually silent, collectively fatal rules: mirror y; scale explicitly
(font units are huge); wrap the commands in `<path d="…">`. Shape with HarfBuzz
(`uharfbuzz`, `kern` on) — raw advances drop kerning — and add tracking
yourself. Check glyph coverage for the brand's language (accents, ñ, «», —,
digits) before adopting a font. Full logotype procedure (3 contrasting
directions, OFL fonts, weight instancing, stem-weight sizing, clear space,
small-size rules, comparison board): `references/wordmark-lockups.md`.

### 10. Compose the lockup — and measure, don't calculate, the alignment

Layout = symbol width + gap + text width + a right margin equal to the left.
Align the text to the symbol's **optical center**, not its bbox.

Arithmetic alignment fails three independent, invisible ways: a group scaled
inside a viewBox has its center at `W*ESC/2`, not the canvas center; accented
capitals change the measured cap block (tens of px); text width is not
`0.6 * font_size`. So render and measure:

```bash
python3 scripts/verificar_alineacion.py png/lockup.png --split <x_fin_simbolo> --tolerancia 8
```

Margins are **per mark** (each symbol's content box differs inside the same
viewBox); store them per mark. Gate `<= 8 px` misalignment in the generator.

### 11. Verify structure, not pixels

Pixel metrics are worthless against a silent renderer: a crop mean is dominated
by background; `maxima` / `-alpha extract` on a PNG without alpha return 255
for anything. An empty render measured "fine". Check the **SVG source**:

```bash
python3 scripts/verificar_lockup.py svg/lockup.svg
```

(paths ≥ glyphs, integer root width, last glyph inside the viewBox, no
transformed group without geometry). Then look at the PNG. When two methods
disagree, trust the simpler structural one and re-derive the metric.

### 12. Rasterize

```python
def render(src, dst, ancho, alto=None):
    if alto is None:                      # never assume width == height
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(src).read())
        alto = max(1, round(ancho * float(vb.group(2)) / float(vb.group(1))))
    r = subprocess.run(["rsvg-convert", "-w", str(ancho), "-h", str(alto), src, "-o", dst],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
```

Height from the viewBox is mandatory — forcing a wide lockup square pushes the
text out of frame. For material SVGs (blur/mask/filters, transparent ground),
render with headless Chromium instead. Then look at the actual PNG at every
`{{TAMANOS_DESPLIEGUE}}` size, side by side.

### 13. The brand guide (markdown + generated PDF)

```
{{DIR_MARCA}}/
  generar.py            # geometry + flat variants
  generar_lockup.py     # symbol + wordmark composition
  svg/                  # artifacts (do not hand-edit)
  png/
  manual-de-marca.md    # palette, type, rules, minimum sizes — measured
  generar_manual_pdf.py # PDF generator, gated on a contrast sweep
  referencia/           # prior marks, historical
```

The guide carries measurements, not adjectives: contrast per color (with where
it was computed), minimum legible size per mark (as a table), which variant
goes where, and the ruled-out treatments stated explicitly. Ship a PDF via
`{{PIPELINE_PDF}}` that **obeys its own rules** — and measure contrast on the
raster, because hex-computed contrast overstates small antialiased text badly
(6.67:1 calculated vs 2.47:1 measured). See `references/brand-manual-pdf.md`.

## Reglas de decisión

- **Live mark unknown or several candidates** → hash the served asset or ask;
  never pick by filename/mtime.
- **Existing mark to reproduce** → measure it, enumerate its elements, get
  confirmation; skip the concept recipes.
- **Open concept + mood word only** → ask for 3–6 liked references, then
  research real marks, then design.
- **Concept hits a named icon in the adversarial check** → discard the whole
  geometry family; do not tweak color/thickness.
- **Same structural verdict 3+ times** → change topology or metaphor.
- **Written palette vs sampled artwork disagree** → the written decision wins;
  log the conflict.
- **Line color fails contrast** → raise value within the same hue; do not
  desaturate or swap families.
- **Material/filters or transparent ground needed** → Chromium, not rsvg.
- **Rounds keep missing on technique** → validate in 3D, deliver flat SVG.
- **Each exploration round** → name the current best candidate and offer
  "consolidate this and move on" explicitly. Pipeline after a pick: symbol →
  logotype (3 directions) → brand guide; ask for the pick at each gate.
- **Full manual-scale deliverable** → approve the index/outline first; ask the
  order of the sections needing discussion; write each closed decision to the
  project's canonical brief on disk immediately.

## Verificación

- [ ] Source mark confirmed (hash/URL match or explicit owner confirmation)
- [ ] Element inventory of the mark confirmed (when reproducing)
- [ ] Adversarial named-icon collision check run on the 512 material render and
      the 32 px one-ink render; real verdict recorded
- [ ] Geometry gates pass in the generator: crossings, separation, centering
- [ ] Contrast gate passes for every line color vs `{{COLOR_FONDO}}`
- [ ] `scripts/verificar_lockup.py` exits 0 on every lockup SVG
- [ ] `scripts/verificar_alineacion.py` exits 0 on every lockup PNG
- [ ] PNGs viewed at every `{{TAMANOS_DESPLIEGUE}}`; minimum size documented
- [ ] Guide PDF: contrast measured on the raster by band sweep; declared hexes
      present in the render
- [ ] Every number reported traces to a command actually run

## Pitfalls

**Renderer (rsvg) — all exit 0, all silent** (`references/rsvg-silent-failures.md`)
- `SVGPathPen` output not wrapped in `<path d="…">` → text content, dropped.
- Root `<svg width>` with decimals → transformed groups dropped. Integer width;
  decimals only in the viewBox.
- No opaque background rect → transformed groups dropped. `fill="none"` or
  zero opacity does not count. Transparent variants → another engine.
- "It rendered" proves nothing: exit 0 + plausible file size ≠ content.

**Identity / source**
- Never build a mark from a description of a mark.
- Never pick the asset to redesign by filename; a folder of marks is not a mark.
- Never retype a source path's `d` by hand — a `d` can hold several subpaths;
  extract it in the generator and assert equality
  (`references/mark-animation.md`).
- Do not `clip-path` a monogram's inner orb to the outer path — it often lives
  in a hole of that path; clipping erases it.

**Concept & taste**
- A mark passing every numeric/adversarial check can still be rejected as
  "generic" if its aesthetic family is wrong; only the client's liked
  references test that.
- Open "is this good?" self-critique gets a charitable answer; ask by name.
- Never escalate an exploration to a 3D/WebGL material lab.
- Node/graph marks: clean and few beats rich and many; never bolt a second
  graphic system onto the form (`references/node-graph-marks.md`).
- A 3D render that passes every check can still be rejected as "a render, not a
  logo". Deliver flat.

**Measurement honesty**
- Never report a measurement you did not take; fabricated ratios get adopted.
- Vision reviewers hallucinate defects (spacing numbers, slivers, clipping,
  asymmetry in exact constructions) and swing scores on identical files.
  Confirm each defect numerically before changing geometry.
- When vision is unavailable/rate-limited, verify numerically (IoU, frame diff)
  and say the check was numeric. Never claim to have seen pixels you did not.
- Don't verify a rendered page with fixed sample rectangles — they drift onto
  empty ground. Sweep every band that holds ink.
- Hex-computed contrast is not the shipped ratio; measure the raster.

**Fonts & environment**
- A webfont that fails to load falls back silently; all families then measure
  the same width. Verify with `document.fonts.load(...)` and compare a DOM
  width against a deliberately nonexistent family. A wrong relative `url()` in
  `@font-face` is the usual cause.
- Check glyph coverage for the brand's language before adopting a font.
- A brand repo's Python/Node deps may live in a sibling project (venv,
  `node_modules`); grep existing scripts' import paths before installing.
  Use `{{PYTHON_CON_DEPS}}` consistently.

**Swatch / comparison boards**
- A contrast `color` set on an outer wrapper bleeds onto sibling captions that
  sit on the page background (invisible labels) — scope it to the chip.
- A flat flex row of N swatches orphans the last one; build explicit paired
  groups for semantic pairs. Ask vision specifically about missing/cut labels.
- Inlining the same SVG several times needs per-copy id prefixes, or gradients
  resolve to another copy.

## Variantes

- **Exploration library** (many concepts, one board): `references/logo-exploration-library.md`
- **Reference raster → measured flat logo** (+ glass variant): `references/reference-to-flat-logo.md`
- **3D validation → flat delivery**: `references/3d-brand-mark-workflow.md`,
  `references/flat-logo-visible-nucleus.md`
- **Woven / interlocking marks**: `references/real-occlusion-weaving.md`
- **Node / synapse / graph language; monogram + node**: `references/node-graph-marks.md`
- **Logotype & lockups**: `references/wordmark-lockups.md`
- **Animation of the approved mark** (draw-on, breathing node): `references/mark-animation.md`
- **Social covers / avatars / OG images from the guide**: `references/social-covers-from-brand-guide.md`
- **Fast 3-mockup set for a small-business client**: `references/small-business-mockup-set.md`
- **Palette from a moodboard**: `references/moodboard-palette-extraction.md`
- **Guide as a designed PDF**: `references/brand-manual-pdf.md`

## Implementación de referencia

The lessons above were distilled from one identity project; its brand-specific
choices are described here generically, so the pattern can be re-applied
without inheriting them:

- **Symbol:** a woven three-fold mark — three tapered ribbons growing from a
  central sphere ("nucleus"), cyclic over/under, glass/soft-3D material in the
  presentation variant; a monogram-plus-node variant where a letter's terminal
  dissolves into beads that stop a synapse gap short of a three-lobed node.
- **Palette:** a three-hue gradient (cool → warm) on a near-black background;
  line colors walked up the same hue until each cleared the guide's 4.5:1.
- **Presentation aesthetic:** a retro-screen texture (scanlines, chromatic
  aberration, grain, bloom) used only on video/channel art, capped at ~1.2 %
  scanline amplitude in documents.
- **Wordmark:** a mono ExtraBold, caps, +0.10 em tracking, as the continuity
  direction against two contrasting geometric directions.
- **Toolchain:** Python generators (fontTools + HarfBuzz + shapely + numpy),
  rsvg for flat exports, headless Chromium for material SVGs and the PDF guide,
  Blender (Cycles, headless) for 3D validation.

Replace each with the target brand's own decisions — `{{PALETA}}`,
`{{FUENTE_WORDMARK}}`, `{{TEXTURA_PRESENTACION}}` — before reusing any
generator.

## Reference files

- `references/rsvg-silent-failures.md` — the three rsvg failure modes, reproductions, minimal fixes.
- `references/color-contrast-gate.md` — palette from artwork without promoting glows; the gate.
- `references/moodboard-palette-extraction.md` — board API fetch + PIL dominant/complementary colors.
- `references/generic-icon-traps.md` — geometry families that always read as a UI icon.
- `references/real-occlusion-weaving.md` — provable crossings, over/under patches, clip+blur seam.
- `references/3d-brand-mark-workflow.md` — SDF → mesh → headless Cycles → post, as validation.
- `references/flat-logo-visible-nucleus.md` — nucleus-last draw order, outward-bowing arms.
- `references/reference-to-flat-logo.md` — measured (not described) raster → vector; glass variant.
- `references/logo-exploration-library.md` — brief, material recipe, checker, subagents, board, rounds.
- `references/node-graph-marks.md` — node/synapse/graph language that reads tasteful, collision set.
- `references/wordmark-lockups.md` — symbol chosen → logotype directions and lockups.
- `references/mark-animation.md` — animating the approved mark; frame-diff verification.
- `references/brand-manual-pdf.md` — guide PDF that applies its own rules; raster contrast sweep.
- `references/social-covers-from-brand-guide.md` — banners/avatars/OG via HTML + Chromium, numeric checks.
- `references/small-business-mockup-set.md` — 3 layouts from one script; tracing/hand-building letterforms.
- `scripts/verificar_lockup.py` — structural verification of lockup SVGs.
- `scripts/verificar_alineacion.py` — measured optical alignment and margins of lockup PNGs.

Origen: abstraída de una skill interna de identidad visual y assets SVG (2026-11).
