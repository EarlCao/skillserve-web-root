---
type: guide
tags: [security, auth, tokens]
sources: [backend/config/sanctum.php, backend/config/client-auth.php, backend/app/Providers/AppServiceProvider.php, backend/app/Modules/ClientAuthentication/Services/ClientSessionService.php, frontend/src/services/axios.js, mobile lib/core/services/token_storage.dart, mobile lib/core/services/api_client.dart]
---
# Token and Session Management

| | Admin Web | Mobile |
|---|---|---|
| Token type | Sanctum personal access token `admin-session`, abilities `*` | `client-access` (ability `client:auth`) + opaque rotating refresh token; optional `client-background` (`client:notifications`) |
| Lifetime | `system.session_timeout_minutes` (default 1440; DEPLOYMENT.md suggests 480 in production) | access 60 min (`CLIENT_ACCESS_TOKEN_EXPIRATION`); refresh 525600 min from last use (`CLIENT_REFRESH_TOKEN_EXPIRATION`); background 525600 min (`CLIENT_BACKGROUND_TOKEN_EXPIRATION`, but see KI-01) |
| Enforcement | `expires_at` set at login **and** `Sanctum::authenticateAccessTokensUsing` rejects tokens older than the timeout (so lowering the setting ends existing sessions) | `expires_at`; refresh rows in `client_refresh_tokens` |
| Client storage | `localStorage['skillserve:token']` (JSON string) | flutter_secure_storage (Keystore/Keychain); migrated from SharedPreferences once |
| On 401 | token removed, `skillserve:unauthorized` event → logged out | single-flight refresh; if refresh refused → session cleared, `onSessionRevoked` (with restriction reason) |
| Logout | revokes current token | revokes **all** tokens + refresh tokens |
| Password change | other tokens revoked (current kept) | all sessions end |
| Password reset | all tokens revoked | (reset flow incomplete — KI-02) |
| Suspension / ban / deletion | login refused (403) | `revokeAll`; 403 `meta.account` everywhere |
| `SANCTUM_EXPIRATION` | env default 1440 (framework-level expiry for tokens without `expires_at`) | — |

## Refresh token rotation (`ClientSessionService`)

- Each login starts a **family** (`family_id`). Every refresh locks the presented row, checks it is
  unrevoked and unexpired, marks it revoked with `replaced_by`, and issues a new access + refresh
  pair in the same family.
- **Reuse detection:** presenting an already-revoked refresh token revokes the entire family
  (possible theft) — hence the app's single-flight refresh.
- Refresh token secrets are stored only as SHA-256 hashes (`token_hash`).

## Risks and mitigations noted in the repo

- Admin token in `localStorage` is readable by any script on the page → production CSP
  `script-src 'self'`, recommended `X-Frame-Options: DENY` / `frame-ancestors 'none'`, and a short
  session timeout ([[CORS and Security Headers]]).
- KI-01: session timeout applies to the mobile background token ([[Known Issues and Gaps]]).

Related: [[Authentication Flows]] · [[ADR-003 Sanctum Bearer Tokens with Rotating Mobile Refresh]]
