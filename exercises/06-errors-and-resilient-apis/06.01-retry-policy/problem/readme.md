# Retry Policy and Failure Contracts

Implement `run_with_retry` in `retry_policy.py`.

## Requirements

- `RetryPolicy` validates: attempts >= 1, non-negative delays, multiplier >= 1,
  and optional positive maximum delay.
- `run_with_retry(operation, policy, *, retry_on, sleep, on_retry)` returns the
  operation result on success.
- Retry only exceptions matching `retry_on`; all others propagate immediately.
- Use exponential backoff: `initial_delay * multiplier**retry_index`, capped by
  `max_delay`. Do not sleep after the final failure.
- Invoke `on_retry(RetryEvent)` before each sleep. A callback failure must not hide
  the operation failure; chain the callback error from it.
- When attempts are exhausted, raise `RetryExhausted` from the final operation error.
- Preserve traceback causality and never catch `BaseException` subclasses such as
  `KeyboardInterrupt` unless explicitly listed by the caller.

## Discuss aloud

- Which operations are safe to retry, and how does idempotency change the answer?
- When should jitter be added?
- Which layer should translate infrastructure errors into domain errors?
