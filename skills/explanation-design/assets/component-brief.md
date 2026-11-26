# Component specification

Use with the [figure brief](figure-brief.md) when a structural/design view must explain components, interfaces, ownership, or shared resources. Skip for figures whose question is only sequence, state, or numerical comparison. This is a semantic handoff, not a pixel layout or a required description of every implementation detail. Reuse IDs and evidence from the common brief instead of repeating them.

## Scope and hierarchy

- View level (logical module / runtime instance / process / host) and question:
- Parent-view correspondence, if any; distinguish decomposition from deployment or another perspective change:
- Containment tree with boundary kinds, owners, and instance counts; mark ranges or unknown counts explicitly:
- Parts to expand / summarize / move to a detail view, with reasons tied to the question:

## Components

Record one entry per meaningful component or repeated family; distinguish the family/type from its instances. Use a table or short records. Include only fields relevant to the reader's question, but explicitly mark consequential gaps as **unknown**, **not applicable**, or **omitted with reason**. A missing source fact is not permission to invent an interface or internal module.

- Stable ID / exact visible label / kind / source and fact, inference, proposal, or unknown:
- Parent boundary or owner / count and instance scope / shared users, if any:
- Responsibility / internal parts or state to show / interfaces or access points supported by evidence:
- Depiction: shape and its meaning / enclosure, compartments, ports, or repeated units / expand or summarize / distinctions that must remain visible:

Record a shared resource once within its actual ownership scope. A summarized repeated family must retain its count and per-instance state; a common source definition does not establish a single runtime instance. Unknown ownership must not become an ownership claim through containment. Do not add decorative ports for an unspecified API.

## Relationships

For each relationship that matters, record:

- Source ID and relevant port → target ID and relevant port (or an undirected pair); use component endpoints when ports are unknown or irrelevant:
- Meaning: membership, dependency, call, read/write, transfer, resource use, or another named relation / direction and label / source and claim status:
- Payload, order, synchronization, guard, or failure contract **only where relevant and evidenced**; record consequential unknowns:
- Depiction: containment or line / endpoint and arrow meaning; clarify whether it asserts execution order:

Membership can be expressed by the hierarchy without a redundant edge list. Referenced IDs must resolve. Describe missing connections as unknown or deliberately omitted rather than drawing plausible routes.

## Before rendering

Can a producer determine the relevant boundaries, counts, sharing, internal detail, and relationship meanings without deciding new system facts? Trace one instance and one important connection against the sources. Resolve missing known facts in the brief; preserve unknowns and their implications visibly when they affect the answer. Do not stop for user approval as a routine step.

If the view is crowded, use overview/detail correspondence or summarize a repeated family while retaining ownership and cardinality. Do not flatten required structure into a chain or delete essential distinctions to satisfy a node budget. Leave coordinates, spacing, and routing to diagram-design.
