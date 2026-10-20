# TTL-Aware LRU Cache

Implement `TTLCache` in `ttl_cache.py` using standard-library collections.

## Requirements

- The constructor accepts a positive `capacity`, positive default TTL, and an
  injectable monotonic `clock`.
- `put(key, value, ttl=None)` inserts or replaces a value. Per-item TTL overrides
  the default and must be positive.
- `get(key, default=MISSING)` returns a live value and marks it most recently used.
  A missing or expired key raises `KeyError` unless a default was supplied.
- Expired entries behave as absent and do not consume capacity once observed.
- Inserting beyond capacity evicts the least recently used live entry.
- `len(cache)`, membership, and `purge_expired()` reflect only live entries.
- Target complexity: average O(1) for `get` and `put`, excluding removal of entries
  already known to be expired.

Do not use `functools.lru_cache` or scan the entire cache on every access.

## Discuss aloud

- Which clock is appropriate for TTLs, and why?
- What consistency trade-off does lazy expiration make?
- How would you make the cache thread-safe without holding a lock during loading?
