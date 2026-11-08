# Flat logo with a visible central nucleus

When a mark has a central sphere (hub, keystone, cell body) with ribbons/arms
growing out of it, the nucleus is easily buried by the ribbons in the flat SVG.
This covers the structural fix and how the 3D validation maps to it.

## The problem

If all ribbons originate at the exact center and converge at the same point,
they occlude the nucleus by construction. Drawing the nucleus first makes it
worse — it is always covered.

Symptoms in the render:
- the center is a muddy knot where overlaps compress
- the nucleus reads as a bead threaded by tubes, not a source with growth
- the metaphor is lost; the mark reads as a generic trefoil/pinwheel

## The structural fix

### 1. Draw order: nucleus LAST

Later elements paint on top. The nucleus is the last element (after ribbons,
after node dots).

```xml
<!-- ribbons first -->
<path d="..." fill="url(#grad0)"/>
<path d="..." fill="url(#grad1)"/>
<path d="..." fill="url(#grad2)"/>
<!-- nodes on the outer ring -->
<circle cx="..." cy="..." r="..." fill="url(#nodoGrad)"/>
<!-- NUCLEUS LAST -->
<circle cx="..." cy="..." r="..." fill="url(#nucleoGrad)"/>
```

### 2. Ribbons bow outward — a real central void

Place nodes on an OUTER ring (radius 0.5–0.6 of the mark's extent). Each ribbon
is an arc between two nodes on that ring, bowed away from the center, leaving a
physical gap around the nucleus (vault reading: ribs springing from pillars,
converging at the keystone).

```python
R_ANCLA = 0.55
N = {i: (R_ANCLA*cos(radians(a)), R_ANCLA*sin(radians(a)))
     for i, a in enumerate([90, 210, 330])}
for i in range(3):
    a, b = N[i], N[(i+1) % 3]
    p = arc_points(a, b, bow=0.35)  # bow > 0 pushes the arc away from center
```

### 3. Gradient direction follows the form

Per-strand `linearGradient`s (start → end of each ribbon) keep the brand hues
distinct. One global diagonal gradient washes them into a single muddy hue.

## 3D → 2D mapping

1. Validate the form in 3D (`3d-brand-mark-workflow.md`): sphere + tapered
   tubes, smooth-min only between sphere and tubes.
2. Project orthographically (drop z, keep x,y). z is used only for draw order
   and shadow placement in the flat version.
3. Flat SVG: occlusion via draw order (not clip-paths), highlights on the
   upper-left edges (same light as the 3D), soft shadows via `feGaussianBlur`
   on offset duplicates (presentation variant only), nucleus last.

## Pitfalls

- **Nodes too close to center** (ring radius < 0.4): clutter. Use ≥ 0.5.
- **All ribbons the same width**: vary the profile (thicker at nodes, thinner
  mid-arc) to read as growth, not machinery.
- **Nucleus drawn first**: the single most common failure.
- **Radial 3-arm grammar = generic atom/science icon.** Flagged by the
  adversarial reviewer every time; polishing doesn't fix topology. After 3+
  flags, propose a different structure or metaphor.
- **Terminal dots read as electrons**: small white dots at the end of radial
  arms make it an atom. Remove them or integrate them into the tip.
- **Specular highlight on the nucleus breaks flatness**: use a flat radial
  gradient (white → brand hue), no specular, no glow in the master.
- **Arms slide behind the nucleus instead of emanating from it**: arms must
  start INSIDE the nucleus (radius ~0.06–0.08) and taper outward.
