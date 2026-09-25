---
type: troubleshooting
tags: [troubleshooting, deployment, render, neon]
sources: [DEPLOYMENT.md → Troubleshooting, skill-serve-mobile-application/SETUP_CREDENTIALS.md]
---
# Deployment Issues

| Symptom | Cause | Fix |
|---|---|---|
| "Connection refused" on Render | wrong `DB_*` values | check `DB_HOST/DATABASE/USERNAME/PASSWORD`; Neon dashboard status |
| SSL errors to Neon | SSL not required | `DB_SSLMODE=require` |
| `could not translate host name "ep-xxx.neon.tech/dbname?sslmode=require"` | a connection-string tail in `DB_HOST` | bare hostname only; keep other parts in separate vars; unset `DB_URL` unless complete |
| `SQLSTATE[25P02] current transaction is aborted` during migrations | migrations running through the **pooler** | ensure the direct host is used (derived from `-pooler`, or set `DB_DIRECT_HOST` without `-pooler`) — the error names the *second* statement |
| `Production seeding requires a non-default ADMIN_PASSWORD value` | default/empty admin passwords in production | set real values (only read on account *creation*) |
| Login times out (~2 min) after idle | free-tier cold start; boot runs migrations/seed before serving | `db:seed-if-empty` avoids reseeding; `PHP_CLI_SERVER_WORKERS=4`; keep-alive ping on `/up` or a paid instance |
| Announcements/notifications never delivered | queue worker/scheduler not running or asleep | `start.sh` supervises both; on free tier they sleep — scheduled items send on wake |
| Migrations fail on deploy | missing `APP_KEY` etc. | generate `APP_KEY` in Render; "APP_KEY is already present" log line is harmless |
| Frontend can't reach API | wrong `VITE_API_BASE_URL` or CORS | set the var (rebuild) and add the origin to `FRONTEND_URLS` |
| Uploads vanish after deploy | no persistent disk | attach disk at `/var/www/html/storage/app` (paid instance); `/api/health` storage status |
| `/api/health` storage `down` | disk missing or not writable | check mount and permissions; see start-up warning |
| OTP mail hangs ~60 s then 500s | SMTP blocked on host | `MAIL_MAILER=brevo-api` + `BREVO_API_KEY` (read via `config()` so it survives `config:cache`) |
| Mail configured locally but not in production | env only in local `.env` | set mail vars on Render (`SETUP_CREDENTIALS.md` §3) |
| nginx 502/504 during restart | app/Reverb restarting | nginx answers a retryable JSON 503; wait |

Related: [[Render Backend Service]] · [[NeonDB]] · [[Release Workflow]]
