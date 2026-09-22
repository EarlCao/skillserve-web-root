---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Data Management

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Exports, archives and deleted-record management.

Feature note: [[Data Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/data-management/archives` | `DataManagement::DataManagementController@archives` | `auth:sanctum` | `manage data`; `restore archived records` |
| POST | `/api/data-management/archives` | `DataManagement::DataManagementController@archive` | `auth:sanctum` | `archive records` |
| POST | `/api/data-management/archives/{archive}/restore` | `DataManagement::DataManagementController@restoreArchive` | `auth:sanctum` | `restore archived records` |
| GET | `/api/data-management/deleted` | `DataManagement::DataManagementController@deleted` | `auth:sanctum` | `manage deleted records` |
| DELETE | `/api/data-management/deleted/{type}/{id}` | `DataManagement::DataManagementController@permanentlyDelete` | `auth:sanctum` | `manage deleted records` |
| POST | `/api/data-management/deleted/{type}/{id}/restore` | `DataManagement::DataManagementController@restoreDeleted` | `auth:sanctum` | `restore deleted records` |
| GET | `/api/data-management/export` | `DataManagement::DataManagementController@export` | `auth:sanctum` | `export system data` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
