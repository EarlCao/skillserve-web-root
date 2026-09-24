---
type: reference
tags: [database, migrations, change-management]
sources: [backend/database/migrations]
---
# Migrations Timeline

All **69** migrations in `backend/database/migrations`, in execution order. "Kind" was classified
during the audit by reading each `up()` method. Most are additive; the notable exceptions are
flagged.

> [!important] Deployment behaviour
> Production runs `php artisan migrate --force` on **every container start** (`deploy/render/start.sh`),
> through Neon's **direct** host. A migration that fails blocks the whole boot. Rollback of a
> deploy does **not** roll back migrations — keep them backward-compatible
> ([[Release Workflow]], [[NeonDB]]).

## Phases

| Period | What was added |
|---|---|
| framework + 2026-08-07 | users/cache/jobs, settings, Sanctum tokens, Spatie permission tables, activity log, media, admin/user-management columns, bans |
| 2026-08-12 → 08-22 | service categories/subcategories, granular permissions, provider profiles + verification, services, bookings |
| 2026-09-03 → 09-05 | reviews, messages, reports, dispute fields, announcements, notifications, dashboard/analytics/recognition/audit permissions, badges |
| 2026-09-08 | data archives, support tickets, client refresh tokens, idempotency keys, message read state, private verification storage |
| 2026-09-12 → 09-18 | email OTP, Google sub, PHP currency, users → roles link (drops `user_type`) |
| 2026-09-20 → 09-22 | pending registrations, profile photo, client preferences, portfolio items, availabilities, accepting-bookings flag, service address, one-open-report index, rescheduled_at, payment settlement, favorites, cancellation fee |

## Full list

