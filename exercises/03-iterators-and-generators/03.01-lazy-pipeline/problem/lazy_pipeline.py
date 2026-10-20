"""Day 3: implement lazy iterator and generator utilities."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class RecordError(ValueError):
    def __init__(self, line_number: int, text: str) -> None:
        self.line_number = line_number
        self.text = text
        super().__init__(f"invalid record at line {line_number}")


def read_records(lines: Iterable[str]) -> Iterator[dict[str, Any]]:
    raise NotImplementedError


def windowed(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    raise NotImplementedError


def batched(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    raise NotImplementedError


class Pipeline(Generic[T]):
    def __init__(self, source: Iterable[T]) -> None:
        raise NotImplementedError

    def map(self, function: Callable[[T], U]) -> "Pipeline[U]":
        raise NotImplementedError

    def filter(self, predicate: Callable[[T], bool]) -> "Pipeline[T]":
        raise NotImplementedError

    def take(self, count: int) -> "Pipeline[T]":
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        raise NotImplementedError
