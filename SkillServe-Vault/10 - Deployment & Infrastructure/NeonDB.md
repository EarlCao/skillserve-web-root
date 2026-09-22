---
type: reference
tags: [deployment, database, neon]
sources: [DEPLOYMENT.md, backend/config/database.php]
---
# NeonDB

Production PostgreSQL. Connection is configured with separate `DB_*` variables — **not** `DB_URL`
(when set, Laravel parses it and ignores the others).

## Pooler vs direct host

| Host | Example shape | Used for |
|---|---|---|
| `DB_HOST` | `ep-xxx-pooler.<region>.aws.neon.tech` | normal queries (pgBouncer, transaction mode) |
| direct | `ep-xxx.<region>.aws.neon.tech` | migrations / DDL |

`config/database.php` derives the direct host by stripping `-pooler` from `DB_HOST` unless
`DB_DIRECT_HOST` is set (a `DB_DIRECT_HOST` that still contains `-pooler` is ignored) and exposes it as
the `pgsql.direct` connection; with a direct endpoint configured, prepares are emulated on the
pooled connection. Why: pgBouncer transaction mode can't run the DDL and server-side prepared
statements migrations need → `SQLSTATE[25P02] current transaction is aborted` (the error names the
*second* statement).

Both hosts must be **bare hostnames** (no `/db?sslmode=…`), else "could not translate host name".
`DB_SSLMODE=require`, port 5432.

## Free-tier limits (as recorded in DEPLOYMENT.md)

0.25 CPU / 1 GB RAM, 512 MB storage, 100 connections, 10 branches, 1 project.

**Needs Verification:** the plan actually in use and whether Neon branches are used for dev/staging
(DEPLOYMENT.md's diagram mentions a "dev branch" option, but the release workflow is main-only).

Related: [[Database Overview]] · [[Deployment Issues]] · [[ADR-014 Neon Pooled and Direct Hosts]]
