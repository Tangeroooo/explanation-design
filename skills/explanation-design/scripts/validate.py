#!/usr/bin/env python3
"""Dependency-free package checks, not a YAML parser or semantic quality evaluator."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from assemble import validate


def check(root):
    entry = (root / "SKILL.md").read_text(encoding="utf-8")
    assert entry.startswith("---\n"), "missing frontmatter"
    front, body = entry[4:].split("\n---\n", 1)
    assert re.search(r"^name: explanation-design$", front, re.M), "invalid name"
    assert re.search(r"^description: .+", front, re.M), "missing description"
    assert "[TODO:" not in body, "unfinished scaffold"
    assert len(body.splitlines()) <= 150, "entrypoint is too large; use progressive disclosure"
    for file in [root / "SKILL.md", *root.glob("references/*.md")]:
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            path = (file.parent / unquote(parsed.path)).resolve()
            assert path.is_relative_to(root.resolve()) and path.is_file(), f"broken local reference: {file.name}: {target}"
    validate(json.loads((root / "assets/document.json").read_text(encoding="utf-8")), root / "assets")
    print("Package structure valid (semantic and visual quality not assessed)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        check(args.root)
    except (AssertionError, ValueError, OSError) as exc:
        parser.exit(1, f"Error: {exc}\n")
