---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Bookings

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Admin booking management, payments and refunds.

Feature note: [[Booking Management]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `/api/bookings` | `Bookings::BookingController@index` | `auth:sanctum` | policy `viewAny` → `view bookings` |
| GET | `/api/bookings/{booking}` | `Bookings::BookingController@show` | `auth:sanctum` | policy `view` → `view bookings` |
| PATCH | `/api/bookings/{booking}/cancel` | `Bookings::BookingController@cancel` | `auth:sanctum` | policy `cancel` → `cancel bookings` |
| PATCH | `/api/bookings/{booking}/dispute` | `Bookings::BookingController@dispute` | `auth:sanctum` | policy `manageDispute` → `manage booking disputes` |
| GET | `/api/bookings/{booking}/history` | `Bookings::BookingController@history` | `auth:sanctum` | policy `view` → `view bookings` |
| PATCH | `/api/bookings/{booking}/mark-paid` | `Bookings::BookingController@markPaid` | `auth:sanctum` | policy `managePayments` → `manage booking payments` |
| PATCH | `/api/bookings/{booking}/refund` | `Bookings::BookingController@refund` | `auth:sanctum` | policy `managePayments` → `manage booking payments` |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
