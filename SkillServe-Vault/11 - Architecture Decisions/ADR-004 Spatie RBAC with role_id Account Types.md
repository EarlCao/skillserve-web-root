---
type: adr
adr: 4
status: accepted
tags: [adr, architecture]
---
# ADR-004 Spatie RBAC with role_id Account Types

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-08-07 (Spatie), 2026-09-18 (role_id) |

## Context

Admins need fine-grained permissions; customers/providers need a simple account type. A `user_type` string duplicated role information.

## Decision

Spatie roles/permissions for staff; `users.role_id` (FK to roles, NOT NULL) is the source of truth, with fixed ids 1 super-admin, 2 admin, 3 provider, 4 customer. Staff roles are mirrored into `model_has_roles`; account types carry no permissions. `user_type` column dropped.

## Consequences

- Simple checks (`isClientAccount`, `isAdministrator`).
- Roles 1–4 must never be renamed/deleted; migration pinned ids and reset the sequence.
- Two sources (role_id and Spatie pivot) kept in sync by model hooks and a listener.

## Evidence

- `backend/database/migrations/2026_09_18_000001_link_users_to_roles.php`
- `backend/app/Shared/Enums/AccountRole.php`
- `backend/app/Models/User.php`

## Related

[[User Types and Roles]] · [[Authorization and RBAC]] · [[ADR Index]]
