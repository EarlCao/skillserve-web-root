---
type: table
tags: [database, table, support]
domain: Support
soft_deletes: false
---
# support_ticket_messages

Thread messages on a ticket (requester and staff).

- **Model:** `backend/app/Modules/Support/Models/SupportTicketMessage.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_08_000003_create_support_tickets_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `support_ticket_id` | FK |  |
| `author_id` | FK users null |  |
| `body` | text |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(support_ticket_id, created_at)

## Foreign keys

- support_ticket_id → support_tickets cascade on delete

## Related

[[support_tickets]] · [[Database Index]]
