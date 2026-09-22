---
type: table
tags: [database, table, framework]
domain: Framework
soft_deletes: false
---
# cache and cache_locks

Database cache store (`CACHE_STORE=database`) incl. rate-limiter counters and Spatie permission cache.

- **Model:** `—`
- **Soft deletes:** no
- **Migrations:** `0001_01_01_000001_create_cache_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `cache.key` | string PK |  |
| `cache.value` | mediumText |  |
| `cache.expiration` | bigint indexed |  |
| `cache_locks.key` | string PK |  |
| `cache_locks.owner` | string |  |
| `cache_locks.expiration` | bigint indexed |  |

## Related

[[Database Index]]
