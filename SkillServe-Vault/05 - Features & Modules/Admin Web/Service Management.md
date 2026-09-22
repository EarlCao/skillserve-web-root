---
type: feature
platform: admin-web
status: implemented
module_number: 5
tags: [feature, admin-web]
---
# Service Management

Admin requirement module **5** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Services`  |
| Frontend module | `frontend/src/modules/services` |
| Admin route(s) | `/admin/services` |
| Endpoints | [[API - Services]] |
| Permissions | `view services`, `edit services`, `approve services`, `reject services`, `feature services`, `delete services` (or `manage services`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 5.1 | View All Services | `GET /api/services` |
| A 5.2 | Search Services | `search` title, provider, category |
| A 5.3 | Filter Services | `category_id`, `status`, `approval_status`; sort title/created_at/average_rating/price |
| A 5.4 | Review Service Submission | details modal (`GET /api/services/{id}`) |
| A 5.5 | Approve Service | `PATCH …/approve` → visible in app; provider notified |
| A 5.6 | Reject Service | `PATCH …/reject` with reason; provider notified |
| A 5.7 | Edit Service | `PUT /api/services/{id}`; provider notified of changed fields |
| A 5.8 | Hide Service | `PATCH …/hide` (toggle) |
| A 5.9 | Feature Service | `PATCH …/feature` — refused when featured services are disabled in settings |
| A 5.10 | Delete Service | `DELETE /api/services/{id}` soft delete; restorable |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`ServiceManagementTest`, `SettingsEnforcementTest` — see [[Backend Test Suite]].

## Notes

- No admin create endpoint: services are created by providers in the app (moderation-only management).

## Related

[[Service Approval Lifecycle]] · [[services]] · [[Admin Web Features Index]]
