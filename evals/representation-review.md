# Representation review — 2026-11-25

This is an author-performed application of the revised instructions to synthetic requirements. It evaluates representation decisions and figure briefs, not an independent agent run, rendered diagrams, or production-system correctness. No private transcripts or system artifacts are included. Diagram production remains the responsibility of the separately installed diagram-design skill.

## 1. Independent divisions and physical membership

**Input.** Explain an illustrative ID space `[0, 24)`. Lookup shards cover six IDs each; index partitions cover eight. Physical file A contains IDs `{0, 2, 9}`, file B contains `{1, 5}`. Explain how ID 9 relates to all three structures.

**Applied brief.** The message is that lookup range, index range, and physical membership are different relationships. Expand the overview's “stored records” object. Draw the first two divisions as aligned tracks on one ID axis; show physical files separately with discrete membership marks or mapping edges. Carry ID 9 through shard 1 `[6, 12)`, partition 1 `[8, 16)`, and file A. Assign stable roles to shard, partition, and file symbols; use neutral context and label the traced ID. Numbers are illustrative.

**Acceptance review.** The arithmetic and set membership resolve to the stated destinations. Putting files into contiguous interval boxes would falsely imply that file A contains IDs 1–8; that draft choice was rejected. The brief preserves independent axes and does not invent nesting. A field table alone would hide the mismatched boundaries.

## 2. Overlapping resource limits

**Input.** An illustrative node has a 16 GiB capacity. Cache limit H is 8 GiB, work limit B is 5 GiB, and combined limit T is 12 GiB. Assume cache and work usage are disjoint, each obeys its own limit, and their sum must obey T. A separate pressure signal uses working set, with thresholds at 85% and 95% of capacity.

**Applied brief.** Use separate aligned limit tracks for H, B, and T on a GiB axis. Show T as a constraint on the sum, not a third allocation. Put the working-set pressure signal on a separate labeled track; its thresholds are 13.6 GiB and 15.2 GiB. Do not imply that working set equals accounted cache plus work. Preserve these equations in the caption: `cache <= 8`, `work <= 5`, `cache + work <= 12`.

**Acceptance review.** A three-part stacked bar would double-count T and was rejected. At cache 8 GiB and work 5 GiB, both individual limits pass but the combined limit fails. This concrete counterexample is visible in the proposed encoding. Exact bar geometry must come from reproducible calculations during production; no rendered scale was verified here.

## 3. Failure timing and what remains

**Input.** Files must finish uploading before a catalog pointer is published. An upload failure leaves unreferenced partial output. A definitive publish conflict leaves complete but unreferenced files. Successful publication followed by local cleanup failure leaves a readable published version and local temporary files. No unspecified retry behavior may be assumed.

**Applied brief.** Use aligned small multiples of the shared upload → publish → cleanup path, with one labeled version carried through all cases. Mark each stopping point and depict the remote files, catalog pointer, and local temporary files that remain. Keep locations and object shapes constant. Use explicit “unreferenced,” “published,” and “cleanup failed” labels in addition to status color. Distinguish a definitive conflict from an unknown publication result; the latter is outside the supplied scenario.

**Acceptance review.** A lookup table can summarize outcomes but cannot replace the order that explains them. A generic red “failed” terminal would wrongly make cleanup failure look like publication failure. No automatic retry or deletion guarantee was added. A short sequence remains suitable for the normal interaction; the branch comparison does not require replacing it.

## 4. Ownership and progressive detail

**Input.** Processes P and Q both call `update_record(node_id)`. P passes `P`; Q passes `Q`. Each process owns one coordinator, several workers with mailboxes, and one shared pool. Explain ownership before tracing a request to a worker.

**Applied brief.** Begin with separate process boundaries. Expand P using the same name and identity color, showing one coordinator, repeated worker/mailbox pairs, and a pool outside the worker boundaries but inside P. Route a concrete request to one worker and label the record `record:P`. Show `record:Q` separately if needed to answer the ownership question. Source modules and process instances are different views.

**Acceptance review.** Shared helper calls do not establish shared record ownership: the argument values select different records. Placing a copy of the pool inside every worker would invent per-worker ownership. The request flow revisits only the relevant worker and shared pool; it need not repeat the entire overview or add four fixed sections for every component.

## 5. Correction reaches the delivered image

**Input.** Prose and an SVG source now say “at least 64 units.” The PNG still says “more than 64 units.” The upload returns HTTP 200, but its downloaded body is HTML.

**Applied review.** The correction is incomplete in two independent places: the PNG must be regenerated from the authoritative source, and the download is not a valid image. Check the boundary value 64 in prose and figure labels, inspect the regenerated image, then verify returned image bytes and the published display if accessible. A correct local render does not establish a correct published view.

