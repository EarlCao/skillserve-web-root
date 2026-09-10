# Group 6 — Web Project

Full-stack project with a **Laravel** backend (`backend/`), a **React + Vite** frontend (`frontend/`), and a **PostgreSQL** database — all running via Docker Compose.

## Cloning the repositories

The project root is **not** a git repository — the frontend and backend are two
separate repositories that must be cloned side by side:

```bash
# from any folder, create the project folder and clone both repos into it
mkdir skillserve && cd skillserve

git clone https://github.com/EarlCao/skillserve-web-backend.git backend
git clone https://github.com/EarlCao/skillserve-web-frontend.git frontend
```

Both repos have `main` and `dev` branches. `dev` is the active development
branch:

```bash
cd backend && git checkout dev
cd ../frontend && git checkout dev
```

> **Important:** `docker-compose.yml` and this `README.md` live at the project
> root, which is *outside* both repositories. When you clone fresh, copy
> `docker-compose.yml` from this workspace into the new project root before
> running the stack (or commit it to one of the two repos so it travels with
> the code). The Dockerfiles inside `backend/` and `frontend/` **are** tracked
> by their respective repos.

## Quick start

```bash
docker compose up -d --build
```

This starts three services:

| Service   | Container        | URL                      | Notes                              |
|-----------|------------------|--------------------------|------------------------------------|
| Database  | `group6-db`      | `localhost:5433`         | PostgreSQL 17, database `group6_db` |
| Backend   | `group6-backend` | `http://localhost:8000`  | Laravel 13 (PHP 8.3), migrations run automatically |
| Frontend  | `group6-frontend`| `http://localhost:5173` | Vite dev server with HMR           |
| Reverb    | `group6-reverb`  | `localhost:8080`         | Laravel Reverb WebSocket server (broadcasting) |

> **Networking note:** this machine is a Hyper-V VM whose sandbox blocks
> outbound traffic from containers on Docker's bridge network, so all services
> run with `network_mode: host` and bind directly to the host's ports.
>
> **If you move this stack to a machine with normal Docker networking**, you
> must remove all of these together, or the build fails with
> `network.host is not allowed`:
> 1. `network_mode: host` on every service (and re-add `ports:` mappings), and
> 2. `network: host` in each `build:` section, and
> 3. `--network=host` in the `RUN` steps of `backend/Dockerfile` and
>    `frontend/Dockerfile`.
>
> Also note that `docker build ./backend` directly will *not* work in this
> sandbox — builds must go through `docker compose build`.
>
> **File ownership:** the backend container runs as uid 1000 to match the host
> user. If your user id is different, pass it when starting: `HOST_UID=$(id -u)
> docker compose up -d --build`.

## Backend packages

The Laravel backend ships with these packages:
`laravel/sanctum` (API tokens), `spatie/laravel-permission` (roles & permissions),
`darkaonline/l5-swagger` (API docs at `/api/documentation` — annotated with
PHP 8 attributes), `spatie/laravel-activitylog`,
`spatie/laravel-medialibrary` + `intervention/image` (file/media uploads),
`maatwebsite/excel` (Excel import/export), `barryvdh/laravel-dompdf` (PDF),
`spatie/laravel-backup`, `spatie/laravel-settings`, `ramsey/uuid`,
`nwidart/laravel-modules` (modular structure under `Modules/`), and
`laravel/reverb` (broadcasting, served on port 8080).

Realtime notifications use Laravel Reverb over authenticated private channels.
The frontend reads `frontend/.env` for `VITE_REVERB_APP_KEY`,
`VITE_REVERB_HOST`, `VITE_REVERB_PORT`, and `VITE_REVERB_SCHEME`; override them
for another environment. The frontend connects after authentication and listens
on `App.Models.User.{id}`. Database notifications remain the source of truth,
so clients can reconnect and refresh the notification inbox safely.

