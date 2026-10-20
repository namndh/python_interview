"""Day 14: implement a thread-safe lease-based job state machine."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum
from time import monotonic


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    DEAD = "dead"


class JobConflict(ValueError):
    pass


class InvalidTransition(RuntimeError):
    pass


@dataclass(frozen=True)
class Job:
    id: str
    payload: bytes
    status: JobStatus
    attempts: int
    max_attempts: int
    available_at: float
    lease_owner: str | None = None
    lease_until: float | None = None


class JobQueue:
    def __init__(self, clock: Callable[[], float] = monotonic) -> None:
        raise NotImplementedError

    def enqueue(self, job_id: str, payload: bytes, max_attempts: int = 3) -> Job:
        raise NotImplementedError

    def claim(self, worker_id: str, lease_seconds: float) -> Job | None:
        raise NotImplementedError

    def complete(self, job_id: str, worker_id: str) -> Job:
        raise NotImplementedError

    def fail(self, job_id: str, worker_id: str, retry_delay: float = 0) -> Job:
        raise NotImplementedError

    def get(self, job_id: str) -> Job:
        raise NotImplementedError

    def stats(self) -> Mapping[JobStatus, int]:
        raise NotImplementedError
