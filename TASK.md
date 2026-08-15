# Task: implement a bounded TTL/LRU cache

Complete `challenge/cache.py` so it exports a class named `TTLCache` with the
following interface:

```python
TTLCache(max_size: int, default_ttl: float = 60.0, clock=None)
cache.set(key, value, ttl=None)
cache.get(key, default=None)
cache.prune_expired()
cache.clear()
len(cache)
key in cache
```

## Required behavior

1. `max_size` must be a positive integer; otherwise raise `ValueError`.
2. `clock` is a zero-argument callable returning monotonic seconds. If omitted,
   use `time.monotonic`.
3. `set` stores a value until `clock() + ttl`. When `ttl` is omitted, use
   `default_ttl`. A non-positive TTL is allowed and expires immediately.
4. `get` returns `default` for absent or expired keys and removes expired
   entries.
5. A successful `get` makes that key the most recently used key.
6. When insertion exceeds `max_size`, evict the least recently used live key.
   Expired entries should be removed before evicting a live key.
7. Overwriting a key replaces its value and expiry and makes it most recently
   used.
8. `len(cache)` and `key in cache` must not count expired entries.
9. `prune_expired` removes all expired entries and returns the number removed.
10. `clear` removes all entries.

## Constraints

- Use only the Python standard library.
- Do not sleep in the implementation or tests.
- Public methods do not need to be thread-safe.
- Keys may be any hashable value; values may be any Python object.

## Evaluation

Run:

```bash
python evaluate.py challenge/cache.py
```

The score is the percentage of deterministic test cases passed. The evaluator
prints failing tracebacks so the result is reproducible and auditable.
