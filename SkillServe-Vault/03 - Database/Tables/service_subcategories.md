---
type: table
tags: [database, table, catalog]
domain: Catalog
soft_deletes: true
---
# service_subcategories

One level of subcategories under a category.

- **Model:** `backend/app/Modules/ServiceCategories/Models/ServiceSubcategory.php`
- **Soft deletes:** yes
- **Migrations:** `2026_08_12_000002_create_service_subcategories_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `category_id` | FK service_categories |  |
| `name` | string |  |
| `description` | text null |  |
| `status` | string default 'enabled' |  |
| `created_at, updated_at` |  |  |
| `deleted_at` | soft delete | no deleted_by column |

## Indexes & constraints

- unique(category_id, name)

## Foreign keys

- category_id → service_categories **cascade on delete**

## Related

[[service_categories]] · [[services]] · [[Database Index]]
