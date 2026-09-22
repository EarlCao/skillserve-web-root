---
type: table
tags: [database, table, audit]
domain: Audit
soft_deletes: false
---
# activity_log

Spatie activity log — the audit trail read by Security and Audit Logs, booking/dispute history and user moderation history.

- **Model:** `Spatie\Activitylog\Models\Activity`
- **Soft deletes:** no
- **Migrations:** `2026_08_07_053623_create_activity_log_table`, `…053624_add_event_column`, `…053625_add_batch_uuid_column`, `2026_09_05_000015_add_audit_log_query_indexes`, `2026_09_05_000016_add_audit_action_index`, `2026_09_08_000009_add_activity_subject_history_index`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `log_name` | string null, indexed | per module, e.g. `system_settings`, `service_categories` |
| `description` | text | action |
| `subject_type, subject_id` | nullable morphs |  |
| `event` | string null |  |
| `causer_type, causer_id` | nullable morphs | actor |
| `properties` | json null | details incl. IP / user agent for auth events |
| `batch_uuid` | uuid null |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(log_name)
- index(created_at)
- index(causer_type, causer_id, created_at)
- index(description, created_at)
- index(log_name, subject_type, subject_id, created_at)

## Related

[[Security and Audit Logs]] · [[Audit Logging]] · [[Database Index]]
