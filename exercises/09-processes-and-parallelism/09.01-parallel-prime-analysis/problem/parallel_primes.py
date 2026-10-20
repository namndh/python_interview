"""Day 9: implement CPU-bound work using process-based parallelism."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class PrimeSummary:
    item_count: int
    prime_count: int
    largest_prime: int | None


def is_prime(value: int) -> bool:
    raise NotImplementedError


def analyze_chunk(values: Sequence[int]) -> PrimeSummary:
    raise NotImplementedError


def parallel_prime_summary(
    values: Iterable[int], *, max_workers: int = 2, chunk_size: int = 1_000
) -> PrimeSummary:
    raise NotImplementedError
