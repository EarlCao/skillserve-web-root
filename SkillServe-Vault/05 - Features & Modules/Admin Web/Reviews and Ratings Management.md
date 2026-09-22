---
type: feature
platform: admin-web
status: implemented
module_number: 8
tags: [feature, admin-web]
---
# Reviews and Ratings Management

Admin requirement module **8** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Reviews`  |
| Frontend module | `frontend/src/modules/reviews` |
| Admin route(s) | `/admin/reviews` |
| Endpoints | [[API - Reviews]] |
| Permissions | `view reviews`, `edit reviews`, `delete reviews` (or `manage reviews`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 8.1 | View Reviews and Ratings | `GET /api/reviews` |
| A 8.2 | Search Reviews | user, provider, service |
| A 8.3 | Filter Reviews | `rating`, `is_reported`, `status`; sort rating/created_at |
| A 8.4 | Review Reported Feedback | Reported filter — reviews reported from the app set `is_reported` |
| A 8.5 | Hide Review | `PATCH …/hide {is_hidden: true}`; reviewer notified |
| A 8.6 | Remove Review | `DELETE /api/reviews/{id}` → status removed + soft delete; restorable |
| A 8.7 | Restore Review | `PATCH …/hide {is_hidden: false}`; reviewer and provider notified |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`ReviewListTest`, `ReviewRemovalTest`, `ClientReportTest` — see [[Backend Test Suite]].

## Related

[[Reviews and Ratings Rules]] · [[reviews]] · [[Admin Web Features Index]]
