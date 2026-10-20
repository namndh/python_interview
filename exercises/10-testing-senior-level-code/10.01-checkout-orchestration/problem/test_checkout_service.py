from decimal import Decimal

import pytest

from checkout_service import (
    CheckoutService,
    Order,
    OrderLine,
    OrderPlaced,
    PlaceOrder,
)


class Collaborators:
    def __init__(self) -> None:
        self.calls: list[tuple[object, ...]] = []

    def reserve(self, lines: tuple[OrderLine, ...]) -> str:
        self.calls.append(("reserve", lines))
        return "reservation-1"

    def release(self, reservation_id: str) -> None:
        self.calls.append(("release", reservation_id))

    def charge(self, customer_id: str, amount: Decimal) -> None:
        self.calls.append(("charge", customer_id, amount))

    def save(self, order: Order) -> None:
        self.calls.append(("save", order))

    def publish(self, event: OrderPlaced) -> None:
        self.calls.append(("publish", event))


def command() -> PlaceOrder:
    return PlaceOrder(
        "customer-1",
        (OrderLine("book", 2, Decimal("12.50")), OrderLine("pen", 1, Decimal("2.00"))),
    )


def test_happy_path_returns_order_and_coordinates_in_order() -> None:
    collaborators = Collaborators()
    service = CheckoutService(collaborators, collaborators, collaborators, collaborators, lambda: "order-1")
    order = service.place_order(command())
    assert order == Order("order-1", "customer-1", command().lines, Decimal("27.00"))
    assert [call[0] for call in collaborators.calls] == ["reserve", "charge", "save", "publish"]
    assert collaborators.calls[-1] == ("publish", OrderPlaced("order-1", Decimal("27.00")))


def test_payment_failure_releases_reservation_and_propagates() -> None:
    class DecliningCollaborators(Collaborators):
        def charge(self, customer_id: str, amount: Decimal) -> None:
            super().charge(customer_id, amount)
            raise RuntimeError("declined")

    collaborators = DecliningCollaborators()
    service = CheckoutService(collaborators, collaborators, collaborators, collaborators, lambda: "order-1")
    with pytest.raises(RuntimeError, match="declined"):
        service.place_order(command())
    assert [call[0] for call in collaborators.calls] == ["reserve", "charge", "release"]


def test_invalid_command_has_no_side_effects() -> None:
    collaborators = Collaborators()
    service = CheckoutService(collaborators, collaborators, collaborators, collaborators, lambda: "order-1")
    with pytest.raises(ValueError):
        service.place_order(PlaceOrder("customer-1", ()))
    assert collaborators.calls == []
