---
type: feature
platform: admin-web
status: implemented
module_number: 3
tags: [feature, admin-web]
---
# User Management

Admin requirement module **3** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Users`  |
| Frontend module | `frontend/src/modules/users` |
| Admin route(s) | `/admin/users`, `/admin/users/:userId` |
| Endpoints | [[API - Users]] |
| Permissions | `view users`, `edit users`, `suspend users`, `activate users`, `ban users`, `delete users` (or `manage users`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 3.1 | View All Users | `GET /api/users` paginated (customers and providers; staff live in Admin Management) |
| A 3.2 | Search Users | `search` by name, email, id |
| A 3.3 | Filter Users | type, status, verification filters; sortable by name, created_at, last_login_at |
| A 3.4 | View User Profile | `GET /api/users/{id}` + `moderation-history` (activity log) |
| A 3.5 | Edit User Information | `PUT/PATCH /api/users/{id}` (`user_type` may only be `customer`) |
| A 3.6 | Suspend User | `PATCH …/suspend` with reason → app signs the user out; notification |
| A 3.7 | Activate User | `PATCH …/activate` (not for banned accounts) |
| A 3.8 | Ban User | `PATCH …/ban` days/forever; `…/unban`; ban email; expiry lifted by scheduler |
| A 3.9 | Delete User | `DELETE /api/users/{id}` soft delete (not self), restorable in Data Management |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`UserManagementTest`, `AccountStatusTest`, `AdminDecisionNotificationTest` — see [[Backend Test Suite]].

## Notes

- Demo seed: 150 customers with a spread of suspended/banned/unverified states.

## Related

[[Account Status Lifecycle]] · [[users]] · [[Admin Web Features Index]]
