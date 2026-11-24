# explanation-design

English | [Korean](README.ko.md)

An agent skill for explaining code, documents, designs, and data so readers can understand behavior, conditions, and choices. Works with Claude Code and Codex.

The workflow is reader question → evidence and claims → causes and execution flow → appropriate representation → semantic and visual verification. Answer short questions in chat; produce Markdown, HTML, source records, and figure briefs when useful. The skill does not assume a particular language, database, or product.

Default instructions, references, templates, and UI metadata are in English. Korean reference editions are preserved as [SKILL.ko.md](skills/explanation-design/SKILL.ko.md), `references/*.ko.md`, `assets/*.ko.*`, and `agents/openai.ko.yaml`. Only `SKILL.md` and `agents/openai.yaml` are the default entry points. Explanations still follow the user's requested language; instruction language does not force English answers.

## Installation

### npx skills

The actual help output and Codex/Claude Code installation were verified with `skills` CLI **1.9.0** on **2026-11-24** using Node.js 22.22.1. Check the [official CLI](https://github.com/vercel-labs/skills) for current Node.js requirements and options.

Install for both agents from your target project:

```bash
npx skills add Tangeroooo/explanation-design --skill explanation-design --agent codex claude-code
```

Add `--global` to install across projects. To pin the verified CLI version, use `npx skills@1.9.0 …`. Installation can update an existing copy; preserve any local skill edits first.

```bash
# Install from a local checkout
npx skills add ./explanation-design --skill explanation-design --agent codex claude-code

# Inspect installations / update
npx skills list --agent codex claude-code
npx skills update explanation-design
```

The verified CLI installs project skills under `.agents/skills/` for Codex and `.claude/skills/` for Claude Code. See the [official agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) for global paths. Start a new session if an agent has not picked up a new installation.

### Copy without the CLI

Clone the repository, then run these commands **from your target project**. Replace `/path/to/explanation-design` with the actual checkout. Each copy stops if its destination exists; compare existing changes before replacing a copy.

```bash
mkdir -p .agents/skills .claude/skills
test ! -e .agents/skills/explanation-design && cp -R /path/to/explanation-design/skills/explanation-design .agents/skills/
test ! -e .claude/skills/explanation-design && cp -R /path/to/explanation-design/skills/explanation-design .claude/skills/
```

## Usage

Use `$explanation-design` in Codex or `/explanation-design` in Claude Code with a request, or ask naturally for an explanation task.

```text
$explanation-design Read this function and explain what state remains after
failure or cancellation. Separate inferences from unknowns.

$explanation-design Compare realistic designs under these constraints.
Explain the contracts to preserve, data/control flow, change points,
and conditions that would change your recommendation.

$explanation-design Calculate overall and within-group differences in this data.
Check units and samples. If a chart helps, preserve the original data
and reproducible plotting code.
```

Respond in the user's language. There is no fixed number of sections, figures, or output files. Adapt the English or Korean templates to the reader's language.

## Responsibilities with diagram-design

explanation-design owns evidence investigation, claims, explanation order, representation choice, figure briefs, semantic verification, and document assembly. For diagram layout, style, visual verification, and SVG/PNG export, read and apply the **separately installed diagram-design** skill. Do not hardcode its path or version or duplicate its renderer.

If diagram-design is unavailable, complete the explanation, tables, and brief and mark requested figures unproduced. Short explanations without diagrams do not require it. Exact quantitative charts use original data and standard plotting tools such as Matplotlib, not image-generation models.

Actual integration example: [production brief](examples/code/figures/brief.md) → [diagram HTML](examples/code/figures/delivery-flow.html) → [SVG](examples/code/figures/delivery-flow.svg) / [PNG](examples/code/figures/delivery-flow.png) → [assembled explanation HTML](examples/code/output/index.html).

## Applied examples

These are synthetic fixtures for explanation and evaluation, not verification of production systems. The original examples and evaluation records are in Korean and demonstrate output in the reader's language.

| Case | Question and main judgment | Artifacts |
|---|---|---|
| Code | State after send/ack failures; external effects versus call success | [Markdown](examples/code/output/explanation.md), [HTML](examples/code/output/index.html), [input](examples/code/input/worker.py) |
| Design | Local queue, DB job table, or broker under recovery-after-acceptance constraints | [Markdown](examples/design/output/explanation.md), [HTML](examples/design/output/index.html), [requirements](examples/design/input/requirements.md) |
| Data | Falling within-group error rates but rising overall rate as workload mix changes | [Markdown](examples/data/output/document/explanation.md), [HTML](examples/data/output/document/index.html), [source](examples/data/input/cohorts.csv), [plotting code](examples/data/analyze.py) |
| Additional code evaluation | Cancellation after a cache update, cleanup failure, stale overwrite by concurrent requests | [input](evals/holdout/input/cache.py), [independent explanation](evals/independent/holdout.md) |

The [evaluation report](evals/report.md) separates structural, evidence/semantic, and visual verification, corrections, rechecks, and unverified areas. [Evaluation inputs](evals/cases.json) and a [rubric](evals/rubric.md) are included.

## Document assembly and verification

The core tools use only the **Python 3.10+ standard library**. The assembler packages authored plain-text blocks and assets; it does not assess evidence or explanation quality.

```bash
python3 skills/explanation-design/scripts/assemble.py examples/code/document.json --out build/code
python3 skills/explanation-design/scripts/assemble.py examples/design/document.json --out build/design
python3 skills/explanation-design/scripts/assemble.py examples/data/document.json --out build/data
python3 scripts/check.py
```

Share `index.html` with its accompanying `assets/` and `briefs/` folders. See the [input example](skills/explanation-design/assets/document.json) and [contract](skills/explanation-design/references/rendering.md). diagram-design's self-contained diagram HTML and the explanation document have different packaging.

The input `language` controls generated document labels: English for `en`/`en-*`, Korean for `ko`/`ko-*`, and English fallback for other tags. Authored content is preserved, not translated. The [Korean sample](skills/explanation-design/assets/document.ko.json) is available separately.

Install optional development dependencies only for chart regeneration, the official skill validator, or browser inspection:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python examples/data/analyze.py --plot
.venv/bin/python -m playwright install chromium
.venv/bin/python scripts/review_visuals.py --out build/visual-review
```

Browser checks inspect page overflow, broken images/links, and SVG text bounds and save screenshots. A person or agent must still open those screenshots for visual review. `scripts/check.py` and CI do not establish semantic or visual quality.

## Structure and maintenance

```text
skills/explanation-design/
  SKILL.md                 # Default English workflow and routing
  SKILL.ko.md              # Korean reference edition
  references/              # Read selectively; *.ko.md editions alongside
  assets/                  # Explanation/figure templates and JSON samples
  scripts/                 # Structural checks and mechanical assembly
  agents/openai.yaml       # Default English Codex UI metadata
  agents/openai.ko.yaml    # Preserved Korean metadata for reference
examples/                  # Raw evidence, explanations, actual figures, calculations
evals/                     # Evaluation inputs, independent runs, verification report
tests/                     # Assembly, calculation, failure-path, publishing checks
```

When instructions change, apply them to relevant requests and inspect the outcome. Keep English and Korean reference editions aligned. When sources change, recheck claims and versions/hashes in document.json and regenerate assembled outputs. File existence and syntax alone are insufficient verification.

## Publish to GitHub

The target is the public repository `Tangeroooo/explanation-design`.

```bash
gh auth status
bash scripts/publish-github.sh
```

The script checks the account, origin, branch, existing history, and required tests before committing and pushing. Authentication and network failures are not interpreted as repository absence. Creation requires an explicit 404 plus a successful owned-repository listing; existing repositories are checked for public visibility. It never force-pushes, resets, or automatically merges. If the remote is ahead or diverged, changes are preserved and the script stops for explicit integration. Existing staged changes also cause it to stop for review.
