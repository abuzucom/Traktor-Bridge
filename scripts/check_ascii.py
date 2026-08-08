#!/usr/bin/env python3
"""Check given files for non-ASCII prose and dash punctuation."""
import re
import sys
from pathlib import Path

INLINE_CODE = re.compile(r"`[^`]*`")
DASH_SUBSTITUTE = re.compile(r" -{1,3} ")
EM_EN_DASH = re.compile(r"[–—]")


def find_violations(text: str, path: str) -> list[str]:
    """Return style violations in the given prose file."""
    violations = []
    in_fence = False
    for number, raw in enumerate(text.splitlines(), start=1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        prose = INLINE_CODE.sub("", raw)
        if EM_EN_DASH.search(prose):
            violations.append(f"{path}:{number}: em/en dash character")
        if DASH_SUBSTITUTE.search(prose):
            violations.append(f"{path}:{number}: spaced hyphen used as punctuation")
        if any(ord(char) > 127 for char in prose):
            violations.append(f"{path}:{number}: non-ASCII character in prose")
    return violations


def main() -> int:
    """Check each supplied file."""
    paths = sys.argv[1:]
    if not paths:
        print("usage: check_ascii.py FILE [FILE ...]", file=sys.stderr)
        return 1
    violations = []
    for path in paths:
        violations.extend(find_violations(Path(path).read_text(encoding="utf-8"), path))
    for message in violations:
        print(message, file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
