---
type: table
tags: [database, table, mobile]
domain: Mobile
soft_deletes: false
---
# client_preferences

Per-account app preferences (absent row = defaults).

- **Model:** `backend/app/Modules/ClientPreferences/Models/ClientPreference.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_20_000003_create_client_preferences_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `user_id` | FK users unique |  |
| `booking_notifications, service_notifications, message_notifications, announcement_notifications` | bool default true | mute categories |
| `private_profile` | bool default false | hides provider from discovery |
| `activity_personalization` | bool default true |  |
| `reduce_motion` | bool default false |  |
| `theme` | string(10) default 'system' | light / dark / system (CHECK on pgsql) |
| `created_at, updated_at` |  |  |

## Foreign keys

- user_id → users cascade on delete

## Related

[[Client Settings and Preferences]] · [[Notifications Catalog]] · [[Database Index]]
