---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Providers

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin provider management and verification workflow.

Feature note: [[Service Provider Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/providers` | `Providers::ProviderController@index` | `auth:sanctum` | policy `viewAny` → `view providers` |
| GET | `/api/providers/{provider}` | `Providers::ProviderController@show` | `auth:sanctum` | policy `view` → `view providers` |
| PATCH | `/api/providers/{provider}/activate` | `Providers::ProviderController@activate` | `auth:sanctum` | policy `activate` → `activate providers` |
| PATCH | `/api/providers/{provider}/suspend` | `Providers::ProviderController@suspend` | `auth:sanctum` | policy `suspend` → `suspend providers` |
| GET | `/api/providers/{provider}/verification-documents/{document}/download` | `Providers::ProviderController@downloadVerificationDocument` | `auth:sanctum` | policy `view` → `view providers` |
| GET | `/api/providers/{provider}/verification-history` | `Providers::ProviderController@verificationHistory` | `auth:sanctum` | policy `view` → `view providers` |
| PATCH | `/api/providers/{provider}/verification/approve` | `Providers::ProviderController@approveVerification` | `auth:sanctum` | policy `verify` → `verify providers` |
| PATCH | `/api/providers/{provider}/verification/reject` | `Providers::ProviderController@rejectVerification` | `auth:sanctum` | policy `reject` → `reject providers` |
| PATCH | `/api/providers/{provider}/verification/remove` | `Providers::ProviderController@removeVerification` | `auth:sanctum` | policy `removeVerification` → `verify providers` |
| PATCH | `/api/providers/{provider}/verification/request-info` | `Providers::ProviderController@requestAdditionalInfo` | `auth:sanctum` | policy `requestAdditionalInfo` → `verify providers` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
