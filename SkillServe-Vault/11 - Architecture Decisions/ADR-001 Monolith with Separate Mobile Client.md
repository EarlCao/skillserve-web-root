---
type: adr
adr: 1
status: accepted
tags: [adr, architecture]
---
# ADR-001 Monolith with Separate Mobile Client

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-08-07 (repo layout); restated in TEST_PLAN.md |

## Context

The platform needs an admin console and a customer/provider mobile app over the same data.

## Decision

One Laravel API (`backend/`) serves both the React admin web (`/api/*`, admin Sanctum tokens) and the Flutter app (`/api/client/v1/*`, rotating refresh tokens). No microservices (AGENT.md forbids splitting services).

## Consequences

- Single database and business-rule layer; client modules reuse admin models/actions.
- Two API surfaces with different auth and middleware must be kept apart ([[Authorization and RBAC]]).
- The 2026-09-08 readiness audit explicitly recommended stabilising the monolith rather than rewriting.

## Evidence

- `AGENT.md`
- `TEST_PLAN.md → Design decisions`
- `ADMIN_WEB_MOBILE_READINESS_AUDIT.md §1`
- `backend/app/Modules/ClientMarketplace/Providers/ClientMarketplaceServiceProvider.php`

## Related

[[Architecture Overview]] · [[ADR Index]]
