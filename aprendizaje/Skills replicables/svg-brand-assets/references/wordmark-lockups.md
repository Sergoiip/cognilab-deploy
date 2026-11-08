# Wordmark + lockup directions (symbol chosen -> logotype)

Use once the user has picked the symbol and asks for the full logotype (symbol + name).
Next step after the user picks a direction is the brand manual remaster — ask for the pick
before touching the manual.

## Procedure

1. **Read what the brand already fixed.** Brand note/manual typography section (e.g. a fixed
   family, weight and tracking) and look at the ORIGINAL wordmark with vision (case, weight,
   tracking, gradient). One of the directions should stay close to it.
2. **Pick 3 directions that differ in several dimensions at once** — letter construction, width,
   case, and lockup arrangement — not three fonts in the same setup. A set that worked:
   - Geometric heavy caps (Outfit Black 900), horizontal, optical-center alignment — closest to
     an original heavy geometric wordmark.
   - Wide heavy lowercase, tight tracking (Unbounded Black 900), horizontal, word baseline resting
     on the symbol's foot — the expressive/retro option; word may continue the symbol gradient.
   - Mono ExtraBold caps tracked +0.10 (JetBrains Mono), stacked with tagline — continuity with an
     existing manual/brochure; institutional.
3. **Fonts locally, licensed.** Download OFL fonts from the google/fonts GitHub mirror
   (`https://github.com/google/fonts/raw/main/ofl/<family>/<Family>%5Bwght%5D.ttf` + `OFL.txt`),
   then pin a static weight with `fontTools.varLib.instancer.instantiateVariableFont(tt, {'wght': 900})`.
   Keep the OFL license next to the fonts and state "commercial use allowed" in the board.
4. **Text -> outlines with real kerning.** Shape with HarfBuzz (`pip install uharfbuzz`;
   `hb.shape(font, buf, {'kern': True})`), draw each glyph with fontTools `SVGPathPen` through a
   `TransformPen(esc,0,0,-esc,x,y)` (mirror y), add tracking as `tracking_em*upm` between glyphs.
   Scale by cap height (`OS/2.sCapHeight`, fallback: bounds of 'H'). Never ship `<text>`.
5. **Quick specimen first.** Symbol + name in 6-9 font/case/tracking combos on one sheet; pick the
   3 directions from it before building full lockups.
6. **Size by measured stem weight.** Measure the wordmark stem (bbox width of 'l') at the candidate
   cap height and compare with the symbol's stroke at lockup scale; aim for ~0.8-0.95 of the symbol
   stroke. Wide faces read heavier than their stem number — check visually after.
7. **Unit x = symbol stroke width at lockup scale.** Symbol-text gap ~0.7-0.9 x; clear space = x on
   all sides; stacked gaps equal (symbol->name = name->tagline).
8. **Vertical alignment:** caps block centered at ~0.51 of symbol height (slightly below geometric
   center); a baseline "resting on the L foot" must be raised ~7% of symbol height or it reads as
   sinking (round foot vs flat baseline).
9. **Variants per direction:** one-ink light, one-ink dark, `{{TEXTURA_PRESENTACION}}` (symbol SVG nested with
   prefixed ids + viewBox padded so the halo is not cut). Stacked-with-tagline needs a
   `sin-lema` variant: the tagline dies below ~40 px; rule = no tagline in nav/small sizes.
10. **Comparison board (Compare surface):** per direction: hero on dark (presentation variant), one ink on dark
    and on light, a nav-bar mock at ~30 px, and real sizes 40/24/16 px. Symbol family (main + node
    variants) in the header. Uniquify ids per inlined SVG copy. Verify in Chromium: 0 console errors,
    0 duplicate ids, 0 horizontal overflow at 390 px.

## Pitfalls

- Vision reviewers invent spacing numbers ("6-8 px gap") — measure the shapely distance between
  symbol geometry and text bbox before changing anything.
- Contact-sheet panel padding is not a lockup defect; check the SVG's own viewBox/margins.
- Gradient text fill: put the gradient in userSpaceOnUse across the word's x span, not objectBoundingBox,
  so it continues the symbol's palette instead of restarting.
