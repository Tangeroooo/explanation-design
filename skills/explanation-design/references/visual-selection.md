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
