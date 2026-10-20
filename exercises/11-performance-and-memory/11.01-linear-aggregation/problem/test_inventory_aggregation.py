from datetime import datetime, timedelta, timezone

import pytest

from inventory_aggregation import InventoryEvent, InventorySummary, aggregate_inventory

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_aggregates_in_first_seen_order_from_one_shot_input() -> None:
    events = iter(
        [
            InventoryEvent("b", 2, NOW),
            InventoryEvent("a", 5, NOW + timedelta(seconds=1)),
            InventoryEvent("b", -1, NOW + timedelta(seconds=2)),
        ]
    )
    assert aggregate_inventory(events) == (
        InventorySummary("b", 1, NOW, NOW + timedelta(seconds=2)),
        InventorySummary("a", 5, NOW + timedelta(seconds=1), NOW + timedelta(seconds=1)),
    )


@pytest.mark.parametrize("sku,delta", [("", 1), ("a", True), ("a", 1.5)])
def test_rejects_invalid_events(sku: str, delta: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        aggregate_inventory([InventoryEvent(sku, delta, NOW)])  # type: ignore[arg-type]


def test_scaling_uses_hash_lookup_not_repeated_linear_scan() -> None:
    class TrackedSku:
        comparisons = 0

        def __init__(self, value: int) -> None:
            self.value = value

        def __hash__(self) -> int:
            return hash(self.value)

        def __eq__(self, other: object) -> bool:
            type(self).comparisons += 1
            return isinstance(other, TrackedSku) and self.value == other.value

    events = [InventoryEvent(TrackedSku(index), 1, NOW) for index in range(1_000)]
    aggregate_inventory(events)
    assert TrackedSku.comparisons < 5_000
