---
type: reference
tags: [security, rbac, permissions]
sources: [backend/database/seeders/RolePermissionSeeder.php, backend/app/Modules/*/Policies]
---
# Permission Catalog

All **66** permissions created by `RolePermissionSeeder` (guard `web`), plus the 7 granular service permissions created only by migration (see below). `super-admin` gets all;
`admin` gets the ✅ ones (seeder); anything else is granted per role in Admin Management.

| Module | Permission | admin |
|---|---|---|
| Admin Management | `manage administrators` *(protected)*, `view administrators`, `create administrators`, `edit administrators` | |
| Users | `manage users`, `view users`, `edit users`, `delete users`, `suspend users`, `activate users`, `ban users` | |
| Providers | `manage providers`, `view providers`, `edit providers`, `delete providers`, `suspend providers`, `activate providers`, `verify providers`, `reject providers` | |
| Services | `manage services` (seeder) · `view/create/edit/delete/approve/reject/feature services` (migration only) | |
| Service Categories | `manage service categories`, `view service categories`, `create service categories`, `edit service categories`, `delete service categories` | |
| Bookings | `manage bookings`, `view bookings`, `cancel bookings`, `manage booking disputes`, `manage booking payments` | |
| Commissions | `view commissions`, `manage commissions`, `settle commissions` | `manage` configures the tiers; `settle` records or waives what a provider owes. Deliberately separate — configuring rates and writing off revenue are different powers |
| Identity | `view identity verifications`, `verify identities`, `reject identities` | Reviewing means handling government ID documents, so these are granted through a custom role rather than carried by a general admin role. Approving does not imply rejecting |
| Reviews | `view reviews`, `manage reviews`, `edit reviews`, `delete reviews` | |
| Reports | `view reports` ✅, `manage reports`, `investigate reports`, `resolve reports`, `manage moderation` | partial |
| Notifications | `view notifications`, `send announcements`, `target notifications`, `schedule announcements` | |
| Dashboard | `view dashboard` ✅ | ✅ |
| Analytics | `view analytics`, `export analytics` | |
| Provider Recognition | `view provider recognition` ✅, `manage provider badges` ✅, `assign provider badges` ✅, `manage featured providers` ✅, `view top rated providers` ✅ | ✅ |
| Audit | `view audit logs` ✅, `view login activity` ✅, `monitor security events` ✅ | ✅ |
| Settings | `manage settings` | |
| Data Management | `manage data`, `export system data`, `archive records`, `restore archived records`, `restore deleted records`, `manage deleted records` | |
| Support | `view support`, `manage support`, `assign support tickets`, `respond to support tickets`, `resolve support tickets` | |

> [!info] Granular service permissions come from a migration, not the seeder
> `ServicePolicy` checks `view services`, `create services`, `edit services`, `delete services`,
> `approve services`, `reject services`, `feature services`. The seeder's list contains only
> `manage services`; the granular names are created by the data migration
> `2026_08_19_000001_add_granular_management_permissions`, which runs on every database before
> seeding. Because the seeder then calls `syncPermissions($permissions)` on `super-admin`, that role
> ends up without the granular service rows (harmless — `Gate::before` grants super-admin
> everything). Keep the seeder list and the migrations in step when adding permissions.

> [!warning] Needs Verification — `admin` role on existing databases
> Migrations granted additional permissions to `admin` (e.g. data management); the seeder later
> re-syncs `admin` to the short list above. The real state depends on run order — query
> `role_has_permissions` to confirm.

Policy → permission mapping per ability: see [[Authorization and RBAC]] and the generated
endpoint notes ([[Endpoints Index]]).
