---
type: adr
adr: 9
status: accepted
tags: [adr, architecture]
---
# ADR-009 No Account Deactivation

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09-21 |

## Context

Mobile requirement M 15.2 asks for account deactivation requests.

## Decision

Accounts are either active or deleted. Self-deletion is a soft delete an admin can restore; purge after 30 days if unreferenced. Administrators (A 15.4) can still be activated/deactivated.

## Consequences

- One clear path instead of two overlapping states.
- M 15.2 is deliberately not implemented and must be defended as a design decision.

## Evidence

- `TEST_PLAN.md (both) → Design decisions`
- `PENDING_FIXES.md M2`

## Related

[[Client Data and Account Control]] · [[Account Status Lifecycle]] · [[ADR Index]]
