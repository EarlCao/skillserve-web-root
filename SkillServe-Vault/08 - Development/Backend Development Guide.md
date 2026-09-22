---
type: guide
tags: [development, backend, how-to]
sources: [backend/routes/api.php, backend/app/Providers/AppServiceProvider.php, backend/app/Modules/ClientMarketplace/Providers/ClientMarketplaceServiceProvider.php, CLAUDE.md]
---
# Backend Development Guide

How to add or change backend behaviour so it matches the existing modules.

## Adding an admin endpoint to an existing module

1. **Request:** `app/Modules/<M>/Requests/<Verb><Thing>Request.php` extending `BaseFormRequest`
   (rules + `prepareForValidation` normalisation).
2. **Policy / gate:** add a method to the module policy (check the granular permission OR the
   module's `manage …`); if a new permission is needed, add it to `RolePermissionSeeder` **and**
   create a data migration that upserts it (see existing `add_*_permissions` migrations).
3. **Service / action:** business rule in the service; single write in an action; wrap state changes
   in `$this->transaction()` with `lockForUpdate()`.
4. **Event + listeners:** fire an event; register `Log…Activity` / `Notify…` listeners in
   `AppServiceProvider::boot()` (no auto-discovery).
5. **Controller:** `$this->authorize(...)` → service → `return $this->success(new XResource(...))`
   (or `paginated`).
6. **Route:** in `app/Modules/<M>/Routes/api.php` under the module prefix with `auth:sanctum`.
7. **Swagger:** `#[OA\...]` attributes on the controller method (never docblocks).
8. **Test:** `app/Modules/<M>/Tests/Feature/*Test.php` extending `Tests\TestCase` — happy path,
   validation, authorization, failure paths.
9. **Docs:** `l5-swagger:generate` → `php api-docs/generate.php` → copy to the mobile repo →
   regenerate vault endpoint notes ([[API Documentation Pipeline]]).
10. **Frontend/mobile:** add the API call, query key, UI; update [[Frontend-to-API Map]] /
    [[Mobile-to-API Map]].

## Adding a new module

- Create `app/Modules/<Name>/{Controllers,Requests,Services,Actions,Policies,Resources,Routes,Tests/Feature}`.
- Admin: include `Routes/api.php` in `routes/api.php` (`Route::group([], base_path(...))`).
- Client (mobile): include it from `ClientMarketplaceServiceProvider::boot()` inside the
  `api/client/v1` group (it gets `EnsurePlatformAvailable`); protect with
  `auth:sanctum` + `EnsureClient`/`EnsureProvider`/`EnsureMobileAccount`.
- Register policies/gates/listeners in `AppServiceProvider`.
- If admins should see live updates, add the model to `RealtimeChangeTracker::MODEL_RESOURCES` and
  the resource → query-key mapping in `frontend/src/services/liveUpdates.js`.

## Migrations

- Additive by default; nullable or defaulted columns; no destructive change during normal deploys.
- Write the data impact, deploy order and rollback in the PR/commit and in [[Migrations Timeline]].
- PostgreSQL-only SQL must degrade gracefully on SQLite (see the `getDriverName() === 'pgsql'`
  pattern in the announcements and client_preferences migrations).

## Checks

```bash
docker compose exec backend composer test
docker compose exec backend php artisan test --filter=<Class>
docker compose exec backend ./vendor/bin/pint --dirty
```

Related: [[Backend Architecture]] · [[Coding Conventions]] · [[Backend Test Suite]]
