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
| Screens / routes | `/payments`, `/payment-details/:bookingId`, plus the "How to pay" card on `/booking-details/:id` |
| Code (Flutter `lib/`) | `features/payments/ (services/payment_service.dart, controllers/payment_controller.dart, views/*)` |
| Endpoints | [[API - Client Bookings]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Payment history | read from the customer's bookings (`payment_method`, `payment_status`, amounts, refunds) — no payments endpoint | implemented |
| — | Choose how to pay | the booking form offers `on_hand` and `gcash`, the only two the API accepts. Bookings made by older builds still display their old method | implemented |
| — | Where to send a GCash payment | the booking's `payment_instructions` (the provider's own number and account name, the amount and the booking reference) on an unpaid GCash booking, with a copy button | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`session_roles_payments_test`, and `booking_test` for the payment methods and `payment_instructions`
(Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Payments are recorded, not processed ([[ADR-007 Payments Recorded Not Processed]]).
- There is **no "Pay now" button**, and there should not be one: the customer pays the provider
  directly and SkillServe is never in the payment path
  ([[ADR-021 Direct Payment with Provider-Remitted Commission]]).
  `POST /bookings/{booking}/pay` exists but refuses every booking with a 422 today.
- The app never guesses at a provider's payment details. When the API omits `payment_instructions`
  there is nothing to show, and when the provider has saved none the API's own note tells the
  customer to message them instead.

## Related

[[Payments and Refunds]] · [[Client Mobile Features Index]]
