---
type: feature
platform: admin-web
status: implemented
module_number: 15
tags: [feature, admin-web]
---
# Admin Management

Admin requirement module **15** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Administrators`  |
| Frontend module | `frontend/src/modules/administrators` |
| Admin route(s) | `/admin/administrators`, `/admin/administrators?tab=roles`, `/admin/administrators?tab=permissions` |
| Endpoints | [[API - Administrators, Roles and Permissions]] |
| Permissions | administrators: `view|create|edit administrators`; roles & permissions: `manage administrators`; `super-admin` is never assigned (there is exactly one) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 15.1 | View Administrators | `GET /api/administrators` (role-bearing accounts only) |
| A 15.2 | Add Administrator | `POST /api/administrators` |
| A 15.3 | Edit Administrator | `PUT /api/administrators/{id}`; `PATCH …/password` admin password reset |
| A 15.4 | Activate or Deactivate Administrator | `PATCH …/status` active/inactive (inactive cannot sign in) |
| A 15.5 | Manage Roles | CRUD `/api/roles` (roles 1–4 fixed; provider/customer not assignable) |
| A 15.6 | Manage Permissions | one row per admin area with *No access / View / Full control* (`config/permission-areas.php`, `GET /api/permissions` returns `view_permissions` + `permissions` per area); *What's included* lists the exact permissions; a role that matches no level shows *Custom*; `PUT /api/roles/{id}/permissions` |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`AdministratorManagementTest`, `RoleManagementTest`, `RolePermissionSeederTest` — see [[Backend Test Suite]].

## Notes

- **One super administrator (2026-10-13).** A new administrator is always `admin` — the Add form has
  no role field, and `POST /api/administrators` accepts `role` only as `admin` (optional). Nobody,
  not even the super administrator, can grant `super-admin`: store and update reject it with 422.
  This also closes the 2026-09-08 audit's super-admin escalation (formerly guarded by
  `AdministratorPolicy::assignSuperAdmin`, now unreachable).
- Administrators' profile photos show in the list, the details and the header, falling back to
  initials when there is none or it fails to load (`UserAvatar`).
- `SystemRole::PROTECTED_PERMISSIONS = ['manage administrators']`.

## Related

[[Authorization and RBAC]] · [[Permission Catalog]] · [[roles]] · [[Admin Web Features Index]]
