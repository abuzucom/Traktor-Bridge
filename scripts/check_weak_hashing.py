#!/usr/bin/env python3
"""Flag unjustified MD5 and SHA-1 calls."""
import re
import sys
from pathlib import Path

HASH_CALL = re.compile(r"hashlib\.(?:md5|sha1)\s*\(|\b(?:md5|sha1)\s*\(", re.I)


def find_violations(text: str, path: str) -> list[str]:
    """Return hash calls without same-line justification comments."""
    violations = []
    for number, line in enumerate(text.splitlines(), start=1):
        for match in HASH_CALL.finditer(line):
            tail = line[match.end():]
            if "#" not in tail and "//" not in tail:
                violations.append(f"{path}:{number}: unjustified MD5/SHA-1 call")
    return violations


def main() -> int:
    violations = []
    for path in sys.argv[1:]:
        violations.extend(find_violations(Path(path).read_text(encoding="utf-8"), path))
    for message in violations:
        print(message, file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
