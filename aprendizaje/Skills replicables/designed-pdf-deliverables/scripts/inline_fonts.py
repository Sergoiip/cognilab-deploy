#!/usr/bin/env python3
"""Make an HTML file self-contained for online sharing by inlining its fonts.

Every @font-face `src:url(...)` that points at a file is replaced with a
data:<mime>;base64 URI, so the document renders identically with no server,
no network and no sibling font files. Optionally strips @font-face rules for
families the document never uses (--drop), which keeps a brand CSS carrying
many exploratory faces from ballooning the output (e.g. ~800 KB -> ~6 MB).

Usage:
    python3 inline_fonts.py IN.html OUT.html
    python3 inline_fonts.py IN.html OUT.html --base path/to/fonts --drop FamilyA FamilyB

--base resolves a relative url() against that directory (default: the HTML's
own directory). Exit code is non-zero if any `file://` reference survives or a
font file is missing, so this works as a build gate.
"""
import argparse
import base64
import re
import sys
from pathlib import Path

FONT_MIME = {'.ttf': 'font/ttf', '.otf': 'font/otf', '.woff': 'font/woff', '.woff2': 'font/woff2'}


def to_data_uri(path: Path) -> str:
    mime = FONT_MIME.get(path.suffix.lower(), 'application/octet-stream')
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def main() -> int:
    ap = argparse.ArgumentParser(description="Inline @font-face files as data URIs.")
    ap.add_argument('src', help='input HTML')
    ap.add_argument('out', help='output HTML')
    ap.add_argument('--base', help='directory that relative url() paths resolve against')
    ap.add_argument('--drop', nargs='*', default=[],
                    help='font-family names whose @font-face rules should be removed')
    a = ap.parse_args()

    html = Path(a.src).read_text(encoding='utf-8')
    base = Path(a.base).resolve() if a.base else Path(a.src).resolve().parent

    # 1) Drop whole @font-face blocks for families the document never uses.
    for fam in a.drop:
        pat = re.compile(r"@font-face\s*\{[^}]*font-family\s*:\s*['\"]?" + re.escape(fam)
                         + r"['\"]?\s*;[^}]*\}", re.I)
        html, n = pat.subn('', html)
        if n:
            print(f'  dropped {n} @font-face for {fam!r}')

    # 2) Replace every remaining url(...) that resolves to a font file with a data URI.
    missing = []

    def swap(m):
        quote, raw = m.group(1), m.group(2)
        if raw.startswith('data:') or raw.startswith('http'):
            return m.group(0)
        target = raw[7:] if raw.startswith('file://') else raw
        p = Path(target)
        if not p.is_absolute():
            p = base / p
        p = p.resolve()
        if p.suffix.lower() not in FONT_MIME:
            return m.group(0)
        if not p.exists():
            print(f'  !! missing font: {raw}', file=sys.stderr)
            missing.append(raw)
            return m.group(0)
        return "url('" + to_data_uri(p) + "')"

    html = re.sub(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)", swap, html)

    leftovers = re.findall(r"url\(\s*['\"]?file://[^)]*\)", html)
    Path(a.out).write_text(html, encoding='utf-8')
    print(f'{a.out}: {len(html)} bytes, {len(leftovers)} file:// url() left, {len(missing)} missing')
    return 1 if (leftovers or missing) else 0


if __name__ == '__main__':
    sys.exit(main())
