---
type: reference
tags: [development, environment, configuration]
sources: [backend/.env.example, README.md, DEPLOYMENT.md, backend/config, frontend/src/app/config.js, mobile lib/core/config/app_config.dart]
---
# Environment Variables

Names only; see [[Secrets and Environment]] for where values live.

## Backend (`backend/.env`, Render environment)

| Variable | Local default | Production | Read by |
|---|---|---|---|
| `APP_ENV` / `APP_DEBUG` | `local` / `true` | `production` / `false` | framework; CORS localhost pattern only when `local` |
| `APP_KEY` | generated on start | Render "Generate" | framework |
| `APP_URL` | `http://localhost:8000` | backend URL | public disk URL, password reset URL default |
| `APP_TIMEZONE` | `UTC` | `UTC` | storage timezone |
| `BUSINESS_TIMEZONE` | `Asia/Manila` | `Asia/Manila` | `BusinessTime`, settings timezone |
| `FRONTEND_URL` / `FRONTEND_URLS` | `http://localhost:5173` / — | admin web URL(s) | CORS, admin reset link (`config('app.frontend_url')`) |
| `DB_CONNECTION`, `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `DB_SSLMODE` | pgsql, 127.0.0.1, 5433, group6_db, group6, (local), prefer | Neon pooler host, 5432, …, `require` | `config/database.php` |
| `DB_DIRECT_HOST` | — | optional (derived from `-pooler` host) | migrations connection |
| `DB_URL` | empty | leave unset (overrides DB_* when set) | framework |
| `SESSION_DRIVER` / `CACHE_STORE` / `QUEUE_CONNECTION` | database | database | framework |
| `BROADCAST_CONNECTION` | `reverb` | `reverb` | broadcasting |
| `REVERB_APP_ID`, `REVERB_APP_KEY`, `REVERB_APP_SECRET` | `group6`, `skillserve-local-key`, local secret | real values | Reverb |
| `REVERB_HOST`, `REVERB_PORT`, `REVERB_SCHEME`, `REVERB_SERVER_HOST`, `REVERB_SERVER_PORT` | 127.0.0.1, 8080, http, 0.0.0.0, 8080 | forced to 127.0.0.1:8080 by `start.sh` | Reverb / publisher |
| `MAIL_MAILER`, `MAIL_*`, `BREVO_API_KEY` | `log` | `brevo-api` or smtp | mail |
| `SANCTUM_EXPIRATION` | 1440 | 1440 | Sanctum default expiry |
| `LOGIN_RATE_LIMIT` | 5 | 5 | `login` limiter |
| `CLIENT_AUTH_RATE_LIMIT` | 20 | 20 | `client-auth` limiter |
| `CLIENT_ACCESS_TOKEN_EXPIRATION` | 60 | — | `config/client-auth.php` |
| `CLIENT_REFRESH_TOKEN_EXPIRATION` | 525600 | — | same |
| `CLIENT_BACKGROUND_TOKEN_EXPIRATION` | 525600 | — | same |
| `CLIENT_PROFILE_PHOTO_DISK` | `public` | — | same |
| `CLIENT_PASSWORD_RESET_URL` | `APP_URL/client/reset-password` | **not documented** | mobile reset email link (KI-02) |
| `GOOGLE_CLIENT_ID` | empty | web client id | Google token audience check |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` (`SYSTEM_ADMIN_*` retired — no second admin is seeded) | `*@skillserve.test`, `SkillServe#2026` | real, non-default (enforced) | `RolePermissionSeeder` |
| `DEMO_CUSTOMER_EMAIL`, `DEMO_PROVIDER_EMAIL`, `DEMO_ACCOUNT_PASSWORD` | defaults | skipped in prod unless non-default | `DemoAccountSeeder` |
| `SEED_MODE` | `demo` | `starter` then `admin-only` | `DatabaseSeeder` |
| `L5_SWAGGER_GENERATE_ALWAYS` | true | false | l5-swagger |
| `SWAGGER_UI_ENABLED` | false (always on locally) | off unless demoing | `EnsureSwaggerUiEnabled` |
| `API_CACHE_MAX_AGE` | 0 | 0 | `CacheApiResponse` |
| `PHP_CLI_SERVER_WORKERS` | — | 4 (Dockerfile.render) | PHP built-in server |
| `HOST_UID` | 1000 | — | docker-compose build arg |
| `POSTGRES_DB/USER/PASSWORD` | group6 defaults | — | docker-compose |

## Admin web (`frontend/.env`, Render static-site env — inlined at build time)

`VITE_API_BASE_URL`, `VITE_REVERB_APP_KEY`, `VITE_REVERB_HOST`, `VITE_REVERB_PORT`,
`VITE_REVERB_SCHEME`. Changing one needs a rebuild/redeploy.

## Mobile (`--dart-define` / `env/*.json`)

`API_BASE_URL`, `REVERB_APP_KEY`, `REVERB_HOST`, `REVERB_PORT`, `REVERB_SCHEME`,
`GOOGLE_WEB_CLIENT_ID`.

Related: [[Local Setup]] · [[Render Backend Service]]
