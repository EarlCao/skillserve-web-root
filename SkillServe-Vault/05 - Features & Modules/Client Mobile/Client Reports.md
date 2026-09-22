---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Reports

Mobile requirement(s): **M5.7, M6.4, M7.5** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/file-report`, `/my-reports`, `report sheet on reviews/messages` |
| Code (Flutter `lib/`) | `features/reports/ (controllers/report_controller.dart, services/report_service.dart, views/*)` |
| Endpoints | [[API - Client Reports]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | File and follow reports | against the other party of a booking, a review or a received message; status + outcome visible, notes hidden | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`reports_support_test`, `ClientReportTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Reports and Moderation Lifecycle]] · [[Client Mobile Features Index]]
