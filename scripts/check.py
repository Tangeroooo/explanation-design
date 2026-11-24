#!/usr/bin/env python3
"""Portable structural checks plus behavioral tooling tests; no visual pass implied."""
import json
import hashlib
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/explanation-design"


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


if __name__ == "__main__":
    run(sys.executable, str(SKILL / "scripts/validate.py"))
    for path in sorted((ROOT / "examples").glob("*/document.json")):
        run(sys.executable, str(SKILL / "scripts/assemble.py"), str(path), "--check")
        for source in json.loads(path.read_text(encoding="utf-8"))["sources"]:
            href = urlsplit(source.get("href", ""))
            if source["version"].startswith("sha256:") and not href.scheme and href.path:
                content = (path.parent / unquote(href.path)).read_bytes()
                expected = "sha256:" + hashlib.sha256(content).hexdigest()
                if source["version"] != expected:
                    raise SystemExit(f"Source changed; recheck claims and update version: {path}: {source['id']}")
    json.loads((ROOT / "evals/cases.json").read_text())
    run("bash", "-n", "scripts/publish-github.sh")
    run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v")
    print("Structural/tooling checks passed; see evals/report.md for semantic and visual results.")
