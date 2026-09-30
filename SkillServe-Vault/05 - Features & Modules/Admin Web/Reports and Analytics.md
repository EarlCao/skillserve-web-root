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
| — | Commission report | `type=commissions`: each booking's amount paid, rate, commission and commission status; status filter is `commission_status`, search is booking number or provider |
| A 13.7 | Export Reports | `GET /api/analytics/reports/export` → CSV download (capped at **5,000** rows) |
| — | General report | `GET /api/analytics/reports/general/export?from=&to=` → one `.xlsx`: see [[#General report]] |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`AnalyticsTest` — see [[Backend Test Suite]].

## General report

The **General report (Excel)** button on the Reports page generates every category at once for the
selected date range (the other filters do not apply). The workbook (`maatwebsite/excel`) holds:

1. **Summary** — period, generation time (Manila), each category's record count with a status
   breakdown, and commission collected / outstanding / waived in pesos. Counts are complete even when
   a category sheet is capped.
2. One sheet per category — Users, Providers, Services, Bookings, Reviews, System Activity,
   Commissions — with the same columns as that category's CSV, latest first, capped at 5,000 rows
   (`ReportService::EXPORT_LIMIT`).

Categories come from `ReportRequest::TYPES`, so a new report type appears in the workbook
automatically. Cells go through `ReportService::exportCell`, the same formula-injection guard as
the CSV export (user text starting with `=`, `+`, `-`, `@` is prefixed with `'`).

## Notes

- The SPA downloads the CSV with the raw axios instance (exception to the `services/api.js` rule).

## Related

[[Admin Web Features Index]]
