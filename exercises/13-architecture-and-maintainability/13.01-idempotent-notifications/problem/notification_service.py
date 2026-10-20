"""Day 13: implement an idempotent service across explicit ports."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


@dataclass(frozen=True)
class Notification:
    id: str
    recipient: str
    template: str
    context: dict[str, str]


class DeliveryResult(Enum):
    SENT = "sent"
    DUPLICATE = "duplicate"


class DeliveryStateUnknown(RuntimeError):
    pass


class DeduplicationStore(Protocol):
    def claim(self, message_id: str) -> bool: ...
    def release(self, message_id: str) -> None: ...
    def complete(self, message_id: str) -> None: ...


class Renderer(Protocol):
    def render(self, template: str, context: dict[str, str]) -> str: ...


class Transport(Protocol):
    def send(self, recipient: str, body: str) -> None: ...


class Metrics(Protocol):
    def observe(self, outcome: str, duration: float) -> None: ...


class NotificationService:
    def __init__(
        self,
        store: DeduplicationStore,
        renderer: Renderer,
        transport: Transport,
        metrics: Metrics,
        clock: Callable[[], float],
    ) -> None:
        raise NotImplementedError

    def deliver(self, notification: Notification) -> DeliveryResult:
        raise NotImplementedError
