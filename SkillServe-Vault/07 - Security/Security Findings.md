---
type: reference
tags: [security, findings, known-issue]
audited_on: 2026-09-22
---
# Security Findings (audit 2026-09-22)

Observations from reading the code. None were exploited or tested at runtime. Severity uses the
`AGENT_REVIEW.md` scale. Master list with all non-security issues: [[Known Issues and Gaps]].

| ID | Severity | Finding | Evidence | Suggested direction |
|---|---|---|---|---|
| SF-1 | MEDIUM | Admin token stored in `localStorage` | `frontend/src/constants` `STORAGE_KEYS.token`, `services/axios.js` | Mitigated by prod CSP `script-src 'self'` and short session timeout; frame-blocking headers must be set in the host (Needs Verification that they are) |
| SF-2 | LOW | `/api/health` exposes raw DB exception message publicly | `backend/routes/api.php` (`'error' => $e->getMessage()`) | return a generic "down" without the message |
| SF-3 | LOW | Admin routes accept any Sanctum token that passes permission checks (no `admin:*` ability requirement outside `/auth/*`) | module `Routes/api.php` files use only `auth:sanctum` | safe today because mobile accounts have no permissions; an ability check would add defence in depth |
| SF-4 | LOW (Needs Verification) | `local` disk (`serve: true`) shares `storage/app/private` with the private `verification` disk | `config/filesystems.php` | confirm nothing generates temporary URLs for that disk; or point `local` elsewhere |
| SF-5 | INFO | Session-timeout rule also applies to the mobile background token (functional bug, KI-01) | `AppServiceProvider` Sanctum callback | exempt `client-background` or name-check by ability |
| SF-6 | INFO | Frontend fallback Reverb key hard-coded (`5854c89d…`) | `frontend/src/app/config.js` | a public key, but mismatched defaults cause silent realtime failure — require the env var |
| SF-7 | INFO | Refresh endpoint limited only by the general 60/min limiter | `ClientAuthentication/Routes/api.php` | tokens are high-entropy and hashed; acceptable |

## Previously reported and now resolved (per repo docs, confirmed in code)

| From | Issue | Now |
|---|---|---|
| Readiness audit 2026-09-08 CRITICAL-1 | non-super-admins could assign `super-admin` | `AdministratorPolicy::assignSuperAdmin` checked on store/update |
| Readiness audit HIGH-2 | verification documents possibly public | private `verification` disk + streaming endpoint + migration moving old files |
| PENDING_FIXES M7 | CORS trusted all `*.vercel.app` / `*.onrender.com` | explicit origin list (`CorsTest`) |
| PENDING_FIXES M3 | public mobile auth endpoints not rate-limited | `client-auth` limiter |
| PENDING_FIXES H3 | vulnerable dependencies | `league/commonmark` 2.10.1, `maatwebsite/excel` 3.1.70; `composer audit` clean (as reported 2026-09-21; not re-run in this audit) |

Related: [[Security Index]] · [[Known Issues and Gaps]]
