# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

SkillServe admin platform. Follow the full rulebook in @AGENT.md (architecture, backend/frontend rules, "before finishing" checklist). Review format: `AGENT_REVIEW.md`. Requirements source of truth: `SkillServe_Admin_Web_Functionalities.pdf`.

## Repos and git
- Three separate git repos: the root (docs, docker-compose, scripts, `api-docs/`), `backend/` (Laravel 13) and `frontend/` (React/Vite). Run git commands inside the repo you changed; root `.gitignore` excludes `/backend` and `/frontend`.
- Work directly on `main` (Render auto-deploys it). Use conventional commits, e.g. `feat(bookings): ...`, `fix(frontend): ...`.
- A companion Flutter app lives at `/mnt/c/Users/earlf/OneDrive/Desktop/skill-serve-mobile-application` (own repo). It only consumes `/api/client/v1/*`.

## Running things
- Backend commands go through Docker Compose from the root: `docker compose exec backend php artisan ...`, `docker compose exec backend composer test`, `docker compose exec backend ./vendor/bin/pint --dirty`. Single test: `docker compose exec backend php artisan test --filter=ClassName`.
- Ports: backend 8000, Vite 5173, Reverb 8080, Postgres 5433 (`docker compose exec db psql -U group6 -d group6_db`). All services use `network_mode: host`; build with `docker compose build`, not `docker build ./backend`.
- `scripts/fresh-demo.sh` and `scripts/fresh-admin.sh` run `migrate:fresh` and wipe the database; don't run them without asking.
- Frontend: `npm run lint` and `npm run build` in `frontend/`. There is no frontend test framework and no Prettier config.
- Seeded logins (password `SkillServe#2026`): `admin@skillserve.test` (super-admin), `system@skillserve.test` (admin); mobile `customer@skillserve.test` and `provider@skillserve.test` (demo seed only, `DemoAccountSeeder`).

## Backend gotchas
- Tests run on in-memory SQLite, not Postgres. Every test must extend `Tests\TestCase` (it forces SQLite so `RefreshDatabase` can't wipe the live DB). Postgres-only SQL may behave differently in tests.
- Modules are plain namespaces under `app/Modules/<Name>` (`nwidart/laravel-modules` is not used for layout). Module tests go in `app/Modules/<Name>/Tests/Feature/*Test.php` and are picked up by the `Modules` suite.
- Wiring is manual: include each module's `Routes/api.php` in `routes/api.php`; register policies and event listeners in `app/Providers/AppServiceProvider.php`. Client/mobile routes are mounted under `api/client/v1` by `ClientMarketplaceServiceProvider`.
- Responses use the `{ success, message, data, errors, meta }` envelope via the `App\Shared\Traits\ApiResponse` trait (`App\Shared\Services\ApiResponder`); pagination goes in `meta.pagination`. Base classes live in `app/Shared`.
- Swagger must use PHP 8 attributes (`#[OA\Get(...)]`), never `@OA` docblocks — l5-swagger v11 ignores docblocks. Shared schemas are in `app/Shared/Swagger/OpenApi.php`.
- After changing endpoints, regenerate docs: `docker compose exec backend php artisan l5-swagger:generate`, then `php api-docs/generate.php` from the root, then copy `api-docs/` into the Flutter repo's `api-docs/`.
- Explain data impact, deploy order and rollback for any migration. Production uses NeonDB: `DB_HOST` is the `-pooler` host and migrations use the derived direct host.

## Frontend gotchas
- Plain JS/JSX (no TypeScript), relative imports (no `@/` alias), React Compiler enabled.
- Feature code calls `src/services/api.js`, never the raw axios instance. Query keys live in `QUERY_KEYS` in `src/constants`.
- Gate UI with `hasCapability` / `hasAnyCapability` from `src/utils/permissions.js`, and routes with `RequirePermission`; keep permission strings identical to backend Spatie permissions.
- Money is Philippine pesos: use `formatCurrency` from `src/utils` and `DEFAULT_CURRENCY` (`PHP`).
