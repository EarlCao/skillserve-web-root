---
type: guide
tags: [development, database, seeding]
sources: [backend/database/seeders, backend/app/Console/Commands/SeedIfEmpty.php, scripts/fresh-demo.sh, scripts/fresh-admin.sh]
---
# Seeding and Demo Data

## Seed modes (`SEED_MODE`, `DatabaseSeeder`)

| Mode | Seeders | Use |
|---|---|---|
| `admin-only` | `RolePermissionSeeder` | minimal; production after first deploy |
| `starter` | + `ServiceCategorySeeder` (8 categories, 25 subcategories; keeps existing) | first production deploy |
| `demo` (default) | + `UsersSeeder`, `ProviderSeeder`, `DemoAccountSeeder`, `ProviderRecognitionSeeder`, `ServiceSeeder`, `BookingSeeder`, `ReportSeeder`, `NotificationSeeder` | local demos only — **never production** |

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
| `ProviderRecognitionSeeder`, `NotificationSeeder` | badges; notifications/announcements |

All seeders are idempotent top-ups ("re-running only tops up what's missing").

## Safety

- `RolePermissionSeeder` throws in production if `ADMIN_PASSWORD`/`SYSTEM_ADMIN_PASSWORD` are empty
  or the default. Accounts use `firstOrCreate`, so changing the env var later does **not** change an
  existing password.
- Production start runs `php artisan db:seed-if-empty` — seeds only when `roles` is empty
  (`--fresh` forces).
- `scripts/fresh-demo.sh` / `scripts/fresh-admin.sh` run `migrate:fresh --seed` inside the backend
  container → **wipe the database**. Only for disposable local databases; never run without asking
  (CLAUDE.md).

Related: [[User Types and Roles]] · [[Go-Live Checklist]]
