"""Day 12: inspect functions, code objects, defaults, and bytecode."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CallableAnalysis:
    positional_argument_count: int
    local_names: tuple[str, ...]
    free_variables: tuple[str, ...]
    cell_variables: tuple[str, ...]
    globals_loaded: frozenset[str]
    opcode_counts: tuple[tuple[str, int], ...]


def analyze_callable(function: Callable[..., Any]) -> CallableAnalysis:
    raise NotImplementedError


def mutable_default_parameters(function: Callable[..., Any]) -> tuple[str, ...]:
    raise NotImplementedError
