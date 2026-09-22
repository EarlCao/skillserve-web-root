---
type: table
tags: [database, table, moderation]
domain: Moderation
soft_deletes: true
---
# reports

Polymorphic reports against users, reviews, messages (and services from seed/admin).

- **Model:** `backend/app/Modules/ReportsAndModeration/Models/Report.php`
- **Soft deletes:** yes
- **Migrations:** `2026_09_04_000002_create_reports_table`, `2026_09_21_000001_add_one_open_report_per_subject_index`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `reportable_type, reportable_id` | morphs |  |
| `reporter_id` | FK users null |  |
| `reason` | string(100), indexed | `Report::REASONS` |
| `description` | text null |  |
| `status` | string(20) default 'pending' | pending / investigating / resolved / rejected |
| `investigation_notes` | json null |  |
| `investigated_by/at, resolved_by/at, resolution_note, rejected_by/at, reject_reason` |  |  |
| `moderation_action` | string(30) null | warning / suspend / ban / hide / remove |
| `action_taken_by/at, action_note` |  |  |
| `created_at, updated_at` |  |  |
| `deleted_at, deleted_by` | soft delete |  |

## Indexes & constraints

- index(status)
- index(reason)
- index(reportable_type)
- index(reporter_id)
- partial unique `reports_one_open_per_subject` (reporter_id, reportable_type, reportable_id) WHERE status IN (pending, investigating) AND deleted_at IS NULL

## Foreign keys

- reporter_id and actor FKs → users null on delete

## Related

[[Reports and Moderation Lifecycle]] · [[Database Index]]
