---
type: table
tags: [database, table, media]
domain: Media
soft_deletes: false
---
# media

Created for spatie/laravel-medialibrary, which was never used and was removed on 2026-10-06. The table stays (empty, harmless); dropping it would be a separate schema change.

- **Model:** `—`
- **Soft deletes:** no
- **Migrations:** `2026_08_07_053626_create_media_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `model_type, model_id` | morphs |  |
| `uuid` | uuid unique null |  |
| `collection_name, name, file_name, mime_type, disk, conversions_disk` | strings |  |
| `size` | bigint |  |
| `manipulations, custom_properties, generated_conversions, responsive_images` | json |  |
| `order_column` | int null idx |  |
| `timestamps` |  |  |

## Notes

> [!warning] Needs Verification
> No model implements `HasMedia`; the table is probably unused.

## Related

[[Database Index]]
