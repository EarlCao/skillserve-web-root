---
type: table
tags: [database, table, auth]
domain: Auth
soft_deletes: false
---
# personal_access_tokens

Sanctum tokens for admins (`admin-session`), mobile (`client-access`) and background (`client-background`).

- **Model:** `Laravel\Sanctum\PersonalAccessToken`
- **Soft deletes:** no
- **Migrations:** `2026_08_07_053614_create_personal_access_tokens_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `tokenable_type, tokenable_id` | morphs | the user |
| `name` | text | `admin-session` / `client-access` / `client-background` |
| `token` | string(64) unique | SHA-256 of the secret |
| `abilities` | text null | `["*"]` admin, `["client:auth"]`, `["client:notifications"]` |
| `last_used_at` | timestamp null |  |
| `expires_at` | timestamp null, indexed |  |
| `created_at, updated_at` |  | created_at also checked against session timeout |

## Related

[[Token and Session Management]] · [[Database Index]]
