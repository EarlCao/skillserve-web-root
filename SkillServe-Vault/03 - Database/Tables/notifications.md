---
type: table
tags: [database, table, notifications]
domain: Notifications
soft_deletes: false
---
# notifications

Laravel database notifications (in-app feed for every account).

- **Model:** `Illuminate\Notifications\DatabaseNotification`
- **Soft deletes:** no
- **Migrations:** `2026_09_05_000005_create_notifications_table`, `2026_10_13_000005_add_archived_at_to_notifications`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | uuid PK |  |
| `type` | string | notification class |
| `notifiable_type, notifiable_id` | morphs |  |
| `data` | text | JSON payload |
| `read_at` | timestamp null |  |
| `archived_at` | timestamp null | set by the mobile archive; archived rows are read and left out of the feed and unread count |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(notifiable_type, notifiable_id, read_at)
- `notifications_notifiable_archived_index` (notifiable_type, notifiable_id, archived_at)

## Related

[[Notifications Catalog]] · [[Client Notifications]] · [[Database Index]]
