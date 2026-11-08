#!/usr/bin/env python3
"""Legibility audit of finished PDFs: font size per text fragment, weighted by characters.

Usage:
    python3 pdf_font_audit.py a.pdf [b.pdf ...] [--min-median 11] [--min-size 9]

Prints pages, median size (pt) and the share of text under 9 / 10 / 11 / 12 pt.
Default gate for reading documents: median >= 11 pt and nothing under 9 pt.
Exit code 1 if any PDF fails the gate (use --no-gate to only report).
Uses poppler's pdftohtml (no Python PDF deps). Sizes are read at -zoom 1, i.e. points.
Text inside raster images is not seen (it is illustration, not reading text).
"""
import argparse
import collections
import os
import re
import shutil
import subprocess
import sys
import tempfile


def audit(pdf):
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "out")
        subprocess.run(["pdftohtml", "-xml", "-i", "-q", "-zoom", "1", pdf, base],
                       capture_output=True, check=False)
        xml_path = base + ".xml"
        if not os.path.exists(xml_path):
            raise RuntimeError(f"pdftohtml produced no output for {pdf}")
        with open(xml_path, errors="ignore") as fh:
            x = fh.read()
    fs = {m.group(1): int(m.group(2))
          for m in re.finditer(r'<fontspec id="(\d+)" size="(\d+)"', x)}
    cnt = collections.Counter()
    for m in re.finditer(r'<text[^>]*font="(\d+)"[^>]*>(.*?)</text>', x):
        t = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        cnt[fs.get(m.group(1), 0)] += len(t)
    tot = sum(cnt.values())
    ordered = sorted(cnt.elements())
    med = ordered[len(ordered) // 2] if ordered else 0
    share = (lambda lim: sum(v for k, v in cnt.items() if k < lim) / tot) if tot else (lambda lim: 0.0)
    return x.count('<page '), med, share, tot


def main() -> int:
    ap = argparse.ArgumentParser(description="Font-size legibility audit for PDFs (poppler pdftohtml).")
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--min-median", type=float, default=11, help="minimum median size in pt")
    ap.add_argument("--min-size", type=float, default=9, help="no text fragment below this size (pt)")
    ap.add_argument("--no-gate", action="store_true", help="report only, always exit 0")
    a = ap.parse_args()

    if not shutil.which("pdftohtml"):
        print("Missing dependency: pdftohtml (poppler-utils)", file=sys.stderr)
        return 2

    failed = False
    for p in a.pdfs:
        try:
            pages, med, share, tot = audit(p)
        except RuntimeError as e:
            print(f"ERROR {e}", file=sys.stderr)
            failed = True
            continue
        below = share(a.min_size)
        ok = tot > 0 and med >= a.min_median and below == 0
        failed |= not ok
        print(f"{'OK  ' if ok else 'FAIL'} {os.path.basename(p)[:54]:54} pag={pages:3} med={med}pt "
              f"<9pt={share(9):.0%} <10pt={share(10):.0%} <11pt={share(11):.0%} <12pt={share(12):.0%}")
    return 0 if (a.no_gate or not failed) else 1


if __name__ == "__main__":
    sys.exit(main())
