---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Reports and Moderation

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin report queue and moderation actions.

Feature note: [[Reports and Moderation]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/reports` | `ReportsAndModeration::ReportController@index` | `auth:sanctum` | policy `viewAny` → `view reports` |
| GET | `/api/reports/reasons` | `ReportsAndModeration::ReportController@reasons` | `auth:sanctum` | policy `viewAny` → `view reports` |
| GET | `/api/reports/{report}` | `ReportsAndModeration::ReportController@show` | `auth:sanctum` | policy `view` → `view reports` |
| PATCH | `/api/reports/{report}/action` | `ReportsAndModeration::ReportController@takeAction` | `auth:sanctum` | policy `action` → `manage moderation` |
| PATCH | `/api/reports/{report}/investigate` | `ReportsAndModeration::ReportController@investigate` | `auth:sanctum` | policy `investigate` → `investigate reports` |
| PATCH | `/api/reports/{report}/notes` | `ReportsAndModeration::ReportController@addNote` | `auth:sanctum` | policy `addNote` → `investigate reports` |
| PATCH | `/api/reports/{report}/reject` | `ReportsAndModeration::ReportController@reject` | `auth:sanctum` | policy `reject` → `resolve reports` |
| PATCH | `/api/reports/{report}/resolve` | `ReportsAndModeration::ReportController@resolve` | `auth:sanctum` | policy `resolve` → `resolve reports` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
