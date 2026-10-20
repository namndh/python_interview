# Bounded Asynchronous Map

Implement `bounded_map` in `bounded_async_map.py`.

## Requirements

- Apply an async callable to every input with at most `limit` calls in flight.
- Preserve input order in the returned list even when tasks finish out of order.
- `limit` must be positive; an empty input returns immediately.
- An optional positive per-item timeout raises `TimeoutError`.
- On the first operation failure or timeout, cancel and await all unfinished work so
  no background tasks survive the call. Re-raise the original failure.
- If the caller cancels `bounded_map`, clean up children and propagate cancellation.
- Avoid creating an unbounded number of tasks for a very large iterable.

Use structured-concurrency ideas even if you choose not to use a version-specific
`TaskGroup` API directly. The supplied starter and tests run on Python 3.10+.

## Discuss aloud

- Distinguish coroutine objects, tasks, and futures.
- Why must cancellation usually be re-raised?
- Compare a semaphore-only design with a fixed worker-pool design for backpressure.
