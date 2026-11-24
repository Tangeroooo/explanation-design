# Choose an explanation strategy

| Reader's difficulty | Strategy | Check for |
|---|---|---|
| What is responsible for what? | Boundaries and ownership | Mistaking logical modules for processes |
| Why did this outcome occur? | Cause → state change → outcome | Turning correlation into causation |
| What actually happens? | Trace a concrete input | Implying unobserved order or timing |
| When is an operation possible? | State transitions and guards | Omitting the state after an error |
| Should I choose A or B? | Shared comparison criteria and conditional choice | Mixing workloads, guarantees, or cost bases |
| An abstract concept is unclear | Small example and counterexample | Turning example values into general guarantees |

“The cache is fast” is less useful than “When the same key is in memory and within its TTL, the store call is skipped. A miss, expiry, or another process reads the store.” The latter connects conditions to effects.

Use analogies to introduce unfamiliar relationships. A queue as a waiting line can explain arrival order, but parallel processing, redelivery, and priorities differ from one simple line. State those limits. Prefer a short execution example when an analogy would distort the guarantees.

Avoid forcing structure, execution time, and deployment into one figure. Center the main question: use a structural view for boundaries or a sequence view for order, and connect secondary details through a separate table or caption.