| # | Date | Migration | Kind / impact |
|---|---|---|---|
| 1 | 0001-01-01 | `0001_01_01_000000_create_users_table` | schema: new table(s) |
| 2 | 0001-01-01 | `0001_01_01_000001_create_cache_table` | schema: new table(s) |
| 3 | 0001-01-01 | `0001_01_01_000002_create_jobs_table` | schema: new table(s) |
| 4 | 2022-12-14 | `2022_12_14_083707_create_settings_table` | schema: new table(s) |
| 5 | 2026-08-07 | `2026_08_07_053614_create_personal_access_tokens_table` | schema: new table(s) |
| 6 | 2026-08-07 | `2026_08_07_053615_create_permission_tables` | schema: new table(s) |
| 7 | 2026-08-07 | `2026_08_07_053623_create_activity_log_table` | schema: new table(s) |
| 8 | 2026-08-07 | `2026_08_07_053624_add_event_column_to_activity_log_table` | schema (additive) |
| 9 | 2026-08-07 | `2026_08_07_053625_add_batch_uuid_column_to_activity_log_table` | schema (additive) |
| 10 | 2026-08-07 | `2026_08_07_053626_create_media_table` | schema: new table(s) |
| 11 | 2026-08-07 | `2026_08_07_064500_add_administrator_fields_to_users_table` | schema (additive) |
| 12 | 2026-08-07 | `2026_08_07_064501_add_description_to_roles_table` | schema (additive) |
| 13 | 2026-08-07 | `2026_08_07_064502_add_user_management_fields_to_users_table` | schema (additive) |
| 14 | 2026-08-07 | `2026_08_07_073000_add_ban_duration_fields_to_users_table` | schema (additive) |
| 15 | 2026-08-12 | `2026_08_12_000001_create_service_categories_table` | schema: new table(s) |
| 16 | 2026-08-12 | `2026_08_12_000002_create_service_subcategories_table` | schema: new table(s) |
| 17 | 2026-08-19 | `2026_08_19_000001_add_granular_management_permissions` | data: upserts permissions |
| 18 | 2026-08-20 | `2026_08_20_000001_create_provider_profiles_table` | schema: new table(s) |
| 19 | 2026-08-20 | `2026_08_20_000002_create_verification_requests_table` | schema: new table(s) |
| 20 | 2026-08-20 | `2026_08_20_000003_create_verification_documents_table` | schema: new table(s) |
| 21 | 2026-08-21 | `2026_08_21_000001_create_services_table` | schema: new table(s) |
| 22 | 2026-08-22 | `2026_08_22_000001_create_bookings_table` | schema: new table(s) |
| 23 | 2026-09-03 | `2026_09_03_000001_create_reviews_table` | schema: new table(s) |
| 24 | 2026-09-03 | `2026_09_03_000002_add_review_management_permissions` | data: upserts permissions |
| 25 | 2026-09-04 | `2026_09_04_000001_create_messages_table` | schema: new table(s) |
| 26 | 2026-09-04 | `2026_09_04_000002_create_reports_table` | schema: new table(s) |
| 27 | 2026-09-04 | `2026_09_04_000003_add_reports_and_moderation_permissions` | data: upserts permissions |
| 28 | 2026-09-05 | `2026_09_05_000001_add_dispute_management_fields_to_bookings_table` | schema (additive) |
| 29 | 2026-09-05 | `2026_09_05_000002_add_disputed_at_index_to_bookings_table` | schema (additive) |
| 30 | 2026-09-05 | `2026_09_05_000003_sync_super_admin_permissions` | data: grants every permission to super-admin |
| 31 | 2026-09-05 | `2026_09_05_000004_create_announcements_table` | schema: new table(s) |
| 32 | 2026-09-05 | `2026_09_05_000005_create_notifications_table` | schema: new table(s) |
| 33 | 2026-09-05 | `2026_09_05_000006_add_notification_permissions` | data: permissions → super-admin |
| 34 | 2026-09-05 | `2026_09_05_000007_add_dashboard_permission` | data: `view dashboard` → super-admin, admin |
| 35 | 2026-09-05 | `2026_09_05_000008_add_analytics_permissions` | data: analytics permissions → super-admin |
| 36 | 2026-09-05 | `2026_09_05_000009_revoke_analytics_from_admin_role` | data: removes analytics permissions from admin |
| 37 | 2026-09-05 | `2026_09_05_000010_add_featured_to_provider_profiles` | schema (additive) |
| 38 | 2026-09-05 | `2026_09_05_000011_create_provider_badges_tables` | schema: new table(s) |
| 39 | 2026-09-05 | `2026_09_05_000012_add_provider_recognition_permissions` | data: permissions → super-admin, admin |
| 40 | 2026-09-05 | `2026_09_05_000013_grant_provider_recognition_to_admin` | data: recognition permissions → admin |
| 41 | 2026-09-05 | `2026_09_05_000014_add_audit_log_permissions` | data: permissions → super-admin, admin |
| 42 | 2026-09-05 | `2026_09_05_000015_add_audit_log_query_indexes` | schema (additive) |
| 43 | 2026-09-05 | `2026_09_05_000016_add_audit_action_index` | schema (additive) |
| 44 | 2026-09-08 | `2026_09_08_000001_create_data_archives_table` | schema: new table(s) |
| 45 | 2026-09-08 | `2026_09_08_000002_add_data_management_permissions` | data: permissions → super-admin, admin |
| 46 | 2026-09-08 | `2026_09_08_000003_create_support_tickets_tables` | schema: new table(s) |
| 47 | 2026-09-08 | `2026_09_08_000004_add_support_management_permissions` | data: permissions → super-admin |
| 48 | 2026-09-08 | `2026_09_08_000005_create_client_refresh_tokens_table` | schema: new table(s) |
| 49 | 2026-09-08 | `2026_09_08_000006_add_client_idempotency_to_bookings` | schema (additive) |
| 50 | 2026-09-08 | `2026_09_08_000007_add_client_marketplace_indexes` | schema (additive) |
| 51 | 2026-09-08 | `2026_09_08_000008_add_read_state_and_idempotency_to_messages` | schema (additive) |
| 52 | 2026-09-08 | `2026_09_08_000009_add_activity_subject_history_index` | schema (additive) |
| 53 | 2026-09-08 | `2026_09_08_000010_move_verification_documents_to_private_storage` | files: moves documents from `public` to private `verification` disk |
| 54 | 2026-09-12 | `2026_09_12_104918_add_email_otp_to_users_table` | schema (additive) |
| 55 | 2026-09-12 | `2026_09_12_110000_add_google_sub_to_users_table` | schema (additive) |
| 56 | 2026-09-17 | `2026_09_17_000001_use_philippine_peso_as_default_currency` | schema + data: currency default PHP; rewrites USD rows to PHP |
| 57 | 2026-09-18 | `2026_09_18_000001_link_users_to_roles` | schema + data: pins role ids 1–4, adds users.role_id (backfilled), drops users.user_type — **destructive column drop** |
| 58 | 2026-09-20 | `2026_09_20_000001_create_pending_registrations_table` | schema: new table(s) |
| 59 | 2026-09-20 | `2026_09_20_000002_add_profile_photo_to_users_table` | schema (additive) |
| 60 | 2026-09-20 | `2026_09_20_000003_create_client_preferences_table` | schema: new table(s) |
| 61 | 2026-09-20 | `2026_09_20_000004_create_provider_portfolio_items_table` | schema: new table(s) |
| 62 | 2026-09-20 | `2026_09_20_000005_create_provider_availabilities_table` | schema: new table(s) |
| 63 | 2026-09-20 | `2026_09_20_000006_add_accepting_bookings_to_provider_profiles` | schema (additive) |
| 64 | 2026-09-20 | `2026_09_20_000007_add_service_location_to_bookings` | schema (additive) |
| 65 | 2026-09-21 | `2026_09_21_000001_add_one_open_report_per_subject_index` | schema: PostgreSQL partial unique index (raw SQL) |
| 66 | 2026-09-21 | `2026_09_21_000002_add_rescheduled_at_to_bookings` | schema (additive) |
| 67 | 2026-09-21 | `2026_09_21_000003_add_payment_settlement_to_bookings` | schema (additive) |
| 68 | 2026-09-21 | `2026_09_21_000004_create_favorite_providers_table` | schema: new table(s) |
| 69 | 2026-09-22 | `2026_09_22_000001_add_cancellation_fee_to_bookings` | schema (additive) |

