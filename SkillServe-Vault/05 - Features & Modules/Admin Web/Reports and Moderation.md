---
type: feature
platform: admin-web
status: implemented
module_number: 9
tags: [feature, admin-web]
---
# Reports and Moderation

Admin requirement module **9** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/ReportsAndModeration`  |
| Frontend module | `frontend/src/modules/reports` |
| Admin route(s) | `/admin/reports` |
| Endpoints | [[API - Reports and Moderation]] |
| Permissions | `view reports`, `investigate reports`, `resolve reports`, `manage moderation` (or `manage reports`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 9.1 | View User Reports | `GET /api/reports?type=user` |
| A 9.2 | View Service Reports | `type=service` — only seeded data; the app cannot file service reports |
| A 9.3 | View Review Reports | `type=review` |
| A 9.4 | View Message Reports | `type=message` |
| A 9.5 | Investigate Report | `PATCH …/investigate` → investigating |
| A 9.6 | Add Investigation Notes | `PATCH …/notes` (JSON notes with author/time) |
| A 9.7 | Resolve Report | `PATCH …/resolve` with note; reporter notified |
| A 9.8 | Reject Report | `PATCH …/reject` with reason; reporter notified |
| A 9.9 | Take Moderation Action | `PATCH …/action`: warning/suspend/ban (users), hide (services, reviews), remove (reviews, messages) |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`ReportsAndModerationTest`, `ClientReportTest`, `AccountStatusTest`, `AdminDecisionNotificationTest` — see [[Backend Test Suite]].

## Notes

- Reason filter reads `GET /api/reports/reasons` (current + legacy reasons).

## Related

[[Reports and Moderation Lifecycle]] · [[reports]] · [[Admin Web Features Index]]
