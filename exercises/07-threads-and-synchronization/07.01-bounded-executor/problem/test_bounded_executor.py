import threading
from concurrent.futures import CancelledError

import pytest

from bounded_executor import BoundedExecutor


def test_configuration_is_validated() -> None:
    with pytest.raises(ValueError):
        BoundedExecutor(0, 1)
    with pytest.raises(ValueError):
        BoundedExecutor(2, 1)


def test_submit_blocks_at_bound_and_unblocks_on_completion() -> None:
    release = threading.Event()
    second_submitted = threading.Event()
    executor = BoundedExecutor(max_workers=1, max_pending=1)
    first = executor.submit(lambda: release.wait(timeout=2))

    def submit_second() -> None:
        executor.submit(lambda: "second")
        second_submitted.set()

    thread = threading.Thread(target=submit_second)
    thread.start()
    assert not second_submitted.wait(timeout=0.1)
    release.set()
    assert first.result(timeout=1)
    assert second_submitted.wait(timeout=1)
    thread.join(timeout=1)
    executor.shutdown()


def test_failed_and_cancelled_tasks_release_permits() -> None:
    blocker = threading.Event()
    with BoundedExecutor(max_workers=1, max_pending=2) as executor:
        running = executor.submit(lambda: blocker.wait(timeout=2))
        cancelled = executor.submit(lambda: None)
        assert cancelled.cancel()
        replacement = executor.submit(lambda: "replacement")
        blocker.set()
        assert running.result(timeout=1)
        with pytest.raises(CancelledError):
            cancelled.result()
        assert replacement.result(timeout=1) == "replacement"


def test_task_exception_does_not_leak_permit() -> None:
    with BoundedExecutor(1, 1) as executor:
        failed = executor.submit(lambda: 1 / 0)
        with pytest.raises(ZeroDivisionError):
            failed.result(timeout=1)
        assert executor.submit(lambda: 42).result(timeout=1) == 42
