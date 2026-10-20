"""Day 2: implement a generic TTL-aware LRU cache."""

from __future__ import annotations

from collections.abc import Callable
from time import monotonic
from typing import Final, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")
MISSING: Final = object()


class TTLCache(Generic[K, V]):
    def __init__(self, capacity: int, ttl: float, clock: Callable[[], float] = monotonic) -> None:
        raise NotImplementedError

    def put(self, key: K, value: V, ttl: float | None = None) -> None:
        raise NotImplementedError

    def get(self, key: K, default: V | object = MISSING) -> V:
        raise NotImplementedError

    def purge_expired(self) -> int:
        """Remove expired entries and return the number removed."""
        raise NotImplementedError

    def __contains__(self, key: object) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
