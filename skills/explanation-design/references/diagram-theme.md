# Fixed diagram theme

Use this light, role-based palette for new figures. It carries forward the reference guide's pale fills, colored outlines, neutral scaffolding, and consistent roles across views. The theme is already selected; it is not an onboarding question. A later explicit user style request can override it.

## Proceed without style questions

- Do not ask the user to choose a theme, supply a brand URL or tokens, keep defaults, load/save a profile, or approve a style preview. Do not wait for confirmation of diagram type, size, or the rendering plan; choose from the reader's question and intended display size, state consequential assumptions, and proceed.
- Pass this reference as the selected style and standing instruction to `diagram-design`. It replaces the producer's default palette, mixed font families, style-onboarding gate, profile-save offers, and pre-drawing confirmation pause. Continue to use its layout, export, and verification guidance.
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

## Typography and export

Use **Noto Sans KR** for all visible diagram text: titles, node names, identifiers, edge labels, legends, and captions, in both Korean and Latin scripts. Use weight and size for hierarchy (regular 400, emphasis 700), not different font families. Set `font-family: "Noto Sans KR", sans-serif` in HTML/SVG and the equivalent actual font in plotting tools. The fallback is for resilience, not evidence that the requested font rendered.

Load the font before measuring labels, laying out, or exporting; measure and wrap with the same font and weight used in the output. Inspect actual rendered fonts and Korean/Latin glyphs rather than accepting a CSS declaration alone. For portable SVG/HTML, embed or package the font as permitted by the output format and license; keep editable text sources when outlining glyphs. For PNG, verify the font before rasterization. If font loading or embedding fails, report that limitation and do not claim font verification passed or silently substitute the producer's default fonts.
