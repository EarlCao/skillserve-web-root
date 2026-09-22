---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Client Reports

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Reports filed from the app against a user, review or message.

Feature note: [[Client Reports]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/client/v1/reports` | `ClientCommunication::ClientReportController@index` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/reports` | `ClientCommunication::ClientReportController@store` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/reports/{report}` | `ClientCommunication::ClientReportController@show` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
