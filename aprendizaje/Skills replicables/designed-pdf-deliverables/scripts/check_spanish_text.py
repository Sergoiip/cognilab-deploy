#!/usr/bin/env python3
"""Audit authored prose for contamination before delivering it.

The PDF sweep only covers rendered documents. Chat replies and outreach
messages ship straight to a reader, and they carry the same defects:
CJK/Cyrillic fragments, untranslated foreign words, internal note markers
and invisible control characters.

Run this on a candidate text file, not on memory. Claiming a check that
never ran is worse than shipping the fragment.

Usage:
    python3 check_spanish_text.py draft.txt
    cat draft.txt | python3 check_spanish_text.py -
    python3 check_spanish_text.py draft.txt --words-file foreign.txt --markers-file markers.txt

--words-file / --markers-file: one entry per line ('#' comments allowed). Words
are matched as whole words (case-insensitive); markers as substrings. Use
--extend to add to the defaults instead of replacing them. Exit code 1 on any problem.
"""
import argparse
import re
import sys
import unicodedata

STRAY_SCRIPT = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0400-\u04ff]")

# Default: English words that leak into Spanish prose. Whole-word match only,
# because substring matching on short tokens hits real Spanish words.
DEFAULT_WORDS = {
    "the", "and", "with", "from", "your", "this", "that", "have", "been",
    "theory", "specifications", "away", "assistance", "workflow", "cloud",
    "less", "learn", "myself", "because", "should", "would", "could",
}

# Working-note markers that leak into finished prose.
DEFAULT_MARKERS = ("_head", "if you", "let me know", "i hope this helps")


def load_list(path):
    with open(path, encoding="utf-8") as fh:
        return [l.strip() for l in fh if l.strip() and not l.lstrip().startswith("#")]


def audit(text, words, markers):
    problems = []

    stray = STRAY_SCRIPT.findall(text)
    if stray:
        problems.append(f"stray non-Latin characters: {sorted(set(stray))}")

    found = {w.lower() for w in re.findall(r"[A-Za-z]+", text)}
    foreign = sorted(found & words)
    if foreign:
        problems.append(f"untranslated words: {foreign}")

    low = text.lower()
    leaked = [m for m in markers if m.lower() in low]
    if leaked:
        problems.append(f"internal note markers: {leaked}")

    control = {
        c for c in text
        if unicodedata.category(c) in ("Cc", "Cf", "Co", "Cn") and c not in "\n\t"
    }
    if control:
        problems.append(f"control/format characters: {sorted(repr(c) for c in control)}")

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit prose for stray scripts, foreign words and note markers.")
    ap.add_argument("src", help="text file, or '-' for stdin")
    ap.add_argument("--words-file", help="foreign words to flag (one per line)")
    ap.add_argument("--markers-file", help="note markers to flag (one per line)")
    ap.add_argument("--extend", action="store_true",
                    help="add file entries to the defaults instead of replacing them")
    a = ap.parse_args()

    words = set(DEFAULT_WORDS)
    markers = list(DEFAULT_MARKERS)
    if a.words_file:
        extra = {w.lower() for w in load_list(a.words_file)}
        words = (words | extra) if a.extend else extra
    if a.markers_file:
        extra = load_list(a.markers_file)
        markers = (markers + extra) if a.extend else extra

    if a.src == "-":
        text = sys.stdin.read()
    else:
        with open(a.src, encoding="utf-8") as fh:
            text = fh.read()

    problems = audit(text, words, markers)
    print(f"chars: {len(text)}  words: {len(text.split())}")
    if problems:
        print("FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("OK   clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
