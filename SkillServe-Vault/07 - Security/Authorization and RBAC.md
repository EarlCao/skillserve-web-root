---
type: guide
tags: [security, rbac, authorization]
sources: [backend/app/Providers/AppServiceProvider.php, backend/app/Modules/*/Policies, backend/app/Modules/Administrators/Support/SystemRole.php, frontend/src/utils/permissions.js, frontend/src/modules/authentication/routes/guards.jsx]
---
# Authorization and RBAC

Built on **spatie/laravel-permission** (guard `web`) plus Laravel policies and gates.

## Layers

```mermaid
flowchart TB
  R[Request with Sanctum token] --> A{auth:sanctum}
  A -->|admin route| G{Gate::before:<br/>super-admin?}
  G -->|yes| OK[allowed]
  G -->|no| P[Policy method or named gate<br/>hasPermissionTo(granular) OR hasPermissionTo('manage …')]
  P -->|true| OK
  P -->|false| D[403 'This action is unauthorized.']
  A -->|client route| M[EnsureClient / EnsureProvider / EnsureMobileAccount<br/>role_id + token ability client:auth + active + verified]
  M --> O[Ownership / participant check in client policy or service]
```

1. **Super-admin bypass** — `Gate::before` returns true for `super-admin`.
2. **Policies** (registered with `Gate::policy`) for models: User (Administrators), Role, Permission,
   ServiceCategory, Booking, Service, Review, Report, SupportTicket, Announcement, ProviderProfile.
3. **Named gates** (`Gate::define`) for non-model abilities: `view|edit|delete|suspend|activate|ban users`,
   `manage users`, provider gates, `view dashboard`, `view|export analytics`, recognition gates,
   audit gates.
4. **Inline checks** — some controllers call `abort_unless($user->can('…'), 403)` (Settings, Data
   Management, Provider Recognition, Audit, Notifications targeting/scheduling).
5. Most policies accept either the granular permission **or** the module's `manage …` permission
   (e.g. `BookingPolicy::allows` = `manage bookings` OR the specific one).

The generated [[Endpoints Index]] shows the exact ability each admin endpoint checks.

## Mobile authorization

Mobile accounts have **no Spatie roles or permissions**. Access is decided by:
- `role_id` (3 provider / 4 customer) and `isMobileProviderAccount()` (needs a provider profile),
- token ability `client:auth` (background token has only `client:notifications`),
- account `status = active` (else 403 with `meta.account`) and verified email,
- ownership/participant checks: `ClientBookingPolicy`, `ProviderBookingPolicy`, `ClientReviewPolicy`,
  `BookingDisputePolicy`, `BookingMessagePolicy`, `ClientReportPolicy`, and service-level
  `where('client_id', …)` / `where('provider_id', …)` scoping with `firstOrFail()` (404 on others' data).

## Guard rails for staff roles

- Roles 1–4 fixed (`SystemRole::isFixed`) — cannot be renamed/deleted.
- Provider/customer roles cannot be given to administrators (`SystemRole::isAccountType`).
- Only a super-admin may assign `super-admin` (`AdministratorPolicy::assignSuperAdmin`, checked on
  create and update).
- `SystemRole::PROTECTED_PERMISSIONS = ['manage administrators']`.
- `users.role_id` ↔ `model_has_roles` kept in sync (`User::booted`, `SyncUserRoleId` listener).
- Only accounts with at least one staff role may join `admin.data` or sign into the admin web.

## Frontend mirror

`hasCapability(user, permission, managePermission)` and `RequirePermission` hide menus and block
routes client-side. This is UX only — the API enforces everything.

> [!info] Admin API tokens are not scoped by ability
> Admin routes (except `/auth/me|logout|change-password`) require only `auth:sanctum` + permission
> checks, not an `admin:*` token ability. A mobile token reaching an admin route is refused because
> mobile users hold no permissions (not because of the token ability).

Related: [[Permission Catalog]] · [[User Types and Roles]] · [[Admin Management]]
