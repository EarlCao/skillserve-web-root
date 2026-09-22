---
type: table
tags: [database, table, accounts]
domain: Accounts
soft_deletes: true
---
# users

Every account: staff, customers and providers. `role_id` decides the kind.

- **Model:** `backend/app/Models/User.php`
- **Soft deletes:** yes
- **Migrations:** `0001_01_01_000000_create_users_table`, `2026_08_07_064500_add_administrator_fields_to_users_table`, `2026_08_07_064502_add_user_management_fields_to_users_table`, `2026_08_07_073000_add_ban_duration_fields_to_users_table`, `2026_09_12_104918_add_email_otp_to_users_table`, `2026_09_12_110000_add_google_sub_to_users_table`, `2026_09_18_000001_link_users_to_roles (adds role_id, drops user_type)`, `2026_09_20_000002_add_profile_photo_to_users_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `name` | string | display name |
| `first_name` | string null |  |
| `last_name` | string null |  |
| `email` | string unique |  |
| `phone` | string(30) null |  |
| `address` | text null |  |
| `profile_photo_path` | string null | `public` disk |
| `birthday` | date null |  |
| `email_verified_at` | timestamp null |  |
| `role_id` | bigint NOT NULL FK roles | 1 super-admin, 2 admin, 3 provider, 4 customer, ≥5 custom staff |
| `password` | string | hashed cast |
| `status` | string default 'active' | active / suspended / banned (admins: active / inactive) |
| `suspended_at, suspended_by, suspension_reason(500)` |  | suspension |
| `activated_at, activated_by` |  | reactivation |
| `banned_at, banned_by, ban_reason(500)` |  | ban |
| `banned_until` | timestamp null | null = permanent |
| `unban_reason` | string(500) null |  |
| `last_login_at` | timestamp null |  |
| `created_by` | FK users null | creating admin |
| `remember_token` | string null |  |
| `email_otp_hash, email_otp_expires_at, email_otp_attempts` |  | OTP state (tinyint attempts default 0) |
| `google_sub` | string null, indexed | Google account link |
| `created_at, updated_at` | timestamps |  |
| `deleted_at, deleted_by` | soft delete |  |

## Indexes & constraints

- unique(email)
- index(role_id)
- index(google_sub)

## Foreign keys

- role_id → roles.id **restrict on delete**
- created_by, suspended_by, activated_by, banned_by, deleted_by → users.id null on delete

## Notes

- `user_type` column existed until 2026-09-18; it is now a computed attribute on the model.
- Model hook defaults `role_id` to 4 (customer) and syncs Spatie `model_has_roles` for staff roles.

## Related

[[roles]] · [[provider_profiles]] · [[client_preferences]] · [[client_refresh_tokens]] · [[personal_access_tokens]] · [[User Types and Roles]] · [[Account Status Lifecycle]] · [[Database Index]]
