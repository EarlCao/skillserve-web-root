---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Client Disputes

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Either party raises a dispute and uploads evidence.

Feature note: [[Client Disputes]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| PATCH | `/api/client/v1/bookings/{booking}/dispute` | `ClientMarketplace::BookingDisputeController@store` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/bookings/{booking}/dispute/evidence` | `ClientMarketplace::BookingDisputeController@storeEvidence` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/disputes` | `ClientMarketplace::BookingDisputeController@index` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
