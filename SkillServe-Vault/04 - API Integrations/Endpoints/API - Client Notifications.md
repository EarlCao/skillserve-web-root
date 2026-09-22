---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Client Notifications

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Notification feed, read state and the background (closed-app) token.

Feature note: [[Client Notifications]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/client/v1/notifications` | `ClientCommunication::ClientNotificationController@index` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/notifications/background` | `ClientCommunication::ClientNotificationController@background` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureBackgroundNotificationToken` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/notifications/background-token` | `ClientCommunication::ClientNotificationController@backgroundToken` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/notifications/read-all` | `ClientCommunication::ClientNotificationController@readAll` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/notifications/unread-count` | `ClientCommunication::ClientNotificationController@unreadCount` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/notifications/{notification}/read` | `ClientCommunication::ClientNotificationController@markRead` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
