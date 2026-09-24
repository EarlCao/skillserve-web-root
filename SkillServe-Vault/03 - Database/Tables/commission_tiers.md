---
type: table
tags: [database, table, commissions]
domain: Commissions
soft_deletes: true
---
# commission_tiers

The bands an administrator configures to decide what percentage of a booking SkillServe takes.
Replaces the single flat `marketplace.commission_rate` setting, which remains only as a fallback.

- **Model:** `backend/app/Modules/Commissions/Models/CommissionTier.php`
- **Soft deletes:** yes — a retired band stays readable from the bookings charged under it
- **Migrations:** `2026_09_24_000001_create_commission_tiers_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | |
| `name` | string(120) | e.g. "Standard" |
| `min_amount` | decimal(10,2) | **inclusive** lower bound, in pesos |
| `max_amount` | decimal(10,2) null | **inclusive** upper bound; NULL = open-ended top band |
| `percentage` | decimal(5,2) | 0–100, e.g. 12.50 |
| `is_active` | boolean default true | a disabled band charges nobody |
| `created_by, updated_by` | FK users nullOnDelete | |
| `created_at, updated_at, deleted_at` | | |

Bounds are inclusive at **both** ends so a configuration written the way the business states it —
`0–199.99`, `200–499.99`, `500–999.99`, `1000+` — has no gaps for two-decimal peso amounts.

## Indexes & constraints

- index(is_active, min_amount) — the shape of the resolution query
- **`commission_tiers_no_active_overlap`** (PostgreSQL only) —
  `EXCLUDE USING gist (numrange(min_amount, max_amount, '[]') WITH &&) WHERE (is_active AND deleted_at IS NULL)`.
  Two active bands may never claim the same peso amount, or the rate charged would depend on row
  order. `CommissionTierService` refuses overlaps on every driver; this constraint is what closes the
  race between two administrators saving at once. SQLite has no exclusion constraints, hence the
  driver guard in the migration.

## Related

[[Commission Tiers and Settlement]] · [[commission_settlements]] · [[bookings]] · [[Database Index]]
