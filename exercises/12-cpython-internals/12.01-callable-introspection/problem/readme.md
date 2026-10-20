# Callable and Bytecode Introspection

Implement the introspection utilities in `callable_introspection.py` using `inspect`,
function code objects, and `dis`.

## Requirements

- `analyze_callable(function)` returns immutable metadata for a Python function:
  positional argument count, local names, free variables, cell variables, global
  names loaded by bytecode, and an opcode frequency table.
- Global names must be derived from instructions, not from source-code text.
- Opcode counts must reflect only the supplied function's code object, not nested
  functions' code objects.
- Reject built-ins and arbitrary callable objects with `TypeError`.
- `mutable_default_parameters(function)` returns parameter names whose defaults are
  mutable built-in containers (`list`, `dict`, `set`, or `bytearray`) in signature
  order, including keyword-only parameters.

Do not make assertions about version-specific specialized opcodes beyond what the
tests request.

## Discuss aloud

- Explain `LOAD_FAST`, `LOAD_GLOBAL`, `LOAD_DEREF`, and closure cells.
- How do reference counting and cyclic GC divide responsibility in CPython?
- Which GIL guarantees are implementation details, and why is “atomic today” an
  unsafe synchronization contract?
