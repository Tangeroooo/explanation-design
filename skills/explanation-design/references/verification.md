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

Inspect actual output at its intended display size: reading order, endpoints, crossings, clipped labels, actual rendering and glyphs of the selected fonts by text role (Noto Sans KR for explanation, monospace for code/literal identifiers, unless explicitly overridden), the selected role palette, contrast, and comparable text scale across different renderers. Geometry checks can catch defects but do not prove that the picture communicates its intended meaning. Do not weaken a check just to make a broken figure pass; examine false positives and the rendered artifact separately.

## Independent diagram review

Use a separate reviewer for a figure series, a complex figure whose layout carries ownership, concurrency, or failure guarantees, or an explicitly requested review. Simple figures can use author checks. Review representative views before scaling production, then the delivered set for cross-view consistency. This is an internal check, not a user approval gate.

When delegation is permitted, use the available agent mechanism with fresh context: do not inherit the producer's conversation, reasoning, self-assessment, or earlier findings. The producer coordinates the review and edits sources; the reviewer inspects and reports without editing, publishing, or spawning more agents. If delegation is disallowed or delegation/image viewing is unavailable, perform feasible author checks and report independent/visual review as unavailable, not passed.

1. **Read the picture first.** Give only the actual rendered images, intended display size, reader question, audience, and captions/context that the reader will see. The reviewer must open the images, not substitute SVG/HTML source inspection. Ask them to record perceived boundaries, ownership, order, identity, failure outcomes, and ambiguities relevant to the question. Do not expose the production brief, source evidence, or expected answer yet. Preserve this first interpretation before the next handoff.
2. **Compare with evidence.** After the first interpretation is returned, give the same reviewer the relevant brief extracts, selected theme and explicit overrides, minimal versioned raw evidence, and available geometry/font/export observations. Withhold author self-assessments and benchmark answer keys. Compare the initial reading with source-supported meaning; inspect the images again where needed. An omitted contract remains unknown. Check the choice of representation and shapes, abstraction boundaries, role colors and emphasis, overview/detail correspondence, and legibility at the intended size. Judge style against the artifact's applicable brief and explicit overrides; distinguish role identity, status, and editorial emphasis before alleging a color mismatch. A code font is not a prose-font violation; check mixed labels by text role. Image inspection alone cannot establish the exact font; use actual rendered-font observations or mark that check unverified.
3. **Return actionable findings.** Each finding includes `ID | artifact/version and visual location | category | what a reader would infer | supporting evidence or missing evidence | impact | smallest correction`. Categories are meaning error, readability defect, requirement mismatch, unverified claim, and optional preference. Meaning errors, unreadable essential content, and unmet explicit requirements block a pass; a taste preference does not. Missing evidence leaves the affected check unverified. List inspected artifacts, tool observations, and unverified areas separately. Do not substitute an overall beauty score for findings or invent issues to fill a quota.
4. **Adjudicate and recheck.** The producer accepts supported findings, explains rejected findings with evidence, and leaves unresolved ones explicit. Fix authoritative sources, regenerate, and give the reviewer updated renders plus the finding dispositions. Recheck fixes, new defects, and affected related views; later rounds are not blind first readings. Allow at most two correction-and-recheck rounds after the initial review. Stop earlier when blockers are resolved. At the limit, report unresolved blockers and do not label the result passed; do not keep polishing or restart with another reviewer to evade the limit. Do not publish a known misleading figure as verified.

Preserve the first interpretation, evidence handoff, findings/dispositions, reviewed artifact versions, round count, and remaining limits with the task's verification record. Separate mechanical checks, independent review, and actual reader comprehension. For a trial, record accepted defects beyond the producer's prior checks, rejected findings, review effort, and regressions when observed; do not claim improvement from reviewer agreement alone. Do not add themes, profile-save questions, or routine approval pauses through the review loop.

For structure/design requests, explicitly test whether a component view exposes responsibilities, interfaces, ownership, and shared resources. Flag a sequence-only answer when it omits these requested relationships, not merely because it uses sequence. Check that different shapes communicate evidenced differences rather than decoration. Inspect title weight, effective connector/boundary widths, raster density, and the final embed at the intended size against the theme. A 2× export with tiny displayed text or hairline edges still fails readability.

## Keep corrections connected to delivered artifacts

When a claim or term changes, follow it through prose/table → authoritative figure source or generator → SVG/PNG/export → document reference → published bytes or view, where applicable. Edit the source and regenerate its outputs; do not leave a hand-patched generated file that will revert on the next run. Search all affected representations for the retired claim and review replacements in context: one vague word may have referred to different concepts.

Use hashes or regeneration comparisons when stale outputs are a realistic risk. These establish artifact agreement, not factual correctness or visibility. An upload receipt, HTTP 200, or image-reference count does not prove that readers see an image: check actual file type and decoding, and inspect the published surface when available. Report source/render agreement, uploaded-byte agreement, and end-user display as separate checks. Preserve editable sources and their asset mapping for later revisions.

## Record execution and corrections

For a substantial explanation, return to the reader's target task and test a small change in condition. Hold other assumptions fixed: move a failure across a publication boundary, change the instance ID passed to a shared helper, or alter usage without changing resource limits. Derive the outcome from the explanation and check it against the source. Include a case where the result stays the same or becomes unknown when that distinction matters. If answering requires an unstated rule, repair the explanation rather than adding that rule only to the answer key. Keep this proportional to the task; do not turn every short answer into a quiz for the user.

Record the changed condition, predicted result or unknown, evidence, and any correction. Author self-review, an independent agent's task performance, and an actual reader's comprehension are different kinds of evidence; do not report one as another. For independent task-performance tests, keep answer keys and case-specific scoring criteria out of executor prompts. A diagram reviewer receives declared requirements in the second phase above, not benchmark answers.

Solve realistic inputs and evaluate actual outcomes. Matching expected wording with regexes is not behavioral evaluation. Check different request types such as code, design, and data. Record each defect, its cause, and the correction, then rerun the affected case. Ensure the correction generalizes rather than accumulating example-specific rules.

If no visual result was opened, mark it visually unverified. When browser/export tools are unavailable, finish structural and semantic checks and state the actual limits. Syntax checks do not establish explanation or visual quality. For independent evaluation, preserve its inputs, independence, scope, and actual artifacts.
