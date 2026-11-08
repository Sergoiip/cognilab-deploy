# rsvg silent failures

Three ways `rsvg-convert` produces a wrong PNG while reporting success. All
three exit 0, emit no warning, and write a file of plausible size.

Symptom shared by all of them: the PNG looks like a valid render of *part* of
the SVG — usually the wordmark is simply absent, leaving a correct-looking mark
with no text.

## How to recognize the class

`rsvg-convert` returning 0 and a PNG on disk is not evidence of content. Before
believing a render, confirm structurally:

```bash
grep -c '<path' lockup.svg          # path count vs glyph count
grep -o 'viewBox="[^"]*"' lockup.svg
```

Then look at the PNG. If the visual and the exit code disagree with each other,
believe the visual and re-derive whatever metric you trusted.

---

## 1. Bare path data (not a renderer bug — the usual cause)

**Symptom.** Wordmark missing. Everything else renders.

**Mechanism.** `SVGPathPen.getCommands()` returns only drawing commands
(`M308 10Q235 10…`). Emitting that string directly inside a `<g>` makes it
*text content*, not geometry. The parser is correct; the element is not an
element.

**Wrong**

```xml
<g transform="translate(574 0) scale(0.136986)">M308 10Q235 10...</g>
```

**Right**

```xml
<g transform="translate(574 0) scale(0.136986)"><path d="M308 10Q235 10..."/></g>
```

**Detect it** — glifs vs paths must match:

```python
n_glyphs = len(re.findall(r'scale\([\d.]+\)', wm))
n_paths  = wm.count('<path')
assert n_paths >= n_glyphs
```

---

## 2. Decimal width on the root `<svg>`

**Symptom.** Whole groups dropped, intermittently, with no pattern that looks
related to the change you just made.

**Mechanism.** rsvg resolves the root `width` attribute to a surface size. A
decimal value does not land where the transform arithmetic expects, and groups
carrying a `transform` fall outside it.

**Wrong** — `width="1327.42"`

**Right** — `width="1327"`

The `viewBox` may keep its decimals; that is what defines user-space scale:

```xml
<svg viewBox="0 0 1327.42 512" width="1327" height="512">
```

**Reproduction.** Two files, byte-identical except the root width, one with
text and one without.

---

## 3. No opaque background rect

**Symptom.** Text present with a background fill, absent without one. The two
variants look identical in source except for the `<rect>`.

**Mechanism.** Without an opaque rect the viewport is never established, and
groups carrying a `transform` get dropped.

**None of these fix it:**

| Attempt | Result |
| :--- | :--- |
| no rect at all | dropped |
| `<rect fill="none">` | dropped — a rect that paints nothing is not a frame |
| `<rect fill="#000" fill-opacity="0">` | dropped |
| `<rect fill="#ffffff">` | renders |

**Right** — always a real color:

```python
rect = f'<rect width="{W}" height="{H}" fill="{fondo or "#ffffff"}"/>'
```

If a transparent-background variant is genuinely required, rasterize in a
browser or another engine. Do not fight rsvg here.

---

## Why pixel metrics did not catch any of this

Worth stating explicitly, because it is the trap in verifying renders:

- cropping a region and taking `mean` — dominated by the background
- `maxima` on a PNG with no alpha channel — returns 255 for anything
- `-alpha extract` on a PNG without an alpha channel — also returns 255

An entirely empty render measured as healthy by all three. Only `grep -c '<path'`
and looking at the image revealed the problem.

**Rule: assert on the SVG source; look at the PNG. Never on intermediate
brightness numbers.**