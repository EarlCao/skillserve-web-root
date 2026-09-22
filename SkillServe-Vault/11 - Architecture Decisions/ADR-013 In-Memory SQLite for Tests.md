---
type: adr
adr: 13
status: accepted
tags: [adr, architecture]
---
# ADR-013 In-Memory SQLite for Tests

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-08-07 |

## Context

Docker injects pgsql env vars; `RefreshDatabase` could wipe the live local database.

## Decision

`tests/TestCase.php` forces `sqlite` / `:memory:` in putenv, `$_ENV` and `$_SERVER` before boot; every test must extend it.

## Consequences

- Fast, isolated tests; zero risk to the dev DB.
- PostgreSQL-specific behaviour is untested (partial indexes, CHECKs); pgsql-only migration SQL is guarded by driver checks.

## Evidence

- `backend/tests/TestCase.php`
- `CLAUDE.md`

## Related

[[Testing Strategy]] · [[ADR Index]]
