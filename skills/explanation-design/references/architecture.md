# Analyze architecture

Choose the level first: logical module, process, host, or external service. Use separate views when needed; do not flatten these levels into indistinguishable boxes.

For each element, establish responsibility, owned state, public interface, dependency direction, and evidence for placement. The dependency “A imports B” may differ from control flow in which B calls back into A.

Trace data flow and control flow separately for a concrete request. Show reads, writes, ownership transfers, synchronous calls, asynchronous handoffs, and who detects failure. A store icon does not establish durability, replication, or consistency.

For a change explanation, make explicit:

- Contracts to preserve: public APIs, data formats, user-visible success conditions, compatibility.
- Internals that may change: module boundaries, queue placement, batching, caching, within the supported scope.
- Shared identifiers across Before and After, and responsibilities added, removed, or moved.
- Routing, data ownership, and rollback conditions while old and new paths coexist during migration.

Do not infer runtime boundaries from directory names alone. If deployment configuration was not inspected, mark deployment topology unknown. Continue to [design-derivation](design-derivation.md) when recommending structural changes.
