---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Services

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin service moderation.

Feature note: [[Service Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/services` | `Services::ServiceController@index` | `auth:sanctum` | policy `viewAny` → `view services` |
| DELETE | `/api/services/{service}` | `Services::ServiceController@destroy` | `auth:sanctum` | policy `delete` → `delete services` |
| GET | `/api/services/{service}` | `Services::ServiceController@show` | `auth:sanctum` | policy `view` → `view services` |
| PATCH | `/api/services/{service}` | `Services::ServiceController@update` | `auth:sanctum` | policy `update` → `edit services` |
| PUT | `/api/services/{service}` | `Services::ServiceController@update` | `auth:sanctum` | policy `update` → `edit services` |
| PATCH | `/api/services/{service}/approve` | `Services::ServiceController@approve` | `auth:sanctum` | policy `approve` → `approve services` |
| PATCH | `/api/services/{service}/feature` | `Services::ServiceController@feature` | `auth:sanctum` | policy `feature` → `feature services` |
| PATCH | `/api/services/{service}/hide` | `Services::ServiceController@hide` | `auth:sanctum` | policy `hide` → `edit services` |
| PATCH | `/api/services/{service}/reject` | `Services::ServiceController@reject` | `auth:sanctum` | policy `reject` → `reject services` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
