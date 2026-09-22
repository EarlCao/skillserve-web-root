---
type: table
tags: [database, table, catalog]
domain: Catalog
soft_deletes: true
---
# services

Provider service listings.

- **Model:** `backend/app/Modules/Services/Models/Service.php`
- **Soft deletes:** yes
- **Migrations:** `2026_08_21_000001_create_services_table`, `2026_09_17_000001_use_philippine_peso_as_default_currency`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `provider_id` | FK provider_profiles |  |
| `category_id` | FK service_categories |  |
| `subcategory_id` | FK null |  |
| `title` | string |  |
| `description` | text null |  |
| `price` | decimal(10,2) null |  |
| `price_type` | string default 'fixed' | fixed / hourly / custom |
| `currency` | string(3) default 'PHP' | was USD |
| `duration` | string null | free text parsed for booking length |
| `location` | string null |  |
| `status` | string default 'draft' | draft / published / archived |
| `approval_status` | string default 'pending' | pending / approved / rejected |
| `rejection_reason` | text null |  |
| `is_featured, is_hidden` | bool default false |  |
| `total_bookings, completed_bookings, total_reviews` | int default 0 |  |
| `average_rating` | decimal(3,2) default 0 |  |
| `created_by, updated_by, approved_by` | FK users null |  |
| `approved_at` | timestamp null |  |
| `created_at, updated_at` |  |  |
| `deleted_at, deleted_by` | soft delete |  |

## Indexes & constraints

- index(status)
- index(approval_status)
- index(is_featured)
- index(is_hidden)
- index(category_id, status)
- index(provider_id, status)

## Foreign keys

- provider_id → provider_profiles **cascade**
- category_id → service_categories **cascade**
- subcategory_id → service_subcategories null on delete
- user FKs null on delete

## Related

[[provider_profiles]] · [[service_categories]] · [[bookings]] · [[Service Approval Lifecycle]] · [[Database Index]]
