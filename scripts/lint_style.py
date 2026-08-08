#!/usr/bin/env python3
"""Check the canonical instruction file for dash and ASCII style."""
import re
import sys
from pathlib import Path

SOURCE = "AGENTS.md"
INLINE_CODE = re.compile(r"`[^`]*`")
DASH_SUBSTITUTE = re.compile(r" -{1,3} ")
EM_EN_DASH = re.compile(r"[–—]")


def strip_code(line: str) -> str:
    """Remove inline code spans before checking prose."""
    return INLINE_CODE.sub("", line)


def find_violations(text: str) -> list[str]:
    """Return style violations in the source instruction file."""
    violations = []
    in_fence = False
    for number, raw in enumerate(text.splitlines(), start=1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        prose = strip_code(raw)
        if EM_EN_DASH.search(prose):
            violations.append(f"{SOURCE}:{number}: em/en dash character")
        if DASH_SUBSTITUTE.search(prose):
            violations.append(f"{SOURCE}:{number}: spaced hyphen used as punctuation")
        if any(ord(char) > 127 for char in prose):
            violations.append(f"{SOURCE}:{number}: non-ASCII character in prose")
    return violations


def lint() -> int:
    """Lint the source document and return its status."""
    root = Path(__file__).resolve().parent.parent
    source = root / SOURCE
    if not source.is_file():
        print(f"error: {SOURCE} not found at {root}", file=sys.stderr)
        return 1
    violations = find_violations(source.read_text(encoding="utf-8"))
    if violations:
        for message in violations:
            print(message, file=sys.stderr)
        return 1
    print("style clean")
    return 0


if __name__ == "__main__":
    sys.exit(lint())
