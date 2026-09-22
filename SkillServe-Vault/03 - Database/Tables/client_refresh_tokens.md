---
type: table
tags: [database, table, auth]
domain: Auth
soft_deletes: false
---
# client_refresh_tokens

Rotating mobile refresh tokens with family-based reuse detection.

- **Model:** `backend/app/Modules/ClientAuthentication/Models/ClientRefreshToken.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_08_000005_create_client_refresh_tokens_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | uuid PK |  |
| `user_id` | FK users |  |
| `family_id` | uuid, indexed | a login session |
| `token_hash` | string(64) unique | SHA-256 |
| `replaced_by` | uuid null, indexed |  |
| `expires_at` | timestamp, indexed | sliding window, default 1 year |
| `revoked_at` | timestamp null, indexed |  |
| `created_at, updated_at` |  |  |

## Foreign keys

- user_id → users **restrict on delete**

## Related

[[Token and Session Management]] · [[Database Index]]
