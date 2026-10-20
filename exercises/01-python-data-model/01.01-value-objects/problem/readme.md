# Value Objects and the Python Data Model

Implement an immutable, hashable `Money` value object in `value_objects.py`.

## Requirements

- `Money(amount, currency)` accepts `Decimal`, `int`, or decimal `str` amounts.
- Store amounts as `Decimal`, currencies as uppercase three-letter ASCII codes.
- Reject booleans, invalid numeric strings, non-finite values, and invalid currencies.
- Instances are immutable and compare by value.
- Equal instances have equal hashes and can be dictionary keys.
- `+` and `-` operate only on `Money` with the same currency. A currency mismatch
  raises `CurrencyMismatchError`; an unrelated operand returns `NotImplemented`.
- Ordering is supported only between values of the same currency.
- `allocate(parts)` splits the smallest currency unit (0.01) without losing money;
  earlier parts receive any remainder. `parts` must be positive.

Do not use binary floating-point internally.

## Discuss aloud

- Why must equality and hashing be designed together?
- Why is returning `NotImplemented` different from raising `TypeError`?
- What assumptions does this model make about currencies with non-cent minor units?
