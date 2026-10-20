from decimal import Decimal

import pytest

from value_objects import CurrencyMismatchError, Money


def test_normalizes_and_compares_by_value() -> None:
    left = Money("10.50", "usd")
    right = Money(Decimal("10.50"), "USD")
    assert left == right
    assert hash(left) == hash(right)
    assert {left: "paid"}[right] == "paid"


@pytest.mark.parametrize("amount", [True, "nope", "NaN", "Infinity"])
def test_rejects_invalid_amounts(amount: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        Money(amount, "USD")  # type: ignore[arg-type]


@pytest.mark.parametrize("currency", ["US", "EURO", "12A", "U$D", 123])
def test_rejects_invalid_currency(currency: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        Money("1", currency)  # type: ignore[arg-type]


def test_is_immutable() -> None:
    money = Money("1", "USD")
    with pytest.raises(AttributeError):
        money._amount = Decimal("2")  # type: ignore[misc]


def test_arithmetic_and_ordering_require_matching_currency() -> None:
    assert Money("3", "USD") + Money("2", "USD") == Money("5", "USD")
    assert Money("2", "USD") < Money("3", "USD")
    with pytest.raises(CurrencyMismatchError):
        _ = Money("1", "USD") + Money("1", "EUR")
    with pytest.raises(CurrencyMismatchError):
        _ = Money("1", "USD") < Money("1", "EUR")
    with pytest.raises(TypeError):
        _ = Money("1", "USD") + 1  # type: ignore[operator]


def test_allocation_preserves_total_and_distributes_remainder() -> None:
    shares = Money("10.00", "USD").allocate(3)
    assert shares == (Money("3.34", "USD"), Money("3.33", "USD"), Money("3.33", "USD"))
    assert sum((share.amount for share in shares), Decimal()) == Decimal("10.00")
