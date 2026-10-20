import asyncio

import pytest

import managed_attributes
from managed_attributes import CallEvent, Validated, instrument


def positive(value: int) -> int:
    if value <= 0:
        raise ValueError("must be positive")
    return int(value)


class Product:
    quantity = Validated(positive)


def test_descriptor_uses_per_instance_storage_and_validates() -> None:
    first, second = Product(), Product()
    first.quantity = 1
    second.quantity = 2
    assert (first.quantity, second.quantity) == (1, 2)
    with pytest.raises(ValueError):
        first.quantity = 0
    fresh = Product()
    with pytest.raises(AttributeError, match="quantity"):
        _ = fresh.quantity
    assert isinstance(Product.quantity, Validated)


def test_sync_instrumentation_preserves_metadata_and_reports_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    times = iter([10.0, 10.25, 20.0, 20.5])
    monkeypatch.setattr(managed_attributes, "clock", lambda: next(times))
    events: list[CallEvent] = []

    @instrument(events.append)
    def divide(left: int, right: int) -> float:
        """Divide two values."""
        return left / right

    assert divide.__name__ == "divide" and divide.__doc__ == "Divide two values."
    assert divide(6, 2) == 3
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    assert [(event.elapsed, event.succeeded) for event in events] == [(0.25, True), (0.5, False)]
    assert isinstance(events[-1].exception, ZeroDivisionError)


def test_async_instrumentation_waits_for_completion(monkeypatch: pytest.MonkeyPatch) -> None:
    times = iter([1.0, 1.75])
    monkeypatch.setattr(managed_attributes, "clock", lambda: next(times))
    events: list[CallEvent] = []

    @instrument(events.append)
    async def work() -> str:
        await asyncio.sleep(0)
        return "done"

    assert asyncio.run(work()) == "done"
    assert events[0].elapsed == 0.75 and events[0].succeeded
