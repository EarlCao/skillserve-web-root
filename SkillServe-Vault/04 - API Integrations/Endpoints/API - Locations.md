---
type: api-endpoints
generated: true
generated_on: 2026-10-01
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Locations

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-10-01.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Public Philippine address-picker data (PSA PSGC) and the National-ID address matcher.

Feature note: [[Philippine Addresses]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/client/v1/locations/match` | `Locations::LocationController@match` | `EnsurePlatformAvailable` | No controller check found (see middleware / service) |
| GET | `/api/client/v1/locations/regions` | `Locations::LocationController@regions` | `EnsurePlatformAvailable` | No controller check found (see middleware / service) |
| GET | `/api/client/v1/locations/{location}/children` | `Locations::LocationController@children` | `EnsurePlatformAvailable` | No controller check found (see middleware / service) |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
