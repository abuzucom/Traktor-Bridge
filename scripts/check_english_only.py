#!/usr/bin/env python3
"""Warn about likely non-English prose using a small stopword heuristic."""
import re
import sys
from pathlib import Path

ENGLISH = {"the", "is", "and", "of", "to", "in", "that", "it", "for", "on", "with", "as", "this", "a", "or", "but", "if", "from", "by", "at"}
FOREIGN = {"el", "la", "de", "que", "una", "para", "con", "las", "los", "por", "le", "des", "une", "est", "dans", "avec", "pas", "pour", "der", "die", "das", "und", "ist", "nicht", "mit"}


def main() -> int:
    for path in sys.argv[1:]:
        in_fence = False
        for number, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
            if raw.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            words = re.findall(r"\b[a-z]+\b", raw.lower())
            if len(words) < 4:
                continue
            foreign_hits = sum(word in FOREIGN for word in words)
            english_hits = sum(word in ENGLISH for word in words)
            if foreign_hits >= 2 and english_hits == 0:
                print(f"warning: {path}:{number}: likely non-English prose")
    return 0


if __name__ == "__main__":
    sys.exit(main())
