# Descriptors and Decorators

Implement `Validated` and `instrument` in `managed_attributes.py`.

## Requirements

- `Validated(validator)` is a data descriptor using `__set_name__` for private
  per-instance storage.
- Assignment runs `validator(value)` and stores its returned normalized value.
- Reading an unset attribute raises `AttributeError` naming the public attribute.
- Descriptor state must not leak between instances.
- `instrument(callback)` decorates functions and methods. The callback receives an
  immutable `CallEvent` after every call, including failures.
- Events contain qualified function name, elapsed seconds, success flag, and the
  raised exception or `None`.
- The decorator preserves metadata and return values, re-raises the original error,
  and supports both synchronous and asynchronous functions.

Use `time.perf_counter` by default, but make the clock replaceable by assigning the
module-level `clock` variable so tests and callers can make timing deterministic.

## Discuss aloud

- Explain function binding through the descriptor protocol.
- Why is `functools.wraps` operationally important, not merely cosmetic?
- How does decorator order change behavior?
