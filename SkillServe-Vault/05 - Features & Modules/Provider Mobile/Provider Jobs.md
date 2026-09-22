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

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`booking_test`, `session_roles_payments_test`, `ProviderBookingTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Booking Lifecycle]] · [[Payments and Refunds]] · [[Provider Mobile Features Index]]
