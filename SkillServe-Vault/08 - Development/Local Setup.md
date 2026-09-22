---
type: guide
tags: [development, setup, docker]
sources: [README.md, docker-compose.yml, backend/Dockerfile, frontend/Dockerfile, skill-serve-mobile-application/README.md]
---
# Local Setup

Full walkthrough lives in the root `README.md`; this is the condensed, verified version.

## Prerequisites

Git; Docker with Compose v2. Windows: Docker Desktop + WSL 2, clone **inside WSL**. Docker Desktop
needs *host networking* enabled (Settings → Resources → Network, 4.34+). Free ports: **5433**
(Postgres), **8000** (API), **5173** (Vite), **8080** (Reverb).

## Steps

```bash
git clone https://github.com/EarlCao/skillserve-web-root.git skillserve
cd skillserve
git clone https://github.com/EarlCao/skillserve-web-backend.git backend
git clone https://github.com/EarlCao/skillserve-web-frontend.git frontend
# create backend/.env and frontend/.env (contents in README.md → "Create the environment files")
docker compose up -d --build        # first build takes minutes
docker compose logs -f backend      # wait for "Server running on [http://0.0.0.0:8000]"
./scripts/fresh-demo.sh             # FIRST TIME ONLY — wipes the DB and seeds demo data
```

Open <http://localhost:5173> → sign in as `admin@skillserve.test` / `SkillServe#2026`.

| Service | Container | URL |
|---|---|---|
| db | `group6-db` | `localhost:5433` |
| backend | `group6-backend` | `http://localhost:8000` (Swagger `/api/documentation`) |
| frontend | `group6-frontend` | `http://localhost:5173` |
| reverb | `group6-reverb` | `localhost:8080` |

The backend container on start: `composer install` → `key:generate` if empty → `migrate --force` →
background `schedule:work` and `queue:work` → `artisan serve` on 8000. Source is bind-mounted
(no rebuild for code changes); `vendor` lives in a named volume.

## Everyday commands

```bash
docker compose exec backend php artisan <cmd>
docker compose exec backend composer test
docker compose exec backend php artisan test --filter=ClassName
docker compose exec backend ./vendor/bin/pint --dirty
docker compose exec db psql -U group6 -d group6_db
(cd frontend && npm run lint && npm run build)
docker compose restart backend reverb     # after .env changes
```

## Mobile app

```bash
flutter pub get
flutter run --dart-define-from-file=env/local.json        # local backend (localhost:8000)
flutter run --dart-define-from-file=env/production.json   # Render
tool/wsl-flutter.sh analyze | test                        # from WSL (Windows Flutter SDK)
```

Without a define file the app targets production. On an Android emulator, `localhost` is the
emulator itself — **Needs Verification** how the team points a device at the local backend (the
repo only ships `http://localhost:8000/api`).

## Networking note

All services use `network_mode: host` because the original dev VM blocked Docker's bridge network.
Removing it requires changing compose, both Dockerfiles' `--network=host` `RUN` steps and
`DB_HOST` together ([[ADR-012 Docker Host Networking]]). Always `docker compose build`, never
`docker build ./backend`.

Troubleshooting: [[Local Environment Issues]].
