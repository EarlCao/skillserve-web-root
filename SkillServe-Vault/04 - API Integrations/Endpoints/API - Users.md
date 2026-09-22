---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Users

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin User Management (customer and provider accounts).

Feature note: [[User Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/users` | `Users::UserController@index` | `auth:sanctum` | `view users` |
| DELETE | `/api/users/{user}` | `Users::UserController@destroy` | `auth:sanctum` | `delete users` |
| GET | `/api/users/{user}` | `Users::UserController@show` | `auth:sanctum` | `view users` |
| PATCH | `/api/users/{user}` | `Users::UserController@update` | `auth:sanctum` | `edit users` |
| PUT | `/api/users/{user}` | `Users::UserController@update` | `auth:sanctum` | `edit users` |
| PATCH | `/api/users/{user}/activate` | `Users::UserController@activate` | `auth:sanctum` | `activate users` |
| PATCH | `/api/users/{user}/ban` | `Users::UserController@ban` | `auth:sanctum` | `ban users` |
| GET | `/api/users/{user}/moderation-history` | `Users::UserController@moderationHistory` | `auth:sanctum` | `view users` |
| PATCH | `/api/users/{user}/suspend` | `Users::UserController@suspend` | `auth:sanctum` | `suspend users` |
| PATCH | `/api/users/{user}/unban` | `Users::UserController@unban` | `auth:sanctum` | `ban users` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
