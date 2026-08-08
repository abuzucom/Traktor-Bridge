#!/usr/bin/env python3
"""Warn about common British spellings in prose."""
import re
import sys
from pathlib import Path

WORDS = {
    "colour": "color", "behaviour": "behavior", "favour": "favor", "honour": "honor",
    "labour": "labor", "neighbour": "neighbor", "organise": "organize", "optimise": "optimize",
    "realise": "realize", "recognise": "recognize", "analyse": "analyze", "authorise": "authorize",
    "organisation": "organization", "centre": "center", "metre": "meter", "litre": "liter",
    "licence": "license", "defence": "defense", "offence": "offense", "catalogue": "catalog",
    "dialogue": "dialog", "programme": "program", "jewellery": "jewelry",
}
PATTERN = re.compile(r"\b(" + "|".join(sorted(WORDS, key=len, reverse=True)) + r")\b", re.I)


def main() -> int:
    for path in sys.argv[1:]:
        in_fence = False
        for number, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
            if raw.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in PATTERN.finditer(re.sub(r"`[^`]*`", "", raw)):
                word = match.group(1).lower()
                print(f"warning: {path}:{number}: use '{WORDS[word]}' instead of '{match.group(1)}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
