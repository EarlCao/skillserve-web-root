---
type: feature
platform: admin-web
status: implemented
module_number: 2
tags: [feature, admin-web]
---
# Admin Dashboard

Admin requirement module **2** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Dashboard`  |
| Frontend module | `frontend/src/modules/dashboard` |
| Admin route(s) | `/admin` |
| Endpoints | [[API - Dashboard]] |
| Permissions | `view dashboard` |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 2.1 | User Summary | `user_summary`: total_clients, total_providers, active_users, suspended_users |
| A 2.2 | Service Summary | `service_summary`: total_services, approved, pending, reported_services |
| A 2.3 | Booking Summary | `booking_summary` per status (pending, confirmed, active, completed, cancelled, disputed) |
| A 2.4 | Verification Summary | `verification_summary`: pending, approved, rejected (+ additional_info_required) |
| A 2.5 | Reports Summary | `reports_summary`: pending, investigating, resolved, rejected |
| A 2.6 | Recent Activities | `recent_activities` from `activity_log`; live refresh via `admin.data` |
| A 2.7 | Platform Analytics | `analytics.monthly_activity` charts (recharts) |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`DashboardTest`, `RealtimeAdminUpdatesTest` — see [[Backend Test Suite]].

## Notes

- Dashboard queries are aggregate reads over existing tables (`DashboardService`); no dedicated table.

## Related

[[Realtime Architecture]] · [[Admin Web Features Index]]
