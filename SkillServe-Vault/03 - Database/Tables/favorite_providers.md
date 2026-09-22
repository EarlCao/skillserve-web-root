---
type: table
tags: [database, table, mobile]
domain: Mobile
soft_deletes: false
---
# favorite_providers

Customer's saved providers.

- **Model:** `— (pivot, `User::favoriteProviders()`)`
- **Soft deletes:** no
- **Migrations:** `2026_09_21_000004_create_favorite_providers_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `user_id` | FK users |  |
| `provider_profile_id` | FK provider_profiles |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(user_id, provider_profile_id)
- index(provider_profile_id)

## Foreign keys

- both → cascade on delete

## Related

[[Client Favorites]] · [[Database Index]]
