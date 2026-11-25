# Fixed diagram theme

Use this light, role-based palette for new figures. It carries forward the reference guide's pale fills, colored outlines, neutral scaffolding, and consistent roles across views. The theme is already selected; it is not an onboarding question. A later explicit user style request can override it.

## Proceed without style questions

- Do not ask the user to choose a theme, supply a brand URL or tokens, keep defaults, load/save a profile, or approve a style preview. Do not wait for confirmation of diagram type, size, or the rendering plan; choose from the reader's question and intended display size, state consequential assumptions, and proceed.
- Pass this reference as the selected style and standing instruction to `diagram-design`. It replaces the producer's default palette and prose typography, style-onboarding gate, profile-save offers, and pre-drawing confirmation pause. Continue to use its layout, export, and verification guidance.
- Apply tokens to the current artifact or a task-local template. Do not edit a shared skill installation or global profile to satisfy its onboarding gate. A discovered saved profile must not silently replace this theme.
- Ask only when missing content, evidence, or an output constraint materially blocks a correct result; do not turn routine visual choices into questions.

## Palette

| Base token | Hex | Use |
|---|---|---|
| Background | `#fbfcfe` | Canvas |
| Surface | `#ffffff` | Plain panels |
| Ink | `#1f2a3c` | Primary text |
| Muted | `#66748a` | Secondary text and neutral edges |
| Faint | `#c9d1dd` | Subordinate boundaries |
| Grid | `#e4e9f0` | Guides and separators |

| Role | Outline / accent | Pale fill |
|---|---|---|
| Producer / write path | `#c46a17` | `#fff4e8` |
| Consumer / read path | `#2462b8` | `#ebf2fd` |
| Coordination / orchestration | `#6a4cc0` | `#f2eefc` |
| Durable object storage | `#0e7c74` | `#e5f5f2` |
| Log / transport | `#3c4a62` | `#eef1f6` |
| Catalog / metadata | `#b83a30` | `#fdeeee` |
| Memory | `#2d8a4a` | `#e9f6ee` |
| Disk | `#7a5a2e` | `#f6efe4` |
| Failure / danger | `#c62f2f` | `#fdecec` |
| Neutral context | `#66748a` | `#f1f4f8` |
| Attention / threshold | `#b07d0a` | `#fff7df` |

Use only the roles needed by the explanation, not every swatch in every figure. For another domain, assign this same palette to a small set of named roles in the brief and keep that mapping across views. Color encodes role identity; stronger outlines or local emphasis direct attention. Do not recolor a whole role merely to meet an accent-node quota. Keep text in Ink unless the actual contrast has been checked. Failure and metadata must also differ by label, symbol, or line style; color alone cannot distinguish them. Preserve shapes and geometry suited to each concept rather than making every object a colored box.

## Visible weight and resolution

Use these defaults **at the intended display size**, overriding thinner producer-template defaults. They are CSS-pixel targets, not PNG pixel counts or unscaled SVG units.

| Element | Default |
|---|---|
| Figure title | 28–32px, weight **700**, Ink |
| Component/section heading | 16–18px, weight **700** |
| Primary relationship/connector | **2–2.5px** stroke |
| Meaningful component/ownership boundary, secondary connector | **1.5–2px** stroke |
| Focused relationship or changed boundary | **3px** stroke, used sparingly |
| Nonessential grid/separator | 0.75–1px; never the sole carrier of a relationship |

Keep arrowheads, dash spacing, ports, and label clearances proportional to the stronger lines. Do not express uncertainty by making an essential edge nearly invisible; use a labeled/dashed edge of readable weight. Preserve role colors and visual hierarchy rather than making all edges equally heavy.

For a uniformly scaled SVG without non-scaling strokes, `displayed_stroke = source_stroke × displayed_width / viewBox_width`. Apply the same scale reasoning to text. Prefer designing at the intended CSS dimensions; if the embed is smaller, adjust the source or layout and verify again. A large viewBox or a sharper PNG does not fix thin strokes or tiny text after downscaling.

Preserve a vector SVG when the destination supports it. For PNG, rasterize from the vector/HTML at **2× the intended display width and height** by default (for example, a 1200×800 display uses a 2400×1600 PNG). Set the embed/display width explicitly; with `assemble.py`, use the figure's `display_width` so high-resolution pixels do not double its layout size. Do not enlarge an existing low-resolution bitmap. Higher export scale improves sampling, not the intended visual weight.

Inspect the final embed at its actual size and the exported pixels. Record viewBox/layout size, display size, raster dimensions, and export scale. Distinguish thin source strokes, excessive downscaling, insufficient raster density, and upload/viewer resampling before choosing a fix. If a small viewport cannot preserve readable labels and lines, simplify/split or provide local scrolling rather than shrinking the entire structure into a thumbnail. Do not claim the user's original image had a resolution problem without inspecting it.

## Typography and export

Choose fonts by text function, not by whether the text is Korean or English.

- **Explanatory text:** use **Noto Sans KR** for titles, prose, ordinary component names, edge descriptions, legends, and captions in either language. Use weight and size for hierarchy (regular 400, emphasis 700). Set `font-family: "Noto Sans KR", sans-serif` in HTML/SVG and the equivalent actual font in plotting tools.
- **Code and literal technical tokens:** use a consistent, available **monospace** font for code blocks, inline code, variable/function/type names, commands, paths, and literal values. Preserve an appropriate project/producer code font; otherwise choose an available monospace font without asking a theme question. Record the family in the brief. Do not replace it with Noto Sans KR or reject it as a theme violation.
- **Mixed labels:** apply monospace only to the literal token; retain Noto Sans KR for surrounding explanation. For example, “Worker pool” is an ordinary component label, while `worker_pool.acquire()` is code. Keep code spelling intact and verify glyph coverage, including Korean comments where present.

A fallback stack is for resilience, not evidence that the intended fonts rendered.

Load both prose and code fonts before measuring labels, laying out, or exporting; measure and wrap each text run with the font and weight actually used in the output. Inspect actual rendered fonts and Korean/Latin glyphs rather than accepting a CSS declaration alone. For portable SVG/HTML, embed or package the font as permitted by the output format and license; keep editable text sources when outlining glyphs. For PNG, verify the font before rasterization. If font loading or embedding fails, report that limitation and do not claim font verification passed or silently substitute fonts across prose and code roles.
