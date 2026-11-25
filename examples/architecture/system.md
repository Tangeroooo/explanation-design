# Synthetic system

These are stipulated facts for an illustration, not a production system.

- The overview has one logical service S and a catalog. The service-to-catalog edge summarizes record updates; it does not specify the number of processes.
- S is deployed as two processes P and Q. Each process has one coordinator, three workers with mailboxes, and one pool shared by its workers. The two processes have separate pools.
- Both processes use the same source helper, `update_record(node_id, value)`, which writes `record:<node_id>`. P normally passes `P`; Q normally passes `Q`.
- For this synthetic model, the helper selects its key solely from the supplied argument. No concurrent-update ordering or conflict-resolution rule is specified.
- A proposed local change gives P four workers and leaves Q unchanged. Another proposed change makes Q pass `P` to the helper.
