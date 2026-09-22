---
type: table
tags: [database, table, rbac]
domain: RBAC
soft_deletes: false
---
# roles

Spatie roles. Ids 1–4 are fixed (super-admin, admin, provider, customer); custom staff roles follow.

- **Model:** `Spatie\Permission\Models\Role`
- **Soft deletes:** no
- **Migrations:** `2026_08_07_053615_create_permission_tables`, `2026_08_07_064501_add_description_to_roles_table`, `2026_09_18_000001_link_users_to_roles (pins ids 1–4, resets sequence)`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `name` | string |  |
| `description` | string null |  |
| `guard_name` | string | `web` |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(name, guard_name)

## Notes

- Roles 1–4 cannot be renamed/deleted (`SystemRole::isFixed`).

## Related

[[permissions]] · [[Permission Pivot Tables]] · [[users]] · [[Authorization and RBAC]] · [[Database Index]]
