import threading

import pytest

from job_queue import InvalidTransition, JobConflict, JobQueue, JobStatus


class Clock:
    now = 100.0

    def __call__(self) -> float:
        return self.now


def test_enqueue_is_idempotent_but_detects_conflicts() -> None:
    queue = JobQueue(Clock())
    original = queue.enqueue("j1", b"payload", max_attempts=2)
    assert queue.enqueue("j1", b"payload", max_attempts=2) == original
    with pytest.raises(JobConflict):
        queue.enqueue("j1", b"different", max_attempts=2)


def test_claim_complete_and_stats() -> None:
    clock = Clock()
    queue = JobQueue(clock)
    queue.enqueue("j1", b"one")
    claimed = queue.claim("worker-1", lease_seconds=10)
    assert claimed is not None
    assert claimed.status is JobStatus.RUNNING
    assert claimed.attempts == 1
    assert claimed.lease_until == 110
    completed = queue.complete("j1", "worker-1")
    assert completed.status is JobStatus.COMPLETED
    assert queue.claim("worker-1", 10) is None
    assert queue.stats()[JobStatus.COMPLETED] == 1
    assert set(queue.stats()) == set(JobStatus)


def test_expired_lease_can_be_reclaimed_and_old_owner_is_fenced() -> None:
    clock = Clock()
    queue = JobQueue(clock)
    queue.enqueue("j1", b"one")
    queue.claim("old", 5)
    clock.now = 106
    reclaimed = queue.claim("new", 5)
    assert reclaimed is not None and reclaimed.attempts == 2
    with pytest.raises(InvalidTransition):
        queue.complete("j1", "old")
    assert queue.complete("j1", "new").status is JobStatus.COMPLETED


def test_failure_schedules_retry_then_dead_letters() -> None:
    clock = Clock()
    queue = JobQueue(clock)
    queue.enqueue("j1", b"one", max_attempts=2)
    queue.claim("worker", 10)
    failed = queue.fail("j1", "worker", retry_delay=5)
    assert failed.status is JobStatus.PENDING and failed.available_at == 105
    assert queue.claim("worker", 10) is None
    clock.now = 105
    queue.claim("worker", 10)
    assert queue.fail("j1", "worker").status is JobStatus.DEAD


def test_claim_is_atomic_across_threads() -> None:
    queue = JobQueue(Clock())
    queue.enqueue("j1", b"one")
    barrier = threading.Barrier(3)
    claimed: list[str | None] = []

    def worker(name: str) -> None:
        barrier.wait()
        job = queue.claim(name, 10)
        claimed.append(None if job is None else job.id)

    threads = [threading.Thread(target=worker, args=(f"w{index}",)) for index in range(2)]
    for thread in threads:
        thread.start()
    barrier.wait()
    for thread in threads:
        thread.join(timeout=1)
    assert claimed.count("j1") == 1
    assert claimed.count(None) == 1


@pytest.mark.parametrize(
    "job_id,payload,max_attempts",
    [("", b"x", 1), ("j", b"", 1), ("j", b"x", 0)],
)
def test_enqueue_validates_input(job_id: str, payload: bytes, max_attempts: int) -> None:
    with pytest.raises((TypeError, ValueError)):
        JobQueue(Clock()).enqueue(job_id, payload, max_attempts)
