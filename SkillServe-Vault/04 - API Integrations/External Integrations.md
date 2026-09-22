---
type: reference
tags: [api, integrations, infrastructure]
sources: [DEPLOYMENT.md, backend/app/Shared/Services/BrevoApiTransport.php, backend/app/Modules/ClientAuthentication/Services/ClientGoogleAuthService.php, skill-serve-mobile-application/SETUP_CREDENTIALS.md, backend/config/services.php]
---
# External Integrations

| Service | Used for | How it is wired | Config |
|---|---|---|---|
| **NeonDB** | production PostgreSQL | pooled host for queries, direct host for migrations (`config/database.php` → `pgsql.direct`) | `DB_HOST`, `DB_DIRECT_HOST` (optional), `DB_PORT=5432`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `DB_SSLMODE=require` → [[NeonDB]] |
| **Render** | hosting backend (Docker web service) and admin web (static site) | auto-deploy from `main`; configured in the dashboard (no Blueprint; `render.yaml` removed) | → [[Render Backend Service]], [[Frontend Hosting]] |
| **Render persistent disk** | uploads | mounted at `/var/www/html/storage/app` | → [[Render Persistent Disk]] |
| **Brevo** | transactional email (OTP, password reset, moderation mail) | `MAIL_MAILER=brevo-api` uses `BrevoApiTransport` over HTTPS (for hosts that block SMTP) or standard SMTP | `BREVO_API_KEY` (read via `config('services.brevo.api_key')`), timeout `services.brevo.timeout` (15 s) |
| **Google Identity** | "Sign in with Google" on mobile | app gets an ID token (`serverClientId` = web client id); backend verifies with Google's **tokeninfo** endpoint and checks `aud` | backend `GOOGLE_CLIENT_ID`; app `GOOGLE_WEB_CLIENT_ID`; Android OAuth client for `com.skillserve.mobile` + SHA-1 (`SETUP_CREDENTIALS.md` §2) |
| **Laravel Reverb** | WebSockets | self-hosted inside the backend container | `REVERB_*`, `VITE_REVERB_*`, app `REVERB_*` defines |
| **Vercel** | possibly an earlier/alternate admin web host | `frontend/vercel.json` rewrites; CORS allows two `*.vercel.app` origins | **Needs Verification** whether still used |
| **UptimeRobot / cron ping** | keep free-tier Render awake | mentioned as a mitigation only | **Needs Verification** whether configured |

## Mail configuration notes

- Local: `MAIL_MAILER=log` (emails go to `storage/logs/laravel.log`).
- Production: OTP mail must be configured **on Render**, not just locally
  (`SETUP_CREDENTIALS.md` §3). If SMTP hangs ~60 s then 500s, switch to `brevo-api`.
- OTP mail failures are logged to stderr so Render captures them (backend commit 2026-09-13).

## Secrets handling

Real values live only in Render's environment tab and local untracked `.env` files
(`backend/.env`, `backend/.env.production` and `frontend/.env*` are gitignored). The vault never
records secret values. See [[Secrets and Environment]].

Related: [[Environment Variables]] · [[Deployment Index]]
