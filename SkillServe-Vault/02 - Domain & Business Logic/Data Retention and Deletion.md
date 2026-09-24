---
type: domain
tags: [domain, data-management, retention]
sources: [backend/config/data-management.php, backend/app/Modules/DataManagement/Services/DataManagementService.php, backend/app/Console/Commands/PurgeExpiredDeletedRecords.php]
---
# Data Retention and Deletion

## Soft delete everywhere that matters

Soft-deleted tables: `users`, `service_categories`, `service_subcategories`, `services`,
`bookings`, `reviews`, `messages`, `reports`, `support_tickets`. Most carry `deleted_by`.

## Data Management rules (`config/data-management.php`)

| Setting | Value |
|---|---|
| `export_types` | users, providers, services, bookings, reviews, activity |
| `archive_types` | **services** only |
| `resource_types` / `permanent_delete_types` | users, services, bookings, reviews, reports, messages, service_categories, service_subcategories |
| `retention_days` | 30 |

- **Restore** a deleted record: `POST /api/data-management/deleted/{type}/{id}/restore`.
- **Permanent delete**: `DELETE /api/data-management/deleted/{type}/{id}` — refused while
  dependent rows exist (`DataManagementService::DEPENDENTS`), because FKs would cascade or block:

| Type | Blocked while referenced by |
|---|---|
| users | bookings.client_id, provider_profiles.user_id, reviews.reviewer_id, messages.sender_id, messages.receiver_id |
| services | bookings.service_id, reviews.service_id |
| bookings | reviews.booking_id |
| service_categories | services.category_id, service_subcategories.category_id |

- **Automatic purge:** `data-management:purge-expired` (daily) force-deletes records soft-deleted
  more than 30 days ago, skipping those with dependents.
- **Archive** (services): `POST /api/data-management/archives` stores `previous_state` in
  `data_archives` and hides the record; `POST …/archives/{id}/restore` restores it.
- **Export**: `GET /api/data-management/export?type=` streams CSV.

## Account deletion

- Admin: `DELETE /api/users/{id}` (soft, tokens revoked).
- Self-service: `DELETE /api/client/v1/auth/me` with password; refused while a booking is
  pending/confirmed/active/disputed. An admin can restore it within 30 days.
- **Permanent deletion releases the account's National ID** for reuse, and only then — a
  soft-deleted account can be restored for 30 days, so releasing earlier would allow two live
  accounts on one ID. The verification record itself survives with `user_id` nulled, as the audit
  trail for the decision; the encrypted number and the ID images are dropped. See
  [[Identity Verification Lifecycle]].
- **National ID images** are purged on their own timer by `identity:purge-documents` (daily), once
  System Settings → Identity → retention has passed. The decision and its history are kept.
- Account data export: `GET /api/client/v1/auth/me/data-export` (profile, preferences, provider
  profile, bookings, reviews, reports, support tickets, favorites).

Related: [[Data Management]] · [[ADR-016 Soft Delete with 30-Day Purge]] · [[data_archives]]
