---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Platform and Infrastructure

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Health checks, broadcasting auth, Swagger docs, storage and framework routes.

Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `//` | `Closure` | — | — |
| GET, POST | `/api/broadcasting/auth` | `Illuminate\\Broadcasting\\BroadcastController@authenticate` | `auth:sanctum` | — |
| GET | `/api/documentation` | `L5Swagger\\Http::SwaggerController@api` | `Config`, `EnsureSwaggerUiEnabled` | — |
| GET | `/api/health` | `Closure` | — | — |
| GET | `/api/oauth2-callback` | `L5Swagger\\Http::SwaggerController@oauth2Callback` | `Config` | — |
| GET, POST | `/broadcasting/auth` | `Illuminate\\Broadcasting\\BroadcastController@authenticate` | — | — |
| GET | `/docs` | `L5Swagger\\Http::SwaggerController@docs` | `Config`, `EnsureSwaggerUiEnabled` | — |
| GET | `/docs/asset/{asset}` | `L5Swagger\\Http::SwaggerAssetController@index` | `Config` | — |
| GET | `/sanctum/csrf-cookie` | `Laravel\\Sanctum\\Http::CsrfCookieController@show` | — | — |
| GET | `/storage/{path}` | `Closure` | — | — |
| PUT | `/storage/{path}` | `Closure` | — | — |
| GET | `/up` | `Closure` | — | — |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
