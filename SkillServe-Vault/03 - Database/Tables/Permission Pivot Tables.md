---
type: table
tags: [database, table, rbac]
domain: RBAC
soft_deletes: false
---
# Permission Pivot Tables

`model_has_roles`, `model_has_permissions`, `role_has_permissions` (Spatie).

- **Model:** `—`
- **Soft deletes:** no
- **Migrations:** `2026_08_07_053615_create_permission_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `model_has_roles` | role_id, model_type, model_id — PK(role_id, model_id, model_type) | staff role assignment (kept in sync with users.role_id) |
| `model_has_permissions` | permission_id, model_type, model_id — PK | direct permissions (not used by app code found) |
| `role_has_permissions` | permission_id, role_id — PK | role grants |

## Foreign keys

- role_id → roles cascade on delete
- permission_id → permissions cascade on delete

## Related

[[roles]] · [[permissions]] · [[Database Index]]
