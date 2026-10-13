---
type: table
tags: [database, table, providers]
domain: Providers
soft_deletes: false
---
# provider_portfolio_items

A provider's piece of work: title, description and its photos in [[provider_portfolio_images]]
(up to 10, `ProviderPortfolioItem::MAX_IMAGES`). `image_path` is the cover — always the first
photo — kept for app versions that show a single image.

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
| `image_path` | string | cover (first photo), `public` disk |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(provider_profile_id, created_at)

## Foreign keys

- provider_profile_id → provider_profiles cascade on delete

## Related

[[provider_portfolio_images]] · [[Provider Portfolio and Badges]] · [[Database Index]]
