# Reference image → flat vector logo (measured, not described)

Use when the client likes a raster / AI render of a mark and wants THE LOGO
of it.

## The brief behind it

"A logo is flat but can give an impression of depth" → NOT a 3D render. Never
ship blur filters in the master; make the generator assert
`"feGaussianBlur" not in svg` for logo variants. Glow/scanlines belong only to a
separate, labeled presentation piece.

## Geometry: measure pixels, never redraw from a vision description

1. Mask: brightness threshold + opening + largest component + closing.
2. Rotation center (for an N-fold mark): grid search minimizing
   `|P - roll(P, 360°/N)|` on the polar-unwrapped mask. Symmetrize by averaging
   the N rotations (> 0.5).
3. Polar unwrap from the center; per angle read ink intervals → inner edge I(φ)
   and outer edge O(φ) of ONE arm; inner spiral edges from peaks of a
   symmetrized edge map.
4. Build the arm from (I, O), rotate N times, then VERIFY: IoU vs symmetrized
   mask, IoU of the negative-space holes, and outer-contour radius per angle vs
   the reference. Fix by reading the per-angle diff table (it pinpoints dents
   like "−10.7 px at φ=8°"), not by eyeballing. Reachable: IoU ≈ 0.99, contour
   error < 1 px mean.

## Flat depth construction (cyclic over/under)

- Split each arm into pieces: root (under the previous arm + under the center
  orb), main, tail (under the next arm). Draw order: all tails → all roots →
  all mains → orb. Overlap piece ranges a few degrees; straight cuts with the
  same `userSpaceOnUse` gradient → invisible joins.
- A separator line (stroke of the over-piece in background ink) is clipped ONLY
  to the OTHER arms' under-pieces. Clipping to every under-piece draws a seam
  across each arm at its own cuts ("tears").
- A "sinking" gradient on under-pieces must start at opacity 0 EXACTLY at the
  covering piece's boundary; starting earlier leaves a luminance step = seam.
- Everything under the orb gets ONE radial darkening (clipped to the arms) so
  all sides match.
- Start roots far enough under the orb that no background sliver shows; check
  with a geometric mask: background px in the ring r ∈ (R, 1.3R) must be 0.
- Simplify polygons (shapely `simplify` ≈ 0.18 units at a 1000 viewBox): file
  size drops ~4×; verify changed pixels are edge-only.

## Glass / glassmorphism version (still an SVG logo)

- Keep the SATURATED brand fill as the body; add glass cues on top: thin light
  rim, white lens top + TONAL dark bottom, a crisp thin specular line,
  see-through at crossings, a diffuse glow hugging the shape. A milky veil +
  blurred backdrop + tint dropped mean saturation 0.64 → 0.42 and read as
  "cheap filter". Measure mean saturation inside the shape vs the flat master;
  ablate layer by layer to find the culprit (a glow drawn OVER the arms was the
  biggest — draw glows behind).
- See-through at a crossing: the backdrop contains only diffuse light + the
  under-piece in ITS OWN visible color. A sharp copy of all arms in the
  backdrop kills contrast. An under-piece that ENDS under the glass reads as a
  blob — accept it as a subtle cue.
- `clip-path` on a group with stacked layers leaks the bottom layer at the
  clip's antialiased edge (1 px dark line at cuts). Fix: `opacity="0.9999"` on
  the clipped group. Verify with a luminance sweep along arm midlines at the
  cut angles; compare Chromium vs rsvg.
- The vision reviewer plateaus at ~5–6/10 and starts asking for refraction/
  volume — i.e. a render. That contradicts the logo brief: stop and let the
  client choose the dial.

## Vision reviews are noisy

Scores swing several points on near-identical files, and asymmetries get
reported in exact rotational constructions. Use the reviewer to find candidate
defects, confirm each numerically (luminance sweep for seams, ring gap count,
per-angle contour diff), then change geometry. Crop zooms at COMPUTED feature
coordinates, not guessed ones.

## Deliverables that worked

Master color (dark bg) + transparent, mono light, mono dark-on-white,
small-size icon variant (thicker separators, larger orb), optional volume
variant, presentation piece; PNG exports; the scripts + measured profile; a
README with the verification table and discarded routes. Prove
reproducibility: rerun the chain from scratch and diff outputs byte-for-byte.
