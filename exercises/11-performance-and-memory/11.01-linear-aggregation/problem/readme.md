# Linear-Time Event Aggregation

Implement `aggregate_inventory` in `inventory_aggregation.py`.

## Requirements

- Aggregate signed quantity deltas by SKU and report the first and last timestamps.
- Preserve the order in which each SKU first appeared.
- Return immutable `InventorySummary` values in a tuple.
- Reject empty SKUs and boolean/non-integer deltas.
- Accept a one-shot iterable and consume it exactly once.
- Target average O(n) time and O(k) auxiliary space for n events and k SKUs.
- Do not sort, repeatedly scan accumulated output, or materialize the original input.

The scalability test uses equality-comparison counts rather than wall-clock timing,
making the complexity expectation deterministic.

## Discuss aloud

- How would you prove the complexity of your implementation?
- When does a generator reduce memory, and when does it merely defer allocation?
- Which profiler would you use for CPU time, allocation, and production sampling?
