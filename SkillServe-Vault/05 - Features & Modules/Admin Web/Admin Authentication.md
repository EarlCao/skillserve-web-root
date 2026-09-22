---
type: feature
platform: admin-web
status: implemented
module_number: 1
tags: [feature, admin-web]
---
# Admin Authentication

Admin requirement module **1** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Authentication`  |
| Frontend module | `frontend/src/modules/authentication` |
| Admin route(s) | `/login`, `/forgot-password`, `/reset-password`, `/admin/change-password` |
| Endpoints | [[API - Admin Authentication]] |
| Permissions | public (login, forgot, reset — `throttle:login`); signed-in admin for me/logout/change-password (`abilities:admin:auth`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 1.1 | Admin Login | `POST /api/auth/login`; refuses wrong password (401), inactive (403), roleless accounts (401); 5/min per IP |
| A 1.2 | Admin Logout | `POST /api/auth/logout` revokes the current token; SPA clears `localStorage` |
| A 1.3 | Role-Based Access Control | Spatie permissions checked per action (policies/gates); SPA hides menu items and wraps routes in `RequirePermission` |
| A 1.4 | Password Management | change password (other sessions revoked); forgot/reset via separate `admins` password broker, emailed link to `FRONTEND_URL/reset-password`, reset revokes all tokens and is audited |
| A 1.5 | Session Management | token lifetime = System Settings → session timeout; any 401 logs the SPA out |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`AuthenticationTest`, `AdminPasswordResetTest`, `UserRolesTest`, `RoleManagementTest` — see [[Backend Test Suite]].

## Notes

- Login/logout/failed-login/password events are written to the activity log with IP and user agent (visible in [[Security and Audit Logs]]).

## Related

[[Authentication Flows]] · [[Token and Session Management]] · [[Logout (Admin)]] · [[Admin Web Features Index]]
