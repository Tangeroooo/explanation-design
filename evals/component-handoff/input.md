# Synthetic source S1 — component handoff

Version: 2026-11-26. Stipulated facts for an illustration, not production behavior.

1. Logical service S is deployed as processes P and Q. A logical S-to-Catalog edge summarizes record updates. Catalog deployment and durability are unspecified.
2. Each process owns one coordinator, three workers, and one pool shared by those three workers. Each worker owns its own mailbox. P's pool and Q's pool are distinct. Pool type, capacity, and public API are unspecified.
3. A coordinator exposes `submit(job)`. It sends a job to one worker's mailbox through that mailbox's `enqueue(job)` interface. Worker selection, mailbox capacity, delivery order, and how a worker consumes its mailbox are unspecified. Workers use their process's pool; no ordering between workers is specified.
4. A proposed local change adds a fourth worker with its own mailbox to P, using the existing P pool. Q is unchanged. No throughput guarantee follows from this proposal.

Question: Which responsibilities, interfaces, and resources belong to each scope, and what changes when P gains a fourth worker?
