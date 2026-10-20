"""Day 10: implement orchestration designed for deterministic testing."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class OrderLine:
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class PlaceOrder:
    customer_id: str
    lines: tuple[OrderLine, ...]


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    lines: tuple[OrderLine, ...]
    total: Decimal


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str
    total: Decimal


class CheckoutIncomplete(RuntimeError):
    def __init__(self, order_id: str, phase: str) -> None:
        self.order_id = order_id
        self.phase = phase
        super().__init__(f"checkout {order_id} incomplete during {phase}")


class Inventory(Protocol):
    def reserve(self, lines: tuple[OrderLine, ...]) -> str: ...
    def release(self, reservation_id: str) -> None: ...


class Payments(Protocol):
    def charge(self, customer_id: str, amount: Decimal) -> None: ...


class Orders(Protocol):
    def save(self, order: Order) -> None: ...


class Events(Protocol):
    def publish(self, event: OrderPlaced) -> None: ...


class CheckoutService:
    def __init__(
        self,
        inventory: Inventory,
        payments: Payments,
        orders: Orders,
        events: Events,
        make_id: Callable[[], str],
    ) -> None:
        raise NotImplementedError

    def place_order(self, command: PlaceOrder) -> Order:
        raise NotImplementedError
