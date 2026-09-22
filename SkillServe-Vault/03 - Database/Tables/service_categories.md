---
type: table
tags: [database, table, catalog]
domain: Catalog
soft_deletes: true
---
# service_categories

Top-level service categories.

- **Model:** `backend/app/Modules/ServiceCategories/Models/ServiceCategory.php`
- **Soft deletes:** yes
- **Migrations:** `2026_08_12_000001_create_service_categories_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `name` | string unique |  |
| `description` | text null |  |
| `status` | string default 'enabled' | enabled / disabled |
| `created_by` | FK users null |  |
| `created_at, updated_at` |  |  |
| `deleted_at, deleted_by` | soft delete |  |

## Indexes & constraints

- unique(name)

## Foreign keys

- created_by, deleted_by → users null on delete

## Notes

- Delete is blocked while the category has subcategories (README) or services (Data Management dependents).

## Related

[[service_subcategories]] · [[services]] · [[Service Category Management]] · [[Database Index]]
