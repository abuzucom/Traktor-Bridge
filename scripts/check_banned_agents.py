#!/usr/bin/env python3
"""Flag banned-agent authorship in a pull request commit range."""
import argparse
import os
import re
import subprocess
import sys

DENYLIST = ("grok", "xai")
TRAILER = re.compile(r"^Co-authored-by:\s*(?P<name>[^<]*)<(?P<email>[^>]+)>", re.MULTILINE)


def is_banned(name: str, email: str) -> bool:
    """Return whether a name or email matches the denylist."""
    value = f"{name} {email}".lower()
    return any(re.search(rf"\b{re.escape(term)}\b", value) for term in DENYLIST) or value.endswith("@x.ai")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()
    result = subprocess.run(
        ["git", "log", f"{args.base}..{args.head}", "--format=%H%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%B%x1e"],
        capture_output=True,
        text=True,
        check=True,
    )
    violations = []
    for record in result.stdout.split("\x1e"):
        fields = record.strip("\n").split("\x1f", 5)
        if len(fields) != 6:
            continue
        sha, author, author_email, committer, committer_email, body = fields
        for role, name, email in (("author", author, author_email), ("committer", committer, committer_email)):
            if is_banned(name, email):
                violations.append(f"{sha[:12]}: banned-agent {role}")
        for match in TRAILER.finditer(body):
            if is_banned(match.group("name"), match.group("email")):
                violations.append(f"{sha[:12]}: banned-agent co-author")
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    if event_path:
        import json

        with open(event_path, encoding="utf-8") as handle:
            login = json.load(handle).get("pull_request", {}).get("user", {}).get("login", "")
        if is_banned(login, ""):
            violations.append("PR author: banned-agent login")
    for message in violations:
        print(message, file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
