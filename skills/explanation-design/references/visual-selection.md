# Select the representation

| Relationship to communicate | Start with | Use a visual when |
|---|---|---|
| One fact or condition | Short prose | Usually unnecessary |
| Exact attributes or alternatives | Table | Topology changes determine the choice |
| Actual branching or API usage | Short code | Multiple actors, states, or failures interact |
| Responsibilities, boundaries, connections | Architecture view | Connections and boundaries are the question |
| Calls over time | Sequence view | Response and side-effect ordering matters |
| Guards and state changes | State diagram or flowchart | The reader needs to follow exceptional branches |
| Numerical differences or distributions | Table or reproducible chart | Scale, trends, or distributions are clearer visually |

Set one question and one-sentence message for each figure. Use the [figure brief](../assets/figure-brief.md). Connect sources and claim IDs to relationships. Record evidence for **edges as well as nodes**. Labels or a legend should identify whether arrows mean dependency, calls, data, or time.

- Do not merge stages with different guarantees into a single “completed” stage.
- Color may help, but fact/proposal and success/failure distinctions must also be readable without it.
- Split into overview and detail when node count obscures the question, and explain how the views connect.
- State omissions that could change interpretation in captions or prose. Omitting retries or external storage must not imply losslessness.
- For exact quantitative charts, follow [data](data.md). Decorative areas and icon sizes must not imply numerical values.

If removing a figure loses no understanding, do not create it. A figure adds no evidence by itself. Semantic verification remains explanation-design's responsibility after production.

## Choose geometry from the relationship

Choose what the reader needs to see before choosing a tool or template. Rectangles are useful for boundaries and states; the failure is putting prose in boxes without encoding a relationship.

| Question | Useful geometry | What must remain visible |
|---|---|---|
| What owns or contains what? | Nested boundaries; repeated instances | Scope, ownership, shared versus per-instance resources |
| How is one space divided differently? | Aligned interval tracks on a common axis | Unequal boundaries, overlap, mappings; do not invent containment |
| Where does an object go or change? | One identified object across locations or before/after views | Identity versus physical position, copies, versions, publication boundary |
| Who acts, waits, or runs concurrently? | Sequence or actor lanes with waits and gates | Actors, messages, overlap, blocking scope; label unmeasured time as schematic |
| Why do cases end differently? | Aligned small multiples of a shared path | Divergence, stopping point, state left behind, retry or recovery outcome |
| Which transitions are allowed? | State graph, separated by lifecycle or operation if useful | Guards and cross-group transitions; repeated nodes denote the same state |
| Which resource limit applies? | Quantitative bars or threshold tracks | Units, denominators, nested versus disjoint limits, measured versus illustrative values |
| Which exact fields or settings differ? | Table | Matched criteria; no need to turn a lookup into a diagram |

A sequence view can suit a single interaction while a state view or branch comparison suits another part of the same explanation. Keep a successful form; change the form that hides the relationship. Do not reject or impose a renderer for every figure because one layout failed.

## Give visual choices stable meanings

Record a small visual vocabulary in the brief, then let diagram-design implement it.

- Assign hues to the few roles or categories the reader must track across related views, not to every box. Use neutral scaffolding, restrained pale fills, and stronger outlines or accents for the focal relationship. Use the fixed [diagram theme](diagram-theme.md); its role mapping is explicit in the brief and does not require a theme-selection question.
- Keep identity color distinct from status. If an entity's color already resembles an error color, show failure with a label, symbol, or pattern as well. A local role-to-color reassignment needs an explicit legend; a color is not a globally unique identifier.
- Use shapes that expose structure: an actor with mailbox slots, a file with content marks, a log with ordered cells, a pool with repeated workers, or a boundary containing owned resources. Use a plain box when it conveys the required meaning. Icons must not imply a queue, disk, thread, or replica that the evidence does not support.
- Give position, enclosure, line style, arrowheads, and size explicit meanings. Arbitrary placement must not suggest execution order, exclusive routing, ownership, or numeric scale. Use labels and shapes so meaning survives loss of color.
- Across a figure series, keep names, role colors, recurring symbols, and displayed text scale consistent. Equal PNG widths alone do not make text equally readable. Pass the intended display size to the producer and inspect it there.

## Abstract while preserving the explanation

Keep the entities and distinctions needed to answer the figure's question: ownership, cardinality, independent axes, identity changes, ordering constraints, and success or failure boundaries. Omit implementation detail that does not change the answer. Explain what an overview collapses and which detail view opens it.

For a mechanism, carry one concrete request, row, file, or version through the drawing. Label invented example values as illustrative. For a change, keep comparison geometry aligned, mute unchanged context, and emphasize what changes; avoid making the reader visually diff many nearly identical full snapshots.

Test the draft with its long prose removed: can the reader still see the relationship, change, or comparison? Keep essential labels and guards. If only a list remains, move it to prose or a table, or redesign the geometry. Conversely, do not compress a failure scenario into a lookup row when its order and remaining state determine the outcome. Remove redundant prose/table/figure restatements unless they serve a different reader question.
