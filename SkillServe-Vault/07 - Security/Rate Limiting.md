---
type: reference
tags: [security, rate-limit]
sources: [backend/app/Providers/AppServiceProvider.php, backend/bootstrap/app.php, backend/app/Shared/Middleware/AddRateLimitHeaders.php, backend/app/Modules/ClientAuthentication/Services/ClientEmailOtpService.php]
---
# Rate Limiting

| Limiter / control | Limit | Key | Routes |
|---|---|---|---|
| `api` (group default) | 60/min | user id, else IP | all `api/*` except `/api/health` |
| `login` | `LOGIN_RATE_LIMIT` (default 5)/min | IP | `POST /api/auth/login`, `/auth/forgot-password`, `/auth/reset-password`; mobile `/auth/login`, `/auth/google`, `/auth/google/register` |
| `client-auth` | `CLIENT_AUTH_RATE_LIMIT` (default 20)/min per IP **+** 10/min per email | IP and email | mobile register, register-provider, cancel-registration, verify-otp, resend-otp, forgot-password, reset-password |
| `identity-verification` | 5/hour per user **+** 20/hour per IP | user id (else IP) and IP | `POST /client/v1/identity-verification` — deliberately tight: repeated submissions are the one way to probe whether a National ID is already registered |
| OTP attempts | 5 wrong codes → 429 | per code | verify-otp |
| OTP resend cooldown | 60 s → 429 | per account/registration | resend-otp |
| Admin password broker | Laravel reset throttling (`RESET_THROTTLED`) | email | admin reset |

Responses include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
(`AddRateLimitHeaders`; never overrides headers set by the throttle middleware). Both clients show
"Too many attempts. Please wait a minute and try again." on 429.

Limiter state lives in the cache (`CACHE_STORE=database`).

> [!info] Not rate-limited beyond `api`
> `POST /api/client/v1/auth/refresh` and authenticated endpoints use only the 60/min `api` limiter.

Tests: `ClientAuthRateLimitTest`, `AuthenticationTest`, `ClientEmailOtpTest`.
