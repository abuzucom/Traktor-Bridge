#!/usr/bin/env python3
"""Heuristically flag likely committed secrets."""
import re
import sys
from pathlib import Path

PATTERNS = [
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[ops]_[0-9A-Za-z]{36,}\b"),
    re.compile(r"\bgithub_pat_[0-9A-Za-z_]{22,}\b"),
    re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)PRIVATE KEY-----"),
]


def find_violations(text: str, path: str) -> list[str]:
    """Return likely secret violations."""
    violations = []
    if Path(path).name in {".env", ".env.local"}:
        violations.append(f"{path}: file must not be committed")
    for number, line in enumerate(text.splitlines(), start=1):
        if any(pattern.search(line) for pattern in PATTERNS):
            violations.append(f"{path}:{number}: likely secret token")
    return violations


def main() -> int:
    violations = []
    for path in sys.argv[1:]:
        violations.extend(find_violations(Path(path).read_text(encoding="utf-8", errors="ignore"), path))
    for message in violations:
        print(message, file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
