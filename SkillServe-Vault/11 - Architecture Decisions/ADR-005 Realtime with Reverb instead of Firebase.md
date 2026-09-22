---
type: adr
adr: 5
status: accepted
tags: [adr, architecture]
---
# ADR-005 Realtime with Reverb instead of Firebase

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-08-07 (Reverb added), reaffirmed 2026-09 |

## Context

Admin dashboards and mobile notifications/chat should update instantly. The owner wanted realtime built on the Laravel/PostgreSQL backend.

## Decision

Self-hosted Laravel Reverb (Pusher protocol). Admin pages get `admin.data.changed` resource signals; users get private `App.Models.User.{id}` events; chats use presence channels. No Firebase/FCM.

## Consequences

- No third-party push dependency or Google Play Services requirement for delivery while open.
- Closed-app delivery needs another mechanism ([[ADR-006 Closed-App Notifications via WorkManager]]).
- Reverb must run in production (inside the same container behind nginx).

## Evidence

- `PENDING_FIXES.md D3`
- `TEST_PLAN.md design decisions`
- `routes/channels.php`
- `deploy/render/start.sh`

## Related

[[Realtime Architecture]] · [[ADR Index]]
