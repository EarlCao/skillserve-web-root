---
type: reference
tags: [api, conventions]
sources: [backend/app/Shared/Services/ApiResponder.php, backend/bootstrap/app.php, backend/app/Shared/Middleware, api-docs/README.md]
---
# API Conventions

## Envelope

Every JSON response (success or error) on `api/*`:

```json
{ "success": true, "message": "Request successful.", "data": {}, "errors": null, "meta": [] }
```

- Built by `App\Shared\Services\ApiResponder` (`success`, `error`, `paginated`, `noContent`) or the
  `ApiResponse` trait in controllers.
- Errors: `success: false`, `errors` keyed by field for 422.
- `meta` carries extras: `pagination`, `maintenance` (503), `account` (403 restricted),
  `read_only` (settings).

## Pagination

```json
"meta": { "pagination": { "total": 150, "per_page": 15, "current_page": 1, "last_page": 10, "from": 1, "to": 15 } }
```

Query params: `page`, `per_page` (1–100; default = System Settings → default page size via
`PageSize`), plus module-specific `search`, filters, `sort`, `direction` (`asc|desc`), all validated
by Form Requests with whitelisted sort columns.

## Status codes in use

| Code | When |
|---|---|
| 200 / 201 | success |
| 204 | no content |
| 401 | missing/expired/revoked token, wrong credentials |
| 403 | policy denial ("This action is unauthorized."), wrong token surface ("This token is not valid for client access."), restricted account (`meta.account`), unverified email |
| 404 | "Resource not found." (incl. route-model binding misses) |
| 409 | conflicts: already disputed, already paid, duplicate review, booking overlap, sign-up already completed |
| 422 | validation or business-rule refusal (wrong status transition etc.) |
| 429 | rate limit, OTP attempts/cooldown |
| 500 | "Server Error." / "A database error occurred." (no internals leaked) |
| 503 | maintenance mode (mobile API), `Retry-After: 300`, `meta.maintenance: true`; also nginx JSON 503 when the app is restarting |

## Headers

| Header | Direction | Purpose |
|---|---|---|
| `Authorization: Bearer <token>` | request | Sanctum token |
| `Accept: application/json` | request | recommended; `ForceJsonResponse` forces JSON anyway |
| `Idempotency-Key` | request | `POST /client/v1/bookings`, booking messages — safe retries |
| `If-None-Match` | request | conditional GET → 304 |
| `ETag`, `Cache-Control: private, no-cache` | response | `CacheApiResponse` (max-age via `API_CACHE_MAX_AGE`) |
| `X-RateLimit-Limit/Remaining/Reset` | response | `AddRateLimitHeaders` |

## Rate limits

| Limiter | Limit | Applies to |
|---|---|---|
| `api` | 60/min per user id or IP | every `api/*` route except `/api/health` |
| `login` | `LOGIN_RATE_LIMIT`/min per IP (default 5) | admin login, forgot/reset password; mobile login, Google, Google register |
| `client-auth` | `CLIENT_AUTH_RATE_LIMIT`/min per IP (default 20) **and** 10/min per email | mobile register, register-provider, cancel-registration, verify-otp, resend-otp, forgot/reset password |

`POST /client/v1/auth/refresh` has only the `api` limiter.

## REST style

Plural resource paths; state changes are `PATCH /{resource}/{id}/{action}` (e.g.
`/bookings/{id}/cancel`, `/services/{id}/approve`) — the project accepts action sub-resources for
non-CRUD workflows (AGENT.md). `PUT` and `PATCH` are both registered for updates; the OpenAPI spec
documents only `PUT` for those.

## Time and money in payloads

Datetimes are ISO-8601; the server stores UTC and interprets offset-less times as Manila time
([[Time and Timezone Rules]]). Amounts are decimal strings with 2 places; currency `PHP`.

Related: [[Authentication Flows]] · [[Request Lifecycle]] · [[Endpoints Index]]
