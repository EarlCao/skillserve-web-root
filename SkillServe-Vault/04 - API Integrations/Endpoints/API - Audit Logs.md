---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Audit Logs

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Security and audit log viewer.

Feature note: [[Security and Audit Logs]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/audit-logs` | `Audit::AuditLogController@index` | `auth:sanctum` | No controller check found (see middleware / service) |
| GET | `/api/audit-logs/administrators` | `Audit::AuditLogController@administrators` | `auth:sanctum` | `view audit logs`; `view login activity`; `monitor security events` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
