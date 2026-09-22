---
type: feature
platform: client-mobile
status: implemented
tags: [feature, mobile]
---
# Client Booking

Mobile requirement(s): **M5** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/booking-form/:providerId`, `/booking-confirmation`, `/booking-history`, `/booking-details/:id`, `/reschedule-booking/:id` |
| Code (Flutter `lib/`) | `features/booking/ (controllers/booking_controller.dart, services/booking_service.dart, models/booking_model.dart, views/*)` |
| Endpoints | [[API - Client Bookings]], [[API - Client Disputes]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 5.1 | Create Booking | service, schedule (UTC ISO-8601), address, contact phone, notes, payment method; `Idempotency-Key`; refused outside provider hours / overlapping / paused | implemented |
| M 5.2 | View Booking Details | service, provider, schedule, status, payment, cancellation policy | implemented |
| M 5.3 | View My Bookings | `GET /bookings` with status filter | implemented |
| M 5.4 | Monitor Booking Status | pending → confirmed → active → completed / cancelled / disputed, updated by notifications | implemented |
| M 5.5 | Booking History | timeline on the details screen | implemented |
| M 5.6 | Cancel Booking | reason + late-fee warning from `cancellation_policy`; reschedule also available | implemented |
| M 5.7 | Report or Dispute Booking | report the other party / raise a dispute | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`booking_test`, `ClientMarketplaceTest`, `BookingRescheduleTest`, `ProviderBookingTest`, `SettingsEnforcementTest`, `BookingDisputeTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Booking Lifecycle]] · [[Cancellation and Fees]] · [[Client Payments View]] · [[Client Disputes]] · [[Client Mobile Features Index]]
