---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Disputes

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin dispute queue (disputes live on the bookings table).

Feature note: [[Dispute Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/disputes` | `Bookings::DisputeController@index` | `auth:sanctum` | policy `viewDisputes` → `view bookings` |
| GET | `/api/disputes/{booking}` | `Bookings::DisputeController@show` | `auth:sanctum` | policy `viewDisputes` → `view bookings` |
| PATCH | `/api/disputes/{booking}/close` | `Bookings::DisputeController@close` | `auth:sanctum` | policy `manageDispute` → `manage booking disputes` |
| GET | `/api/disputes/{booking}/evidence/{evidence}` | `Bookings::DisputeController@downloadEvidence` | `auth:sanctum` | policy `viewDisputes` → `view bookings` |
| GET | `/api/disputes/{booking}/history` | `Bookings::DisputeController@history` | `auth:sanctum` | policy `viewDisputes` → `view bookings` |
| PATCH | `/api/disputes/{booking}/investigate` | `Bookings::DisputeController@investigate` | `auth:sanctum` | policy `manageDispute` → `manage booking disputes` |
| PATCH | `/api/disputes/{booking}/notes` | `Bookings::DisputeController@addNote` | `auth:sanctum` | policy `manageDispute` → `manage booking disputes` |
| PATCH | `/api/disputes/{booking}/reject` | `Bookings::DisputeController@reject` | `auth:sanctum` | policy `manageDispute` → `manage booking disputes` |
| PATCH | `/api/disputes/{booking}/resolve` | `Bookings::DisputeController@resolve` | `auth:sanctum` | policy `manageDispute` → `manage booking disputes` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
