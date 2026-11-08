#!/usr/bin/env python3
"""Per-page text audit for a generated PDF.

Catches the defect classes that silently survive into a rendered PDF:
  1. Stray CJK / Cyrillic / Hangul characters in authored prose.
  2. Orphan pages - a page holding a handful of characters because the previous
     page's content overflowed.
  3. (warning) Hints of untranslated words or missing accents.

Usage:
    python3 check_pdf_text.py OUT.pdf [--orphan-chars 200] [--hints-file hints.txt]

--hints-file: one substring per line (blank lines and '#' comments ignored) that
replaces the default hint list. Exit code 1 on stray characters or orphan pages.
"""
import argparse
import re
import sys

# CJK, Hiragana/Katakana, Hangul, Cyrillic
STRAY = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0400-\u04ff]")

# Default hints for a Spanish document: common English leaks + unaccented words.
DEFAULT_HINTS = (
    "the ", " and ", " with ", " your ", " theory", "specifications",
    "workflow", "cloud", "note:", "segun", "unico", "OPCION",
)


def load_hints(path):
    with open(path, encoding="utf-8") as fh:
        return tuple(l.rstrip("\n") for l in fh if l.strip() and not l.lstrip().startswith("#"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Per-page text audit for a generated PDF.")
    ap.add_argument("pdf")
    ap.add_argument("--orphan-chars", type=int, default=200,
                    help="flag a page with fewer characters than this as an orphan")
    ap.add_argument("--hints-file", help="file with substrings to warn about (one per line)")
    args = ap.parse_args()

    try:
        from pypdf import PdfReader
    except ImportError:
        print("Missing dependency: pypdf (install it in a venv: pip install pypdf)", file=sys.stderr)
        return 2

    hints = load_hints(args.hints_file) if args.hints_file else DEFAULT_HINTS

    reader = PdfReader(args.pdf)
    pages = [(p.extract_text() or "") for p in reader.pages]

    print(f"pages: {len(pages)}\n")
    orphans = []
    for i, text in enumerate(pages, 1):
        n = len(text.strip())
        head = text.strip()[:60].replace("\n", " ")
        flag = ""
        if n < args.orphan_chars:
            flag = "  <-- ORPHAN?"
            orphans.append(i)
        print(f"  page {i:>3}: {n:>6} chars | {head}{flag}")

    print()
    strays = STRAY.findall("".join(pages))
    if strays:
        print(f"FAIL stray non-Latin characters: {''.join(sorted(set(strays)))!r}")
    else:
        print("OK   no stray non-Latin characters")

    joined = " ".join(pages)
    hits = [w for w in hints if w in joined]
    if hits:
        print(f"WARN possible untranslated words / missing accents: {hits}")

    if orphans:
        print(f"FAIL orphan pages: {orphans} - tighten padding or spacing in the HTML")
    return 1 if (strays or orphans) else 0


if __name__ == "__main__":
    sys.exit(main())
