# Establish actual behavior from code

## Unit of tracing

Follow one concrete input from an entry point. Use `rg` to find callers, error handling, and state updates as well as definitions. Stop guarantees at boundaries whose implementation or contract you have not inspected.

A compact trace table is `input/trigger | function | state read | state changed and side effects | return/exception | evidence`.

1. Check entry-point validation, branches, and call order.
2. Identify mutable state and its actual owner: request, task, process, or external store.
3. Inspect state changes around external calls. Separate memory updates, transmission, persistence, and response.
4. Trace exception propagation and cleanup in `finally`, defer, or drop.
5. Separate return values from observable outcomes. Calling an operation does not establish its success.

## Failure and concurrency

- What remains if cancellation occurs before or after an `await`? Could an external effect succeed while the response fails?
- Which operation is retried? What are the idempotency key's scope, lifetime, and atomicity?
- Which objects and processes does a lock protect? Serial tests in one process do not establish distributed safety.
- Dequeue, processing start, commit, ack, and user response can be separate events. Connect them using implementation and contracts, not names.
- When are connections, files, and permits acquired and released? Inspect error, timeout, and cancellation paths too.

Example: for `await sink.send(item); await broker.ack(id)`, if ack can fail after send succeeds, explain the possibility of duplicate transmission on redelivery. Do not infer the broker's redelivery policy or the sink's deduplication behavior from this code alone.

## Report the findings

Separate four things: intent stated in comments/specs; actual order and state in the implementation inspected; execution observations for specified inputs; and unobserved risk conditions allowed by code and contracts.

If the whole repository was not inspected, limit conclusions to the files and call boundaries checked. Static tracing remains useful when execution is unavailable, but it is not a passed runtime test.
