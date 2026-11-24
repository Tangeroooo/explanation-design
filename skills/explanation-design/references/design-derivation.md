# Derive a design from constraints

State a brief recommendation first, then show the conditions under which it holds. Keep goals, constraints, and current implementation distinct.

## Inputs to the decision

- Goals and acceptance criteria: which observations would count as success? If numbers are unavailable, use qualitative criteria or explicit investigation items rather than inventing targets.
- Contracts to preserve versus internals that may change. Establish from context whether changes to existing APIs, storage formats, or response semantics are authorized.
- Workload, tolerated failures, operational staffing, migration/rollback, time, and cost constraints.
- Two or three realistic alternatives evaluated on shared criteria. Do not add clearly unsuitable straw alternatives. If the user specified a candidate that violates a requirement, retain it and explain the disqualifying condition and what would make it viable.

Evaluate each option through `module/API changes → state and data/control flow → benefits → costs → failure conditions`. Use concrete conditions rather than arbitrary scores. A process-local cache may be small to implement but does not immediately observe writes in other processes. Do not assume invalidation exists unless implemented.

## Make the recommendation actionable

```text
if stale reads within one process are acceptable:
    consider a local TTL cache
elif multiple processes must share the same freshness contract:
    compare a shared cache with direct reads
else:
    establish the freshness contract first
```

Explain why the recommendation fits and **which conditions would change it**. Separate design intent from implementation steps. If code was inspected, connect changes to actual files/functions/structs/traits; otherwise mark names as proposed.

State migration and concurrency are part of the design. Check compatibility while old writers remain, partial rollout, duplicate execution, and interpretation of data after rollback.

Sequence adoption: short term for contracts, observation, and minimal changes; medium term for implementation, integration, and failure checks; long term for reassessment as scale changes. Give verification steps for each phase. Explain how remaining questions affect the conclusion and investigate information already available.
