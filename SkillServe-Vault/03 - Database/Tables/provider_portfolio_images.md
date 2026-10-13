---
type: table
tags: [database, table, providers]
domain: Providers
soft_deletes: false
sources: [backend/database/migrations/2026_10_13_000003_create_provider_portfolio_images_table.php, backend/app/Modules/Providers/Models/ProviderPortfolioImage.php]
---
# provider_portfolio_images

The photos of a [[provider_portfolio_items]] row, in order (cover first). Added 2026-10-13.

- **Model:** `backend/app/Modules/Providers/Models/ProviderPortfolioImage.php`
- **Soft deletes:** no
- **Migrations:** `2026_10_13_000003_create_provider_portfolio_images_table` (backfilled each existing
  item's photo as position 0)

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `provider_portfolio_item_id` | FK |  |
| `path` | string | `public` disk; never exposed — the API returns a URL |
| `position` | smallint, default 0 | order within the item; 0 = cover |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(provider_portfolio_item_id, position)

## Foreign keys

- provider_portfolio_item_id → provider_portfolio_items **cascade on delete** (a photo has no meaning
  without its item; `ProviderAccountService` deletes the files)

## Rules

- 1 to 10 photos per item; the 10 is re-checked under a row lock when photos are added.
- Removing the cover promotes the next photo and updates the item's `image_path`.
- The last photo cannot be removed (422) — delete the item instead.

## Related

[[provider_portfolio_items]] · [[Provider Portfolio and Badges]] · [[Database Index]]
