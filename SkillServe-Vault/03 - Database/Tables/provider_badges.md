---
type: table
tags: [database, table, recognition]
domain: Recognition
soft_deletes: false
---
# provider_badges

Badge definitions.

- **Model:** `backend/app/Modules/ProviderRecognition/Models/ProviderBadge.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_05_000011_create_provider_badges_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `name` | string(100) |  |
| `slug` | string(120) unique |  |
| `description` | text null |  |
| `color` | string(30) default 'primary' |  |
| `is_active` | bool default true, indexed |  |
| `created_at, updated_at` |  |  |

## Related

[[provider_badge_assignments]] · [[Provider Recognition]] · [[Database Index]]