The backend container automatically runs `composer install`, generates an app key
if missing, and applies pending migrations (`php artisan migrate`) on startup.
Source code is bind-mounted, so edits to `backend/` and `frontend/` are picked up
immediately — no rebuild needed. If the app doesn't come up, check
`docker compose ps` and `docker compose logs backend` — a failing migration or
composer error will make the container restart instead of serving.

## Authentication & Authorization (Phase 1)

A modular **Authentication** module is implemented in `backend/app/Modules/Authentication`
and `frontend/src/modules/authentication`.

### API endpoints (`/api/auth/*`)

| Method | Endpoint             | Auth        | Description                        |
|--------|----------------------|-------------|------------------------------------|
| POST   | `/api/auth/login`    | public      | Issue a Sanctum token (rate-limited 5/min/IP) |
| POST   | `/api/auth/logout`   | bearer      | Revoke the current token           |
| GET    | `/api/auth/me`       | bearer      | Current user (roles + permissions) |
| POST   | `/api/auth/change-password` | bearer | Verify + update password      |

All responses use the standard envelope `{ success, message, data, errors, meta }`.
Tokens expire after `SANCTUM_EXPIRATION` minutes (default 1440 = 1 day) and
are revoked on logout. Login/logout/password changes are recorded in the
Spatie activity log.

### First login

Run the seeder once to create the roles, permissions, and the bootstrap
super-admin account:

```bash
docker compose exec backend php artisan db:seed
```

- Email: `admin@skillserve.test`
- Password: `SkillServe#2026` (override via `ADMIN_EMAIL` / `ADMIN_PASSWORD` in `backend/.env`)

Seeding produces exactly this account layout:

| Type | Count | Account |
|------|-------|---------|
| Super admin | 1 | `admin@skillserve.test` (`super-admin` role, bootstrap) |
| System admin | 1 | `system@skillserve.test` (`admin` role; override via `SYSTEM_ADMIN_EMAIL` / `SYSTEM_ADMIN_PASSWORD`) |
| Customers | 150 | Demo `customer` accounts (password `password`) |

The **150 customer accounts** (`UsersSeeder`) populate the User Management
screens. Only customers are seeded as users — role-bearing accounts are
administrators and live in the Administrator Management module. Most
customers are active/verified, with a spread of suspended, banned and
unverified accounts to exercise the moderation features. Both seeders are
idempotent, so re-running only tops up what's missing.

Roles (`super-admin`, `admin`) and permissions (`manage administrators`,
`manage providers`, `manage services`, `manage bookings`, `view reports`)
are defined in `RolePermissionSeeder`.

### Middleware

Reusable middleware included out of the box:

| Middleware | Source | Purpose |
|------------|--------|---------|
| `auth:sanctum` | Laravel Sanctum | Bearer-token auth — expired/revoked tokens return a `401` envelope |
| `role` / `permission` / `role_or_permission` | Spatie (aliased in `bootstrap/app.php`) | RBAC guards, e.g. `->middleware('permission:manage bookings')` or `->middleware('role:admin|super-admin')` |
| `force.json` | `app/Shared/Middleware/ForceJsonResponse.php` | Forces JSON output on every `api/*` request (applied to the `api` group) |
| `throttle:api` | framework | Rate limit: 60 requests/min per user/IP |
| `throttle:login` | `AppServiceProvider` | Login rate limit: 5 attempts/min per IP |
| `EnsureSwaggerUiEnabled` | `app/Shared/Middleware/EnsureSwaggerUiEnabled.php` | Hides the Swagger UI/spec in production unless `SWAGGER_UI_ENABLED=true` |

Usage example (routes/api.php):

```php
Route::middleware(['auth:sanctum', 'permission:manage bookings'])->group(function () {
    // protected module routes
});
```

### Frontend

