---
type: table
tags: [database, table, providers]
domain: Providers
soft_deletes: false
---
# provider_availabilities

Weekly working hours, one window per weekday.

- **Model:** `backend/app/Modules/Providers/Models/ProviderAvailability.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_20_000005_create_provider_availabilities_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `provider_profile_id` | FK |  |
| `day_of_week` | tinyint | 0 = Sunday … 6 |
| `start_time, end_time` | time | Manila wall clock |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(provider_profile_id, day_of_week)

## Foreign keys

- provider_profile_id → provider_profiles cascade on delete

## Related

[[Provider Availability]] · [[Time and Timezone Rules]] · [[Database Index]]
