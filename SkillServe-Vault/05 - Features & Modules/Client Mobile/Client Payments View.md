---
type: feature
platform: client-mobile
status: implemented
tags: [feature, mobile]
---
# Client Payments View

Mobile requirement(s): **(extra)** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/payments`, `/payment-details/:bookingId` |
| Code (Flutter `lib/`) | `features/payments/ (services/payment_service.dart, controllers/payment_controller.dart, views/*)` |
| Endpoints | [[API - Client Bookings]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Payment history | read from the customer's bookings (`payment_method`, `payment_status`, amounts, refunds) — no payments endpoint | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`session_roles_payments_test` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Payments are recorded, not processed ([[ADR-007 Payments Recorded Not Processed]]).

## Related

[[Payments and Refunds]] · [[Client Mobile Features Index]]
