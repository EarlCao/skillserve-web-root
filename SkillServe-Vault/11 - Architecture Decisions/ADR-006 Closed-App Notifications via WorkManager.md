---
type: adr
adr: 6
status: accepted
tags: [adr, architecture]
---
# ADR-006 Closed-App Notifications via WorkManager

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09-21 |

## Context

Without Firebase, the app gets nothing while closed.

## Decision

Issue a narrow read-only background token (`client:notifications`); Android WorkManager polls `GET /client/v1/notifications/background` about every 15 minutes and posts local notifications. The token can't refresh the session or join channels.

## Consequences

- Not instant (≥15 min, OS may stretch it); force-stopped apps get nothing until reopened.
- Separate token avoids collisions with the rotating refresh token.
- Currently undermined by KI-01 (session timeout applied to the background token).

## Evidence

- `core/services/background_notifications.dart`
- `ClientCommunication/Services/BackgroundNotificationService.php`
- `PENDING_FIXES.md (Earlier on 2026-09-21)`

## Related

[[Client Notifications]] · [[Known Issues and Gaps]] · [[ADR Index]]
