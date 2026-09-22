---
type: adr
adr: 7
status: accepted
tags: [adr, architecture]
---
# ADR-007 Payments Recorded Not Processed

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09-21 |

## Context

Customers pay providers off-platform (cash, GCash). Handling card data was out of scope.

## Decision

Bookings carry payment fields; providers mark "payment received" on completed jobs; admins with `manage booking payments` mark paid and record partial/full refunds; every change audited and notified. No payment gateway.

## Consequences

- No PCI scope; simple model.
- Commission (`platform_fee`) and cancellation fees are recorded numbers only — nothing is collected.
- Earnings/payments screens are derived from bookings.

## Evidence

- `Bookings/Services/BookingPaymentService.php`
- `TEST_PLAN.md design decisions`
- migration 2026_09_21_000003

## Related

[[Payments and Refunds]] · [[ADR Index]]
