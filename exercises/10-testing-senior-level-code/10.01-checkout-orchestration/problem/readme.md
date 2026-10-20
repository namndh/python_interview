# Testing Checkout Orchestration

Implement and test `CheckoutService` in `checkout_service.py`. Begin by adding at
least three tests of your own to `test_checkout_service.py` before changing the
implementation.

## Requirements

- An order has a non-empty tuple of positive-quantity lines.
- `place_order(command)` rejects invalid input before invoking any collaborator.
- Reserve inventory, then charge the exact total, persist the confirmed order, and
  finally publish `OrderPlaced`—in that order.
- IDs come from the injected `make_id` callable.
- If payment fails, release the exact reservation and re-raise the payment error.
- Do not save or publish when inventory or payment fails.
- If saving or publishing fails after payment, raise `CheckoutIncomplete` carrying
  the order ID and original phase. Do not pretend an automatic refund is safe.
- Depend on the supplied protocols and keep business logic deterministic.

The supplied tests are acceptance examples, not exhaustive coverage. Add tests for
validation, collaborator ordering, each failure phase, and correct interaction data.

## Discuss aloud

- When is a fake better than a mock?
- Why are tests that mirror implementation calls brittle?
- How would an outbox change the save/publish failure contract?
