---
type: api-endpoints
generated: true
generated_on: 2026-09-22
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Client Authentication

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-09-22.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Mobile registration, OTP, login, Google sign-in, refresh, profile and account deletion.

Feature note: [[Client Authentication and Account]] · Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| POST | `/api/client/v1/auth/cancel-registration` | `ClientAuthentication::ClientAuthController@cancelRegistration` | `EnsurePlatformAvailable`, `throttle:client-auth` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/change-password` | `ClientAuthentication::ClientAuthController@changePassword` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/forgot-password` | `ClientAuthentication::ClientAuthController@forgotPassword` | `EnsurePlatformAvailable`, `throttle:client-auth` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/google` | `ClientAuthentication::ClientAuthController@google` | `EnsurePlatformAvailable`, `throttle:login` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/google/register` | `ClientAuthentication::ClientAuthController@googleRegister` | `EnsurePlatformAvailable`, `throttle:login` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/login` | `ClientAuthentication::ClientAuthController@login` | `EnsurePlatformAvailable`, `throttle:login` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/logout` | `ClientAuthentication::ClientAuthController@logout` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| DELETE | `/api/client/v1/auth/me` | `ClientAuthentication::ClientAuthController@deleteAccount` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/auth/me` | `ClientAuthentication::ClientAuthController@me` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| PATCH | `/api/client/v1/auth/me` | `ClientAuthentication::ClientAuthController@updateProfile` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/auth/me/data-export` | `ClientAuthentication::ClientAuthController@exportData` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| DELETE | `/api/client/v1/auth/me/photo` | `ClientAuthentication::ClientAuthController@deleteProfilePhoto` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/me/photo` | `ClientAuthentication::ClientAuthController@updateProfilePhoto` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/refresh` | `ClientAuthentication::ClientAuthController@refresh` | `EnsurePlatformAvailable` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/register` | `ClientAuthentication::ClientAuthController@register` | `EnsurePlatformAvailable`, `throttle:client-auth` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/register-provider` | `ClientAuthentication::ClientAuthController@registerProvider` | `EnsurePlatformAvailable`, `throttle:client-auth` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/resend-otp` | `ClientAuthentication::ClientAuthController@resendOtp` | `EnsurePlatformAvailable`, `throttle:client-auth` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/reset-password` | `ClientAuthentication::ClientAuthController@resetPassword` | `EnsurePlatformAvailable`, `throttle:client-auth` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/verification-notification` | `ClientAuthentication::ClientAuthController@sendVerificationNotification` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureActiveClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/auth/verify-email/{user}/{hash}` | `ClientAuthentication::ClientAuthController@verifyEmail` | `EnsurePlatformAvailable`, `signed` | Role gate in middleware; ownership/participant check in the client policy or service |
| POST | `/api/client/v1/auth/verify-otp` | `ClientAuthentication::ClientAuthController@verifyOtp` | `EnsurePlatformAvailable`, `throttle:client-auth` | Role gate in middleware; ownership/participant check in the client policy or service |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
