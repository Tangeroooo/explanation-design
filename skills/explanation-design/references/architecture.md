# Analyze architecture

Choose the level first: logical module, process, host, or external service. Use separate views when needed; do not flatten these levels into indistinguishable boxes.

For each element, establish responsibility, owned state, public interface, dependency direction, and evidence for placement. The dependency “A imports B” may differ from control flow in which B calls back into A.

Before drawing a structural view, transfer those findings into the [component specification](../assets/component-brief.md): record each relevant component or repeated family, its ownership/count, internal detail, supported interfaces, and typed relationships. Distinguish missing evidence from deliberate visual omission; a flat inventory of names is not a sufficient handoff.

When a diagram is useful, make that structure visible in a component view using [visual-selection](visual-selection.md): responsibility compartments, interface ports, typed resources, and ownership boundaries. Show a shared resource once under its actual owner, not once per caller. For a redesign, compare aligned Before/After structures or mark changed responsibilities on a stable map. A sequence alone does not satisfy a request to explain module boundaries or architecture; add it only when interaction order answers a further question. Avoid inventing execution order from spatial placement.

Trace data flow and control flow separately for a concrete request. Show reads, writes, ownership transfers, synchronous calls, asynchronous handoffs, and who detects failure. A store icon does not establish durability, replication, or consistency.

For a change explanation, make explicit:

- Contracts to preserve: public APIs, data formats, user-visible success conditions, compatibility.
- Internals that may change: module boundaries, queue placement, batching, caching, within the supported scope.
- Shared identifiers across Before and After, and responsibilities added, removed, or moved.
- Routing, data ownership, and rollback conditions while old and new paths coexist during migration.

Do not infer runtime boundaries from directory names alone. If deployment configuration was not inspected, mark deployment topology unknown. Continue to [design-derivation](design-derivation.md) when recommending structural changes.
