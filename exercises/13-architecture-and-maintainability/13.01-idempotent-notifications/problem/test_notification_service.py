import pytest

from notification_service import (
    DeliveryResult,
    DeliveryStateUnknown,
    Notification,
    NotificationService,
)


class Ports:
    def __init__(self) -> None:
        self.claimed: set[str] = set()
        self.calls: list[tuple[object, ...]] = []
        self.complete_error: Exception | None = None

    def claim(self, message_id: str) -> bool:
        self.calls.append(("claim", message_id))
        if message_id in self.claimed:
            return False
        self.claimed.add(message_id)
        return True

    def release(self, message_id: str) -> None:
        self.calls.append(("release", message_id))
        self.claimed.remove(message_id)

    def complete(self, message_id: str) -> None:
        self.calls.append(("complete", message_id))
        if self.complete_error:
            raise self.complete_error

    def render(self, template: str, context: dict[str, str]) -> str:
        self.calls.append(("render", template))
        return template.format(**context)

    def send(self, recipient: str, body: str) -> None:
        self.calls.append(("send", recipient, body))

    def observe(self, outcome: str, duration: float) -> None:
        self.calls.append(("metric", outcome, duration))


def make_service(ports: Ports) -> NotificationService:
    times = iter([1.0, 1.25])
    return NotificationService(ports, ports, ports, ports, lambda: next(times))


def test_successful_delivery_and_duplicate_short_circuit() -> None:
    ports = Ports()
    notification = Notification("m1", "ada@example.com", "Hi {name}", {"name": "Ada"})
    assert make_service(ports).deliver(notification) is DeliveryResult.SENT
    assert [call[0] for call in ports.calls] == ["claim", "render", "send", "complete", "metric"]
    ports.calls.clear()
    assert make_service(ports).deliver(notification) is DeliveryResult.DUPLICATE
    assert [call[0] for call in ports.calls] == ["claim", "metric"]


def test_send_failure_releases_claim_and_records_failure() -> None:
    class FailingPorts(Ports):
        def send(self, recipient: str, body: str) -> None:
            super().send(recipient, body)
            raise OSError("offline")

    ports = FailingPorts()
    with pytest.raises(OSError, match="offline"):
        make_service(ports).deliver(Notification("m1", "a@example.com", "Hi", {}))
    assert "m1" not in ports.claimed
    assert [call[0] for call in ports.calls][-2:] == ["release", "metric"]


def test_completion_failure_does_not_release_claim() -> None:
    ports = Ports()
    ports.complete_error = OSError("database unavailable")
    with pytest.raises(DeliveryStateUnknown) as error:
        make_service(ports).deliver(Notification("m1", "a@example.com", "Hi", {}))
    assert isinstance(error.value.__cause__, OSError)
    assert "m1" in ports.claimed
    assert not any(call[0] == "release" for call in ports.calls)
