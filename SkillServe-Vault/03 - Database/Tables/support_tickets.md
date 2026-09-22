---
type: table
tags: [database, table, support]
domain: Support
soft_deletes: true
---
# support_tickets

Support tickets from customers and providers.

- **Model:** `backend/app/Modules/Support/Models/SupportTicket.php`
- **Soft deletes:** yes
- **Migrations:** `2026_09_08_000003_create_support_tickets_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `ticket_number` | string(32) unique | `SUP-` + 12 chars |
| `requester_id` | FK users null |  |
| `subject` | string(160) |  |
| `description` | text |  |
| `category` | string(40) default 'general' |  |
| `priority` | string(20) default 'normal' | low / normal / high / urgent |
| `status` | string(20) default 'open' | open / in_progress / resolved |
| `assigned_to, assigned_by` | FK users null |  |
| `assigned_at` |  |  |
| `resolved_by, resolved_at, resolution_note` |  |  |
| `created_at, updated_at` |  |  |
| `deleted_at` | soft delete |  |

## Indexes & constraints

- index(status)
- index(priority)
- index(category)
- index(assigned_to)
- index(requester_id)
- index(created_at)
- index(status, priority)

## Related

[[support_ticket_messages]] · [[Support Ticket Lifecycle]] · [[Database Index]]
