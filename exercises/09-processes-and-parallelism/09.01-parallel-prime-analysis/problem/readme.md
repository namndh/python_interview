# Process-Based Parallel Analysis

Implement the functions in `parallel_primes.py`.

## Requirements

- `is_prime(value)` handles all integers correctly using an O(sqrt(n)) algorithm.
- `analyze_chunk(values)` returns an immutable summary containing item count, prime
  count, and the largest prime or `None`.
- `parallel_prime_summary(values, max_workers, chunk_size)` divides values into
  bounded chunks, processes them with `ProcessPoolExecutor`, and combines summaries.
- Reject non-positive worker and chunk sizes.
- Empty input produces an empty summary without starting a process pool.
- Worker callables and transferred values must be pickle-compatible.
- Do not submit one future per individual number.

## Discuss aloud

- Why can processes improve CPU-bound Python code despite their overhead?
- What cannot safely or cheaply cross a process boundary?
- How do standard CPython, the GIL, and free-threaded builds change the decision?
