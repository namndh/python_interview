import asyncio

import pytest

from bounded_async_map import bounded_map


def test_preserves_order_and_enforces_concurrency_limit() -> None:
    async def scenario() -> None:
        active = 0
        maximum = 0

        async def work(value: int) -> int:
            nonlocal active, maximum
            active += 1
            maximum = max(maximum, active)
            await asyncio.sleep((4 - value) * 0.005)
            active -= 1
            return value * 10

        assert await bounded_map(work, range(4), limit=2) == [0, 10, 20, 30]
        assert maximum == 2

    asyncio.run(scenario())


def test_failure_cancels_unfinished_work() -> None:
    async def scenario() -> None:
        cancelled = asyncio.Event()

        async def work(value: int) -> int:
            if value == 0:
                await asyncio.sleep(0)
                raise LookupError("boom")
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                cancelled.set()
                raise
            return value

        with pytest.raises(LookupError, match="boom"):
            await bounded_map(work, range(3), limit=3)
        assert cancelled.is_set()

    asyncio.run(scenario())


def test_timeout_cleans_up() -> None:
    async def scenario() -> None:
        async def slow(value: int) -> int:
            await asyncio.sleep(1)
            return value

        with pytest.raises(TimeoutError):
            await bounded_map(slow, [1], limit=1, timeout=0.01)

    asyncio.run(scenario())


@pytest.mark.parametrize("limit", [0, -1])
def test_rejects_invalid_limit(limit: int) -> None:
    async def identity(value: int) -> int:
        return value

    with pytest.raises(ValueError):
        asyncio.run(bounded_map(identity, [1], limit=limit))
