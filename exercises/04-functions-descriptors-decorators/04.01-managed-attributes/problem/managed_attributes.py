"""Day 4: implement a validating descriptor and instrumentation decorator."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")
clock: Callable[[], float] = perf_counter


class Validated(Generic[T]):
    def __init__(self, validator: Callable[[T], T]) -> None:
        # Construction must succeed so descriptors can be installed during class
        # creation. Complete the remaining protocol methods as the exercise.
        self.validator = validator
        self.public_name: str | None = None
        self.storage_name: str | None = None

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.public_name = name
        self.storage_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type[object]) -> T | "Validated[T]":
        raise NotImplementedError

    def __set__(self, instance: object, value: T) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class CallEvent:
    function: str
    elapsed: float
    succeeded: bool
    exception: BaseException | None


def instrument(callback: Callable[[CallEvent], None]) -> Callable[[Callable[..., R]], Callable[..., R]]:
    raise NotImplementedError
