---
type: architecture
tags: [architecture, realtime, reverb]
sources: [backend/routes/channels.php, backend/app/Shared/Realtime, backend/app/Modules/ClientCommunication/Events, backend/app/Modules/ClientCommunication/Listeners/BroadcastClientNotification.php, frontend/src/services/echo.js, frontend/src/services/liveUpdates.js, mobile lib/core/services/realtime_client.dart]
---
# Realtime Architecture

Realtime runs on **Laravel Reverb** (Pusher protocol), not Firebase
([[ADR-005 Realtime with Reverb instead of Firebase]]). The database stays the source of truth:
every realtime event is a hint to refetch; clients also poll as a fallback.

## Channels (`backend/routes/channels.php`)

| Channel | Type | Who may join | Used by |
|---|---|---|---|
| `admin.data` | private | any account with at least one Spatie role (staff) | Admin Web live refresh |
| `App.Models.User.{id}` | private | the user with that id; **refused** for background-only tokens (`client:notifications` without `client:auth`) | Admin Web (notifications), Mobile (notifications + chat) |
| `booking-chat.{booking}` | presence | the booking's two participants (reuses `BookingMessagePolicy::viewAny`); member info `{id, name}` | Mobile chat presence + typing |

Channel auth endpoint: `POST|GET /api/broadcasting/auth` with `api` + `auth:sanctum` middleware
(`bootstrap/app.php` → `withBroadcasting`).

## Events

| Event (broadcastAs) | Class | Channel | Delivery | Payload |
|---|---|---|---|---|
| `admin.data.changed` | `App\Shared\Realtime\AdminDataChanged` | `admin.data` | `ShouldBroadcastNow` (immediate, no queue) | `resources: string[]` only — never record data |
| `client.notification.created` | `ClientCommunication\Events\ClientNotificationCreated` | `App.Models.User.{userId}` | `ShouldBroadcast` (**queued**) | the new notification |
| `client.message.created` | `ClientCommunication\Events\ClientMessageCreated` | `App.Models.User.{receiverId}` | `ShouldBroadcast` (**queued**) | `booking_id` + message |
| `client-typing` (whisper) | client event | `presence-booking-chat.{id}` | peer-to-peer via Reverb | `{user_id, typing}` |

### How admin "data changed" works

1. `AppServiceProvider` listens to `eloquent.created|updated|deleted|restored: *` and to
   administrator/role events (pivot writes fire no model events).
2. `RealtimeChangeTracker` (scoped per request) maps models to resource names: User→`users`,
   ProviderProfile/VerificationRequest/VerificationDocument→`providers`, ProviderBadge→
   `provider-recognition`, ServiceCategory/Subcategory→`service-categories`, Service→`services`,
   Booking→`bookings`, Message→`messages`, Review→`reviews`, Report→`reports`,
   SupportTicket(+Message)→`support-tickets`, Announcement→`notifications`, Setting→`settings`,
   DataArchive→`data-management`, Activity→`audit`, Role/Permission→`roles`.
3. On `app->terminating` and `Queue::after`, it broadcasts one `AdminDataChanged`. Writes during a
   read are skipped (loop protection); a missing WebSocket server never fails the request.
4. The SPA maps resources to React Query keys and invalidates them ([[Admin Web Frontend Architecture]]).

### How mobile notifications work

`Illuminate\Notifications\Events\NotificationSent` → `BroadcastClientNotification` listener →
`ClientNotificationCreated` broadcast. The listener honours System Settings → Notifications →
**Push notifications** (off = stays in the in-app feed only).

## Fallbacks

| Client | While socket down | App closed |
|---|---|---|
| Admin Web | polls all open queries every 15 s (visible tab) | — |
| Mobile | polls unread counts every 30 s | WorkManager every ~15 min with the background token ([[ADR-006 Closed-App Notifications via WorkManager]]) |

## Configuration

| Side | Keys |
|---|---|
| Backend | `BROADCAST_CONNECTION=reverb`, `REVERB_APP_ID/KEY/SECRET`, `REVERB_HOST/PORT/SCHEME` (where Laravel publishes), `REVERB_SERVER_HOST/PORT` (where Reverb listens) |
| Admin Web | `VITE_REVERB_APP_KEY/HOST/PORT/SCHEME` |
| Mobile | `--dart-define=REVERB_APP_KEY/HOST/PORT/SCHEME` |
| Production | `start.sh` forces Laravel→Reverb to `127.0.0.1:8080` inside the container; clients use the public host on 443 via nginx (`/app/*`) |

> [!bug] Key defaults disagree
> Local `.env`: `skillserve-local-key`; admin web fallback: `5854c89dcedeece0181cb0c6cb75c711`;
> mobile fallback: `skillserve`. Every environment must set the key explicitly on all three sides.
> See [[Known Issues and Gaps]].

> [!warning] Stale statements elsewhere
> `DEPLOYMENT.md` → Troubleshooting says "The mobile app has no WebSocket connection; it checks
> unread-count every 30 seconds" — outdated: the app now has a Reverb client. The
> `AdminDataChanged` docblock says "production runs no queue worker", but `start.sh` does run one.

## Related

[[Background Jobs and Scheduling]] · [[Realtime Channels and Events]] · [[Realtime Issues]]
