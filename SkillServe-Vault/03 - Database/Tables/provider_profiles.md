---
type: table
tags: [database, table, providers]
domain: Providers
soft_deletes: false
---
# provider_profiles

Professional profile of a provider account; the id used by services, bookings and reviews.

- **Model:** `backend/app/Modules/Providers/Models/ProviderProfile.php`
- **Soft deletes:** no
- **Migrations:** `2026_08_20_000001_create_provider_profiles_table`, `2026_09_05_000010_add_featured_to_provider_profiles`, `2026_09_20_000006_add_accepting_bookings_to_provider_profiles`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `user_id` | FK users unique | one profile per user |
| `business_name, specialization` | string null |  |
| `bio` | text null |  |
| `experience_years` | int default 0 |  |
| `hourly_rate` | decimal(10,2) null |  |
| `location` | string null |  |
| `latitude, longitude` | decimal(10,7) null |  |
| `website` | string null |  |
| `social_links, portfolio, skills, certifications, languages` | json null | `portfolio` JSON predates `provider_portfolio_items` |
| `average_rating` | decimal(3,2) default 0, indexed |  |
| `total_reviews, total_bookings, completed_bookings` | int default 0 | aggregates |
| `verification_status` | string default 'unverified', indexed | unverified / pending / verified / rejected / additional_info_required |
| `verified_at, verified_by` |  |  |
| `rejection_reason, suspension_reason` | string(500) null |  |
| `suspended_at, suspended_by` |  | provider suspension |
| `is_featured` | bool default false, indexed |  |
| `is_accepting_bookings` | bool default true |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(user_id)
- index(verification_status)
- index(average_rating)
- index(is_featured)

## Foreign keys

- user_id → users **cascade on delete**
- verified_by, suspended_by → users null on delete

## Related

[[users]] · [[services]] · [[bookings]] · [[verification_requests]] · [[provider_availabilities]] · [[provider_portfolio_items]] · [[Provider Verification Lifecycle]] · [[Database Index]]
