---
type: table
tags: [database, table, moderation]
domain: Moderation
soft_deletes: false
---
# report_attachments

Photos a reporter sent as proof with a report (mobile). Files live on the private
`report_attachments` disk; moderators open them through `GET /api/reports/{report}/attachments/{attachment}`.

- **Model:** `backend/app/Modules/ReportsAndModeration/Models/ReportAttachment.php` (`MAX_PER_REPORT` = 5)
- **Soft deletes:** no
- **Migrations:** `2026_10_13_000006_create_report_and_support_attachments_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `report_id` | FK reports | cascade on (hard) delete |
| `uploaded_by` | FK users null | null on delete |
| `path` | string | private; hidden from serialisation |
| `mime_type` | string(100) |  |
| `size_bytes` | unsigned int |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(report_id)

## Related

[[reports]] · [[Client Reports]] · [[Reports and Moderation]] · [[Database Index]]
