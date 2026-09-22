---
type: adr
adr: 10
status: accepted
tags: [adr, architecture]
---
# ADR-010 UTC Storage with Manila Business Time

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09-21 |

## Context

Provider hours and booking times were misinterpreted across timezones (PENDING_FIXES C2).

## Decision

Store UTC (`APP_TIMEZONE=UTC`); interpret wall-clock rules in `BUSINESS_TIMEZONE=Asia/Manila` via `BusinessTime`; offset-less input is Manila time; the app sends UTC ISO-8601.

## Consequences

- Correct overlap/hours checks; consistent notifications text.
- System Settings timezone is read-only to avoid a second conflicting value.

## Evidence

- `app/Shared/Helpers/BusinessTime.php`
- `PENDING_FIXES.md C2, L2, L5`

## Related

[[Time and Timezone Rules]] · [[ADR Index]]
