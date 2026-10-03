---
type: guide
tags: [development, database, seeding]
sources: [backend/database/seeders, backend/config/commissions.php, backend/app/Console/Commands/SeedIfEmpty.php, scripts/fresh-demo.sh, scripts/fresh-admin.sh]
---
# Seeding and Demo Data

## Seed modes (`SEED_MODE`, `DatabaseSeeder`)

| Mode | Seeders | Use |
|---|---|---|
| `admin-only` | `RolePermissionSeeder` | the super-admin alone, nothing else |
| `starter` — **the default setup** (default in production) | + `ServiceCategorySeeder` (8 categories, 25 subcategories), `DefaultCommissionTierSeeder` (the Standard preset from `config/commissions.php`: 5/10/15/20 % by booking amount, only if no tier ever existed), `ProviderBadgeSeeder` (Top Rated, Trusted Provider, Fast Responder, Experienced). No sample people; keeps existing rows | production, and every reset (`scripts/fresh-admin.sh`) |
| `demo` (default outside production; **refused in production**, which falls back to `starter`) | + `UsersSeeder`, `ProviderSeeder`, `DemoAccountSeeder`, `ProviderRecognitionSeeder`, `ServiceSeeder`, `BookingSeeder`, `ReportSeeder`, `NotificationSeeder` | local demos only — **never production** |

`DatabaseSeeder` uses `WithoutModelEvents`.

## Demo volumes (targets in seeders)

| Seeder | Target |
|---|---|
| `UsersSeeder` | 150 customers (password `password`), mix of active/suspended/banned/unverified |
| `ProviderSeeder` | 20 provider profiles |
| `DemoAccountSeeder` | `customer@skillserve.test`, `provider@skillserve.test` (password `SkillServe#2026`, override `DEMO_*`; skipped in production with the default password) |
| `ServiceSeeder` | 40 services |
| `BookingSeeder` | 50 bookings |
| `ReportSeeder` | 30 reports (skips pairs that would violate the one-open-report index) |
| `ProviderRecognitionSeeder`, `NotificationSeeder` | the default badges (via `ProviderBadgeSeeder`) awarded to two featured providers; notifications/announcements |

All seeders are idempotent top-ups ("re-running only tops up what's missing").

## Safety

- `RolePermissionSeeder` seeds the super-admin and **nothing else**, and throws in production if `ADMIN_PASSWORD` is empty
  or the default. Accounts use `firstOrCreate`, so changing the env var later does **not** change an
  existing password.
- Production start runs `php artisan db:seed-if-empty` — seeds only when **no super-admin account
  exists** (`users.role_id` = super-admin). Until 2026-09-30 it checked for any role, which a freshly
  migrated database always has (the 2026_09_18 migration inserts the fixed roles), so a reset
  database never got its super-admin
  (`--fresh` forces).
- `scripts/fresh-demo.sh` / `scripts/fresh-admin.sh` run `migrate:fresh --seed` inside the backend
  container → **wipe the database**. `fresh-admin.sh` seeds `starter` (super-admin + default setup)
  and reloads the Philippine locations. Only for disposable local databases; never run without asking
  (CLAUDE.md).

Related: [[User Types and Roles]] · [[Go-Live Checklist]]
