---
type: table
tags: [database, table, notifications]
domain: Notifications
soft_deletes: false
---
# announcements

Admin announcements, immediate or scheduled.

- **Model:** `backend/app/Modules/Notifications/Models/Announcement.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_05_000004_create_announcements_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `created_by` | FK users null |  |
| `title` | string(160) |  |
| `message` | text |  |
| `target` | string(20) | all / customers / providers / selected (CHECK on pgsql) |
| `recipient_ids` | json null |  |
| `recipient_count` | uint default 0 |  |
| `status` | string(20) default 'sent' | pending / scheduled / sent / failed (CHECK on pgsql) |
| `scheduled_at, sent_at` | timestamp null |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(status, scheduled_at)
- index(created_by)
- CHECK announcements_target_check, announcements_status_check (PostgreSQL only)

## Related

[[Notifications and Announcements]] · [[notifications]] · [[Database Index]]
