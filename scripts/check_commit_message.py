#!/usr/bin/env python3
"""Enforce the type: description commit subject format."""
import argparse
import re
import subprocess
import sys

SUBJECT = re.compile(r"^(feat|fix|chore|docs|test): \S.*$")


def check_subjects(subjects: list[tuple[str, str]]) -> list[str]:
    """Return commit subject violations."""
    violations = []
    for sha, subject in subjects:
        clean = re.sub(r" \(#\d+\)$", "", subject)
        prefix = f"{sha[:12]}: "
        if not SUBJECT.match(clean):
            violations.append(f"{prefix}subject must start with 'type: description'")
        elif len(clean) > 50:
            violations.append(f"{prefix}subject exceeds 50 characters")
        elif clean.endswith("."):
            violations.append(f"{prefix}subject ends with a period")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()
    result = subprocess.run(
        ["git", "log", f"{args.base}..{args.head}", "--format=%H%x1f%s"],
        capture_output=True,
        text=True,
        check=True,
    )
    subjects = [tuple(line.split("\x1f", 1)) for line in result.stdout.splitlines() if line]
    violations = check_subjects(subjects)
    for message in violations:
        print(message, file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
