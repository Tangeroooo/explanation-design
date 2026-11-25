# Order the explanation

Each part should connect `reader question → main answer → evidence → next question`. Do not fix the number of sections.

A useful default is direct answer → essential concepts → one input's path → failures or conditions that change the choice → judgment and action. For a cause investigation, start with the observed symptom and its conditions.

Example: “Why can an ack failure cause duplicates?”

1. Answer: successful transmission and successful ack are not one atomic operation.
2. Essential concept: ack is a separate call that reports completion to the broker.
3. Flow: send succeeds → ack fails → broker state remains uncertain → redelivery is conditional on its policy.
4. Limit: broker policy and sink idempotency need separate verification.
5. Action: check observations and retry scope before choosing duplicate tolerance or deduplication.

A module inventory cannot replace this explanation. Introduce why a figure matters before showing it, then explain its conclusion and omissions afterward. Do not hide all important conditions in a caption.

For an unfamiliar system, establish a compact structural map before tracing scenarios. Expand a named component, object, boundary, or edge from that map when the next question needs it. Keep names and visual roles recognizable across views; remind the reader which part is being expanded. A flow can revisit only the relevant part of an earlier structure instead of repeating the whole map. Keep runtime roles distinct from source modules and deployment instances.

Use purpose, structure, behavior, and failure conditions as an internal coverage check, not mandatory headings or a quota of four figures per feature. An API-name match or a minimum paragraph length does not establish coverage: the reader must be able to trace the relevant behavior. When feedback exposes a class of defect, check the same class across the requested scope, including figures, rather than fixing only the example named by the reader.

When shortening a draft, remove repetition and background first. Preserve errors, constraints, and uncertainty that could change the conclusion. Merge or delete paragraphs that answer no new question.
