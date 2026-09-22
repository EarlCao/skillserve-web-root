---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Support Tickets (Admin)

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin support ticket desk.

Feature note: [[Support Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/support/tickets` | `Support::SupportTicketController@index` | `auth:sanctum` | policy `viewAny` → `view support` |
| GET | `/api/support/tickets/assignees` | `Support::SupportTicketController@assignees` | `auth:sanctum` | policy `viewAny` → `view support` |
| GET | `/api/support/tickets/{ticket}` | `Support::SupportTicketController@show` | `auth:sanctum` | policy `view` → `view support` |
| PATCH | `/api/support/tickets/{ticket}/assign` | `Support::SupportTicketController@assign` | `auth:sanctum` | policy `assign` → `assign support tickets` |
| PATCH | `/api/support/tickets/{ticket}/resolve` | `Support::SupportTicketController@resolve` | `auth:sanctum` | policy `resolve` → `resolve support tickets` |
| POST | `/api/support/tickets/{ticket}/responses` | `Support::SupportTicketController@respond` | `auth:sanctum` | policy `respond` → `respond to support tickets` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
