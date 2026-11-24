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

When shortening a draft, remove repetition and background first. Preserve errors, constraints, and uncertainty that could change the conclusion. Merge or delete paragraphs that answer no new question.
