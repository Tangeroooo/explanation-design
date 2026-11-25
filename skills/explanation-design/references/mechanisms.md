# Explain execution, state, and failure

Break down `one input → acceptance → execution start → side effects → persistence/visibility → response` according to the evidence. Systems need not follow this order. Do not add unobserved stages.

## Check concrete scenarios

| Condition | Trace |
|---|---|
| Normal operation | Who changes state, when, and under which success condition |
| Capacity exceeded | Waiting, rejection, or dropping, and who knows which occurred |
| Timeout or cancellation | Whether work continues after the caller gives up, and effects already applied |
| Retry | Whether the whole task or a part repeats, and whether effects can duplicate |
| Crash or restart | Memory and persistent state that remain, and the recovery owner |
| Parallel inputs | Actual mechanisms limiting order, concurrent execution, and state races |

Find intent in comments/specifications, actual behavior in code and execution, and risks in possible combinations of conditions. An ack failure and a sink failure can leave different outcomes. The former may occur after an effect has already happened; do not collapse them into one generic failure.

When a boundary, mapping, or ordering rule is central to understanding the mechanism, explain its consequence with a bounded counterexample: what could change if that distinction were removed or the order reversed? State the changed assumption and trace the resulting state from evidence. For example, if readers follow a published pointer immediately, publishing it before its target exists can expose a missing target. This establishes a consequence under those assumptions, not proof that it was the designer's motivation or the only viable design. If another guard prevents the counterexample, include that guard or choose a supported example. Do not invent failures to make a structure seem necessary.

If the parts are individually clear but the flow is not, inspect what connects them: an identifier, lookup mapping, version selection, or ownership rule. Show that bridge and preserve meaningful asymmetries in read/write permissions, scope, and waiting conditions. Use stable technical names with short definitions; do not merge distinct mechanisms merely because a metaphor or translated term sounds similar.

In timing diagrams, distinguish first-called from first-completed and wall-clock time from logical happens-before. Do not add parallel latency intervals as though they were serial. If estimating waits from queue depth, state assumptions about service rate and steady state.

Assess risk by enabling conditions, actual impact, recoverability, and observation. A possible code path alone does not establish high frequency or an operational incident. Responses may progress from short-term observation/limits to stronger guarantees and later structural changes, without forcing this format onto small questions.
