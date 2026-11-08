# Generic-icon traps that survive any recolor

Three geometry *families* reliably read as a known UI icon regardless of
palette, stroke count, or how many pieces you split them into. Caught only
by rendering and asking vision_analyze the adversarial question directly
(name the specific icons: spinner, camera/QR frame, checkmark, Chrome,
Pac-Man, power button, crypto diamond) — never by eyeballing the SVG source
yourself.

- **Arcs/rings with gaps** (concentric or not, same radius or different)
  -> loading spinner. True for any number of colors or radii, as long as
  the strokes are curved arcs around a shared center.
- **Corner brackets around a square/rect**, even split into independent
  colored pieces with asymmetric gaps -> camera/QR scan-frame or
  fullscreen-expand icon. Any number of bracket fragments falls into this;
  fragmenting it further does not help, because the trap is "brackets at
  the corners of a rectangle", not "one continuous frame".
- **Two straight strokes converging at a vertex**, even with a gap at the
  vertex and an obtuse/open angle -> checkmark. Color-splitting the two
  strokes does not break the association; only removing the convergent-V
  structure does.
- **N equal-size circles/rings, evenly spaced, overlapping or interlocking**
  -> Olympic rings (N=3-5) or Venn diagram, regardless of gradient/palette or
  whether the overlaps show real over-under occlusion. The ring-count and
  even spacing is the trap, not the color treatment.
- **A single curved arm cloned and rotated at 360/N degrees** (N=3 triskelion,
  N=4 pinwheel, etc.) -> generic "AI tech/crypto" logo, atom icon, or
  yin-yang-with-extra-arm. This reads generic even when each clone gets a
  different gradient — the clone-and-rotate construction itself is the
  signature, visible as perfect rotational symmetry with zero organic
  variation between arms. Breaking it requires genuinely different arm
  geometry (length, curvature, endpoint), not just different per-arm color.

When a symbol needs to avoid the whole UI-icon vocabulary, switch to SOLID
filled silhouettes (no stroke-only linework) — irregular polygons, facets
from an off-center apex, overlapping quadrilaterals. Solids are not the
idiom interface icons use, so they tend to read as a mark rather than a
function affordance. Still run solids through the same adversarial check:
they have their own genre traps (low-poly gem/crypto diamond, Pac-Man,
power button, Chrome's 3-segment circle-from-center).

Practical loop: design concept -> render flat at 512px -> vision_analyze
with the explicit named-icon list -> if it hits a named icon, don't tweak
color/thickness, discard the whole geometry family and try a structurally
different one. Record the discarded attempts and the specific verdict in
the README so the next session doesn't re-try the same trap.
