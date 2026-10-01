---
type: api-endpoints
generated: true
generated_on: 2026-10-01
source: php artisan route:list --json -v
tags: [api, endpoints, generated]
---
# API - Platform and Infrastructure

> [!info] Generated file — do not edit by hand
> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on 2026-10-01.
> Authorization is extracted from controller/policy source; request/response shapes live in the
> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).

Health checks, broadcasting auth, Swagger docs, storage and framework routes.

Conventions: [[API Conventions]] · Index: [[API Index]]

| Method | Path | Controller action | Middleware | Authorization |
|---|---|---|---|---|
| GET | `//` | `Closure` | — | — |
| GET, POST | `/api/broadcasting/auth` | `Illuminate\\Broadcasting\\BroadcastController@authenticate` | `auth:sanctum` | — |
| POST | `/api/client/v1/bookings/{booking}/pay` | `ClientMarketplace::ClientPaymentController@store` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureClient` | Role gate in middleware; ownership/participant check in the client policy or service |
| GET | `/api/client/v1/identity-verification` | `IdentityVerification::ClientIdentityVerificationController@show` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | No controller check found (see middleware / service) |
| POST | `/api/client/v1/identity-verification` | `IdentityVerification::ClientIdentityVerificationController@store` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount`, `throttle:identity-verification` | No controller check found (see middleware / service) |
| GET | `/api/client/v1/transaction-eligibility` | `IdentityVerification::TransactionEligibilityController@show` | `EnsurePlatformAvailable`, `auth:sanctum`, `EnsureMobileAccount` | No controller check found (see middleware / service) |
| GET | `/api/commission-tiers` | `Commissions::CommissionTierController@index` | `auth:sanctum` | policy `viewAny` → `view commissions` |
| POST | `/api/commission-tiers` | `Commissions::CommissionTierController@store` | `auth:sanctum` | policy `create` → `manage commissions` |
| GET | `/api/commission-tiers/presets` | `Commissions::CommissionTierController@presets` | `auth:sanctum` | policy `viewAny` → `view commissions` |
| POST | `/api/commission-tiers/presets/{preset}/apply` | `Commissions::CommissionTierController@applyPreset` | `auth:sanctum` | policy `create` → `manage commissions` |
| DELETE | `/api/commission-tiers/{commissionTier}` | `Commissions::CommissionTierController@destroy` | `auth:sanctum` | policy `delete` → `manage commissions` |
| GET | `/api/commission-tiers/{commissionTier}` | `Commissions::CommissionTierController@show` | `auth:sanctum` | policy `view` → `view commissions` |
| PATCH | `/api/commission-tiers/{commissionTier}` | `Commissions::CommissionTierController@update` | `auth:sanctum` | policy `update` → `manage commissions` |
| PUT | `/api/commission-tiers/{commissionTier}` | `Commissions::CommissionTierController@update` | `auth:sanctum` | policy `update` → `manage commissions` |
| GET | `/api/commissions` | `Commissions::CommissionController@index` | `auth:sanctum` | `view commissions` |
| PATCH | `/api/commissions/{booking}/settle` | `Commissions::CommissionController@settle` | `auth:sanctum` | `settle commissions` |
| PATCH | `/api/commissions/{booking}/waive` | `Commissions::CommissionController@waive` | `auth:sanctum` | `settle commissions` |
| GET | `/api/documentation` | `L5Swagger\\Http::SwaggerController@api` | `Config`, `EnsureSwaggerUiEnabled` | — |
| GET | `/api/health` | `Closure` | — | — |
| GET | `/api/identity-verifications` | `IdentityVerification::IdentityVerificationController@index` | `auth:sanctum` | policy `viewAny` → `view identity verifications` |
| GET | `/api/identity-verifications/{identityVerification}` | `IdentityVerification::IdentityVerificationController@show` | `auth:sanctum` | policy `view` → `view identity verifications` |
| PATCH | `/api/identity-verifications/{identityVerification}/approve` | `IdentityVerification::IdentityVerificationController@approve` | `auth:sanctum` | policy `verify` → `verify identities` |
| GET | `/api/identity-verifications/{identityVerification}/documents/{document}/download` | `IdentityVerification::IdentityVerificationController@downloadDocument` | `auth:sanctum` | policy `view` → `view identity verifications` |
| PATCH | `/api/identity-verifications/{identityVerification}/reject` | `IdentityVerification::IdentityVerificationController@reject` | `auth:sanctum` | policy `reject` → `reject identities` |
| GET | `/api/oauth2-callback` | `L5Swagger\\Http::SwaggerController@oauth2Callback` | `Config` | — |
| POST | `/api/webhooks/paymongo` | `Payments::PayMongoWebhookController` | — | — |
| GET, POST | `/broadcasting/auth` | `Illuminate\\Broadcasting\\BroadcastController@authenticate` | — | — |
| GET | `/docs` | `L5Swagger\\Http::SwaggerController@docs` | `Config`, `EnsureSwaggerUiEnabled` | — |
| GET | `/docs/asset/{asset}` | `L5Swagger\\Http::SwaggerAssetController@index` | `Config` | — |
| GET | `/sanctum/csrf-cookie` | `Laravel\\Sanctum\\Http::CsrfCookieController@show` | — | — |
| GET | `/storage/{path}` | `Closure` | — | — |
| PUT | `/storage/{path}` | `Closure` | — | — |
| GET | `/up` | `Closure` | — | — |

Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), `SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.
