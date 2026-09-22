---
type: adr
adr: 11
status: accepted
tags: [adr, architecture]
---
# ADR-011 Philippine Peso Currency

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09-17 |

## Context

The platform operates in the Philippines; early data defaulted to USD.

## Decision

`currency` default `PHP` on services and bookings (existing USD rows rewritten to PHP without amount conversion); frontend `DEFAULT_CURRENCY = 'PHP'` with `formatCurrency`.

## Consequences

- Single-currency platform.
- Historic USD amounts were relabelled, not converted.

## Evidence

- migration 2026_09_17_000001
- `frontend/src/constants/index.js`
- `CLAUDE.md`

## Related

[[services]] · [[bookings]] · [[ADR Index]]
