# Production integration and document assembly

## Boundary with diagram-design

1. Find `diagram-design` in the current session's skill catalog. If its path no longer exists, discover it under known skill/plugin roots with `rg --files --hidden … -g SKILL.md`. Do not hardcode versions or home directories in the skill. With multiple installations, prefer the active catalog match and record ambiguity.
2. Read its actual `SKILL.md`, chosen type reference, and needed style, export, and verification instructions. Apply the selected [diagram theme](diagram-theme.md) and its no-pause instructions instead of the producer's default styling and onboarding. Carry forward explicit user overrides, size, and output decisions. Do not substitute remembered guidance.
3. Pass the [figure brief](../assets/figure-brief.md): question, message, audience, sources, claims, nodes/edges, states, exact labels, omissions, size, the fixed palette and Noto Sans KR requirements, format, and acceptance criteria. Specify visual treatment of facts, inferences, proposals, and unknowns.
4. Apply the skill in the available environment and collect the produced assets and verification results. A skill may be agent instructions rather than a rendering API. Do not claim integration was verified without actual production, checking, and export.
5. Compare meaning: especially arrow direction, guards, numbers, order, and state after failure. If an omission changes interpretation, fix the figure or brief and verify again.
6. For requested SVG/PNG files, use the installed skill's export helpers and verify the actual font and palette in the output as specified in the theme reference. Report filenames, formats, and unverified areas.

If diagram-design is unavailable or its tools fail, finish the feasible explanation, tables, and brief. Mark requested figures unproduced and explain the needed installation/execution. Do not duplicate the producer or report success. Exact numerical charts follow the plotting workflow in [data](data.md).

## Scale deliverables to the request

Short answers need no files. For shared documents, include Markdown/HTML, requested assets, and traceable sources/briefs. diagram-design's self-contained diagram HTML and this skill's explanation HTML with accompanying asset folders are different deliverables.

## `assemble.py` input contract

[document.json](../assets/document.json) is a runnable minimal example. The agent authors JSON after analyzing evidence. Content is plain text; HTML/Markdown syntax is not evaluated. Adapt authored content to the audience's language.

- Top level: `title`, `language`, `summary`, `sources`, `claims`, `sections`.
- Source: unique `id`, `label`, traceable `location`, identifying `version`, optional `href`.
- Claim: unique `id`, `text`, `kind` (`fact`, `inference`, `proposal`, `unknown`), `source_ids`, `basis`. Facts and inferences require sources; proposals and unknowns may use an empty array. Use `basis` for conditions, reasoning, or why something remains unknown.
- Section: unique `id`, `heading`, `blocks`.
- Block `type`: `paragraph` (`text`), `list` (`items`), `code` (`text`, `language`), `table` (`headers`, `rows`), or `figure` (`path`, `alt`, `caption`, `brief`). Optional `claim_ids` connect adjacent claims.
- Figure: an existing local SVG/PNG. `path` and `brief` are relative paths inside the JSON directory. The brief is Markdown. Meaningful `alt` and `caption` are required. Optional `display_width` is a reviewed width in CSS pixels (64–16384); the default is intrinsic width. Preserve a diagram's original width for 12px labels; a larger chart PNG may use a narrower width after verifying labels and axes. Specify SVG display width as needed. The assembler does not judge meaning or legibility.
- Source `href`: HTTP(S) or a file path relative to the **input JSON**. Local source links are checked and rebased for the output location. They may point to evidence in parent folders; copied assets must stay inside the input directory. Unsafe URL schemes, missing assets, duplicate IDs, unresolved claim/source references, and ragged tables are rejected.
- The `language` tag controls generated document labels: English for `en`/`en-*`, Korean for `ko`/`ko-*`, and English fallback for other tags. It does not translate authored blocks. English templates and separate `.ko` reference templates are provided; choose and adapt them to the requested language.

```bash
python3 <skill-dir>/scripts/assemble.py document.json --out dist
python3 <skill-dir>/scripts/assemble.py document.json --check
```

Outputs: `dist/index.html`, `dist/explanation.md`, `dist/assets/…`, `dist/briefs/…`. The source JSON is preserved. HTML uses escaping and CSP without scripts. Reassembly replaces index.html/explanation.md, so use a dedicated generated folder. Assets use content-hash filenames to avoid collisions. Figures keep their display width inside a local horizontal scroller and fit the page in print. Source links need their evidence files when shared; check the sharing scope.
