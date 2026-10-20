# Idempotent Notification Architecture

Implement `NotificationService` in `notification_service.py` using the provided ports.

## Requirements

- Validate non-empty message ID, recipient, and body before side effects.
- Claim a message ID through `DeduplicationStore.claim`. If already claimed, return
  `DUPLICATE` without rendering or sending.
- Render, send, and record success in that order.
- On render or send failure, release the claim and record a failure metric, then
  re-raise the original exception.
- If recording success fails after a send, raise `DeliveryStateUnknown`; do not
  release the claim because doing so could cause duplicate external delivery.
- Record duration with the injected monotonic clock and use only the `Metrics` port.
- The service owns orchestration; transports, templates, storage, and metrics remain
  independently replaceable.

## Discuss aloud

- What makes this module “deep” or “shallow”?
- Is exactly-once delivery achievable here? State the actual guarantee.
- Which failures require reconciliation rather than automatic retry?
