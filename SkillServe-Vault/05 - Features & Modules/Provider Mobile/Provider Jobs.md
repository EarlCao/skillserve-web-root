---
type: feature
platform: provider-mobile
status: implemented
tags: [feature, mobile]
---
# Provider Jobs

Mobile requirement(s): **(provider side of M5)** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/booking-requests`, `/active-jobs`, `/completed-jobs`, `/booking-details/:id` |
| Code (Flutter `lib/`) | `features/booking/controllers/provider_booking_controller.dart`<br>`features/provider/views/booking_requests_screen.dart, active_jobs_screen.dart, completed_jobs_screen.dart` |
| Endpoints | [[API - Provider Bookings (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Accept / decline / cancel / start / complete / payment received | lifecycle transitions with 422 on wrong status; customer's name, phone and job address visible; late provider cancellation fee shown before confirming | implemented |
| — | Confirm GCash payments | *GCash payments* on the job: each proof the customer sent with its screenshot (tap for full size), amount and reference; **Confirm** (a downpayment or the rest — before or after the work) or **Reject** with a reason; *Paid ₱x of ₱y*; updates live ([[booking_payment_proofs]]) | implemented |
| — | Several jobs at once | overlapping bookings are allowed; accept or decline each request | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`booking_test`, `session_roles_payments_test`, `payment_proof_test`, `ProviderBookingTest`, `PaymentProofTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Booking Lifecycle]] · [[Payments and Refunds]] · [[Provider Mobile Features Index]]
