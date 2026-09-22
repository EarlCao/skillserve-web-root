---
type: table
tags: [database, table, framework]
domain: Framework
soft_deletes: false
---
# Queue Tables

`jobs`, `job_batches`, `failed_jobs` for the database queue (`QUEUE_CONNECTION=database`).

- **Model:** `—`
- **Soft deletes:** no
- **Migrations:** `0001_01_01_000002_create_jobs_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `jobs` | id, queue(idx), payload, attempts, reserved_at, available_at, created_at |  |
| `job_batches` | id PK, name, totals, failed_job_ids, options, cancelled_at, created_at, finished_at |  |
| `failed_jobs` | id, uuid unique, connection, queue, payload, exception, failed_at | index(connection, queue, failed_at) |

## Related

[[Background Jobs and Scheduling]] · [[Database Index]]
