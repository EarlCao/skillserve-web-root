---
type: table
tags: [database, table, data-management]
domain: Data Management
soft_deletes: false
---
# data_archives

Archive records (services) with their previous state.

- **Model:** `backend/app/Modules/DataManagement/Models/DataArchive.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_08_000001_create_data_archives_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `resource_type` | string(50) | `services` |
| `resource_id` | bigint |  |
| `archived_by` | FK users null |  |
| `archived_at` | timestamp, indexed |  |
| `previous_state` | json null |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(resource_type, resource_id)

## Related

[[Data Management]] · [[Data Retention and Deletion]] · [[Database Index]]
