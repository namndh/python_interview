"""Day 11: implement a single-pass, linear-time aggregation."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar

SKU = TypeVar("SKU", bound=Hashable)


@dataclass(frozen=True)
class InventoryEvent(Generic[SKU]):
    sku: SKU
    delta: int
    occurred_at: datetime


@dataclass(frozen=True)
class InventorySummary(Generic[SKU]):
    sku: SKU
    quantity: int
    first_seen: datetime
    last_seen: datetime


def aggregate_inventory(events: Iterable[InventoryEvent[SKU]]) -> tuple[InventorySummary[SKU], ...]:
    raise NotImplementedError