- Login at `http://localhost:5173/login`; the admin shell requires auth.
- Route guards are reusable: `RequireAuth`, `GuestOnly`, `RequireRole`, `RequirePermission`
  (from `src/modules/authentication/routes/guards.jsx`).
- The auth token lives in `localStorage` (`skillserve:token`); expired/revoked
  sessions (HTTP 401) are cleared automatically and redirect to login.
- `backend/.env` needs `FRONTEND_URL=http://localhost:5173` for CORS (already set).

## Service Category Management (Phase 2)

A modular **Service Categories** module is implemented in
`backend/app/Modules/ServiceCategories` and `frontend/src/modules/serviceCategories`.

Categories organize the platform's available services; each category can hold
any number of subcategories (one level deep). Categories and subcategories are
soft-deleted and carry an `enabled`/`disabled` status — disabling a category
keeps it in the database but makes it unavailable for selection/display on the
platform (never a physical delete).

### API endpoints (`/api/service-categories*`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/service-categories` | Paginated list — search (name/description), status filter, sort |
| POST | `/api/service-categories` | Create a category |
| GET | `/api/service-categories/{id}` | Category details with its subcategories |
| PUT/PATCH | `/api/service-categories/{id}` | Update name/description |
| PATCH | `/api/service-categories/{id}/status` | Enable or disable |
| DELETE | `/api/service-categories/{id}` | Soft-delete — blocked while the category still has subcategories |
| POST | `/api/service-categories/{id}/subcategories` | Create a subcategory (unique per category) |
| PUT/PATCH | `/api/service-categories/{id}/subcategories/{subId}` | Update a subcategory |
| DELETE | `/api/service-categories/{id}/subcategories/{subId}` | Delete a subcategory |

All endpoints require the `manage service categories` permission (granted to
`super-admin`; assign to other roles through Administrator Management). Category
and subcategory actions are recorded in the Spatie activity log
(`service_categories` / `service_subcategories` log names).

### Frontend

- Admin page at `http://localhost:5173/admin/service-categories` (sidebar →
  Administration → Service Categories), gated by the same permission.
- The list supports search, status filter, sorting and pagination; per-row
  actions cover view/manage subcategories, edit, enable/disable and delete.
- Subcategories are managed inside the category details modal (add / edit /
  delete), always scoped to their parent category.
- Demo data: `ServiceCategorySeeder` (via `php artisan db:seed`) creates 8
  categories with 25 subcategories.

## System Settings

The System Settings module is available at `/admin/settings` for administrators
with the `manage settings` permission. It manages general, marketplace, booking,
notification, platform policy, and technical settings through:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/settings` | Return all settings grouped by area |
| PUT | `/api/settings` | Validate and persist one or more setting groups |

Settings are stored in the existing PostgreSQL `settings` table, and updates are
recorded in the `system_settings` activity log. No schema migration is required.

## Data Management

The Data Management module is available at `/admin/data-management` for users
with the data-management permissions. It provides CSV exports, service archive
and restore, and review, restoration, or permanent removal of soft-deleted
records. Archive metadata is stored in the `data_archives` table; the migration
is additive and does not alter existing records.

## API documentation (Swagger / OpenAPI)

Interactive API docs are generated from OpenAPI annotations (written as PHP 8
attributes) and served by l5-swagger:

| URL | What it is |
|-----|------------|
| `http://localhost:8000/api/documentation` | Swagger UI — interactive docs |
| `http://localhost:8000/docs` | Raw OpenAPI JSON spec (`storage/api-docs/api-docs.json`) |

### How to use Swagger

1. **Start the stack** (if not already running):

   ```bash
   docker compose up -d
   ```

2. **Seed the database once** so the admin account and roles exist (skip if
   you already did this):

   ```bash
   docker compose exec backend php artisan db:seed
   ```

3. **Open the Swagger UI** in your browser:

   ```
   http://localhost:8000/api/documentation
   ```

