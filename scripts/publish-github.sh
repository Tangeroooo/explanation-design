#!/usr/bin/env bash
# No force push, resets, automatic merges, or replacement of existing history.
set -euo pipefail
export GH_HOST=github.com
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"
target=Tangeroooo/explanation-design
remote_url=https://github.com/Tangeroooo/explanation-design.git
python_bin=${PYTHON:-python3}
for tool in git gh "$python_bin"; do command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 1; }; done
"$python_bin" scripts/check.py
account=$(gh api user --jq .login)
if [[ "$account" != Tangeroooo ]]; then
  echo "Expected authenticated GitHub account Tangeroooo; got $account. Switch gh account and retry." >&2
  exit 1
fi
if [[ ! -d .git ]]; then
  echo "Initialize this checkout and integrate any existing remote history before publishing." >&2
  exit 1
fi
if ! git diff --cached --quiet; then
  echo "Existing staged changes found. Review and commit or unstage them before running this script." >&2
  exit 1
fi
if git remote get-url origin >/dev/null 2>&1; then
  actual=$(git remote get-url origin)
  case "$actual" in
    "$remote_url"|https://github.com/Tangeroooo/explanation-design|git@github.com:Tangeroooo/explanation-design.git) ;;
    *) echo "Refusing unexpected origin: $actual" >&2; exit 1 ;;
  esac
  push_actual=$(git remote get-url --push --all origin)
  [[ "$push_actual" == "$actual" ]] || { echo "Separate push URL found; inspect it manually." >&2; exit 1; }
else
  git remote add origin "$remote_url"
fi
[[ $(git branch --show-current) == main ]] || { echo "Expected branch main; switch and integrate changes first." >&2; exit 1; }
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
if gh api "repos/$target" >"$scratch/repo.json" 2>"$scratch/error"; then
  exists=yes
else
  # Only an explicit HTTP 404, after successful account validation, can mean absent.
  if ! "$python_bin" -c 'import pathlib,sys; sys.exit("(HTTP 404)" not in pathlib.Path(sys.argv[1]).read_text())' "$scratch/error"; then
    cat "$scratch/error" >&2
    echo "Repository lookup failed; no creation attempted." >&2
    exit 1
  fi
  gh api 'user/repos?affiliation=owner&per_page=100' --paginate --jq '.[].full_name' >"$scratch/owned"
  if "$python_bin" -c 'import pathlib,sys; sys.exit(sys.argv[2] not in pathlib.Path(sys.argv[1]).read_text().splitlines())' "$scratch/owned" "$target"; then
    echo "Repository is listed but lookup failed; no creation attempted." >&2
    exit 1
  fi
  exists=no
fi
if [[ "$exists" == yes ]]; then
  branch=$("$python_bin" -c 'import json,sys; print(json.load(open(sys.argv[1]))["default_branch"])' "$scratch/repo.json")
  [[ "$branch" == main ]] || { echo "Remote default branch differs: $branch. Integrate explicitly." >&2; exit 1; }
  git fetch origin
  git ls-remote --heads origin >"$scratch/heads"
  if [[ -s "$scratch/heads" ]]; then
    git show-ref --verify --quiet refs/remotes/origin/main || { echo "Remote has history but no main. Integrate explicitly." >&2; exit 1; }
    git rev-parse --verify HEAD >/dev/null 2>&1 || { echo "Remote history exists. Clone it and copy reviewed files there." >&2; exit 1; }
    git merge-base --is-ancestor origin/main HEAD || { echo "Remote has commits not in HEAD. Fetch and integrate; no automatic rewrite attempted." >&2; exit 1; }
  fi
fi
# Stage only this project's deliverables, preserving all other files.
git add -- .gitignore README.md README.ko.md requirements-dev.txt skills examples evals scripts tests .github
git diff --cached --check
if ! git diff --cached --quiet; then
  git commit -m "Implement and validate evidence-based explanation-design skill"
fi
git rev-parse --verify HEAD >/dev/null
if [[ "$exists" == no ]]; then
  gh repo create "$target" --public
else
  visibility=$("$python_bin" -c 'import json,sys; print(json.load(open(sys.argv[1]))["visibility"])' "$scratch/repo.json")
  if [[ "$visibility" != public ]]; then
    gh repo edit "$target" --visibility public --accept-visibility-change-consequences
  fi
fi
git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u origin main
gh api "repos/$target" --jq '{full_name, visibility, html_url}'
