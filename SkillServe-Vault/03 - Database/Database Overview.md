---
type: architecture
tags: [database, postgres]
sources: [docker-compose.yml, backend/config/database.php, backend/tests/TestCase.php, backend/phpunit.xml, DEPLOYMENT.md]
---
# Database Overview

| Environment | Engine | Connection |
|---|---|---|
| Local | PostgreSQL 17 (`postgres:17-alpine`, container `group6-db`) | `127.0.0.1:5433`, db `group6_db`, user `group6` (local-only credentials in `docker-compose.yml`), listens on loopback only |
| Production | **NeonDB** PostgreSQL | `DB_HOST` = Neon **pooler** host; migrations/DDL use the **direct** host (derived by stripping `-pooler`, or `DB_DIRECT_HOST`); `DB_SSLMODE=require` |
| Tests | **SQLite in-memory** | forced by `tests/TestCase.php` before boot |

Open a shell locally: `docker compose exec db psql -U group6 -d group6_db`.

## Conventions observed in migrations

- `bigint` identity PKs; UUID PKs for `notifications` and `client_refresh_tokens`.
- Money `decimal(10,2)`, ratings `decimal(3,2)`, `currency` char(3) default `PHP`.
- Status columns are **strings**, not enums; allowed values are enforced by Form Requests. PostgreSQL
  `CHECK` constraints exist only on `announcements.target/status` and `client_preferences.theme`
  (skipped on SQLite).
- Soft deletes + `deleted_by` on business tables ([[Data Retention and Deletion]]).
- Actor columns (`created_by`, `*_by`) are FKs to `users` with `nullOnDelete`.
- Foreign keys to parents are mostly **cascade** (bookings → services/users/profiles, services →
  profiles/categories); reviews and messages use **restrict**. Force-deletes are guarded in
  application code (Data Management dependents).
- Idempotency via unique indexes (`bookings_client_idempotency_unique`,
  `messages_booking_sender_idempotency_unique`).
- PostgreSQL-only SQL: partial unique index `reports_one_open_per_subject`.
- Permissions are seeded partly by **data migrations** (`add_*_permissions`) and fully by
  `RolePermissionSeeder`.

## Testing caveat

Tests run on SQLite, so PostgreSQL-specific behaviour (CHECK constraints, partial indexes, `ILIKE`,
JSON operators, pgBouncer transaction mode) is **not** exercised by the automated suite. Every test
must extend `Tests\TestCase`, which forces SQLite so `RefreshDatabase` can never wipe the live
database ([[ADR-013 In-Memory SQLite for Tests]]).

## Migration safety rules (project policy)

From AGENT.md / CLAUDE.md: migrations must be backward-compatible and additive where possible;
explain data impact, deploy order and rollback for each; the production container runs
`php artisan migrate --force` on every start, so a bad migration blocks boot. Deploy the backend
before any client that depends on a new column. See [[Release Workflow]].

> [!danger] Destructive scripts
> `scripts/fresh-demo.sh` and `scripts/fresh-admin.sh` run `migrate:fresh` — they **wipe** the
> database. Never run them against anything but a disposable local database.

## Related

[[Entity Relationship Diagram]] · [[Migrations Timeline]] · [[NeonDB]]
