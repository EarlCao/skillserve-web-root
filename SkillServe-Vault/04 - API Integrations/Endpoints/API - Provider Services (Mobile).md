---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Provider Services (Mobile)

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Provider-managed services (subject to admin approval).

Feature note: [[Provider Service Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/client/v1/provider/services` | `ClientMarketplace::ProviderServiceController@index` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/provider/services` | `ClientMarketplace::ProviderServiceController@store` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| DELETE | `/api/client/v1/provider/services/{service}` | `ClientMarketplace::ProviderServiceController@destroy` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/provider/services/{service}` | `ClientMarketplace::ProviderServiceController@show` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/provider/services/{service}` | `ClientMarketplace::ProviderServiceController@update` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PUT | `/api/client/v1/provider/services/{service}` | `ClientMarketplace::ProviderServiceController@update` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
