---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Admin Authentication

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin web sign-in, sign-out, profile and password endpoints (`/api/auth/*`).

Feature note: [[Admin Authentication]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| POST | `/api/auth/change-password` | `Authentication::AuthController@changePassword` | `auth:sanctum`, `abilities:admin:auth` | No controller check found (see middleware / service) |
| POST | `/api/auth/forgot-password` | `Authentication::AuthController@forgotPassword` | `throttle:login` | No controller check found (see middleware / service) |
| POST | `/api/auth/login` | `Authentication::AuthController@login` | `throttle:login` | No controller check found (see middleware / service) |
| POST | `/api/auth/logout` | `Authentication::AuthController@logout` | `auth:sanctum`, `abilities:admin:auth` | No controller check found (see middleware / service) |
| GET | `/api/auth/me` | `Authentication::AuthController@me` | `auth:sanctum`, `abilities:admin:auth` | No controller check found (see middleware / service) |
| POST | `/api/auth/reset-password` | `Authentication::AuthController@resetPassword` | `throttle:login` | No controller check found (see middleware / service) |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
