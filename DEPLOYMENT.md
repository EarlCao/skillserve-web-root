# Deployment Guide — NeonDB + Render

## Overview

This guide covers deploying the SkillServe backend to **Render** with **NeonDB** as the production PostgreSQL database, and setting up a dev/staging workflow where you can test changes before merging to main.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  PRODUCTION (Render)                                     │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐                   │
│  │  Frontend     │    │  Backend     │                   │
│  │  (Static)     │───▶│  (Laravel)   │────▶ NeonDB      │
│  │  Render       │    │  Render      │     (external)   │
│  └──────────────┘    └──────────────┘                   │
│                                                          │
│  URL: *.onrender.com                                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  DEVELOPMENT (Local WSL)                                 │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │  Frontend     │    │  Backend     │    │  NeonDB    │ │
│  │  localhost:5173│───▶│ localhost:8000│───▶│ (dev branch)│
│  └──────────────┘    └──────────────┘    └───────────┘ │
│                                                          │
│  You can also use local Docker PostgreSQL for dev.       │
└─────────────────────────────────────────────────────────┘
```

---

## Step 1 — Create a NeonDB Database

1. Go to [neon.tech](https://neon.tech) and create an account.
2. Create a new project (e.g. `skillserve`).
3. In the NeonDB dashboard, copy the **connection string** — it looks like:
   ```
   postgresql://neondb_owner:password@ep-xxx.us-east-2.aws.neon.tech/skillserve?sslmode=require
   ```
4. **Optional**: Connect pgAdmin to NeonDB to view your data:
   - Host: `ep-xxx.us-east-2.aws.neon.tech`
   - Port: `5432`
   - Database: `skillserve`
   - Username: `neondb_owner`
   - Password: (from NeonDB dashboard)
   - SSL Mode: `Require`

---

## Step 2 — Deploy to Render

The backend and frontend deploy from their own repositories
(`skillserve-web-backend`, `skillserve-web-frontend`), neither of which contains
a Blueprint. Each Render service is therefore configured entirely in the Render
dashboard, and this section is the reference for what that configuration should
be. Keep it in step with the dashboard when you change either.

### Backend — Docker web service

1. [Render Dashboard](https://dashboard.render.com) → **New** → **Web Service**.
2. Connect the `skillserve-web-backend` repo.
3. Runtime: **Docker**, Dockerfile Path: `Dockerfile.render`.
4. Health Check Path: `/up`.
5. Set these on the **Environment** tab:

   ```
   APP_ENV=production
   APP_DEBUG=false
   APP_KEY=            # leave blank — use Render's "Generate" button
   APP_URL=https://skillserve-backend.onrender.com
   FRONTEND_URL=https://skillserve-frontend.onrender.com
   DB_CONNECTION=pgsql
   DB_HOST=ep-xxx-pooler.us-east-2.aws.neon.tech
   DB_DIRECT_HOST=ep-xxx.us-east-2.aws.neon.tech   # optional, see below
   DB_PORT=5432
   DB_DATABASE=neondb
   DB_USERNAME=neondb_owner
   DB_PASSWORD=your-neon-password
   DB_SSLMODE=require
   SESSION_DRIVER=database
   CACHE_STORE=database
   QUEUE_CONNECTION=database
   SANCTUM_EXPIRATION=1440
   LOGIN_RATE_LIMIT=5
   REVERB_APP_ID=skillserve
   REVERB_APP_KEY=generate-a-random-key
   REVERB_APP_SECRET=generate-a-random-secret
   SEED_MODE=admin-only
   ADMIN_EMAIL=admin@yourdomain.com
   ADMIN_PASSWORD=replace-me-with-a-strong-password
   SYSTEM_ADMIN_EMAIL=system@yourdomain.com
   SYSTEM_ADMIN_PASSWORD=replace-me-with-a-strong-password
   ```

   ⚠️ **Seeding.** `SEED_MODE=admin-only` seeds just the roles, permissions
   and the bootstrap admin accounts. The default (`SEED_MODE=demo`) additionally
   seeds the full demo dataset, which must never run against production — and
   since the container seeds on every start, leaving it on `demo` re-seeds demo
   data on every restart. Production seeding also refuses the built-in default
   password (`SkillServe#2026`), so `ADMIN_PASSWORD` and
   `SYSTEM_ADMIN_PASSWORD` must be set to real values before the first deploy.

   ⚠️ Both hosts must be **bare hostnames** copied from Neon's *Connect* panel.
   Do not set `DB_URL` unless it holds a complete connection string — when it is
   set, Laravel parses it and ignores `DB_HOST`/`DB_DATABASE`/`DB_USERNAME`/
   `DB_PASSWORD`.

   **Why two hosts?** Neon's `-pooler` endpoint runs pgBouncer in transaction
   mode, which cannot execute schema changes. `DB_HOST` is the pooled endpoint
   used for normal queries; the direct endpoint is the same host *without*
   `-pooler` and is used for migrations and DDL. Laravel detects the pair and
   routes automatically (`config/database.php` → `pgsql.direct`).

   `DB_DIRECT_HOST` is **optional**: when it is unset, `config/database.php`
   derives it by stripping `-pooler` from `DB_HOST`. Set it only for a host that
   does not follow Neon's naming. A `DB_DIRECT_HOST` that still points at the
   pooler is ignored, because migrations cannot run through it.

