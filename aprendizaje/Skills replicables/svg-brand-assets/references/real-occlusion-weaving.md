# Real occlusion for interlocking/woven marks

For a mark whose concept requires one arm/ribbon/ring visibly passing over
or under another (a trenzado, a knot, a chain, a triquetra), two different
failure modes show up in order: first the geometry doesn't actually cross,
then the occlusion you add looks faked. Both are fixable with real math
instead of eyeballing curves.

## 1. A cloned spiral never crosses its rotated copies — prove it, don't guess

The tempting construction for "3 arms twisting around a center" is: define
one arm as a parametric spiral `r(t) = hub + length*t`, `theta(t) = base_angle
+ twist*ease(t)`, then get the other two arms by rotating `base_angle` by
±120°. This looks like it should eventually self-intersect if `twist` is big
enough. It never does, for any twist value: since every arm shares the exact
same `r(t)` and the exact same `twist*ease(t)` term, the angular difference
between any two arms at matching `t` is just the constant `base_angle`
difference — the twist term cancels out of the *difference*. Two curves with
constant angular separation and identical, monotonic radius cannot occupy the
same Cartesian point.

**Check this numerically before rendering anything**, not after several
failed visual iterations:

```python
def closest_approach(ptsA, ptsB, tmin=0.25):
    bestd = 1e9
    for (xa, ya, ta) in ptsA:
        if ta < tmin: continue
        for (xb, yb, tb) in ptsB:
            if tb < tmin: continue
            d = (xa-xb)**2 + (ya-yb)**2
            bestd = min(bestd, d)
    return bestd**0.5
```

Sweep the twist parameter (e.g. 60° to 180°) and print the minimum distance
for each value. If it stays roughly constant regardless of twist, the arms
are mathematically parallel and no amount of visual tweaking (more curve,
more bulge, more glow) will make them cross — the construction itself rules
it out. Stop iterating on this shape family immediately and switch to one
with a closed-form intersection.

## 2. Circle-circle intersection gives a real, provable crossing

For rings/chain-links/lobes arranged with N-fold symmetry around a shared
center, use literal circle geometry instead of hand-tuned beziers:

```python
def circle_intersections(c1, r1, c2, r2):
    x1, y1 = c1; x2, y2 = c2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    a = (r1**2 - r2**2 + d**2) / (2*d)
    h = math.sqrt(max(r1**2 - a**2, 0))
    xm, ym = x1 + a*dx/d, y1 + a*dy/d
    return (xm + h*dy/d, ym - h*dx/d), (xm - h*dy/d, ym + h*dx/d)
```

Place N circle centers at distance D from the shared center, 360/N degrees
apart, each with radius R. For adjacent circles to overlap away from the
shared center (not swallow it, which bunches all the inner intersection
points into a confusing central blob), pick R and D so that
`0.866*D*sqrt(3)` (roughly, for N=3) `< R < D` — sweep a few (D, R) pairs and
print the distance of each intersection point from the shared center; reject
any configuration where several of those distances cluster below the
tube/stroke width, because that's exactly the "muddy blob in the middle"
failure.

## 3. Alternate over/under like a real chain, not a flat stack

Drawing element 0, then 1, then 2 in sequence gives element 2 on top of
*everything*, which is wrong for a closed 3-element chain (element 0 should
beat element 2 at one of their two crossings, not lose to it everywhere).
Fix with exactly one corrective patch per pair: redraw the element that
should win, clipped to a small circle around ONE of its two crossing points
with that neighbor, after the base draw order. Three elements in a closed
chain need exactly three corrective patches total (one per pair), not one
per crossing point (six).

```python
def clip_patch(element_fn, point, clip_r):
    return (f'<clipPath id="c"><circle cx="{point[0]}" cy="{point[1]}" '
            f'r="{clip_r}"/></clipPath><g clip-path="url(#c)">{element_fn()}</g>')
```

## 4. The clip-path + blur seam

A `feGaussianBlur`-based glow computed on the unclipped shape gets cut off
hard at the clip-path boundary, leaving a visible ring/seam where the glow
should fade smoothly instead. Two mitigations, use both: shrink the blur
radius inside the clipped corrective patch (roughly a third to half of the
blur used on the base unclipped render), and make the clip circle radius
comfortably larger than the stroke/tube width so the hard cutoff lands in
empty space, not through visible ink.

## 5. Even after real occlusion works, check for the Olympic-rings collision

N evenly-spaced, equal-size interlocking circles/rings is itself a known
icon family (see `generic-icon-traps.md`) regardless of how clean the
occlusion is. Getting the geometry right is necessary but not sufficient —
run the adversarial vision_analyze check named in that file before treating
an interlocking-rings concept as finished.
