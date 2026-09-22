---
type: table
tags: [database, table, framework-auth]
domain: Framework / auth
soft_deletes: false
---
# password_reset_tokens

Laravel password broker tokens (admin `admins` broker and mobile reset).

- **Model:** `—`
- **Soft deletes:** no
- **Migrations:** `0001_01_01_000000_create_users_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `email` | string PK |  |
| `token` | string | hashed |
| `created_at` | timestamp null |  |

## Notes

- Admin reset uses a separate `admins` password broker (`PasswordService`).

## Related

[[Admin Authentication]] · [[Client Authentication and Account]] · [[Database Index]]