**Acceptance review.** Reference counts and upload status cannot justify a visual pass. A source hash alone cannot establish PNG freshness. A broad word substitution also needs contextual review if the same term has multiple meanings. These checks do not require building another renderer into explanation-design.

## Outcome and limits

The revised instructions support distinct representations for independent ranges, resource limits, failure timing, and ownership. They reject misleading geometry even when every label is individually true, preserve simple tables for lookups, and keep the narrative coverage check separate from document headings or figure quotas. English and Korean instructions and briefs were reviewed for the same decisions.

This is a semantic review of proposed briefs. No new figure was rendered, no diagram-design export was run, and no independent before/after quality measurement was performed. Run those checks on actual figure-producing tasks before claiming improved visual output. Repository structural/tooling checks are recorded separately by `scripts/check.py`.

Validation run for this change: `python3 scripts/check.py` passed package and example structure checks and all 14 existing tooling/behavior tests. `git diff --check` passed. Those checks do not evaluate the new prose's explanatory or visual quality.

## Follow-up: changed-condition review

The added cases in [cases.json](cases.json) use [explicit synthetic assumptions](transfer/input/scenarios.md). Each request asks for an explanation and a figure brief followed by condition changes. Criteria are for the evaluator, not part of an independent agent's request. The following is author self-review against the supplied assumptions, not an independent run or a test with human readers.

### Publication: existence, visibility, and uncertainty

**Explanation.** Complete remote files make a candidate available to storage operations. Readers select it only after its catalog pointer is published. The publication boundary therefore separates remote existence from reader visibility. In the specified model, publishing a pointer before its target is ready permits an immediate reader to follow it to an incomplete or missing target. This is a consequence of the supplied assumptions, not an observed incident or a claim about designer motivation. A sequence brief should carry one candidate version through files, pointer publication, and local cleanup, and mark the publication boundary explicitly.

| Changed condition | Prediction and supporting assumption |
|---|---|
| Upload succeeds, then a definitive publish conflict | This candidate is not selected; its complete files remain unreferenced. Another writer may have published something else, so “the global pointer did not change” would be an unsupported answer. |
| Publish succeeds, then local cleanup fails | Candidate visibility remains; local temporary files also remain. Cleanup failure does not undo publication. |
| Publication response is lost | Candidate publication is unknown. The writer's observation is insufficient; neither “unpublished” nor “safely retryable” follows. |

**Review finding.** A generic “publish failure” branch would conflate the first and third outcomes. The explanation and brief must preserve definitive conflict versus lost response, not fix the distinction only in the answer key.

### Ownership: preserve the overview while expanding it

**Explanation.** S is a logical role realized by P and Q, not a third process. Its overview update edge expands into each process's helper call and selected catalog key. Each detailed process contains one coordinator, repeated worker/mailbox pairs, and one pool outside the worker boundaries. Normally P selects `record:P` and Q selects `record:Q`. Shared source code does not imply a shared target record.

| Changed condition | Prediction and supporting assumption |
|---|---|
| P gains a fourth worker | P's worker count changes; its pool count stays one. Q still has three workers and one separate pool. |
| Q passes `P` instead of `Q` | Q now selects `record:P`, the same target P selects. The final value and update order remain unknown because the fixture specifies neither. |

**Review finding.** Repeating the pool inside each worker or treating S as an additional deployed process would contradict the overview-to-detail mapping. Matching colors alone would not catch either error.

### Resource limits: distinguish constraints from policy

**Explanation.** H and B separately bound C and W; T additionally bounds their sum. T is not another allocated region. Pressure classifies a separately measured working set and does not supply a request-handling policy. A brief should use aligned budget-limit tracks and a distinct pressure track, with illustrative GiB units and the three inequalities visible.

| Changed condition | Prediction and supporting assumption |
|---|---|
| C = 8, W = 5, T = 12 | Individual checks pass, but 8 + 5 = 13 exceeds T. |
| Only T changes to 13 | All budget checks pass, since equality is allowed; the pressure class cannot be inferred from those counters. |
| Separately, S = 15.2 | 15.2 / 16 = 95%, so pressure is Emergency. Request rejection remains unknown because no policy is specified. |

**Review finding.** A diagram that makes T a third allocation or equates working set with C + W changes the model. Classifying pressure correctly still does not establish what the system does in response.

These reviews cover changed, unchanged, and unknown outcomes. They exercise reasoning from the supplied models and the proposed briefs; they do not establish rendered legibility or measured improvement in reader comprehension. The new cases have not been independently executed.

Follow-up validation: `python3 scripts/check.py` again passed package/example checks and all 14 existing tests; skill-creator `quick_validate.py` and `git diff --check` passed. All nine evaluation cases were checked for unique IDs, nonempty requests/criteria, and existing input/context paths. The three new cases received the author review recorded above, not automated comprehension testing.