4. **Get an access token** — inside Swagger UI, expand **POST
   `/api/auth/login`**, click **Try it out**, keep the default payload
   (`admin@skillserve.test` / `SkillServe#2026`) and click **Execute**.
   Copy the `token` value from the `data.token` field of the response.

5. **Authorize** — click the **Authorize** button (top-right), paste the
   token, and click **Authorize** → **Close**. This sets the `bearerAuth`
   scheme, so every protected request from the UI now carries your token.

6. **Try the protected endpoints** — e.g. expand **GET `/api/auth/me`**
   and click **Execute** to see the current user (with roles and
   permissions), or **POST `/api/auth/change-password`** to update the
   password. Tokens expire after `SANCTUM_EXPIRATION` minutes (default
   1440 = 1 day); expired/revoked tokens return a `401` envelope.

### Keeping the docs up to date

Regenerate the OpenAPI spec after adding or changing endpoints, then generate
the module-by-module Markdown package in `api-docs/`:

```bash
docker compose exec backend php artisan l5-swagger:generate
php api-docs/generate.php
```

The first command updates `backend/storage/api-docs/api-docs.json`. The second
command copies the generated spec to `api-docs/openapi.json` and regenerates
the endpoint files under `api-docs/modules/` plus `api-docs/MODULES.md`.

Run both commands from the project root. The complete mobile integration
package starts at [`api-docs/README.md`](api-docs/README.md).

`L5_SWAGGER_GENERATE_ALWAYS=true` in `backend/.env` also regenerates the
spec automatically on every docs request (dev convenience; flip to `false`
in production and regenerate on deploy instead).

> **Note:** l5-swagger v11 uses an attribute-only analyser, so annotations
> must be written as PHP 8 attributes (`#[OA\Post(...)]`), not `@OA`
> docblocks. Global metadata lives in `app/Shared/Swagger/OpenApi.php`;
> endpoint annotations live on each controller.
>
> In production the docs are hidden by the `EnsureSwaggerUiEnabled`
> middleware unless `SWAGGER_UI_ENABLED=true` in `backend/.env`.

## Mobile app connectivity

The backend already supports mobile clients via the `/api/client/v1/*` endpoints.
Flutter (or any mobile app) connects using stateless Sanctum bearer tokens:

- **Register:** `POST /api/client/v1/auth/register`
- **Login:** `POST /api/client/v1/auth/login` — returns a 60-minute access token and a 14-day rotating refresh token
- **Authenticated requests:** `Authorization: Bearer <token>` header
- **Token refresh:** `POST /api/client/v1/auth/refresh` with the refresh token
- **Logout:** `POST /api/client/v1/auth/logout` — revokes all sessions

CORS is irrelevant for native mobile apps — no configuration changes are needed.
Rate limits are 60 req/min (general) and 5 req/min (login).

The full mobile integration guide — including token lifecycle, secure storage,
error handling, and public vs protected endpoint lists — is in
[`api-docs/README.md`](api-docs/README.md).

## Useful commands

```bash
docker compose ps                # see running services
docker compose logs -f backend   # follow backend logs
docker compose exec backend php artisan tinker
docker compose exec db psql -U group6 -d group6_db   # open a Postgres shell
docker compose down              # stop the stack
docker compose down -v           # stop and delete the database data
```

## Database credentials

- Host: `127.0.0.1` (services share the host network)
- Port: `5433` (the VM sandbox intercepts the well-known Postgres port 5432)
- Database: `group6_db`
- User: `group6`
- Password: `group6secret`

Change the credentials in `docker-compose.yml` (and `backend/.env`) as you like.

## Running without Docker

The Postgres port is reachable on `localhost:5433`, so you can also run the
backend (`php artisan serve`) and frontend (`npm run dev`) locally while the
database runs in Docker. `backend/.env` already points at `127.0.0.1:5433`.

## Project layout

- `backend/` — Laravel API/application (own git repo)
- `frontend/` — React SPA (own git repo)
