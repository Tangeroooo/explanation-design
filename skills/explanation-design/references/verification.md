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

## Record execution and corrections

Solve realistic inputs and evaluate actual outcomes. Matching expected wording with regexes is not behavioral evaluation. Check different request types such as code, design, and data. Record each defect, its cause, and the correction, then rerun the affected case. Ensure the correction generalizes rather than accumulating example-specific rules.

If no visual result was opened, mark it visually unverified. When browser/export tools are unavailable, finish structural and semantic checks and state the actual limits. Syntax checks do not establish explanation or visual quality. For independent evaluation, preserve its inputs, independence, scope, and actual artifacts.
