import pytest

from ttl_cache import TTLCache


class Clock:
    now = 0.0

    def __call__(self) -> float:
        return self.now


def test_get_refreshes_recency_before_eviction() -> None:
    clock = Clock()
    cache = TTLCache[str, int](2, 10, clock)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert "a" in cache and "c" in cache
    assert "b" not in cache


def test_expiration_and_default() -> None:
    clock = Clock()
    cache = TTLCache[str, int](2, 5, clock)
    cache.put("a", 1)
    clock.now = 5
    assert cache.get("a", 99) == 99
    with pytest.raises(KeyError):
        cache.get("a")
    assert len(cache) == 0


def test_per_item_ttl_and_purge_count() -> None:
    clock = Clock()
    cache = TTLCache[str, int](3, 10, clock)
    cache.put("short", 1, ttl=1)
    cache.put("long", 2)
    clock.now = 2
    assert cache.purge_expired() == 1
    assert len(cache) == 1
    assert cache.get("long") == 2


@pytest.mark.parametrize("capacity,ttl", [(0, 1), (-1, 1), (1, 0), (1, -1)])
def test_requires_positive_configuration(capacity: int, ttl: float) -> None:
    with pytest.raises(ValueError):
        TTLCache(capacity, ttl)


def test_replacement_does_not_grow_cache() -> None:
    cache = TTLCache[str, int](1, 10)
    cache.put("a", 1)
    cache.put("a", 2)
    assert len(cache) == 1
    assert cache.get("a") == 2
