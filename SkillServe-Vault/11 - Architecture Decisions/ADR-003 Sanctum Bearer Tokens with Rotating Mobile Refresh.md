---
type: adr
adr: 3
status: accepted
tags: [adr, architecture]
---
# ADR-003 Sanctum Bearer Tokens with Rotating Mobile Refresh

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-08-07 (admin), 2026-09-08 (client refresh tokens) |

## Context

Admin SPA and mobile app need stateless API auth; mobile users should stay signed in until they sign out.

## Decision

Sanctum personal access tokens. Admin: one token per login, lifetime = System Settings session timeout, stored in localStorage. Mobile: 60-min access token + opaque refresh token rotated on every use with family-based reuse detection, sliding window of 1 year; tokens in platform secure storage.

## Consequences

- No cookies/CSRF for the API; admin token exposure mitigated by CSP and short timeout.
- Mobile sessions effectively never expire while used; server can end them (password change, suspension, deletion, token reuse).
- Side effect found: the session-timeout rule also hits the background token (KI-01).

## Evidence

- `backend/app/Modules/ClientAuthentication/Services/ClientSessionService.php`
- `backend/config/client-auth.php`
- AppServiceProvider (Sanctum callback)
- `PENDING_FIXES.md (refresh window change)`

## Related

[[Token and Session Management]] · [[Authentication Flows]] · [[ADR Index]]
