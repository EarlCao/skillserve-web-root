---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Reviews

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin review moderation.

Feature note: [[Reviews and Ratings Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/reviews` | `Reviews::ReviewController@index` | `auth:sanctum` | policy `viewAny` → `view reviews` |
| DELETE | `/api/reviews/{review}` | `Reviews::ReviewController@destroy` | `auth:sanctum` | policy `delete` → `delete reviews` |
| GET | `/api/reviews/{review}` | `Reviews::ReviewController@show` | `auth:sanctum` | policy `view` → `view reviews` |
| PATCH | `/api/reviews/{review}/hide` | `Reviews::ReviewController@hide` | `auth:sanctum` | policy `hide` → `edit reviews` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
