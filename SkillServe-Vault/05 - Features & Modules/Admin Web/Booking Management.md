---
type: feature
platform: admin-web
status: implemented
module_number: 7
tags: [feature, admin-web]
---
# Booking Management

Admin requirement module **7** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Bookings`  |
| Frontend module | `frontend/src/modules/bookings` |
| Admin route(s) | `/admin/bookings` |
| Endpoints | [[API - Bookings]] |
| Permissions | `view bookings`, `cancel bookings`, `manage booking disputes`, `manage booking payments` (or `manage bookings`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 7.1 | View All Bookings | `GET /api/bookings` |
| A 7.2 | View Booking Details | modal: client, provider, service, schedule (Manila time), status, payment, late-cancellation fee |
| A 7.3 | Search Bookings | booking number, client, provider, service |
| A 7.4 | Filter Bookings | status, payment_status, dispute, date range; sort by number/created/price/status/scheduled |
| A 7.5 | Monitor Booking Status | statuses move live as providers act (realtime refresh) |
| A 7.6 | View Booking History | `GET …/history` (activity log: status changes, reschedules, payments) |
| A 7.7 | Cancel Booking | `PATCH …/cancel` with reason (pending/confirmed only); both parties notified |
| A 7.8 | Manage Booking Disputes | `PATCH …/dispute` (investigate/resolve/reject) — see [[Dispute Management]] |
| — | Record payment / refund (extra) | `PATCH …/mark-paid`, `PATCH …/refund` (partial or full; over-refund refused) |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`BookingListTest`, `BookingPaymentTest`, `BookingCancellationTest`, `BookingRescheduleTest`, `ProviderBookingTest` — see [[Backend Test Suite]].

## Related

[[Booking Lifecycle]] · [[Payments and Refunds]] · [[bookings]] · [[Admin Web Features Index]]
