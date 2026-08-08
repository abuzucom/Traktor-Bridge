#!/usr/bin/env python3
"""Check GitHub Actions checkout steps for credential persistence."""
import re
import sys
from pathlib import Path


def find_violations(text: str, path: str) -> list[str]:
    """Return checkout steps missing the required setting."""
    lines = text.splitlines()
    violations = []
    for index, line in enumerate(lines):
        if not re.search(r"uses:\s*actions/checkout@", line):
            continue
        indent = len(line) - len(line.lstrip())
        block = [line]
        for next_line in lines[index + 1:]:
            if next_line.strip() and len(next_line) - len(next_line.lstrip()) <= indent:
                break
            block.append(next_line)
        joined = "\n".join(block)
        if not re.search(r"persist-credentials:\s*false\b", joined):
            violations.append(f"{path}:{index + 1}: checkout needs persist-credentials: false")
    return violations


def main() -> int:
    paths = sys.argv[1:]
    violations = []
    for path in paths:
        violations.extend(find_violations(Path(path).read_text(encoding="utf-8"), path))
    for message in violations:
        print(message, file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
