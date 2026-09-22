---
type: adr
adr: 16
status: accepted
tags: [adr, architecture]
---
# ADR-016 Soft Delete with 30-Day Purge

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09-08 |

## Context

Admins need to review/restore deleted data, but data should not live forever and FKs cascade.

## Decision

Soft deletes on business tables; Data Management lists, restores or permanently deletes them; a daily command purges records deleted >30 days ago unless dependents exist.

## Consequences

- Mistakes are recoverable for 30 days.
- Records referenced by bookings/reviews/messages are never purged automatically.

## Evidence

- `config/data-management.php`
- DataManagementService::DEPENDENTS
- PurgeExpiredDeletedRecords

## Related

[[Data Retention and Deletion]] · [[ADR Index]]
