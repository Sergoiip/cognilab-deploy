# Logo exploration library — many concepts, one brief, one board

Use when the client wants many options / multiple versions of a mark, wants
to explore the current one AND new directions, or previous rounds kept
iterating one shape. The deliverable is a library of FORM concepts in vector,
compared side by side — not a 3D lab of one shape in many materials.

## Project layout

```
<proyecto>/
  BRIEF.md              # brand, aesthetic, palette+gradient, REJECTED, collisions, rules, format
  RECETA-MATERIAL.md    # one material recipe applied identically to every concept
  referencia/           # current mark (split into named pieces), approved material SVG,
                        # client refs, copy of {{LIBRERIA_REGLAS_LOGO}}
  herramientas/         # render.mjs  chequeo.py  construir.py  plantilla.html
  conceptos/<id>/       # <id>-forma.svg, <id>-material.svg, meta.json, generar.py
  conceptos/_flujo/     # iteration engines + out/ contact sheets ("_" = builder ignores)
  conceptos/_descartados/  # rejected variants, kept as provenance
  png/                  # <id>-forma-512/64/32/16.png, <id>-material-512.png
  Biblioteca de isotipos {{NOMBRE_MARCA}}.html   # built board
```

## First round (breadth)

1. **Write BRIEF.md from the notes, not from memory.** Confirmed aesthetic,
   palette hex + gradient stops, claim, rejected directions WITH reason (so no
   subagent re-proposes them), a named collision list, and the design rules.
   Rules worth copying verbatim from `{{LIBRERIA_REGLAS_LOGO}}`: ≤ 2 core
   elements / ≤ 6 shapes, ≥ 40 % negative space, intentional asymmetry, rounded
   negative cutouts, structural mass (no 2–3 thin lines), must read at
   16–32 px, one explainable narrative per concept.
2. **Write RECETA-MATERIAL.md once** (layer order, gradient coordinates,
   opacities, what is forbidden in the symbol). Every concept applies the same
   recipe, so the board compares FORM.
3. **Two files per concept:** `-forma.svg` in ONE ink (no gradients/filters) —
   proof the mark exists without effects — and `-material.svg` with the recipe.
   viewBox `0 0 512 512`, no width/height, no `<text>`/`<image>`/external refs,
   no full-canvas opaque rect, every id prefixed `<id>-`.
4. **Gate with a structural checker** (`chequeo.py`): viewBox, no text, no bg
   rect, single ink in forma, size cap, id prefixes, meta.json keys (`idea,
   por_que_encaja_con_la_marca, riesgos, chequeo_colision, legible_16px`). The
   board build skips anything that fails.
5. **Render material SVGs with headless Chromium, not rsvg** (blur/mask/filters
   render as in a browser; transparent bg works): `render.mjs <svg> <png>
   [size] [bg]` plus a strip mode emitting 512/64/32/16 on the brand bg.
6. **Fan out to parallel subagents, 2 concepts each** (~7 tasks = 14
   concepts). Split ~4 exploring the CURRENT mark in other languages and ~10
   genuinely NEW metaphors. Each task: read BRIEF + RECETA, exact ids, the
   concept spec with its own "avoid:" list, the interpreter that has
   PIL/shapely (`{{PYTHON_CON_DEPS}}`), required outputs, and a MANDATORY
   adversarial vision check by name on the 512 material PNG and the 32 px
   one-ink PNG (max 3 correction rounds), writing the REAL verdict into
   meta.json. Forbid touching other ids' files. Require a structured output.
7. **While they run, build the board:** grid grouped "Exploring the current" /
   "New directions", inspector with a big view, real-pixel sizes 128/64/32/16,
   a ~30 px nav usage with the one-ink version, the meta fields. Toggles:
   material vs one ink, dark vs light bg, texture overlay (presentation only).
   Fonts base64-inlined; single HTML file.
8. **Include the current mark as concept `a0`** so every concept is judged
   against it.
9. After subagents return: rebuild, open in Chromium, check the console, and
   verify each concept file yourself — subagent summaries are self-reports.

## Iterating a concept the client picked (depth)

Each client reaction = one round. Do it yourself (no subagents): the taste
signal is in the details. The client may switch to another library concept at
any round — reuse that concept's generator geometry exactly.

1. Retire disliked variants to `conceptos/_descartados/` (and their PNGs) so the
   board only shows live options.
2. Build a parametric engine in `conceptos/_flujo/` that imports the picked
   concept's geometry (don't redraw it).
3. 3 variants per round, each ONE idea, plus a contact sheet: reference row
   (previous pick) + each variant at 512 and 64/32/16 enlarged.
4. Vision-critique the sheet stating each row's intent: does it meet the
   client's words, tasteful vs corporate/crude, concrete defects with clock
   positions, small-size behavior, ranking. Verify defect claims numerically;
   fix; re-sheet once.
5. Package winners with a per-family packaging script (one-ink path + material
   by layers + meta.json + PNG strip), run the checker, rebuild the board,
   check the console.
6. Adversarial collision check by name on the lead variant; write scores into
   meta.json. Node/graph specifics: `node-graph-marks.md`.
7. Deliver: before/after comparison PNG (one-ink row + material row), a ★
   recommendation, collision scores, the small-size limit, and 1–2 concrete
   next moves to choose from — including "consolidate and move on".

## Pitfalls

- **Re-prefix ids per inline copy on the board.** The same SVG is injected
  several times (tile, inspector, size chips); duplicate ids make gradients
  resolve to another copy → wrong colors or invisible marks. Rewrite `id=`,
  `url(#…)`, `href="#…"` with a per-copy prefix in JS.
- **Small-size slots use the one-ink version.** A material render at 30 px is mud.
- **Community logo skills: inspect before installing.** One blocked by a
  security scanner is read for its rules (clone the repo), not force-installed.
- **Vision rate limits (429) on batch verification.** Verify the 3–4 most
  promising concepts first; report exactly which were not visually verified and
  where their collision notes came from.
- **A failed/looping subagent may already have written its files.** Run the
  checker on its ids before re-dispatching. Keep each task under ~10 min.
- **meta.json naming.** Subagents may write `<id>-meta.json`; normalize.
- **Empty paths.** Generators may emit `<path d=""/>`; strip before the checker.
- **Clipped-fill false positive.** A full-canvas rect inside a `clip-path`
  group is a shape fill; strip clipped groups before testing for opaque
  backgrounds. A full-canvas rect inside a `<mask>` still trips the rule — use a
  large circle in masks instead.
- **Variation engines live in `conceptos/_flujo/`**, never in a non-underscore
  folder (the builder treats it as a broken concept). Don't delete generators:
  they are how the next round reproduces the geometry.
