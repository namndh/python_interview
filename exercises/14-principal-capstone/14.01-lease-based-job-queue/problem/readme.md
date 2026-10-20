# Capstone: Lease-Based Job Queue

Implement the deterministic in-memory `JobQueue` in `job_queue.py`. It models the
state transitions a durable distributed queue would need without hiding them behind
threads or a framework.

## Requirements

- `enqueue(id, payload, max_attempts=3)` is idempotent by ID: equal repeated input
  returns the existing job; conflicting input raises `JobConflict`.
- Jobs begin `PENDING`. `claim(worker_id, lease_seconds)` atomically returns the
  oldest eligible job, marks it `RUNNING`, increments attempts, and sets a lease.
- A pending job is eligible when `available_at <= now`. An expired running lease is
  eligible for reclamation. Use the injected monotonic clock.
- `complete(id, worker_id)` succeeds only for the current lease owner.
- `fail(id, worker_id, retry_delay)` returns the job to `PENDING`, scheduled after
  the non-negative delay, unless attempts are exhausted; then mark it `DEAD`.
- Invalid transitions or lease owners raise `InvalidTransition` without mutation.
- Returned `Job` values are immutable snapshots; callers cannot mutate queue state.
- All public operations are thread-safe. Do not invoke caller-owned code while
  holding the lock.
- `stats()` returns counts for every status from one consistent snapshot.

## Design extension

After tests pass, write brief notes describing durable storage transactions, worker
heartbeats, fencing tokens, clock choice across machines, dead-letter handling,
observability, fairness, and backpressure.

## Discuss aloud

- State the invariants before describing the implementation.
- What delivery guarantee does this queue provide?
- Which races appear when moving from one process to a distributed datastore?
