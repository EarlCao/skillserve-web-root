---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Client Messaging

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Booking-scoped chat and the conversation inbox.

Feature note: [[Client Messaging]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/client/v1/bookings/{booking}/messages` | `ClientCommunication::BookingMessageController@index` | `EnsurePlatformAvailable`, `auth:sanctum` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/bookings/{booking}/messages` | `ClientCommunication::BookingMessageController@store` | `EnsurePlatformAvailable`, `auth:sanctum` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/bookings/{booking}/messages/read` | `ClientCommunication::BookingMessageController@markRead` | `EnsurePlatformAvailable`, `auth:sanctum` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/conversations` | `ClientCommunication::ConversationController@index` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/conversations/unread-count` | `ClientCommunication::ConversationController@unreadCount` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
