---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Provider Bookings (Mobile)

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

The provider's jobs and their lifecycle.

Feature note: [[Provider Jobs]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/client/v1/provider/bookings` | `ClientMarketplace::ProviderBookingController@index` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/provider/bookings/{booking}` | `ClientMarketplace::ProviderBookingController@show` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/provider/bookings/{booking}/cancel` | `ClientMarketplace::ProviderBookingController@cancel` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/provider/bookings/{booking}/complete` | `ClientMarketplace::ProviderBookingController@complete` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/provider/bookings/{booking}/confirm` | `ClientMarketplace::ProviderBookingController@confirm` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/provider/bookings/{booking}/decline` | `ClientMarketplace::ProviderBookingController@decline` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/provider/bookings/{booking}/payment-received` | `ClientMarketplace::ProviderBookingController@paymentReceived` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/provider/bookings/{booking}/start` | `ClientMarketplace::ProviderBookingController@start` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureProvider` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
