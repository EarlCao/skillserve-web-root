---
type: table
tags: [database, table, support]
domain: Support
soft_deletes: false
---
# support_ticket_attachments

Photos (screenshots, proof) the requester sent with a support ticket or one of its replies. Files
live on the private `support_attachments` disk; staff open them through
`GET /api/support/tickets/{ticket}/attachments/{attachment}`.

- **Model:** `backend/app/Modules/Support/Models/SupportTicketAttachment.php` (`MAX_PER_POST` = 5)
- **Soft deletes:** no
- **Migrations:** `2026_10_13_000006_create_report_and_support_attachments_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `support_ticket_id` | FK support_tickets | cascade on (hard) delete |
| `support_ticket_message_id` | FK support_ticket_messages null | null = sent with the ticket itself; cascade |
| `uploaded_by` | FK users null | null on delete |
| `path` | string | private; hidden from serialisation |
| `mime_type` | string(100) |  |
| `size_bytes` | unsigned int |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(support_ticket_id)
- index(support_ticket_message_id)

## Related

[[support_tickets]] · [[support_ticket_messages]] · [[Client Support]] · [[Support Management]] · [[Database Index]]
