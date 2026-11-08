# Deriving a palette from a moodboard/reference board

When the user shares a reference board (Are.na channel, Pinterest board,
Behance gallery) and asks for colors "from there" — complementary accents,
"the real palette this aesthetic uses", a secondary palette to pair with an
existing brand gradient — the only correct source is the board's actual
images. A color picked from the board's title/description text (an aesthetic name
→ guessing muted sage/beige/grey) is indistinguishable from one you made
up; it will not match what's measured from the real pixels, and a user with
the board open will see the mismatch immediately.

## Fetching the board

`web_extract` / `web_search` on a moodboard URL typically returns nothing
useful (JS-rendered grids, or a JSON API endpoint with no readable markdown).
Go straight to the platform's API.

**Are.na v3 API:**

```
GET https://api.are.na/v3/channels/<slug>                      # metadata, counts, _links
GET https://api.are.na/v3/channels/<slug>/contents?page=N&per=40   # paginated blocks
```

Two things that break a naive fetch:

- **`urllib.request` gets a 403** that `curl` does not. Use `terminal("curl -s
  -o /tmp/out.json '<url>'")` and read the file, not Python's stdlib HTTP
  client.
- **The JSON contains raw control characters** inside string fields (notably
  long-form `description.markdown` blocks) that break `json.loads` with
  `Invalid control character at: line 1 column N`. Strip them before parsing:

  ```python
  import re, json
  raw = open('/tmp/out.json', 'rb').read().decode('utf-8', errors='replace')
  clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw)
  d = json.loads(clean)
  ```

- Paginate with `meta.total_pages` / `meta.has_more_pages`; a few hundred
  blocks (5-10 pages) is enough for a stable dominant-color sample, pulling
  all 1000+ is wasted time.
- Each `Image` block's `image.small.src` or `image.src` (original, on
  cloudfront) is a normal URL — fetch it with `urllib.request` directly for
  the per-image download (only the channel-listing endpoint needed curl).
- Some displayed/imgix URLs in the JSON look truncated in printed output
  (`https://images.are.na/eyJidW...sfX0=`) — that is the execution sandbox's
  own display redaction of a long base64-looking token, not a real truncation
  in the data. The in-memory string is the full signed URL and downloads fine;
  don't try to "fix" or reconstruct it.

## Extracting dominant color per image

```python
import io, urllib.request
from PIL import Image

def fetch_img(url, size=(60, 60)):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=15).read()
    return Image.open(io.BytesIO(data)).convert('RGB').resize(size)

def dominant_color(im, n=3):
    pal_im = im.resize((40, 40)).convert('P', palette=Image.ADAPTIVE, colors=n)
    pal = pal_im.getpalette()
    counts = pal_im.getcolors()
    idx = sorted(counts, reverse=True)[0][1]
    return tuple(pal[idx*3:idx*3+3])
```

Run this over 40-60 sampled images (one per block is plenty — do not over-crop
or hand-tune per-image; the point is a population of real colors, not a
perfect per-image read).

## Matching board colors to an existing brand palette (complementary pairing)

Convert both the brand's gradient stops and the board's sampled dominant
colors to HSV. For each brand color, its complement target hue is `(h + 0.5) %
1.0`; rank board candidates by hue distance to that target, after filtering
out near-black/near-white/low-saturation samples (background, skin tone
highlights, blown-out whites) that would never read as an intentional accent:

```python
import colorsys

def hsv(rgb):
    r, g, b = (c / 255 for c in rgb)
    return colorsys.rgb_to_hsv(r, g, b)

def hue_dist(h1, h2):
    d = abs(h1 - h2) % 1.0
    return min(d, 1 - d)

candidates = [rgb for rgb in sampled_colors
              if 0.15 <= hsv(rgb)[1] <= 0.85 and 0.12 <= hsv(rgb)[2] <= 0.92]

for name, brand_rgb in brand_palette.items():
    bh, _, _ = hsv(brand_rgb)
    target = (bh + 0.5) % 1.0
    best = min(candidates, key=lambda c: hue_dist(hsv(c)[0], target))
    # best is a real, measured color from the board — not invented
```

The saturation/value filter matters as much as the hue match: an unfiltered
nearest-hue search returns near-black or near-white "colors" constantly
(shadows, blown highlights), which are technically close in hue but useless
as a named accent swatch.

## When the new palette replaces a previous one

If an earlier muted/desaturated palette gets rejected as "too flat, doesn't
contrast", don't just lower the mood further — the board-measured candidates
naturally carry more saturation than a hand-guessed "muted" set (they come
from real photography, which has contrast and grain, not from someone
imagining what "muted" should look like), so re-deriving from real pixels
often solves the contrast complaint by itself.
