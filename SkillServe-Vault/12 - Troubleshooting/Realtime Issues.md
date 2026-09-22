---
type: troubleshooting
tags: [troubleshooting, realtime]
sources: [backend/routes/channels.php, frontend/src/services/echo.js, frontend/src/services/liveUpdates.js, mobile lib/core/services/realtime_client.dart]
---
# Realtime Issues

| Symptom | Likely cause | Check / fix |
|---|---|---|
| Admin pages only refresh every ~15 s | socket not live → polling fallback | Reverb running? `VITE_REVERB_APP_KEY` = backend `REVERB_APP_KEY`? `VITE_REVERB_HOST/PORT/SCHEME` correct (prod: backend host, 443, https)? |
| `admin.data` subscription refused | account has no staff role, or token invalid | channel requires `roles()->exists()` |
| Phone gets notifications late (~30 s) | socket down, polling fallback | app `REVERB_APP_KEY` define matches backend; wss on 443 in production |
| No realtime notifications at all on phones | queue worker not running (`ClientNotificationCreated` / `ClientMessageCreated` are **queued** broadcasts) or push setting off | run `queue:work`; System Settings → Notifications → Push |
| Closed-app notifications stop after a day | KI-01 (background token hits session timeout) | sign out/in as a workaround; fix per [[Known Issues and Gaps]] |
| Presence/typing not shown | not a booking participant, or background token used | `booking-chat.{id}` uses `BookingMessagePolicy::viewAny` |
| `App.Models.User.{id}` refused for the background task | by design | background token may only poll `/notifications/background` |
| Realtime works locally, not on Windows | `localhost` → `::1` in WSL | configs rewrite `localhost` to `127.0.0.1` |

Related: [[Realtime Architecture]] · [[Realtime Channels and Events]]
