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

## Step 2 — Deploy Backend to Render

> **Which repository is Render connected to?** Render only reads `render.yaml`
> from the root of the repository that a service is connected to. In this
> project the backend lives in its own repo (`skillserve-web-backend`), which
> does not contain `render.yaml` — so a service created from that repo is
> configured entirely through the Render dashboard (see **Option C**). Options A
> and B only apply if `backend/` and `frontend/` are part of the same repo as
> `render.yaml`.

### Option A: Using render.yaml (Blueprint)

1. Push your code to GitHub (the `main` branch).
2. Go to [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Connect your GitHub repo.
4. Render will detect `render.yaml` and set up:
   - A web service for the backend
   - A static site for the frontend
5. Set the environment variables in Render's dashboard:
   - `DB_HOST`, `DB_PORT`, `DB_CONNECTION`, `DB_SSLMODE` — already declared in
     `render.yaml`; Render applies them on sync (see the note below)
   - `DB_DATABASE` — the database name from your Neon project (Neon's default is
     `neondb`, but it must match the connection string exactly)
   - `DB_USERNAME` — the Neon role, e.g. `neondb_owner`
   - `DB_PASSWORD` — the Neon password
   - `APP_URL` — your Render backend URL (e.g. `https://skillserve-backend.onrender.com`)
   - `FRONTEND_URL` — your Render frontend URL
   - `REVERB_APP_KEY`, `REVERB_APP_SECRET` — generate new ones for production

   ⚠️ **NeonDB is an external database**, so `fromDatabase` in `render.yaml` cannot
   supply it (that property only resolves Render-managed Postgres).

   ⚠️ **`DB_HOST` must be the bare hostname** — only this, nothing else:
   ```
   ep-xxx-pooler.us-east-2.aws.neon.tech
   ```
   Do not paste the connection string, and do not append the database name or
   `?sslmode=require`. A value like
   `ep-xxx-pooler.us-east-2.aws.neon.tech/SkillServe_DB?sslmode=require` is handed
   to libpq as the host, and the deploy dies with a DNS failure.

   Also delete any `DB_URL` variable from the dashboard — when it is set, Laravel
   derives host/port/database/user/password from it and ignores the values above.

### Option B: Manual Setup

1. **Backend Web Service**:
   - Go to **New** → **Web Service**
   - Connect your GitHub repo
   - Runtime: `PHP`
   - Build Command:
     ```bash
     cp .env.production .env
     composer install --no-dev --optimize-autoloader
     php artisan key:generate --no-interaction --force
     php artisan config:cache
     php artisan route:cache
     php artisan view:cache
     php artisan migrate --force
     php artisan db:seed --force
     ```
   - Start Command: `php artisan serve --host=0.0.0.0 --port=$PORT`
   - Health Check Path: `/up`

2. **Set Environment Variables** in Render dashboard:
   ```
   APP_ENV=production
   APP_DEBUG=false
   APP_URL=https://skillserve-backend.onrender.com
   DB_CONNECTION=pgsql
   DB_HOST=ep-xxx-pooler.us-east-2.aws.neon.tech
   DB_PORT=5432
   DB_DATABASE=neondb
   DB_USERNAME=neondb_owner
   DB_PASSWORD=your-neon-password
   DB_SSLMODE=require
   SESSION_DRIVER=database
   CACHE_STORE=database
   QUEUE_CONNECTION=database
   FRONTEND_URL=https://skillserve-frontend.onrender.com
   SANCTUM_EXPIRATION=1440
   ```

3. **Frontend Static Site**:
   - Go to **New** → **Static Site**
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
   - Set environment variables:
     ```
     VITE_API_BASE_URL=https://skillserve-backend.onrender.com/api
     VITE_REVERB_APP_KEY=your-reverb-key
     VITE_REVERB_HOST=skillserve-backend.onrender.com
     VITE_REVERB_PORT=443
     VITE_REVERB_SCHEME=https
     ```

### Option C: Backend repo as a standalone Docker web service

This is the setup this project actually uses: the backend is deployed from its
own repository, so there is no Blueprint and the dashboard is the single source
of truth for its configuration.

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
   DB_PORT=5432
   DB_DATABASE=neondb
   DB_USERNAME=neondb_owner
   DB_PASSWORD=your-neon-password
   DB_SSLMODE=require
   SESSION_DRIVER=database
   CACHE_STORE=database
   QUEUE_CONNECTION=database
   ```

   ⚠️ `DB_HOST` must be the **bare hostname** copied from Neon's *Connect* panel.
   Do not set `DB_URL` unless it holds a complete connection string — when it is
   set, Laravel parses it and ignores `DB_HOST`/`DB_DATABASE`/`DB_USERNAME`/
   `DB_PASSWORD`.

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

### Migrations fail on deploy
- Check Render logs: **Logs** tab → filter by service.
- Ensure `APP_KEY` is generated (Render auto-generates it via `generateValue`).
  The log line `Unable to set application key. APP_KEY is already present in the
  environment.` is harmless — it only means the key came from the platform
  instead of the `.env` file.

### Frontend can't reach backend API
- Ensure `VITE_API_BASE_URL` is set correctly in the frontend service.
- Check CORS settings — `FRONTEND_URLS` must include the frontend domain.
