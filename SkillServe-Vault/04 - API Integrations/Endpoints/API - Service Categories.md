---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Service Categories

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Categories and nested subcategories.

Feature note: [[Service Category Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/service-categories` | `ServiceCategories::ServiceCategoryController@index` | `auth:sanctum` | policy `viewAny` → `view service categories` |
| POST | `/api/service-categories` | `ServiceCategories::ServiceCategoryController@store` | `auth:sanctum` | policy `create` → `create service categories` |
| DELETE | `/api/service-categories/{serviceCategory}` | `ServiceCategories::ServiceCategoryController@destroy` | `auth:sanctum` | policy `delete` → `delete service categories` |
| GET | `/api/service-categories/{serviceCategory}` | `ServiceCategories::ServiceCategoryController@show` | `auth:sanctum` | policy `view` → `view service categories` |
| PATCH | `/api/service-categories/{serviceCategory}` | `ServiceCategories::ServiceCategoryController@update` | `auth:sanctum` | policy `update` → `edit service categories` |
| PUT | `/api/service-categories/{serviceCategory}` | `ServiceCategories::ServiceCategoryController@update` | `auth:sanctum` | policy `update` → `edit service categories` |
| PATCH | `/api/service-categories/{serviceCategory}/status` | `ServiceCategories::ServiceCategoryController@updateStatus` | `auth:sanctum` | policy `updateStatus` → `edit service categories` |
| POST | `/api/service-categories/{serviceCategory}/subcategories` | `ServiceCategories::ServiceCategoryController@storeSubcategory` | `auth:sanctum` | policy `update` → `edit service categories` |
| DELETE | `/api/service-categories/{serviceCategory}/subcategories/{serviceSubcategory}` | `ServiceCategories::ServiceCategoryController@destroySubcategory` | `auth:sanctum` | policy `update` → `edit service categories` |
| PATCH | `/api/service-categories/{serviceCategory}/subcategories/{serviceSubcategory}` | `ServiceCategories::ServiceCategoryController@updateSubcategory` | `auth:sanctum` | policy `update` → `edit service categories` |
| PUT | `/api/service-categories/{serviceCategory}/subcategories/{serviceSubcategory}` | `ServiceCategories::ServiceCategoryController@updateSubcategory` | `auth:sanctum` | policy `update` → `edit service categories` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
