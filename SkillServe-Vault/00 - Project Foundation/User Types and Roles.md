---
type: domain
tags: [foundation, roles, security]
sources: [backend/app/Shared/Enums/AccountRole.php, backend/app/Models/User.php, backend/database/migrations/2026_09_18_000001_link_users_to_roles.php, backend/database/seeders/RolePermissionSeeder.php]
---
# User Types and Roles

Every account is a row in `users` with a required `role_id` → `roles.id`. The first four role ids
are fixed (`AccountRole` enum):

| role_id | Role name | Kind | App | Signs in via |
|---|---|---|---|---|
| 1 | `super-admin` | staff | Admin Web | `POST /api/auth/login` |
| 2 | `admin` | staff | Admin Web | `POST /api/auth/login` |
| 3 | `provider` | account type (no permissions) | Mobile (provider shell) | `POST /api/client/v1/auth/login` |
| 4 | `customer` | account type (no permissions) | Mobile (customer shell) | `POST /api/client/v1/auth/login` |
| ≥5 | custom staff roles | staff | Admin Web | created in Admin Management |

A **guest** is an unauthenticated mobile user: they can browse the public catalog
(`/api/client/v1/categories|services|providers`, `/platform`) and marketing screens.

## Rules implemented in code

- `users.role_id` is the source of truth. `User::booted()` defaults new users to `customer` and
  syncs the Spatie role assignment: staff role ids get a `model_has_roles` row; account types
  (3, 4) have **no** Spatie roles.
- `User::isAdministrator()` = role_id is not 3 or 4. `isClientAccount()` = role 4.
  `isMobileProviderAccount()` = role 3 **and** a `provider_profiles` row exists.
- Admin login rejects accounts without any Spatie role (`LoginAction`) → customers/providers cannot
  sign into the admin web.
- Mobile middleware (`EnsureClient`, `EnsureProvider`, `EnsureMobileAccount`, `EnsureActiveClient`)
  rejects staff accounts and requires the `client:auth` token ability.
- Roles 1–4 cannot be renamed or deleted (`SystemRole::isFixed`); roles 3–4 cannot be assigned to
  administrators (`SystemRole::isAccountType`). Only a super-admin may assign `super-admin`
  (`AdministratorPolicy::assignSuperAdmin`).
- `Gate::before` grants **every** ability to `super-admin` (`AppServiceProvider`).
- The legacy `users.user_type` column was dropped (migration `2026_09_18_000001`); `user_type` is
  now a computed attribute (`customer` / `provider` / `admin`).

## Default permissions

| Role | Permissions (from `RolePermissionSeeder`) |
|---|---|
| super-admin | all 66 permissions (and `Gate::before` bypass) |
| admin | `view reports`, `view dashboard`, `view provider recognition`, `manage provider badges`, `assign provider badges`, `manage featured providers`, `view top rated providers`, `view audit logs`, `view login activity`, `monitor security events` |

> [!warning] Needs Verification — admin role drift between migrations and seeder
> Some permission migrations grant extra permissions to the `admin` role (e.g.
> `2026_09_08_000002_add_data_management_permissions` grants data-management permissions to
> `super-admin` **and** `admin`), but `RolePermissionSeeder` later calls `syncPermissions` on
> `admin` with the short list above. The effective permission set of `admin` on an existing
> database therefore depends on whether the seeder ran after those migrations. Check with
> `select … from role_has_permissions` on production.

Full catalogue: [[Permission Catalog]]. Mechanics: [[Authorization and RBAC]].

## Seeded accounts

| Email | Role | Seeded in mode |
|---|---|---|
| `admin@skillserve.test` (override `ADMIN_EMAIL`) | super-admin | all modes |
| *(none)* | — | Seeding creates **only** the super-admin. The former `system@skillserve.test` account was removed by migration `2026_09_25_000001`; further staff accounts are created by hand in Administrator Management |
| `customer@skillserve.test` | customer | demo |
| `provider@skillserve.test` | provider | demo |
| 150 demo customers (password `password`) | customer | demo |

Local password: `SkillServe#2026`. Production seeding refuses that default. See
[[Seeding and Demo Data]].
