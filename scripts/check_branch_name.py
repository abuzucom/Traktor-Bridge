#!/usr/bin/env python3
"""Enforce the <type>/<kebab-description> branch convention."""
import argparse
import os
import re
import subprocess
import sys

PREFIXES = ("feat", "fix", "chore", "docs", "test")
EXEMPT = ("main", "master", "HEAD")


def check_branch(branch: str, prefixes=PREFIXES) -> list[str]:
    """Return violations for a branch name."""
    if not branch or branch in EXEMPT:
        return []
    pattern = rf"^(?:{'|'.join(prefixes)})/[a-z0-9]+(?:-[a-z0-9]+)*$"
    if re.fullmatch(pattern, branch):
        return []
    return [f"branch '{branch}' does not match <type>/<kebab-description>"]


def current_branch() -> str:
    """Return the CI head branch or checked-out branch."""
    if os.environ.get("GITHUB_HEAD_REF"):
        return os.environ["GITHUB_HEAD_REF"]
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("branch", nargs="?", default=current_branch())
    args = parser.parse_args()
    violations = check_branch(args.branch)
    for message in violations:
        print(message, file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
