---
type: feature
platform: admin-web
status: implemented
module_number: 19
tags: [feature, admin-web]
---
# Logout (Admin)

Admin requirement module **19** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Authentication`  |
| Frontend module | `frontend/src/modules/authentication` |
| Admin route(s) | `header menu → Sign out` |
| Endpoints | [[API - Admin Authentication]] |
| Permissions | signed-in admin |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 19.1 | Admin Logout | confirm dialog → `POST /api/auth/logout`; local state cleared even if the call fails; realtime disconnected; redirected to `/login` |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`AuthenticationTest` — see [[Backend Test Suite]].

## Related

[[Admin Authentication]] · [[Admin Web Features Index]]
