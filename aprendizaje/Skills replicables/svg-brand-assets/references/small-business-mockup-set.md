# Quick 3-mockup set for a small-business client

Use when a third-party client (shop, small business) is unhappy with their
current logo and you need options to show them fast. Different from the
open-ended exploration library: the client has an existing mark whose palette
and subject must be KEPT, often plus a voice-note brief.

## Procedure

1. **Transcribe the client's voice notes first** (local speech-to-text); list
   the brief (categories, services, palette to keep, contact line) and confirm
   it.
2. **Vision-analyze the current logo, but sample the palette from pixels**, not
   from the client's color words (a client said "metallic blue" while the
   pixels were mint green): PIL, quantize pixels with `max-min > 50`, print the
   top hexes.
3. **Three layouts from ONE script** (`generar_mockups.py`) so a pick can be
   refined by re-running: A emblem/circular (profile photo), B horizontal
   (cover/banner), C full catalog card (logo + categories + service icons +
   contact bar). Same palette, monogram and icons across all three; only
   composition changes.
4. **Category icons** as simple stroke paths in a 100×100 box. Never put
   third-party brand marks in them.
5. **Unknown contact data → an obvious placeholder** (`{{TELEFONO_CONTACTO}}`)
   and say so in the reply.
6. Render with `rsvg-convert`, then vision-check EACH PNG specifically for
   cut-off text, overlaps and missing items. Fix and re-render before showing.

## Keeping the client's own letterforms ("same style as my logo")

When the client likes the SHAPE of their current monogram and wants it in a new
layout, trace the pixels; don't redraw from a vision description (inconsistent
across calls, gives no geometry).

1. Mask each letter by color with numpy (e.g. green: `max>55 & (g-r)>20`;
   silver: `max>50 & (g-r)<18`). Too-high thresholds drop dark metallic
   shading and leave the letter incomplete (an S read as a "5"); sweep
   35/50/65 and keep the lowest that still separates it from neighbours.
2. Crop to the letter's bbox (ImageMagick
   `-morphology Close Disk:2 -define connected-components:verbose=true
   -connected-components 8 null:`), keep only the largest component.
   `keep-top=1` can keep the BACKGROUND component and invert the shape; a small
   pure-Python BFS over the crop is the reliable fallback without scipy.
3. Save as PBM with the letter black, run
   `potrace -s -t 30 -a 1.2 -O 0.6 --flat`, store the SVGs in `assets/` next
   to the generator, and have the generator read their `d` strings (potrace
   coords are px×10, y-up: wrap in `translate(0 H) scale(0.1 -0.1)`).
4. Reuse the letters' ORIGINAL relative offsets/scale; separate overlapping
   letters with a thin background-colored `stroke` and `paint-order="stroke"`
   on the top one.
5. Center decorative elements from the monogram's computed width, then confirm
   with a numpy bbox of the render — trust measured bboxes over vision prose.
6. Tell the client the letters are a raster trace (approximate edges; tiny
   sizes need a simplified variant) and offer a hand-built pass once a
   direction is picked.

## Hand-built letterforms (when the trace looks rough)

- Define glyphs in a 0..100 height box as lists of `("o", pts)` outer pieces and
  `("h", pts)` holes: one stroke width, 45° chamfered corners, pointed
  terminals. Orient outers and holes oppositely and fill nonzero so overlapping
  pieces union cleanly.
- ONE shared slant (e.g. 12°) on every glyph, monogram, wordmark and text, so
  the system reads as one family. Draw only the letters the brand name needs.
- A small per-pair KERN table: angular letters leave optical holes equal
  advances don't fix. Render, look at the gaps, adjust.
- Metal look = vertical gradient with a hard "horizon" stop at ~50 % plus a
  diagonal low-opacity sheen clipped to the glyph.
- Make icon stroke width scale-independent (`sw*100/size` inside the scaled
  group) or small icons end up with thicker lines than large ones.
- Auto-fit the canvas: render once, numpy bbox of pixels with `max>62`, then
  rewrite `width/height/viewBox` and the background rect with equal margins.
  Re-measure each stacked row's center; slanted text drifts off-center by
  `height·tan(slant)/2` unless compensated.

## Pitfalls

- **Python env:** fontTools and PIL may live only in one interpreter; run the
  generator with `{{PYTHON_CON_DEPS}}` consistently.
- **Widths are guessed, so assert them.** A wide wordmark plus category cards
  overflowed the canvas edge and only the vision pass caught it. Have `text()`
  return its width and `assert x + width < W - margin`.
- **Keep an ornament ≥ 30 px clear of the monogram** or it reads as stuck on.
- **Replica / counterfeit merchandise:** keep "replica"-type wording out of
  logos and public banners (platform bans, trademark exposure); tell the
  operator before building social profiles. Product-line tiers belong only on
  internal catalog pieces, if at all.
- Deliver to the client's own project folder (`{{DIR_CLIENTE}}/mockups/`, SVG +
  PNG), not into a personal notes vault, and offer derived variants (round
  avatar, cover, sticker) once the client picks one.
