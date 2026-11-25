# Synthetic scenarios for explanation transfer

These are supplied model assumptions, not claims about a production system. Use only the section named by the request. Implementation details and designer motivations not stated here remain unknown.

## Publication

- A writer produces immutable files for a candidate version. Upload success means those files are complete and readable in remote storage.
- Readers select a version exclusively through a catalog pointer. They do not discover candidate versions by listing remote files. Once a pointer is published, readers may follow it immediately without another readiness check.
- The writer uploads the candidate files, then conditionally publishes the pointer, then removes local temporary files.
- A definitive publish conflict means this candidate's pointer was not published. Another writer may have published a different version. This candidate's complete remote files remain unreferenced.
- A successful publication makes the candidate readable. Subsequent local cleanup failure leaves that publication intact and leaves local temporary files.
- If the publication response is lost, the writer has no evidence of whether publication succeeded. A successful or failed outcome cannot be inferred from the missing response alone. No reconciliation or retry mechanism is specified.
- No automatic remote-file deletion policy is specified.

## Ownership

- The overview has one logical service S and a catalog. The service-to-catalog edge summarizes record updates; it does not specify the number of processes.
- S is deployed as two processes P and Q. Each process has one coordinator, three workers with mailboxes, and one pool shared by its workers. The two processes have separate pools.
- Both processes use the same source helper, `update_record(node_id, value)`, which writes `record:<node_id>`. P normally passes `P`; Q normally passes `Q`.
- For this synthetic model, the helper selects its key solely from the supplied argument. No concurrent-update ordering or conflict-resolution rule is specified.
- A proposed local change gives P four workers and leaves Q unchanged. Another proposed change makes Q pass `P` to the helper.

## Resource limits

- An illustrative node has a capacity of 16 GiB. Cache usage C and work usage W are disjoint, nonnegative quantities in GiB.
- The budget checks are `C <= H`, `W <= B`, and `C + W <= T`, with H = 8, B = 5, T = 12 GiB. Passing the budget checks requires all three inequalities. Equality is allowed.
- A separate measured working set S need not equal C + W. Pressure is Normal below 85% of capacity, High from 85% up to but excluding 95%, and Emergency at or above 95%.
- Pressure classification alone does not specify request rejection, eviction, waiting, or retry behavior. No such policy is supplied.
