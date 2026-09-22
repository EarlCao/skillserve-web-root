---
type: adr
adr: 15
status: accepted
tags: [adr, architecture]
---
# ADR-015 Swagger Attributes and Generated API Docs

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-08-07 (l5-swagger), 2026-09-10 (api-docs generator) |

## Context

The mobile team needed an accurate, current API reference.

## Decision

Document endpoints with PHP 8 `#[OA\...]` attributes (l5-swagger v11 ignores docblocks); generate `api-docs/openapi.json` + per-module markdown with `api-docs/generate.php`; copy into the Flutter repo. The vault adds generated endpoint notes from the live route table.

## Consequences

- Docs follow code if regenerated; forgetting to regenerate causes drift.
- Swagger UI hidden in production by default.

## Evidence

- `CLAUDE.md`
- `api-docs/generate.php`
- `.claude/skills/sync-api-docs`

## Related

[[API Documentation Pipeline]] · [[ADR Index]]
