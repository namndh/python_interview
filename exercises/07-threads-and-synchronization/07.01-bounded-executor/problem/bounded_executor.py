"""Day 7: implement a thread-safe bounded executor."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from types import TracebackType
from typing import Any, TypeVar

T = TypeVar("T")


class BoundedExecutor:
    def __init__(self, max_workers: int, max_pending: int) -> None:
        raise NotImplementedError

    def submit(self, function: Callable[..., T], /, *args: Any, **kwargs: Any) -> Future[T]:
        raise NotImplementedError

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        raise NotImplementedError

    def __enter__(self) -> "BoundedExecutor":
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        raise NotImplementedError
