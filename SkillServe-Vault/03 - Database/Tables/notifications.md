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
- **Migrations:** `2026_09_05_000005_create_notifications_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | uuid PK |  |
| `type` | string | notification class |
| `notifiable_type, notifiable_id` | morphs |  |
| `data` | text | JSON payload |
| `read_at` | timestamp null |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(notifiable_type, notifiable_id, read_at)

## Related

[[Notifications Catalog]] · [[Client Notifications]] · [[Database Index]]
