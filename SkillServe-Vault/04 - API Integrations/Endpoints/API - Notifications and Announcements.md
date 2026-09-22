---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Notifications and Announcements

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin announcements and notification history.

Feature note: [[Notifications and Announcements]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/notifications` | `Notifications::NotificationController@index` | `auth:sanctum` | policy `viewAny` → `view notifications` |
| POST | `/api/notifications/announcements` | `Notifications::NotificationController@store` | `auth:sanctum` | policy `create` → `send announcements`; `schedule announcements`; `target notifications` |
| DELETE | `/api/notifications/announcements/{announcement}` | `Notifications::NotificationController@destroy` | `auth:sanctum` | policy `delete` → `send announcements` |
| GET | `/api/notifications/recipients` | `Notifications::NotificationController@recipients` | `auth:sanctum` | `target notifications` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
