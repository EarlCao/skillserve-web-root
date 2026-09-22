---
type: table
tags: [database, table, platform]
domain: Platform
soft_deletes: false
---
# settings

System Settings values (spatie/laravel-settings table layout).

- **Model:** `backend/app/Modules/Settings/Models/Setting.php`
- **Soft deletes:** no
- **Migrations:** `2022_12_14_083707_create_settings_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `group` | string | general / marketplace / booking / notifications / policies / system |
| `name` | string | setting key |
| `locked` | bool default false |  |
| `payload` | json | value |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(group, name)

## Notes

- Keys and defaults: `config/system-settings.php` → [[System Settings Catalog]].

## Related

[[System Settings]] · [[System Settings Catalog]] · [[Database Index]]
