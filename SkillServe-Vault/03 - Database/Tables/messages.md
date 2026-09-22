---
type: table
tags: [database, table, communication]
domain: Communication
soft_deletes: true
---
# messages

Booking-scoped chat messages (also reportable).

- **Model:** `backend/app/Modules/ReportsAndModeration/Models/Message.php`
- **Soft deletes:** yes
- **Migrations:** `2026_09_04_000001_create_messages_table`, `2026_09_08_000008_add_read_state_and_idempotency_to_messages`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `sender_id, receiver_id` | FK users |  |
| `booking_id` | FK bookings null |  |
| `content` | text |  |
| `status` | string(20) default 'active' | active / removed |
| `removed_by, removed_at` |  | moderation |
| `read_at` | timestamp null |  |
| `client_idempotency_key` | string(100) null |  |
| `created_at, updated_at` |  |  |
| `deleted_at, deleted_by` | soft delete |  |

## Indexes & constraints

- index(status)
- index(booking_id)
- index(sender_id, receiver_id)
- index(receiver_id, read_at)
- unique(booking_id, sender_id, client_idempotency_key)

## Foreign keys

- sender_id, receiver_id → users **restrict**
- booking_id → bookings null on delete

## Related

[[Client Messaging]] · [[reports]] · [[Database Index]]
