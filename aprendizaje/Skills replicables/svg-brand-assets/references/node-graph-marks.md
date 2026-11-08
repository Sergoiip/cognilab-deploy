# Node / synapse / graph language inside a mark — tasteful vs corporate

Rules that held up under adversarial review across several rounds with a
client who wanted "interconnected nodes, synapse + cybernetic, everything
emanating from a central idea" without looking corporate or crude. Order = the
order in which that taste resolved. Treat them as strong defaults, and confirm
against your own client's references.

## 1. Never bolt a second graphic system onto the form

- Straight spokes to the center read as a hub-and-spoke stock icon; a
  neighbor mesh reads as a blockchain / neural-net cliché. Random Poisson
  nodes + random edges erase the form (arms lose their curve). All rejected.
- Connections follow the form's own flow: put nodes on curved lanes parallel
  to each arm's medial axis (skeletonize the arm silhouette, spline it, offset
  by a fixed pitch). A fixed hex grid reads as a halftone filter.
- One idea per variant. Extra effects (Y-branches, random synapses, many lanes)
  read as accidental and turn to mush below 64 px.

## 2. The central node: clean shape, visibly the source — never a fused blob

- A gap ring that keeps chains off the core keeps the circle clean but reads as
  "not connected" — rejected when the center must be the source of everything.
- Thick trunks fused into the core with fillets read as crude — rejected.
- What works: a perfect circle (no fusion) with arms leaving its edge almost
  TANGENTLY as strokes with a gentle root flare
  (`width = base_taper + flare·exp(-s/~20)`) that thin outward. Check the
  spines' start angle vs radial first (~75–80° = near tangent, ideal).
- In a material/glass variant: a neutral-white pearl core with a thin rim; a
  tinted pearl edge against differently-hued strokes reads as a seam. Anything
  fusing into the core uses neutral white light fading in opacity, clipped to
  the body, and the pearl fades to transparent instead of ending in a hard disc.

## 3. Clean line language for "organic + cybernetic" (best reception)

- Organic = curved, tapering strokes. Cybernetic = straight, thin,
  CONSTANT-weight links.
- Synapse = every stroke stops a fixed gap (~5 u at 512) before the node it
  reaches. Legible from ~128 px; at 32/16 only the silhouette + core survives —
  say so and plan a small-size variant.
- Few nodes: 3–4 per arm + 1–2 side nodes; sizes step down outward; 1–2 loose
  spark dots after the tip that CONTINUE the spine's curvature (sparks off the
  tangent read as debris).
- Interconnection: one short bridge per arm pair (tip node → nearest side node
  of the next arm). Long bridges cross strokes. Gate in code: links
  intersecting any stroke/core must be 0; bridge clearance > 15 px.
- Hollow-ring ("circuit pad") nodes add nothing below 64 px — skip.

## 4. Gooey / metaball node attached to a glyph (monogram + node)

- Build the node as an SDF: hub disc + satellite discs + waisted necks,
  smooth-min union, contour. Solid, no inner hole.
- Thin pointed necks (waist ≤ 0.5) read as an ink splat. Use thick concave
  necks (waist ~0.8, k ~12) and lobes close to the hub (distance ≈
  `(r_hub + r_lobe)·1.15`) so the node shares the glyph's stroke weight.
- 4 similar lobes read as molecule / virus / paw / flower. Prefer 3 lobes of
  clearly different sizes (cell budding). Bead-chain arms read as a paw print;
  continuous tapering gooey arms read as a mini triskelion.
- Auto-fit every satellite/arm to the free space: walk its distance down until
  disc + air clears the glyph (≥ 18 px) and the canvas margin; for rotational
  arms, scan start angle and scale for max clearance. Trails go only into open
  space; drop dots that don't fit.
- Fade = radial luminance mask centered on the node, built with a large circle
  (not a full-canvas `<rect>`, which the structural checker flags).

### Letter terminal dissolving into a node

- When a client sends a mockup, rebuild it, don't trace it: keep its spirit,
  fix misaligned dots and stray editor artifacts (selection handles, leftover
  icons).
- "Letter dissolves toward a node" = continue the letter's OWN curve past its
  terminal (e.g. a superellipse with radius growing slightly = an opening
  spiral). Beads sit ON that curve with monotonic sizes and steps; the first
  1–2 joined to the terminal by thinning necks (melting), then loose; stop at a
  fixed synapse gap (10–15 u) from the node's receiving lobe.
- Letter character: variable stroke (strong stem, thinning toward the
  terminal), liquid inner fillets (closing +k/−k ~24 u), slightly fuller
  rounded ends.
- Node: hub + 3 asymmetric lobes, one facing the incoming beads; lighter than
  the stroke (hub radius ~0.3× the stem). Trails turn in the SAME rotational
  sense as the incoming curve, or reviewers read a fork. Grid-search the hub
  position for glyph clearance ≥ 24, synapse gap in range, all inside margins.
- Curve-above-dot silhouettes risk a "?" read at 32/16 px: plan a dedicated
  small-size mark.

## 5. Material layers for node/graph marks

- Links at ~0.55–0.62 opacity under the node body; radial luminance mask from
  the core outward (white → ~0.25) for a dying-phosphor fade; colored bloom in
  the brand gradient (screen blend); keep halos out of any gap ring (measured
  ring luminance must equal the background).
- Simplify buffers (6–16 segments) + `simplify(0.12–0.18)`: ~4× smaller files
  with no visible change.

## 6. Collision set and reviewer hygiene

- Name-check every round: three-connected-circles triskelion marks (e.g. the
  pre-2013 Ripple logo), Cardano, Wipro, Trisquel, Razer, the Isle of Man
  triskelion, generic network/neural icon, molecule, virus, spinner, pinwheel,
  galaxy; for monograms also Google G, Pac-Man, Coinbase, Carrefour, Chanel/CK.
- Any three-arms-from-a-center silhouette sits at ~6–7/10 against the closest
  triskelion: report it and recommend a formal trademark search; archetypes
  (pinwheel/galaxy) are vibe echoes, not legal risk.
- Reviewers hallucinate stray slivers, blank 16 px renders, "dashed" links and
  clipping. Verify numerically (piece areas, mean ink per size, clearances)
  before acting.

## Generator modules worth having (by role)

Spines/lanes along the form · SDF bead chains · line-language variant ·
monogram + node · one packaging script per family (one-ink + material +
meta.json + PNG strip). Keep them in the exploration's `_flujo/` folder so the
next round re-uses exact geometry.
