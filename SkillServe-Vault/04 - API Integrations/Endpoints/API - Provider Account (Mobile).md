---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Provider Account (Mobile)

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Provider profile, portfolio, availability, badges and verification upload.

Feature note: [[Provider Account and Verification]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/client/v1/provider/availability` | `ClientMarketplace::ProviderProfileController@availability` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PUT | `/api/client/v1/provider/availability` | `ClientMarketplace::ProviderProfileController@updateAvailability` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/provider/badges` | `ClientMarketplace::ProviderProfileController@badges` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/provider/portfolio` | `ClientMarketplace::ProviderProfileController@portfolio` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/provider/portfolio` | `ClientMarketplace::ProviderProfileController@storePortfolioItem` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| DELETE | `/api/client/v1/provider/portfolio/{item}` | `ClientMarketplace::ProviderProfileController@destroyPortfolioItem` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/provider/profile` | `ClientMarketplace::ProviderProfileController@show` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/provider/profile` | `ClientMarketplace::ProviderProfileController@update` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/provider/verification` | `ClientMarketplace::ProviderVerificationController@show` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/provider/verification` | `ClientMarketplace::ProviderVerificationController@store` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
