# Lazy Iterator Pipeline

Implement the streaming helpers in `lazy_pipeline.py`.

## Requirements

- `read_records(lines)` lazily parses non-blank JSON lines into dictionaries and
  raises `RecordError(line_number, text)` for invalid JSON or non-object values.
- `windowed(iterable, size)` lazily yields overlapping fixed-size tuples. It must
  work with one-shot and infinite iterators and reject non-positive sizes.
- `batched(iterable, size)` lazily yields non-overlapping tuples, including a final
  partial tuple.
- `Pipeline` composes lazy `map`, `filter`, and `take` operations. Iterating it must
  not eagerly consume the source, and each operation returns a new pipeline.
- `Pipeline` is intentionally one-shot when its source is one-shot.

Use iterator protocols and generators; do not materialize the input.

## Discuss aloud

- Distinguish iterable, iterator, and generator.
- When does generator cleanup happen, and how can a generator own a resource safely?
- What do `send`, `throw`, `close`, and `yield from` add to the basic protocol?
