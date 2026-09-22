---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Administrators, Roles and Permissions

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Staff accounts, roles and the permission catalogue.

Feature note: [[Admin Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/administrators` | `Administrators::AdministratorController@index` | `auth:sanctum` | policy `viewAny` → `manage administrators` |
| POST | `/api/administrators` | `Administrators::AdministratorController@store` | `auth:sanctum` | policy `create` → `manage administrators`; `assignSuperAdmin` |
| GET | `/api/administrators/{administrator}` | `Administrators::AdministratorController@show` | `auth:sanctum` | policy `view` → `manage administrators` |
| PATCH | `/api/administrators/{administrator}` | `Administrators::AdministratorController@update` | `auth:sanctum` | policy `update` → `manage administrators`; `assignSuperAdmin` |
| PUT | `/api/administrators/{administrator}` | `Administrators::AdministratorController@update` | `auth:sanctum` | policy `update` → `manage administrators`; `assignSuperAdmin` |
| PATCH | `/api/administrators/{administrator}/password` | `Administrators::AdministratorController@resetPassword` | `auth:sanctum` | policy `resetPassword` → `edit administrators` |
| PATCH | `/api/administrators/{administrator}/status` | `Administrators::AdministratorController@updateStatus` | `auth:sanctum` | policy `updateStatus` → `edit administrators` |
| GET | `/api/permissions` | `Administrators::PermissionController@index` | `auth:sanctum` | policy `viewAny` → `manage administrators` |
| GET | `/api/roles` | `Administrators::RoleController@index` | `auth:sanctum` | policy `viewAny` → `manage administrators` |
| POST | `/api/roles` | `Administrators::RoleController@store` | `auth:sanctum` | policy `create` → `manage administrators` |
| DELETE | `/api/roles/{role}` | `Administrators::RoleController@destroy` | `auth:sanctum` | policy `delete` → `manage administrators` |
| GET | `/api/roles/{role}` | `Administrators::RoleController@show` | `auth:sanctum` | policy `view` → `manage administrators` |
| PATCH | `/api/roles/{role}` | `Administrators::RoleController@update` | `auth:sanctum` | policy `update` → `manage administrators` |
| PUT | `/api/roles/{role}` | `Administrators::RoleController@update` | `auth:sanctum` | policy `update` → `manage administrators` |
| PUT | `/api/roles/{role}/permissions` | `Administrators::RoleController@syncPermissions` | `auth:sanctum` | policy `syncPermissions` → `manage administrators` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
