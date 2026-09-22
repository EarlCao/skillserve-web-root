---
type: reference
tags: [api, realtime]
sources: [backend/routes/channels.php, frontend/src/services/echo.js, mobile lib/core/services/realtime_client.dart]
---
# Realtime Channels and Events

Client-facing contract for Reverb. Architecture and internals: [[Realtime Architecture]].

## Connecting

| | Admin Web | Mobile |
|---|---|---|
| Library | `laravel-echo` + `pusher-js`, broadcaster `reverb` | custom Pusher-protocol v7 client over `web_socket_channel` |
| URL | `ws(s)://VITE_REVERB_HOST:VITE_REVERB_PORT/app/VITE_REVERB_APP_KEY` | `ws(s)://REVERB_HOST:REVERB_PORT/app/REVERB_APP_KEY?protocol=7&client=skillserve-flutter&version=1.0` |
| Channel auth | `POST {API}/broadcasting/auth` with `Authorization: Bearer` | same |
| Production | host = backend host, port 443, `wss` (nginx routes `/app/*` to Reverb) | same |

## Subscriptions

| Channel | Event | Payload | Subscriber |
|---|---|---|---|
| `private-admin.data` | `.admin.data.changed` | `{ resources: ["bookings", …] }` | Admin Web (`liveUpdates.js`) |
| `private-App.Models.User.{id}` | `.client.notification.created` | stored notification | Admin Web (re-dispatched as `skillserve:realtime-notification`), Mobile |
| `private-App.Models.User.{id}` | `.client.message.created` | `{ booking_id, message }` | Mobile chat |
| `presence-booking-chat.{bookingId}` | members + `client-typing` whisper `{user_id, typing}` | — | Mobile chat |

## Guarantees

- Best effort only; the database is authoritative. Clients refetch on events and poll when the socket
  is down (admin 15 s, mobile 30 s).
- Message realtime is **not** gated by the "message notifications" preference (muting the alert
  must not freeze an open chat); the separate `BookingMessageNotification` is gated.
- Notification broadcasts are gated by System Settings → push notifications.

Related: [[Client Messaging]] · [[Client Notifications]] · [[Realtime Issues]]
