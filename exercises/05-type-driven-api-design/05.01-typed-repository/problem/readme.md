# Type-Driven Repository API

Implement a typed repository boundary and `UserService` in `typed_repository.py`.

## Requirements

- `Entity` exposes a string `id`; concrete immutable `User` values also contain a
  normalized email and display name.
- Define a generic structural `Repository[T]` protocol with `get`, `add`, `remove`,
  and `list` operations.
- `InMemoryRepository[T]` implements it, rejects duplicate IDs, returns snapshots
  rather than its mutable internal storage, and raises `EntityNotFound` as needed.
- `UserService.register(email, display_name)` validates and normalizes inputs,
  creates IDs through an injected callable, and rejects duplicate normalized emails.
- `UserService.rename(user_id, display_name)` replaces the immutable stored value.
- The service depends on the protocol, not on `InMemoryRepository`.

Keep the public types precise: avoid `Any`, unchecked casts, and repository methods
specific to `User`.

## Discuss aloud

- Why is `Protocol` useful at an architectural boundary?
- What variance would be safe for a read-only repository? Why not this one?
- Where should uniqueness be guaranteed in a production system?
