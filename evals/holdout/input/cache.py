"""Request-scoped refresh. store and pool implementations are not supplied."""
cache = {}


async def refresh(key, store, pool):
    permit = await pool.acquire()
    try:
        value = await store.read(key)
        cache[key] = value
        await store.record_seen(key)
        return value
    finally:
        permit.release()
