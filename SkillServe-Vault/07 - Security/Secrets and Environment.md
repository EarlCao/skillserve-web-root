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
| Render environment | n/a | `APP_KEY`, `DB_*` (Neon), `REVERB_APP_SECRET`, `BREVO_API_KEY`/SMTP, `GOOGLE_CLIENT_ID`, `ADMIN_PASSWORD`. **Not** the `PAYMONGO_*` values — see below |

## PayMongo: the secret that should not exist

Nothing routes to PayMongo ([[ADR-021 Direct Payment with Provider-Remitted Commission]]), so
`PAYMONGO_SECRET_KEY` and `PAYMONGO_WEBHOOK_SECRET` should be **unset everywhere**, including
Render. A key that is never stored cannot be leaked.

Two controls back that up, because the previous leak (`PENDING_FIXES.md` → **C5**, resolved
2026-09-30: live secret key regenerated in PayMongo, both variables deleted from Render) happened by a
key being pasted into a chat:

- `PayMongoClient` refuses every request while an `sk_live_` key is configured unless
  `PAYMONGO_ALLOW_LIVE=true` is set as well. The refusal is logged as `critical`; the key never is.
- `php artisan paymongo:status` reports any environment's posture, and `--probe-key` confirms
  whether a given key is still accepted by PayMongo — how a rotated-out key is verified dead. The
  prompted key is hidden, not logged and not stored.

An exposed key is rotated in PayMongo's dashboard — see `DEPLOYMENT.md` → "Rotating an exposed
PayMongo key" and [[PayMongo Setup]].

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
