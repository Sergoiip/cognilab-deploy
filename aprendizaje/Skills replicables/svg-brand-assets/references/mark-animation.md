# Animating an existing brand mark (SVG / CSS)

Use when the approved mark must be animated — a draw-on intro, a breathing/live logo, an
activity indicator — as a web asset (HTML/CSS/SVG) or as a source for video.

## 0. Read the geometry from the approved SVG; never retype it

- The approved SVG is the single source of truth. The generator script should `re.search`
  the `d` attributes out of it and inject them, so a hand-copy error becomes impossible.
  Assert `d_used == d_source` at generation time.
- **A `<path>` `d` can hold several subpaths.** `re.findall(r'[Mm][^Mm]+', d)` lists them.
  A monogram path is frequently the letter outline PLUS a cut-out as a second subpath;
  copying only the first half silently drops part of the mark (a two-letter monogram loses
  a whole letter). Never eyeball-copy a `d` string.
- **The node of a monogram is often a HOLE in the outer path (an evenodd subpath) plus a
  separate luminous orb element.** Do NOT `clip-path` the orb to the outer path — the orb
  lives inside the hole, so clipping it erases it. Paint the orb's shapes directly, on top,
  unclipped. (Symptom of getting this wrong: the orb vanishes and the still no longer
  matches the approved source, with no error.)

## 1. To move a metaball node's lobes independently, rebuild it as circles + a gooey filter

- A baked node path cannot have its lobes moved — you can only scale/rotate it whole. To
  animate the lobes (rotating, extending, breathing) rebuild the node as N overlapping
  `<circle>`s inside a `filter` that does `feGaussianBlur` then `feColorMatrix` alpha
  contrast (the "goo" recipe). The liquid necks then reform as the circles move, which is
  exactly the metaball behaviour the mark already has.
- **Calibrate the circles against the real node before animating.** Render the candidate
  circle set to a mask, compute IoU against the node's own mask, and search the parameters
  (coarse grid, then coordinate descent or Powell). Hub + 4 lobes reaches 98%+ IoU. Store
  the calibrated params in the generator; never eyeball the radii/positions.
- Paint the node body and the bright orb from the SAME circle set (two passes: gradient
  body, then the light orb) so they stay in register while animating.
- Keep the goo filter's `feColorMatrix` alpha constants in the generator too — they set how
  fused the lobes look and are as load-bearing as the positions.
- **Giving every lobe the same keyframe/rotation reads as a rigid disc spinning, not a living
  node — users reject it outright ("no me convence") even though nothing is technically
  broken.** A single shared `transform:rotate()` keyframe applied to all lobes around one
  center preserves their relative angles, so it looks like one solid wheel turning, the
  opposite of organic. Animate each lobe independently instead: translate it along ITS OWN
  radial vector from the node center (`ux,uy = normalize(lobe_pos - center)`), with its own
  duration, delay and amplitude (stagger these, e.g. 2.3-3.1s durations with 0-1s delays) so
  the lobes extend/retract like separate organic parts breathing out of phase, never in
  lockstep. Verify the asynchrony by sampling each lobe's screen position at several instants
  and confirming they do not all move the same direction/amount at the same time — a
  synchronized-looking diff is the same bug by another measurement.

## 2. Draw-on: measure the path length, never guess it

- `stroke-dasharray` / `stroke-dashoffset` for a draw-on must equal the real path length.
  Get it in the browser: `document.querySelector('#path').getTotalLength()`. A guessed
  value draws the stroke only partway (guessed 1400 against a real 1851 = a stroke that
  never closes).
- Sequence the intro as separate animations with delays: outline draws → fill fades in →
  node buds → node goes live. Not one keyframe chain; each stage is independently tunable.

## 3. Verify the animation actually ran, AND that the still frame still matches

- **Frame-diff.** Capture the render at two instants and diff the pixels; every panel that
  should move must show changed rows. Zero change = dead animation (bad selector, filter,
  or `animation-name`), and a build log will not tell you.
- **Compare the at-rest frame against the approved source** by IoU, or assert the injected
  path equals the source path. An animated mark that no longer matches the approved still
  is a different mark.
- **Production rule: an intro animation runs ONCE on entry.** Only an "activity"
  indicator loops. Never ship an infinite loop as the default.

## Pitfalls

- Rotating lobes: set `transform-origin` in the SAME user units as the geometry (e.g.
  `352.75px 283.2px`), not a percentage — a percentage origin drifts with the element box.
- Weaving `<use href="#id">` across separate `<svg>` blocks works in-browser, but keep the
  `<defs>` in one block and assert each `use`'s rendered bbox is non-zero (`getBBox()`).
- Reference a node's centroid from the measured mask (centroid of the ink), not the
  geometric middle of the viewBox.
