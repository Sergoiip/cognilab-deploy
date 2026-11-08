# 3D brand mark workflow — SDF to Blender to post (validation only)

**The 3D render is a VALIDATION tool, not the deliverable.** A physically
rendered mark that passes every check gets rejected with "a logo doesn't look
like that — that's a render; a logo is flat but can give an impression of
depth." Use the render to validate form, occlusion and material, then project
to a flat SVG with simulated depth (`flat-logo-visible-nucleus.md`).

Worked example (generic): three tapered ribbons growing from a central sphere,
woven over/under in a trefoil, soft-3D/glass material, a three-hue brand
gradient on a near-black ground.

## 1. Parametrize in numpy

Each strand is a 3D centerline through polar control points `(dθ, r, z)`
relative to a base direction (90°, 210°, 330° for 3-fold symmetry):

```python
def catmull(pts, n=900, alpha=0.5):
    # centripetal Catmull-Rom, resampled by arc length
    ...

def profile(s, keys):
    # smoothstep interpolation of width w(s) from (s, value) keys
    ...
```

Width profile: thick at the head (s≈0.4–0.5), tapering to a thin tail
(s→1.0). Root ≈ 0.20·R, head ≈ 0.24·R, tail ≈ 0.04·R.

## 2. Build the SDF

```python
vox = 0.0065; ext = 1.14; zext = 0.42
xs = np.arange(-ext, ext+vox, vox, dtype=np.float32)
zs = np.arange(-zext, zext+vox, vox, dtype=np.float32)
X, Y, Z = np.meshgrid(xs, xs, zs, indexing="ij")
P = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
f = v["flat"]  # ~0.60 — flatten factor for the tube cross-section
d_soma = np.linalg.norm(P - [0, 0, soma_z], axis=1) - soma_r
D = np.full(len(P), 9.0, np.float32)
for st in strands:
    C = st["C"].copy(); C[:, 2] /= f
    rho = st["w"] / 2
    tree = cKDTree(C)
    Q = P.copy(); Q[:, 2] /= f
    dist, idx = tree.query(Q[sel], k=10, distance_upper_bound=rho.max()+0.12)
    dk = np.where(np.isfinite(dist), dist - rho[idx], 9.0).min(1)
    D = np.minimum(D, smin(dk, d_soma, v["fillet"]))  # fillet <= 0.05
D = np.minimum(D, d_soma)
```

`smin(a, b, k)` with small k blends strand roots into the sphere organically;
strand↔strand stays a hard `min` so crossings remain crisp.

## 3. Measure crossings before rendering (shapely)

```python
from shapely.geometry import LineString
for a in range(3):
    for b in range(a+1, 3):
        la, lb = LineString(A["C"][:, :2]), LineString(B["C"][:, :2])
        for g in la.intersection(lb).geoms:
            ia = np.argmin(np.linalg.norm(A["C"][:, :2] - [g.x, g.y], axis=1))
            ib = np.argmin(np.linalg.norm(B["C"][:, :2] - [g.x, g.y], axis=1))
            za, zb = A["C"][ia, 2], B["C"][ib, 2]
            need = v["flat"] * (A["w"][ia] + B["w"][ib]) / 2
            assert abs(za - zb) > need, f"crossing too tight: {abs(za-zb)} vs {need}"
```

## 4. Export mesh with attributes

```python
from skimage.measure import marching_cubes
verts, faces, normals, _ = marching_cubes(D, level=0.0, spacing=(vox,)*3)
verts = taubin(verts, faces)  # 10 iters, λ=0.5, μ=−0.53 (no shrinkage)
np.savez_compressed("mesh.npz", verts=verts, faces=faces, s=s_attr, k=k_attr, soma=soma_w)
```

Per-vertex attributes: `s` (position along strand), `k` (strand id), `soma`
(proximity weight for color blending).

## 5. Blender render (headless, Cycles GPU)

Launch with a clean environment — Blender launched from a Python process that
has `PYTHONPATH`/`PYTHONHOME`/`VIRTUAL_ENV` set fails with
`No module named 'math'` / `_posixsubprocess`:

```bash
env -u PYTHONHOME -u PYTHONPATH -u VIRTUAL_ENV PATH=/usr/local/bin:/usr/bin:/bin \
  blender -b --factory-startup -P render.py -- mesh.npz out
```

Material settings that matter:
- Per-strand color: attribute `(k + s) / 3` → 3-stop ramp of `{{PALETA}}`, the
  middle hue as a narrow bridge (a global object-space ramp washes the palette
  into one muddy middle hue)
- SSS: weight 0.45–0.7, scale 0.14–0.25
- Coat: weight 1.0, roughness 0.16; Sheen: 0.25
- **AO** (`ShaderNodeAmbientOcclusion`, distance 0.18, 16 samples) multiplied
  into base color at 0.55–0.75 — the single most important setting for a woven
  mark; without it crossings read as flat overlapping shapes
- Emission on the sphere: soft (`soma^1.6 * 3.2 + 0.14`), not blown out
- Lighting: large soft key area light upper-left, fill lower-right, two rim
  lights in brand hues from behind
- Film transparent, view transform Standard, 256+ samples, denoise

## 6. Post-process (numpy)

```python
# bloom: threshold 0.9, 3 blur scales (0.6 %, 2 %, 5.5 % of width)
bright = np.clip(prem - 0.9, 0, None)
bloom = 0.55*blur(bright, W*0.006) + 0.35*blur(bright, W*0.02) + 0.22*blur(bright, W*0.055)
# tonemap: soft shoulder at 0.82 to preserve hue in highlights
# optional texture layer: scanlines (6 %, period ≈ H/530), chromatic aberration
#   (1.5 px on high-contrast edges only), vignette, grain
```

## 7. Export variants (of the validation render)

Clean, textured (`{{TEXTURA_PRESENTACION}}`), transparent; size ladder 2048 →
16 px. Then go flat.

## Pitfalls

- **Smooth-min fillet too large** (`k > 0.05`): the sphere fuses into the
  strands and the mark reads as a bead threaded by tubes.
- **Bloom threshold too low** (~0.55) with wide radii bleaches the inner 15–20 %
  of each strand and makes crossings illegible. Threshold 0.9, aura weight
  ~0.25, widest blur 5.5 % of width.
- **Taubin smoothing is mandatory** — raw marching cubes stair-steps at any
  resolution; Laplacian smoothing shrinks the form.
- **The render is not the logo.** See the top of this file.
