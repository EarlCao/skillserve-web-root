---
type: table
tags: [database, table, auth]
domain: Auth
soft_deletes: false
---
# pending_registrations

Sign-ups waiting for OTP verification (no user exists yet).

- **Model:** `backend/app/Modules/ClientAuthentication/Models/PendingRegistration.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_20_000001_create_pending_registrations_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `email` | string unique | one in-flight sign-up per address |
| `first_name, last_name` | string |  |
| `password` | string | hashed |
| `role_id` | uint (no FK) | 3 provider / 4 customer |
| `business_name, specialization` | string null | provider only |
| `experience_years` | smallint default 0 |  |
| `bio` | text null |  |
| `email_otp_hash` | string |  |
| `email_otp_expires_at` | timestamp |  |
| `email_otp_attempts` | tinyint default 0 |  |
| `expires_at` | timestamp, indexed | 24 h |
| `created_at, updated_at` |  |  |

## Notes

- No FK on role_id on purpose: transient rows must never block a roles change.

## Related

[[Registration and OTP Flow]] · [[Database Index]]
