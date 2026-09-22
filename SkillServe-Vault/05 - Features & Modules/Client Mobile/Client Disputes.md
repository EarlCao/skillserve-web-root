---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Disputes

Mobile requirement(s): **M11** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `booking details → Raise a dispute`, `/my-reports (disputes list)`, `dispute card → Add photo` |
| Code (Flutter `lib/`) | `features/reports/ (services/report_service.dart, views/my_reports_screen.dart, file_report_screen.dart)` |
| Endpoints | [[API - Client Disputes]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 11.1 | Submit Dispute | either party, active/completed booking, once | implemented |
| M 11.2 | View My Disputes | `GET /disputes` | implemented |
| M 11.3 | View Dispute Details | status, reason, resolution, evidence | implemented |
| M 11.4 | Submit Evidence | up to 5 photos while open | implemented |
| M 11.5 | View Dispute Updates | notifications on each admin action | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`reports_support_test`, `BookingDisputeTest`, `AdminDecisionNotificationTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Disputes Lifecycle]] · [[Client Mobile Features Index]]
