---
type: adr
adr: 17
status: accepted
tags: [adr, architecture]
---
# ADR-017 Separate Customer and Provider Shells

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09-17 onwards |

## Context

Customers and providers have different workflows and permissions in one app.

## Decision

Two shells (`/client`, `/provider`) and a route guard (`redirectFor`) that assigns every route to customer-only, provider-only, shared, marketplace or signed-out sets; the API enforces the same split (`EnsureClient`, `EnsureProvider`). Owner requirement: keep them separate and role-guarded.

## Consequences

- Clear UX per role; providers don't shop as customers (read-only preview allowed).
- Every new route must be classified or it is reachable by both roles.

## Evidence

- `lib/routes/app_router.dart`
- mobile TEST_PLAN.md design decisions

## Related

[[Mobile App Architecture]] · [[ADR Index]]
