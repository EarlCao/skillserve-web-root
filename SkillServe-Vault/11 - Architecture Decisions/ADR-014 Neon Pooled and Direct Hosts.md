---
type: adr
adr: 14
status: accepted
tags: [adr, architecture]
---
# ADR-014 Neon Pooled and Direct Hosts

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09 (config/database.php) |

## Context

Neon's pooled endpoint (pgBouncer, transaction mode) breaks migrations (`SQLSTATE[25P02]`).

## Decision

Use the pooler host for queries and derive a direct host (strip `-pooler`, or `DB_DIRECT_HOST`) for migrations/DDL via a `pgsql.direct` connection.

## Consequences

- Migrations work on every boot; no manual host juggling.
- Hosts must be bare hostnames; `DB_URL` must stay unset.

## Evidence

- `backend/config/database.php`
- `DEPLOYMENT.md troubleshooting`

## Related

[[NeonDB]] · [[ADR Index]]
