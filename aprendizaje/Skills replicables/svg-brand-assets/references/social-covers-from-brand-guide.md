# Social covers / avatars / OG images from a brand guide (HTML → Chromium PNG)

Use when asked to "update the logos and covers on the networks" and a brand
guide already defines the identity.

## Procedure

1. **Read the guide and the brand folder's index first.** Check the covers and
   social-templates folders: if they are empty or marked "to produce", the
   client's "I already have them" means the guide, not finished files. Produce
   the covers per the guide instead of asking again, then show them.
2. **Snapshot the CURRENT channel art** (avatar, banner — via API where
   available) so the redesign starts from the real state and can be reverted.
3. **One HTML, one piece per size.** Copy the approved logo SVG variant (e.g.
   the hero variant on dark) + the font file next to one `portadas.html`. One
   `.pieza` per size, shown with `:target`; render each with:
   ```bash
   chromium --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
     --force-device-scale-factor=1 --allow-file-access-from-files \
     --virtual-time-budget=4000 --window-size=W,H \
     --screenshot=out.png "file://$PWD/portadas.html#id"
   ```
   Typical sizes: YouTube banner 2560×1440, avatar 1080×1080, social/OG 1200×630.
4. **Depth recipe that reads professional on dark:** layered radial light from
   the palette hues, a large blurred halo directly behind the logo (alpha ~0.6
   or it is invisible), decorative elements only at the periphery,
   scanlines/vignette within the guide's texture budget — all UNDER the logo.
5. **Verify with numbers, not only vision:** PIL/numpy bbox of pixels above a
   brightness threshold → margins L/R/T/B (centered within a few px); banner
   content inside the 1546×423 centered safe crop; avatar max content radius /
   half-canvas ≤ ~60 % plus a circular-crop simulation at 160/98/48 px. Vision
   models misjudge centering and halo strength; measure, then fix.
6. **Re-render after every CSS fix and confirm the replacement applied** (grep
   the HTML). A silent no-op `str.replace` looks like "the reviewer is wrong".
7. Save finals + source into the brand folder and update its README table.
   **Do not publish to profiles until the client approves.**

## Decoration density (node networks, spheres, etc.)

- Too dense (10+ elements, mid nodes, dots, glows on lines, pulses) reads as
  "overloaded"; too sparse and loose (floating elements with a few edge nodes)
  reads as wasted. What landed: few hero elements (banner ~6, social ~4) as the
  ONLY nodes, joined by thin low-opacity lines, no line glow, no dots/pulses,
  lines fading before the logo, wide negative space.
- When asked to "use/expand" an element better, change its **role** (e.g.
  spheres become the network's hubs) rather than adding more. When told
  "overloaded", cut element TYPES, not just opacity.
- Generate the decoration from a seeded script that injects SVG between HTML
  comment markers, with a keep-out ellipse around the logo and hard edge
  margins; pick the best of several hundred seeds by quadrant weight balance
  plus left/right count. Keep earlier versions in `_v1/`, `_v2/`.
- Vision models invent defects (cut-off nodes, uneven weight). Check border
  brightness (max in the outer 4 px < node core brightness ⇒ nothing cut) and
  left/right bright-pixel counts numerically before reacting.
- Orphan elements (a node with no edge) read as errors: connect every hub to its
  nearest neighbour.

Tools: PIL/numpy may not be in the system Python; use `{{PYTHON_CON_DEPS}}` (a
permanent venv), not an ad-hoc install.
