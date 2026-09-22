---
type: table
tags: [database, table, reviews]
domain: Reviews
soft_deletes: true
---
# reviews

Customer reviews of completed bookings.

- **Model:** `backend/app/Modules/Reviews/Models/Review.php`
- **Soft deletes:** yes
- **Migrations:** `2026_09_03_000001_create_reviews_table`, `2026_09_08_000007_add_client_marketplace_indexes`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `booking_id` | FK bookings unique | one review per booking |
| `reviewer_id` | FK users |  |
| `provider_id` | FK provider_profiles |  |
| `service_id` | FK services |  |
| `rating` | tinyint | 1–5 (validated) |
| `comment` | text null |  |
| `status` | string(20) default 'active' | active / hidden / removed |
| `is_reported` | bool default false |  |
| `report_reason` | text null |  |
| `hidden_by, hidden_at, removed_by, removed_at` |  |  |
| `created_at, updated_at` |  |  |
| `deleted_at, deleted_by` | soft delete |  |

## Indexes & constraints

- unique(booking_id)
- index(status)
- index(rating)
- index(is_reported)
- index(provider_id, status)
- index(service_id, status)
- index(reviewer_id, created_at)

## Foreign keys

- booking_id, reviewer_id, provider_id, service_id → **restrict on delete**
- moderator FKs → users null on delete

## Related

[[Reviews and Ratings Rules]] · [[bookings]] · [[Database Index]]
