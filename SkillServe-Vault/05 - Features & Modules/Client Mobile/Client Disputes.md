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
| Screens / routes | `booking details → Raise a dispute` / `Track dispute`, `/my-disputes` (Settings → Reports & disputes → My disputes), `dispute card → Add photo` |
| Code (Flutter `lib/`) | `features/reports/ (services/report_service.dart, views/my_disputes_screen.dart, raise_dispute_sheet.dart, case_card.dart)` |
| Endpoints | [[API - Client Disputes]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 11.1 | Submit Dispute | either party, active/completed booking, once; photos can be attached in the same sheet | implemented |
| M 11.2 | View My Disputes | `GET /disputes` | implemented |
| M 11.3 | View Dispute Details | status, reason, resolution, evidence | implemented |
| M 11.4 | Submit Evidence | up to 5 photos while open | implemented |
| M 11.5 | View Dispute Updates | notifications on each admin action | implemented |

Disputes have their own screen, separate from *My Reports*: a dispute is a case about a booking, a
report is a complaint about a person or content, and they have different lifecycles. A disputed
booking shows **Track dispute** (either party), which opens *My Disputes*. Providers do not see the
"With <provider>" line on a card, since that is their own name.

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`reports_support_test`, `BookingDisputeTest`, `AdminDecisionNotificationTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Disputes Lifecycle]] · [[Client Mobile Features Index]]
