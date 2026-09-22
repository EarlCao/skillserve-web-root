---
type: architecture
tags: [architecture, backend, api]
sources: [backend/bootstrap/app.php, backend/app/Providers/AppServiceProvider.php, backend/app/Shared/Middleware]
---
# Request Lifecycle

What happens to `PATCH /api/bookings/42/cancel` (admin) or a mobile request.

```mermaid
sequenceDiagram
  autonumber
  participant Client
  participant MW as Global + api group middleware
  participant Auth as auth:sanctum
  participant Role as Mobile role middleware
  participant Ctl as Controller
  participant Svc as Service / Action
  participant DB as PostgreSQL
  participant Ev as Events/Listeners
  participant RT as RealtimeChangeTracker
  Client->>MW: HTTP request
  Note over MW: HandleCors (prepended)<br/>throttle:api (60/min user or IP)<br/>SubstituteBindings<br/>ForceJsonResponse, CacheApiResponse, AddRateLimitHeaders
  MW->>Auth: bearer token
  Note over Auth: Sanctum token lookup.<br/>Non client-access tokens also checked<br/>against System Settings session timeout
  Auth->>Role: (client routes) EnsurePlatformAvailable,<br/>EnsureClient / EnsureProvider / EnsureMobileAccount
  Role->>Ctl: FormRequest validates
  Ctl->>Ctl: $this->authorize(...) or can(...) (admin)
  Ctl->>Svc: call service
  Svc->>DB: transaction + lockForUpdate where state changes
  Svc->>Ev: event(new BookingCancelled ...)
  Ev->>DB: activity_log row, notifications rows
  Svc-->>Ctl: model
  Ctl-->>Client: ApiResponder envelope (Resource)
  Note over RT: app->terminating: broadcast AdminDataChanged<br/>(resources changed) on admin.data
```

## Key details

- **Sanctum token validity** (`AppServiceProvider`): for any token whose name is not
  `client-access` (i.e. admin sessions and background tokens), the token must be younger than
  `system.session_timeout_minutes`. Admin tokens also get `expires_at` = login + timeout.
- **Rate limiters:** `api` 60/min per user id or IP; `login` `LOGIN_RATE_LIMIT`/min per IP (default
  5); `client-auth` `CLIENT_AUTH_RATE_LIMIT`/min per IP (default 20) + 10/min per email.
  `/api/health` skips `throttle:api`. See [[Rate Limiting]].
- **Maintenance mode** only affects `/api/client/v1/*` (except `/platform`); the admin API keeps
  working.
- **Concurrency:** state transitions lock the row (`lockForUpdate`) inside
  `HandlesTransactions::transaction()` (e.g. `ProviderBookingService::transition`,
  `DisputeService::lock`, `BookingPaymentService::markPaid`).
- **Idempotency:** booking creation and message sending accept an `Idempotency-Key` header, backed
  by unique indexes (`bookings_client_idempotency_unique`,
  `messages_booking_sender_idempotency_unique`).
- **Caching headers:** GET responses carry an ETag and `private, no-cache` (`API_CACHE_MAX_AGE`
  default 0); a matching `If-None-Match` returns 304.

## Related

[[Backend Architecture]] · [[API Conventions]] · [[Realtime Architecture]]
