---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Client Catalog

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Public marketplace discovery (no token required).

Feature note: [[Service and Provider Discovery]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/client/v1/categories` | `ClientMarketplace::ClientCatalogController@categories` | `EnsurePlatformAvailable` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/categories/{category}` | `ClientMarketplace::ClientCatalogController@category` | `EnsurePlatformAvailable` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/providers` | `ClientMarketplace::ClientCatalogController@providers` | `EnsurePlatformAvailable` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/providers/{provider}` | `ClientMarketplace::ClientCatalogController@provider` | `EnsurePlatformAvailable` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/services` | `ClientMarketplace::ClientCatalogController@services` | `EnsurePlatformAvailable` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/services/{service}` | `ClientMarketplace::ClientCatalogController@service` | `EnsurePlatformAvailable` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
