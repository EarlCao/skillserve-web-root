---
type: reference
tags: [deployment, render, backend]
sources: [DEPLOYMENT.md, backend/Dockerfile.render, backend/deploy/render/start.sh, backend/deploy/render/nginx.conf]
---
# Render Backend Service

| Setting | Value (per `DEPLOYMENT.md`) |
|---|---|
| Type | Render **Web Service**, runtime Docker |
| Repo | `skillserve-web-backend`, branch `main`, auto-deploy |
| Dockerfile | `Dockerfile.render` |
| Health check | `/up` |
| Instance | paid (Starter+) required for the persistent disk; the free tier sleeps when idle |
| Disk | mount `/var/www/html/storage/app` ([[Render Persistent Disk]]) |
| Configuration | dashboard only — no Blueprint (`render.yaml` was removed) |

> [!warning] Needs Verification — live service
> Hostname (`skillserve-web-backend.onrender.com` per the mobile app vs `skillserve-backend.onrender.com`
> in DEPLOYMENT.md examples), instance type, whether the disk is attached, and whether a keep-alive
> ping exists could not be verified from the code.

## Image (`Dockerfile.render`)

`php:8.3-cli-alpine` + nginx + pdo_pgsql/gd/zip/exif/pcntl; composer install at build; non-root
`app` user; `cp .env.example .env` (real values come from Render env vars);
`ENV PHP_CLI_SERVER_WORKERS=4`; `EXPOSE 10000`; `CMD sh deploy/render/start.sh`.

## Start-up (`deploy/render/start.sh`)

```mermaid
sequenceDiagram
  participant S as start.sh
  S->>S: key:generate if APP_KEY empty
  S->>S: export REVERB_HOST=127.0.0.1:8080 (internal publish)
  S->>S: mkdir storage/app/public, private/dispute-evidence; write-check
  S->>S: config:cache, route:cache, view:cache, storage:link --force
  S->>S: migrate --force (direct Neon host)
  S->>S: db:seed-if-empty
  S->>S: supervise php -S 127.0.0.1:8000 (Laravel)
  S->>S: supervise reverb:start 127.0.0.1:8080
  S->>S: supervise queue:work (--max-time=3600)
  S->>S: supervise schedule:work
  S->>S: wait_for_port 8000 (60 s), 8080 (30 s)
  S->>S: exec nginx on $PORT (default 10000)
```

`supervise` restarts a process 1 s after it exits. nginx routes WebSocket upgrades to Reverb and
everything else to PHP, returns a JSON 503 on 502/504, and allows 20 MB bodies.

## Required environment (names)

`APP_ENV=production`, `APP_DEBUG=false`, `APP_KEY`, `APP_URL`, `FRONTEND_URL` (+`FRONTEND_URLS`),
`DB_CONNECTION=pgsql`, `DB_HOST` (pooler), optional `DB_DIRECT_HOST`, `DB_PORT=5432`,
`DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `DB_SSLMODE=require`, `SESSION_DRIVER/CACHE_STORE/
QUEUE_CONNECTION=database`, `SANCTUM_EXPIRATION`, `LOGIN_RATE_LIMIT`, `REVERB_APP_ID/KEY/SECRET`,
`SEED_MODE=starter` (first deploy) then `admin-only`, `APP_TIMEZONE=UTC`,
`BUSINESS_TIMEZONE=Asia/Manila`, `ADMIN_EMAIL/PASSWORD`, `SYSTEM_ADMIN_EMAIL/PASSWORD` (non-default),
mail (Brevo), `GOOGLE_CLIENT_ID`; `SWAGGER_UI_ENABLED` off unless demoing.

Verify after deploy: logs show migrations/seeding; `GET /api/health` → database and storage `up`;
`GET /api/client/v1/platform` answers.

Related: [[NeonDB]] · [[Release Workflow]] · [[Deployment Issues]]
