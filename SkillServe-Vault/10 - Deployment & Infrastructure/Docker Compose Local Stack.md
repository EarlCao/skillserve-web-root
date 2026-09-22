---
type: reference
tags: [deployment, docker, local]
sources: [docker-compose.yml, backend/Dockerfile, frontend/Dockerfile]
---
# Docker Compose Local Stack

Compose project name `group6`. **All services use `network_mode: host`** and build with
`network: host`.

| Service | Image / build | Container | Port | Notes |
|---|---|---|---|---|
| `db` | `postgres:17-alpine` | `group6-db` | 5433 (loopback only: `listen_addresses=127.0.0.1`) | volume `db_data`; healthcheck `pg_isready`; creds from `POSTGRES_*` (defaults `group6_db` / `group6` / local password) |
| `backend` | `./backend` (`Dockerfile`, `php:8.3-cli-alpine`, pdo_pgsql gd zip exif pcntl, composer 2, non-root user with `UID=${HOST_UID:-1000}`) | `group6-backend` | 8000 | bind-mount `./backend`, named volume `backend_vendor`; env forces pgsql on 127.0.0.1:5433; depends on healthy db |
| `frontend` | `./frontend` (`node:22-alpine`, `npm ci`, non-root `node`) | `group6-frontend` | 5173 | bind-mount `./frontend`, anonymous `node_modules`; `npm run dev -- --host 0.0.0.0 --port 5173` |
| `reverb` | `./backend` (same image) | `group6-reverb` | 8080 | `php artisan reverb:start --host=0.0.0.0 --port=8080` |

Backend container `CMD`: `composer install` → `php artisan key:generate` (ignored if set) →
`php artisan migrate --force` → background `schedule:work` and
`queue:work --queue=default --sleep=3 --tries=3 --timeout=90` → `php artisan serve --host=0.0.0.0 --port=8000`.

Why port 5433 and host networking: the original dev machine is a Hyper-V VM whose sandbox
intercepts 5432 and blocks bridge-network egress (comments in `docker-compose.yml`;
[[ADR-012 Docker Host Networking]]).

Commands: `docker compose up -d --build`, `docker compose ps`, `docker compose logs -f backend`,
`docker compose down` (keep data) / `down -v` (delete DB volume).

Related: [[Local Setup]] · [[Local Environment Issues]]
