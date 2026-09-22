---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Provider Recognition

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Badges, featured and top-rated providers.

Feature note: [[Provider Recognition]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/provider-recognition/badges` | `ProviderRecognition::ProviderRecognitionController@badges` | `auth:sanctum` | `view provider recognition` |
| POST | `/api/provider-recognition/badges` | `ProviderRecognition::ProviderRecognitionController@storeBadge` | `auth:sanctum` | `manage provider badges` |
| DELETE | `/api/provider-recognition/badges/{badge}` | `ProviderRecognition::ProviderRecognitionController@destroyBadge` | `auth:sanctum` | `manage provider badges` |
| PUT | `/api/provider-recognition/badges/{badge}` | `ProviderRecognition::ProviderRecognitionController@updateBadge` | `auth:sanctum` | `manage provider badges` |
| GET | `/api/provider-recognition/providers` | `ProviderRecognition::ProviderRecognitionController@providers` | `auth:sanctum` | `view provider recognition` |
| POST | `/api/provider-recognition/providers/{provider}/badges` | `ProviderRecognition::ProviderRecognitionController@assignBadge` | `auth:sanctum` | `assign provider badges` |
| DELETE | `/api/provider-recognition/providers/{provider}/badges/{badge}` | `ProviderRecognition::ProviderRecognitionController@removeBadge` | `auth:sanctum` | `assign provider badges` |
| PATCH | `/api/provider-recognition/providers/{provider}/featured` | `ProviderRecognition::ProviderRecognitionController@featured` | `auth:sanctum` | `manage featured providers` |
| GET | `/api/provider-recognition/top-rated` | `ProviderRecognition::ProviderRecognitionController@topRated` | `auth:sanctum` | `view top rated providers` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
