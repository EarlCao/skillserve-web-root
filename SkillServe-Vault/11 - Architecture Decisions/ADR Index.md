---
type: index
tags: [index, adr]
---
# ADR Index

Architecture Decision Records. None existed in the repos; these were **reconstructed** from the code,
`TEST_PLAN.md` design decisions, `PENDING_FIXES.md`, `DEPLOYMENT.md`, `CLAUDE.md` and git history.
New decisions: copy [[Template - ADR]] and add a row.

| # | Decision | First evidence |
|---|---|---|
| 001 | [[ADR-001 Monolith with Separate Mobile Client]] | 2026-08-07 (repo layout); restated in TEST_PLAN.md |
| 002 | [[ADR-002 Modules as Plain Namespaces]] | 2026-08-07 |
| 003 | [[ADR-003 Sanctum Bearer Tokens with Rotating Mobile Refresh]] | 2026-08-07 (admin), 2026-09-08 (client refresh tokens) |
| 004 | [[ADR-004 Spatie RBAC with role_id Account Types]] | 2026-08-07 (Spatie), 2026-09-18 (role_id) |
| 005 | [[ADR-005 Realtime with Reverb instead of Firebase]] | 2026-08-07 (Reverb added), reaffirmed 2026-09 |
| 006 | [[ADR-006 Closed-App Notifications via WorkManager]] | 2026-09-21 |
| 007 | [[ADR-007 Payments Recorded Not Processed]] | 2026-09-21 |
| 008 | [[ADR-008 Uploads on Render Persistent Disk]] | 2026-09-21 |
| 009 | [[ADR-009 No Account Deactivation]] | 2026-09-21 |
| 010 | [[ADR-010 UTC Storage with Manila Business Time]] | 2026-09-21 |
| 011 | [[ADR-011 Philippine Peso Currency]] | 2026-09-17 |
| 012 | [[ADR-012 Docker Host Networking]] | 2026-08-07 |
| 013 | [[ADR-013 In-Memory SQLite for Tests]] | 2026-08-07 |
| 014 | [[ADR-014 Neon Pooled and Direct Hosts]] | 2026-09 (config/database.php) |
| 015 | [[ADR-015 Swagger Attributes and Generated API Docs]] | 2026-08-07 (l5-swagger), 2026-09-10 (api-docs generator) |
| 016 | [[ADR-016 Soft Delete with 30-Day Purge]] | 2026-09-08 |
| 017 | [[ADR-017 Separate Customer and Provider Shells]] | 2026-09-17 onwards |
| 018 | [[ADR-018 Blind Index for National ID Uniqueness]] | 2026-09-24 |
| 019 | [[ADR-019 Payment Gateway Abstraction with PayMongo Deferred]] | 2026-09-24 |

Back to [[Home]]
