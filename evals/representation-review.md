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