### Uploaded files — Render persistent disk

A Render web service has an **ephemeral filesystem**: every deploy or restart
resets the container, and anything written to it is lost. Uploads —
profile photos, portfolio images, provider verification documents and dispute
evidence — are all written under `storage/app` by Laravel's local disks:

| Disk | Folder | Holds | Access |
|------|--------|-------|--------|
| `public` | `storage/app/public` | profile photos, portfolio images | public, served at `/storage/...` |
| `verification` | `storage/app/private` | provider ID and certificate uploads | private; streamed by the API to admins |
| `dispute_evidence` | `storage/app/private/dispute-evidence` | dispute photos | private; streamed by the API to admins |

To keep them, attach a **persistent disk** to the backend service so that
folder lives outside the container:

1. The service must be on a paid instance type (**Starter** or above); the
   free tier cannot have a disk. Change it under **Settings → Instance Type**.
2. **Settings → Disks → Add Disk**:
   - Mount Path: `/var/www/html/storage/app` (the app lives in
     `/var/www/html`, see `Dockerfile.render`)
   - Size: 1 GB is plenty to start; it can be grown later, not shrunk.
3. Save. Render redeploys with the disk mounted.

On start-up, `deploy/render/start.sh` recreates the folders on a new, empty
disk and links `public/storage` to `storage/app/public`. It logs a warning if
`storage/app` is not writable, and `GET /api/health` then reports
`services.storage` as `down`. Check both after the first deploy with the disk.

Things to know:

- A service with a disk runs as **one instance** and has a few seconds of
  downtime on each deploy, because the disk can be attached to one running
  container at a time. That is fine for this project.
- Render snapshots the disk daily; restore from **Disks → Snapshots**.
- Files uploaded before the disk existed lived in the old container and are
  already gone; those users re-upload them.
- Only `storage/app` is on the disk. Logs, caches and compiled views stay in
  the container and are rebuilt on every start.

### Frontend — static site

