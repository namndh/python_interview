# Thread-Safe Bounded Executor

Implement `BoundedExecutor` in `bounded_executor.py`.

## Requirements

- Wrap a `ThreadPoolExecutor` while limiting the total number of running plus queued
  tasks to `max_pending`.
- `submit` blocks when all permits are occupied and returns a normal `Future`.
- A permit is released when its future completes successfully, fails, or is cancelled.
- If underlying submission fails, release the permit immediately.
- `shutdown` delegates to the executor and makes future submissions fail.
- Support the context-manager protocol.
- Configuration requires `max_workers >= 1` and `max_pending >= max_workers`.
- Internal synchronization must remain correct even when a submitted task completes
  before its completion callback is attached.

## Discuss aloud

- What does the GIL protect, and what race conditions remain possible?
- Why is a bounded queue a reliability feature?
- How can callback execution order lead to deadlock or permit leakage?