## Notes on risky migrations

- **`2026_09_18_000001_link_users_to_roles`** — pins role ids 1–4 (renumbering existing roles if
  needed and resetting the sequence), backfills `role_id` from staff roles and `user_type`, makes it
  NOT NULL, then **drops `user_type`**. Its `down()` recreates `user_type` (default `customer`,
  `provider` for role 3 — any other earlier value is not restored), drops `role_id`, and deletes the
  provider/customer roles if they carry no permissions. A rollback is therefore lossy.
- **`2026_09_17_000001_use_philippine_peso_as_default_currency`** — rewrites every `USD` value to
  `PHP` in `services` and `bookings` (no conversion of amounts).
- **`2026_09_08_000010_move_verification_documents_to_private_storage`** — moves files, not rows;
  its rollback copies them back to the public disk (the docblock warns to disable the private
  download endpoint if rolled back).
- **Permission data migrations** grant/revoke permissions to `super-admin`/`admin` directly; the
  seeder later re-syncs the `admin` role (see [[User Types and Roles]]).
- **`2026_09_21_000001_add_one_open_report_per_subject_index`** — raw PostgreSQL SQL with a
  `WHERE` clause, run without a driver guard on both PostgreSQL and the SQLite test database (SQLite
  also supports partial unique indexes).

## 2026-09-24 — commissions and identity verification

- **`2026_09_24_000001_create_commission_tiers_table`** — new table. On PostgreSQL it also adds an
  `EXCLUDE USING gist` constraint so two *active* bands cannot claim the same peso amount; the
  statement is guarded by a driver check because SQLite has no exclusion constraints, so that rule
  is application-only in the test database.
- **`2026_09_24_000002_add_commission_permissions`** — permission data migration.
- **`2026_09_24_000003_add_commission_snapshot_to_bookings`** — adds `commission_rate` and
  `commission_tier_id`, both nullable. `platform_fee` keeps its meaning, so no backfill: existing
  rows read correctly as "charged before tiers existed".
- **`2026_09_24_000004_add_commission_settlement`** — adds `commission_status` (NOT NULL with a
  default, a metadata-only change on PostgreSQL 11+) and `commission_settled_at`, plus the
  `commission_settlements` table. Every existing booking becomes `pending`, and because only
  bookings paid *after* the deploy move to `outstanding`, no provider is retroactively put in debt.
- **`2026_09_24_000005_create_identity_verification_tables`** — three new tables. Raw SQL adds the
  partial unique index `identity_verifications_active_id_number`, run **without** a driver guard
  because PostgreSQL and SQLite both support partial indexes (same approach as
  `2026_09_21_000001`). `user_id` is `nullOnDelete` on purpose so the record outlives the account.
- **`2026_09_24_000006_add_identity_verification_permissions`** — permission data migration.

All six are additive. Rolling back 000005 drops every verification decision, and the stored ID
images must be removed from the private disk separately.

## Related

[[Database Overview]] · [[Changelog]] · [[Database Index]]
