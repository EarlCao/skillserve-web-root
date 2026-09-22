---
type: feature
platform: admin-web
status: implemented
module_number: 13
tags: [feature, admin-web]
---
# Reports and Analytics

Admin requirement module **13** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Analytics`  |
| Frontend module | `frontend/src/modules/analytics` |
| Admin route(s) | `/admin/analytics` |
| Endpoints | [[API - Analytics]] |
| Permissions | `view analytics`, `export analytics` (super-admin by default; revoked from `admin` by migration) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 13.1–13.6 | User / Provider / Service / Booking / Review / System Activity reports | `GET /api/analytics/reports?type=users|providers|services|bookings|reviews|activity` with date range, search, status, sort |
| A 13.7 | Export Reports | `GET /api/analytics/reports/export` → CSV download (capped at **5,000** rows) |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`AnalyticsTest` — see [[Backend Test Suite]].

## Notes

- The SPA downloads the CSV with the raw axios instance (exception to the `services/api.js` rule).

## Related

[[Admin Web Features Index]]
