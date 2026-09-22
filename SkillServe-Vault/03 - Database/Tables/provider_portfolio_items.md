---
type: table
tags: [database, table, providers]
domain: Providers
soft_deletes: false
---
# provider_portfolio_items

Provider portfolio gallery images.

- **Model:** `backend/app/Modules/Providers/Models/ProviderPortfolioItem.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_20_000004_create_provider_portfolio_items_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `provider_profile_id` | FK |  |
| `title` | string |  |
| `description` | text null |  |
| `image_path` | string | `public` disk |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(provider_profile_id, created_at)

## Foreign keys

- provider_profile_id → provider_profiles cascade on delete

## Related

[[Provider Portfolio and Badges]] · [[Database Index]]
