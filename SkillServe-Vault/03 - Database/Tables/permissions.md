---
type: table
tags: [database, table, rbac]
domain: RBAC
soft_deletes: false
---
# permissions

Spatie permissions (66 seeded by `RolePermissionSeeder`).

- **Model:** `Spatie\Permission\Models\Permission`
- **Soft deletes:** no
- **Migrations:** `2026_08_07_053615_create_permission_tables`, `many `add_*_permissions` data migrations (2026-08-19 … 2026-09-08)`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `name` | string | e.g. `view bookings` |
| `guard_name` | string | `web` |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(name, guard_name)

## Related

[[Permission Catalog]] · [[roles]] · [[Database Index]]
