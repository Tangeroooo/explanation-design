# Verification and improvement

Do not claim more than a check actually establishes.

| Layer | Check | Evidence |
|---|---|---|
| Structural | Frontmatter, references, JSON, assets, links, exports | Commands run and their outcomes |
| Evidence and meaning | Claims and sources, causality, execution, constraints, failures, prose/table/figure agreement | Inspected locations, calculations, scenarios, corrections |
| Visual | Actual renders: clipping, overlaps, fonts, directions, axes, legibility, narrow screens | PNG/HTML actually viewed, viewport, observed defects |

## Quality questions

- Does the opening answer the main question? Can the reader explain the conclusion and its limits afterward?
- Are important claims traceable to evidence? Are facts, inferences, proposals, and unknowns distinct?
- Is the connection from input to processing, state change, and outcome justified?
- Are constraints, failures, and counterexamples that could change the result included?
- Does the representation help? Is a short question being overproduced?
- Do figure edges, order, units, and scope match the prose? Do omissions distort guarantees?

## Review meaning before scaling production

For a figure series, produce and inspect a representative structural view and, if needed, a flow or failure view before applying the vocabulary to the full set. Use existing user preferences; this is a verification step, not a new approval requirement. Finish by checking the whole delivered set for consistent names, symbols, scale, and the defect classes found in the representative views.

Trace a concrete example through each consequential diagram. Check implied claims as well as labels: an arrow can invent order, two aligned paths can imply exclusive routing, containment can invent ownership, and bars can falsely imply disjoint budgets. Follow runtime arguments and instance identities when verifying ownership; shared helper calls or symbol counts do not prove that two processes write the same object. Check the scope of words such as “always,” “only,” and “all.” A coherent explanation of why a design exists is still an inference unless evidence supports it.

Inspect actual output at its intended display size: reading order, endpoints, crossings, clipped labels, font glyphs, contrast, and comparable text scale across different renderers. Geometry checks can catch defects but do not prove that the picture communicates its intended meaning. Do not weaken a check just to make a broken figure pass; examine false positives and the rendered artifact separately.

## Keep corrections connected to delivered artifacts

When a claim or term changes, follow it through prose/table → authoritative figure source or generator → SVG/PNG/export → document reference → published bytes or view, where applicable. Edit the source and regenerate its outputs; do not leave a hand-patched generated file that will revert on the next run. Search all affected representations for the retired claim and review replacements in context: one vague word may have referred to different concepts.

Use hashes or regeneration comparisons when stale outputs are a realistic risk. These establish artifact agreement, not factual correctness or visibility. An upload receipt, HTTP 200, or image-reference count does not prove that readers see an image: check actual file type and decoding, and inspect the published surface when available. Report source/render agreement, uploaded-byte agreement, and end-user display as separate checks. Preserve editable sources and their asset mapping for later revisions.

## Record execution and corrections

Solve realistic inputs and evaluate actual outcomes. Matching expected wording with regexes is not behavioral evaluation. Check different request types such as code, design, and data. Record each defect, its cause, and the correction, then rerun the affected case. Ensure the correction generalizes rather than accumulating example-specific rules.

If no visual result was opened, mark it visually unverified. When browser/export tools are unavailable, finish structural and semantic checks and state the actual limits. Syntax checks do not establish explanation or visual quality. For independent evaluation, preserve its inputs, independence, scope, and actual artifacts.
