---
type: table
tags: [database, table, auth]
domain: Auth
soft_deletes: false
---
# pending_registrations

Sign-ups that are not accounts yet: waiting for the emailed code, then for the password (no user exists until both are in).

- **Model:** `backend/app/Modules/ClientAuthentication/Models/PendingRegistration.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_20_000001_create_pending_registrations_table`, `2026_10_01_000002_add_structured_addresses`, `2026_10_03_000001_add_password_step_to_pending_registrations`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `email` | string unique | one in-flight sign-up per address |
| `first_name, last_name` | string |  |
| `password` | string null, hashed | chosen after the code; set up front only by older app versions |
| `role_id` | uint (no FK) | 3 provider / 4 customer |
| `business_name, specialization` | string null | provider only |
| `experience_years` | smallint default 0 |  |
| `bio` | text null |  |
| `birthday` | date null | read from the National ID; copied to `users.birthday` |
| `address_*` | as on [[users]] | read from the National ID; copied to the account with its formatted text |
| `email_otp_hash` | string |  |
| `email_otp_expires_at` | timestamp |  |
| `email_otp_attempts` | tinyint default 0 |  |
| `email_verified_at` | timestamp null | set when the code is confirmed |
| `registration_token_hash` | string(64) null | SHA-256 of the token returned once at sign-up; required to set the password or cancel |
| `google_sub` | string null | the Google identity a Google sign-up started from; copied to `users.google_sub` |
| `expires_at` | timestamp, indexed | 24 h |
| `created_at, updated_at` |  |  |

## Notes

- No FK on role_id on purpose: transient rows must never block a roles change.

## Related

[[Registration and OTP Flow]] · [[Database Index]]
