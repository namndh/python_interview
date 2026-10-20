"""Day 6: implement explicit retry and exception contracts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from time import sleep as real_sleep
from typing import TypeVar

T = TypeVar("T")


class RetryExhausted(RuntimeError):
    def __init__(self, attempts: int) -> None:
        self.attempts = attempts
        super().__init__(f"operation failed after {attempts} attempts")


@dataclass(frozen=True)
class RetryPolicy:
    attempts: int = 3
    initial_delay: float = 0.1
    multiplier: float = 2.0
    max_delay: float | None = None

    def __post_init__(self) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class RetryEvent:
    attempt: int
    delay: float
    exception: Exception


def run_with_retry(
    operation: Callable[[], T],
    policy: RetryPolicy,
    *,
    retry_on: tuple[type[Exception], ...] = (Exception,),
    sleep: Callable[[float], None] = real_sleep,
    on_retry: Callable[[RetryEvent], None] | None = None,
) -> T:
    raise NotImplementedError
