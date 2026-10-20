"""Day 1: implement an immutable Money value object."""

from __future__ import annotations

from decimal import Decimal


class CurrencyMismatchError(ValueError):
    """Raised when arithmetic mixes currencies."""


class Money:
    __slots__ = ("_amount", "_currency", "_frozen")

    def __init__(self, amount: Decimal | int | str, currency: str) -> None:
        raise NotImplementedError

    @property
    def amount(self) -> Decimal:
        raise NotImplementedError

    @property
    def currency(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __add__(self, other: object) -> "Money":
        raise NotImplementedError

    def __sub__(self, other: object) -> "Money":
        raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        raise NotImplementedError

    def allocate(self, parts: int) -> tuple["Money", ...]:
        raise NotImplementedError
