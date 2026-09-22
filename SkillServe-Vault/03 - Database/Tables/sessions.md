---
type: table
tags: [database, table, framework]
domain: Framework
soft_deletes: false
---
# sessions

Database session store (`SESSION_DRIVER=database`). The API is token-based, so this is framework plumbing.

- **Model:** `—`
- **Soft deletes:** no
- **Migrations:** `0001_01_01_000000_create_users_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | string PK |  |
| `user_id` | FK-ish bigint null, indexed |  |
| `ip_address` | string(45) null |  |
| `user_agent` | text null |  |
| `payload` | longText |  |
| `last_activity` | int, indexed |  |

## Related

[[Database Index]]
