# Audience and scope

Choose depth by what the reader needs to do after reading, rather than by their job title.

| Reader's next action | Include | May shorten |
|---|---|---|
| Change code or investigate a failure | Functions, state owners, error paths, reproduction conditions | Familiar background |
| Make an operational or adoption decision | Goals, constraints, costs, failure impact, conditions that change the choice | Internal functions that do not affect the decision |
| Understand an unfamiliar concept | One concrete input, essential terms, causes and outcomes | Implementation detail, while preserving important guarantees |

Determine what is being explained, why it matters now, what the reader knows, and which version and boundary are covered. Increase depth only as needed to answer those questions.

- For “Does the data survive after the response?”, prioritize the order of response and persistence over a module inventory.
- For a nontechnical audience, explain terms while preserving conditions. “Accepted” must not become “durably stored.”
- Without sources, explain general principles without presenting them as the actual behavior of a specific system.
- If no format is specified, use chat for short explanations, tables for comparisons, and documents for longer material that needs repeated reference or sharing. Save files when requested or needed in context.

A useful internal note is `audience / question / next decision / prior knowledge / scope / unverified areas`. Do not turn the entire note into a questionnaire for the user.
