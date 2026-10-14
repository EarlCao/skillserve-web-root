---
type: api-endpoints
generated: true
generated_on: 2026-10-14
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Admin Inbox

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-10-14.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Each administrator's own alerts: the Inbox page and the bell.

Feature note: [[Admin Inbox]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/inbox` | `Notifications::AdminInboxController@index` | `auth:sanctum` | `use admin inbox` |
| POST | `/api/inbox/read-all` | `Notifications::AdminInboxController@readAll` | `auth:sanctum` | `use admin inbox` |
| GET | `/api/inbox/unread-count` | `Notifications::AdminInboxController@unreadCount` | `auth:sanctum` | `use admin inbox` |
| PATCH | `/api/inbox/{alert}/read` | `Notifications::AdminInboxController@markRead` | `auth:sanctum` | `use admin inbox` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
