---
type: feature
platform: admin-web
status: implemented
module_number: 16
tags: [feature, admin-web]
---
# Security and Audit Logs

Admin requirement module **16** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Audit`  |
| Frontend module | `frontend/src/modules/audit` |
| Admin route(s) | `/admin/audit-logs` |
| Endpoints | [[API - Audit Logs]] |
| Permissions | `view audit logs` (all view), `view login activity` (login view), `monitor security events` (security view) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 16.1 | View Audit Logs | `GET /api/audit-logs` over `activity_log` |
| A 16.2 | Search Audit Logs | `search` |
| A 16.3 | Filter Audit Logs | `administrator_id`, `module`, `action`, `from`, `to`; `GET …/administrators` for the actor filter |
| A 16.4 | View Login Activity | `view=login`: administrator_logged_in / logged_out / login_failed |
| A 16.5 | Monitor Security Events | `view=security`: authentication + administrators log entries (failed logins, password changes, bans…) |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`AuditLogTest` — see [[Backend Test Suite]].

## Notes

- Authorization is chosen per `view` inside the controller (`can(match($view){…})`).

## Related

[[activity_log]] · [[Audit Logging]] · [[Admin Web Features Index]]
