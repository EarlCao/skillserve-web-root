---
type: architecture
tags: [architecture, realtime, reverb]
sources: [backend/routes/channels.php, backend/app/Shared/Realtime, backend/app/Modules/ClientCommunication/Events, backend/app/Modules/ClientCommunication/Listeners/BroadcastClientNotification.php, frontend/src/services/echo.js, frontend/src/services/liveUpdates.js, mobile lib/core/services/realtime_client.dart, mobile lib/features/marketplace/views/marketplace_live_sync.dart, mobile lib/features/marketplace/services/catalog_updates.dart]
---
# Realtime Architecture

Realtime runs on **Laravel Reverb** (Pusher protocol), not Firebase
([[ADR-005 Realtime with Reverb instead of Firebase]]). The database stays the source of truth:
every realtime event is a hint to refetch; clients also poll as a fallback.

## Channels (`backend/routes/channels.php`)

| Channel | Type | Who may join | Used by |
|---|---|---|---|
| `admin.data` | private | any account with at least one Spatie role (staff) | Admin Web live refresh |
| `marketplace` | **public** | anyone connected — no auth, guests included (the catalog is public) | Mobile Home, Explore, provider profile and service details live refresh |
| `App.Models.User.{id}` | private | the user with that id; **refused** for background-only tokens (`client:notifications` without `client:auth`) | Admin Web (notifications), Mobile (notifications + chat) |
| `booking-chat.{booking}` | presence | the booking's two participants (reuses `BookingMessagePolicy::viewAny`); member info `{id, name}` | Mobile chat presence + typing |

Channel auth endpoint: `POST|GET /api/broadcasting/auth` with `api` + `auth:sanctum` middleware
(`bootstrap/app.php` → `withBroadcasting`).

## Events

| Event (broadcastAs) | Class | Channel | Delivery | Payload |
|---|---|---|---|---|
| `admin.data.changed` | `App\Shared\Realtime\AdminDataChanged` | `admin.data` | `ShouldBroadcastNow` (immediate, no queue) | `resources: string[]` only — never record data |
| `marketplace.changed` | `App\Shared\Realtime\MarketplaceChanged` | `marketplace` | `ShouldBroadcastNow` (immediate, no queue) | `resources: string[]` only (`services`, `providers`, `categories`, `reviews`, `settings`) |
| `client.notification.created` | `ClientCommunication\Events\ClientNotificationCreated` | `App.Models.User.{userId}` | `ShouldBroadcastNow` (immediate since 2026-10-14; a failed push is logged) | the new notification |
| `client.message.created` | `ClientCommunication\Events\ClientMessageCreated` | `App.Models.User.{receiverId}` | `ShouldBroadcastNow` (immediate since 2026-10-14; a failed push is logged) | `booking_id` + message (with `image_url`) |
| `client.notifications.changed` | `ClientCommunication\Events\ClientNotificationsChanged` | `App.Models.User.{userId}` | `ShouldBroadcastNow` | `{}` — archived/restored/deleted elsewhere |
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

### How the mobile marketplace stays live

The same tracker also collects changes the **public catalog** shows and broadcasts them once per
request as `MarketplaceChanged` on the public `marketplace` channel:

| Model | Resource |
|---|---|
| Service | `services` |
| ServiceCategory, ServiceSubcategory | `categories` |
| ProviderProfile, ProviderPortfolioItem, ProviderAvailability, ProviderBadge | `providers` |
| Review | `reviews` |
| Setting (e.g. "Enable featured services") | `settings` |
| User — only a **provider** account, and only when `name`, `first_name`, `last_name`, `profile_photo_path`, `status`, `suspended_at`, `banned_at`, `banned_until` or `deleted_at` changed, or the user was deleted | `providers` |

A sign-in (`last_login_at`) or token refresh therefore never makes every open app refetch. So a
provider publishing a service (with "Require service approval" off), an administrator approving
one, a new review or a renamed category all reach open apps within a second.

On the phone, `MarketplaceLiveSync` (wraps the app in `main.dart`, inside `NotificationPoller`)
subscribes with `RealtimeClient.listenPublic` while the app is in the foreground, coalesces bursts
(400 ms) and fires `CatalogUpdates.instance.changed(resources)`. `MarketplaceController` (Home),
`DiscoveryController` (Explore rails and the search on screen), `ProviderProfileScreen` and
`ServiceDetailsScreen` listen and refetch **silently** — the lists stay on screen, and a failed
refresh keeps them; only a 404 (the listing or provider is no longer public) replaces an open
detail page with its "no longer available" state. Public channels survive `RealtimeClient.disconnect()` (sign-out ends only the
private and presence channels).

### How mobile notifications work

`Illuminate\Notifications\Events\NotificationSent` → `BroadcastClientNotification` listener →
`ClientNotificationCreated` broadcast. The listener honours System Settings → Notifications →
**Push notifications** (off = stays in the in-app feed only).

## Fallbacks

| Client | While socket down | App closed |
|---|---|---|
| Admin Web | polls all open queries every 15 s (visible tab) | — |
| Mobile | polls unread counts every 30 s; re-checks the marketplace every 60 s, and once on reconnect and on returning to the app | WorkManager every ~15 min with the background token ([[ADR-006 Closed-App Notifications via WorkManager]]) |

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
