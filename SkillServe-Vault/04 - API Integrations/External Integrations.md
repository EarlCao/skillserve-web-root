---
type: reference
tags: [api, integrations, infrastructure]
sources: [DEPLOYMENT.md, backend/app/Shared/Services/BrevoApiTransport.php, backend/app/Shared/Services/ResendApiTransport.php, backend/app/Shared/Services/GmailApiTransport.php, backend/app/Shared/Services/MailjetApiTransport.php, backend/app/Shared/Services/TwilioVerifyClient.php, backend/app/Shared/Services/SendGridApiTransport.php, backend/app/Modules/ClientAuthentication/Services/ClientGoogleAuthService.php, skill-serve-mobile-application/SETUP_CREDENTIALS.md, backend/config/services.php]
---
# External Integrations

| Service | Used for | How it is wired | Config |
|---|---|---|---|
| **NeonDB** | production PostgreSQL | pooled host for queries, direct host for migrations (`config/database.php` → `pgsql.direct`) | `DB_HOST`, `DB_DIRECT_HOST` (optional), `DB_PORT=5432`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `DB_SSLMODE=require` → [[NeonDB]] |
| **Render** | hosting backend (Docker web service) and admin web (static site) | auto-deploy from `main`; configured in the dashboard (no Blueprint; `render.yaml` removed) | → [[Render Backend Service]], [[Frontend Hosting]] |
| **Render persistent disk** | uploads | mounted at `/var/www/html/storage/app` | → [[Render Persistent Disk]] |
| **Brevo** (back 2026-10-07, new account) | every email: the mobile 6-digit codes (sign-up, resend, forgot password), admin password reset, notifications | `MAIL_MAILER=brevo-api`: `BrevoApiTransport` posts to `https://api.brevo.com/v3/smtp/email` over HTTPS; a refusal raises Brevo's `code` and `message`. Brevo answers 201 even for a suspended account, so delivery is checked in Brevo → Transactional → Logs | `BREVO_API_KEY` (`xkeysib-…`); `MAIL_FROM_ADDRESS` on a domain authenticated in Brevo (free DigitalPlat domain, DNS on Cloudflare); Security → Authorized IPs blocking **off** (Render has no fixed IP). Free: 300/day. The first account was suspended on ~2026-10-02 |
| Resend (built; needs a domain) | every email: the mobile 6-digit codes (sign-up, resend, forgot password), admin password reset, notifications | `MAIL_MAILER=resend-api`: `ResendApiTransport` posts to `https://api.resend.com/emails` over HTTPS with the API key as a Bearer token; anything but a 2xx raises Resend's error name and message | `RESEND_API_KEY` (*Sending access*); `MAIL_FROM_ADDRESS` on a domain verified in Resend (free DigitalPlat domain, DNS on Cloudflare). Without a verified domain Resend only delivers to the account owner's own address. Free: 3,000/month, 100/day, 1 domain |
| Gmail API (built; no-domain alternative) | every email, sent as the owner's Gmail | `MAIL_MAILER=gmail-api`: `GmailApiTransport` exchanges the refresh token (scope `gmail.send`) for an access token, cached ~1 h, and posts the MIME message to `users.messages.send` | `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN` (OAuth client in the sign-in Cloud project; consent screen *In production* so the token does not expire after 7 days). Free, about 500/day |
| Mailjet (built; account blocked 2026-10-06) | every email: the mobile 6-digit codes (sign-up, resend, forgot password), admin password reset, notifications | `MAIL_MAILER=mailjet-api`: `MailjetApiTransport` posts to the Send API v3.1 over HTTPS; a refused message raises Mailjet's error code | `MAILJET_API_KEY`, `MAILJET_SECRET_KEY`; `MAIL_FROM_ADDRESS` must be a validated sender. Free: 200/day, 6,000/month |
| Twilio Verify (built, unused) | the mobile 6-digit codes: sign-up, resend, forgot password | `OTP_DRIVER=twilio`: `TwilioVerifyClient` starts a verification (channel `email`) and checks it; SkillServe still enforces the 10-minute expiry, 5 attempts and the 60-second resend window | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_VERIFY_SERVICE_SID`, optional `TWILIO_VERIFY_RESET_TEMPLATE_ID` |
| SendGrid (built, unused) | the email behind Twilio Verify (linked in Twilio → Verify → Email Integration), and every other email via `MAIL_MAILER=sendgrid-api` (`SendGridApiTransport`, HTTPS) | | `SENDGRID_API_KEY`; `MAIL_FROM_ADDRESS` must be a verified sender |
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