1. [Render Dashboard](https://dashboard.render.com) → **New** → **Static Site**.
2. Connect the `skillserve-web-frontend` repo.
3. Build Command: `npm install && npm run build`. Publish Directory: `dist`.
4. **Redirects/Rewrites** tab: add a rewrite from `/*` to `/index.html`, so a
   refresh on a deep link such as `/admin/bookings` still loads the app.
5. Set these on the **Environment** tab. Vite inlines them at build time, so
   changing one needs a redeploy:

   ```
   VITE_API_BASE_URL=https://skillserve-backend.onrender.com/api
   VITE_REVERB_APP_KEY=same-value-as-the-backend-REVERB_APP_KEY
   VITE_REVERB_HOST=skillserve-backend.onrender.com
   VITE_REVERB_PORT=443
   VITE_REVERB_SCHEME=https
   ```

---

## Step 3 — Dev/Prod Workflow

### Branch Strategy

```
main (production)     ← stable, deployed to Render
  ↑
dev                   ← active development, test here first
  ↑
feature-branches      ← individual features
```

### Workflow

1. **Create a feature branch** from `dev`:
   ```bash
   git checkout dev
   git checkout -b feature/my-feature
   ```

2. **Develop locally** using Docker (local PostgreSQL):
   ```bash
   docker compose up -d --build
   ```

3. **Test locally** — run the app at `http://localhost:5173` and verify the API at `http://localhost:8000/api`.

4. **Merge to `dev`** when ready:
   ```bash
   git checkout dev
   git merge feature/my-feature
   git push origin dev
   ```

5. **Test on dev NeonDB branch** (optional):
   - Create a separate NeonDB branch for dev testing
   - Or use a separate NeonDB project for dev
   - Update `DB_URL` in your local `.env` to point to the dev NeonDB
   - Connect pgAdmin to verify data

6. **Merge to `main`** when dev is verified:
   ```bash
   git checkout main
   git merge dev
   git push origin main
   ```
   - Render auto-deploys on push to `main`

---

## Step 4 — Connect pgAdmin to NeonDB

### For Development/Testing

1. Open pgAdmin.
2. Right-click **Servers** → **Register** → **Server**.
3. **General** tab:
   - Name: `SkillServe Dev` (or `SkillServe Prod`)
4. **Connection** tab:
   - Host: `ep-xxx.us-east-2.aws.neon.tech` (from NeonDB dashboard)
   - Port: `5432`
   - Database: `skillserve`
   - Username: `neondb_owner`
   - Password: (from NeonDB dashboard)
5. **SSL** tab:
   - SSL Mode: `Require`
   - Root Certificate: Download from NeonDB and select the `.pem` file
6. Click **Save**.

You can now browse tables, run queries, and verify data after each deployment.

---

## Environment Variables Reference

| Variable | Dev (Local) | Production (Render) |
|----------|-------------|---------------------|
| `APP_ENV` | `local` | `production` |
| `APP_DEBUG` | `true` | `false` |
| `APP_URL` | `http://localhost` | `https://skillserve-backend.onrender.com` |
| `DB_URL` | _(not used)_ | _(leave unset)_ |
| `DB_HOST` | `127.0.0.1` | Neon pooled hostname (bare, no `/db` or query) |
| `DB_DIRECT_HOST` | _(unset)_ | optional — derived from `DB_HOST` when unset |
| `SEED_MODE` | `demo` | `admin-only` |
| `ADMIN_PASSWORD` | `SkillServe#2026` | required, non-default |
| `SYSTEM_ADMIN_PASSWORD` | `SkillServe#2026` | required, non-default |
| `DB_PORT` | `5433` | `5432` |
| `DB_DATABASE` | `group6_db` | Neon database name |
| `DB_SSLMODE` | `prefer` | `require` |
| `SESSION_DRIVER` | `database` | `database` |
| `CACHE_STORE` | `database` | `database` |
| `FRONTEND_URL` | `http://localhost:5173` | `https://skillserve-frontend.onrender.com` |

---

## NeonDB Free Tier Limits

- **Compute**: 0.25 CPU, 1 GB RAM (free tier)
- **Storage**: 512 MB
- **Connections**: 100 simultaneous
- **Branches**: 10 total
- **Projects**: 1

For production, consider upgrading to a paid plan for better performance.

---

## Troubleshooting

### "Connection refused" on Render
- Ensure `DB_HOST`, `DB_DATABASE`, `DB_USERNAME` and `DB_PASSWORD` are set
  correctly in Render's environment variables.
- Check NeonDB dashboard for connection status.

### SSL errors connecting to NeonDB
- Set `DB_SSLMODE=require` in your environment.
- NeonDB requires SSL for all connections.

### `could not translate host name "ep-xxx.neon.tech/dbname?sslmode=require" to address`
- Laravel received the **tail of a connection string** as the host instead of a
  hostname. Laravel builds the pgsql DSN as `host=<DB_HOST>`, so anything after
  the hostname (`/dbname`, `?sslmode=require`, `&channel_binding=require`) is
  passed straight to libpq, which then fails to resolve it.
- Fix: set `DB_HOST` to the bare hostname (`ep-xxx-pooler.us-east-2.aws.neon.tech`).
  Keep `DB_DATABASE`, `DB_USERNAME` and `DB_PASSWORD` as separate variables —
  they are not part of the host.
- If `DB_URL` is set in the service environment, it takes precedence over
  `DB_HOST`; remove it unless it holds the complete, valid connection string.

### `SQLSTATE[25P02] current transaction is aborted` during migrations
- This is Neon's **pooled** endpoint rejecting schema changes. pgBouncer in
  transaction mode cannot support the DDL and server-side prepared statements
  that Laravel's migrations use, so the first statement silently does nothing
  and the next one in the same transaction reports the abort.
- Fix: make sure the direct endpoint is in use. `config/database.php` derives
  it from `DB_HOST` by stripping `-pooler`; for a host that doesn't follow
  Neon's naming, set `DB_DIRECT_HOST` to the endpoint **without** `-pooler`
  (Neon's *Connect* panel → connection pooling off).
- Note the visible error names the *second* statement (`alter table ... add
  constraint ...`), not the one that actually failed, so don't chase the
  constraint itself.

### `Production seeding requires non-default ADMIN_PASSWORD and SYSTEM_ADMIN_PASSWORD values`
- `RolePermissionSeeder` refuses to create admin accounts in production with the
  built-in default password. Set `ADMIN_PASSWORD` and `SYSTEM_ADMIN_PASSWORD` in
  the service environment to real values.
- These are only read when the account is *created* — `firstOrCreate` means
  changing the variable later does not update an existing account's password.

### Login times out (~2 min) after the service has been idle
- Render's **free tier spins idle services down**; the next request pays a full
  container cold start. The container runs migrations and seeding *before*
  `artisan serve` starts listening, so that first request waits for the whole
  boot.
- Seeding is guarded: the container now runs `php artisan db:seed-if-empty`,
  which skips seeding when the database is already seeded (`--fresh` forces a
  re-run). Demo data is therefore inserted only on the very first boot, not on
  every cold start.
- `php artisan serve` is also started with `PHP_CLI_SERVER_WORKERS=4` so
  concurrent browser requests don't queue behind a single worker.
- Remaining mitigations: keep a health-check ping on the service (Render
  cron-job / UptimeRobot hitting `/up`) so it never sleeps, or upgrade off the
  free tier.

### Announcements or notifications are never delivered
- Queued work (announcements, scheduled announcements, realtime notification
  broadcasts) needs a queue worker, and expired bans need the scheduler.
  `Dockerfile.render` starts both in the background next to `artisan serve`,
  restarting each if it exits.
- On the free tier they sleep with the service, so a scheduled announcement
  whose time passes while the service is idle is sent on the next wake-up.
- The mobile app has no WebSocket connection; it checks
  `GET /api/client/v1/notifications/unread-count` every 30 seconds while open
  and signed in, so new notifications appear within about 30 seconds.

### Migrations fail on deploy
- Check Render logs: **Logs** tab → filter by service.
- Ensure `APP_KEY` is set (use the **Generate** button on the Environment tab).
  The log line `Unable to set application key. APP_KEY is already present in the
  environment.` is harmless — it only means the key came from the platform
  instead of the `.env` file.

### Frontend can't reach backend API
- Ensure `VITE_API_BASE_URL` is set correctly in the frontend service.
- Check CORS settings — `FRONTEND_URLS` must include the frontend domain.
