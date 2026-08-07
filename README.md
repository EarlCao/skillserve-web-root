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

The backend container automatically runs `composer install`, generates an app key
if missing, and applies pending migrations (`php artisan migrate`) on startup.
Source code is bind-mounted, so edits to `backend/` and `frontend/` are picked up
immediately — no rebuild needed. If the app doesn't come up, check
`docker compose ps` and `docker compose logs backend` — a failing migration or
composer error will make the container restart instead of serving.

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
