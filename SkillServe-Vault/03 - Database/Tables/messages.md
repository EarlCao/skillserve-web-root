---
type: table
tags: [database, table, communication]
domain: Communication
soft_deletes: true
---
# messages

Chat messages (also reportable): a booking's chat (`booking_id`) or a conversation before booking
([[inquiries]], `inquiry_id`) — never both (Postgres check `messages_one_thread_check`).

- **Model:** `backend/app/Modules/ReportsAndModeration/Models/Message.php`
- **Soft deletes:** yes
- **Migrations:** `2026_09_04_000001_create_messages_table`, `2026_09_08_000008_add_read_state_and_idempotency_to_messages`, `2026_10_13_000004_add_image_to_messages`, `2026_10_14_000002_create_inquiries_and_link_messages`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `sender_id, receiver_id` | FK users |  |
| `booking_id` | FK bookings null |  |
| `inquiry_id` | FK inquiries null | set instead of `booking_id` before a booking |
| `content` | text | empty when the message is a photo alone |
| `image_path` | string null | photo on the private `message_images` disk; never exposed — read via `image_url` |
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
- unique(inquiry_id, sender_id, client_idempotency_key) — `messages_inquiry_sender_idempotency_unique`
- check `num_nonnulls(booking_id, inquiry_id) <= 1` (PostgreSQL)

## Foreign keys

- sender_id, receiver_id → users **restrict**
- booking_id → bookings null on delete
- inquiry_id → inquiries null on delete

## Related

[[Client Messaging]] · [[inquiries]] · [[reports]] · [[Database Index]]
