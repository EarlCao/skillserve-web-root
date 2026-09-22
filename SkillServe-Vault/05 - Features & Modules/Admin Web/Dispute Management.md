---
type: feature
platform: admin-web
status: implemented
module_number: 10
tags: [feature, admin-web]
---
# Dispute Management

Admin requirement module **10** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Bookings` (DisputeController) |
| Frontend module | `frontend/src/modules/disputes` |
| Admin route(s) | `/admin/disputes` |
| Endpoints | [[API - Disputes]] |
| Permissions | view: `view bookings`; act: `manage booking disputes` (or `manage bookings`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 10.1 | View Disputes | `GET /api/disputes` (filter status, sort) |
| A 10.2 | View Dispute Details | `GET /api/disputes/{booking}` — parties, booking, statement, evidence |
| A 10.3 | Review Dispute Evidence | `GET …/evidence/{evidence}` streams private photos |
| A 10.4 | Review Dispute History | `GET …/history` |
| A 10.5 | Add Dispute Notes | `PATCH …/notes` |
| A 10.6 | Resolve Dispute | `PATCH …/resolve` (booking → completed) / `…/reject`; both parties notified |
| A 10.7 | Close Dispute | `PATCH …/close` — only from resolved |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`DisputeManagementTest`, `BookingDisputeTest`, `AdminDecisionNotificationTest` — see [[Backend Test Suite]].

## Notes

- Rejected disputes leave the booking `disputed` and cannot be closed — see [[Disputes Lifecycle]] (Needs Verification).

## Related

[[Disputes Lifecycle]] · [[bookings]] · [[Admin Web Features Index]]
