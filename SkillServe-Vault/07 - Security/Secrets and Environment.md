---
type: guide
tags: [security, secrets, environment]
sources: [backend/.gitignore, frontend/.gitignore, skill-serve-mobile-application/.gitignore, .gitignore, README.md, DEPLOYMENT.md]
---
# Secrets and Environment

> [!danger] Never commit or paste secrets into this vault
> Real values live only in the Render dashboard (Environment tab) and in local untracked files.
> This vault records variable **names** and local-only defaults, never production values.

## Where secrets live

| Location | Tracked in git? | Contents |
|---|---|---|
| `backend/.env` | no (gitignored) | local config incl. local DB password, Reverb local key/secret |
| `backend/.env.production` | no (gitignored) — exists on the dev machine | a production-style env file (keys only were inspected during the audit; values not read) |
| `backend/.env.example` | **yes** | template with local defaults |
| `frontend/.env*` | no (`.env`, `.env.*` ignored, `.env.example` allowed) | `VITE_API_BASE_URL`, `VITE_REVERB_*` |
| mobile `env/local.json`, `env/production.json` | **yes** | only `API_BASE_URL` (public URLs) |
| mobile `android/key.properties`, `*.jks`, `*.keystore` | no | release signing — back up securely |
| Render environment | n/a | `APP_KEY`, `DB_*` (Neon), `REVERB_APP_SECRET`, `BREVO_API_KEY`/SMTP, `GOOGLE_CLIENT_ID`, `ADMIN_PASSWORD`, `SYSTEM_ADMIN_PASSWORD` |

## Values that are public by design

- Reverb **app key** (sent to browsers/phones); the **secret** must stay private.
- Google **web client id** (compiled into the app as `GOOGLE_WEB_CLIENT_ID` default).
- Local-only credentials in `README.md`/`docker-compose.yml` (`group6` / local password,
  `SkillServe#2026` seed password) — explicitly "never use in production"; production seeding
  refuses the default admin password.

## Rules (AGENT.md)

- Never expose secrets, credentials, tokens or private env values in code, logs, fixtures, commits
  or responses.
- The admin login event carries the plain token in memory but the listener does not log it.

> [!bug] Health endpoint echoes database errors
> `GET /api/health` returns `$e->getMessage()` of a failed DB connection in its JSON body, publicly.
> Connection error messages can include host names. See [[Security Findings]].

Related: [[Environment Variables]] · [[External Integrations]]
