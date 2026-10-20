"""Day 8: implement bounded asynchronous processing with cleanup."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def bounded_map(
    function: Callable[[T], Awaitable[R]],
    items: Iterable[T],
    *,
    limit: int,
    timeout: float | None = None,
) -> list[R]:
    raise NotImplementedError
