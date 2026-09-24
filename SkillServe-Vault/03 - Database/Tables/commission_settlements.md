---
type: table
tags: [database, table, commissions, payments]
domain: Commissions
soft_deletes: false
---
# commission_settlements

Proof that SkillServe received its share of a booking. One row per booking, written when an
administrator records the remittance. The money itself moves off-platform, exactly as booking
payments do — see [[ADR-007 Payments Recorded Not Processed]].

- **Model:** `backend/app/Modules/Commissions/Models/CommissionSettlement.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_24_000004_add_commission_settlement`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | |
| `booking_id` | FK, **unique** | one booking settles once |
| `provider_profile_id` | FK, indexed | denormalised so settlement history stays queryable per provider |
| `amount` | decimal(10,2) | always taken from `bookings.platform_fee`, never from the request |
| `method` | string | gcash / bank_transfer / cash / offset / other |
| `reference` | string null | e.g. a GCash reference number |
| `notes` | text null | |
| `settled_by` | FK users nullOnDelete | kept even if the administrator leaves |
| `settled_at` | timestamp, indexed | |
| `created_at, updated_at` | | |

## Indexes & constraints

- unique(booking_id) — with the row lock in `CommissionLedger::settle`, this is what makes a double
  settlement impossible
- index(provider_profile_id), index(settled_at)

## Foreign keys

- booking_id → bookings cascade on delete
- provider_profile_id → provider_profiles cascade on delete
- settled_by → users null on delete

## Related

[[Commission Tiers and Settlement]] · [[commission_tiers]] · [[bookings]] · [[Payments and Refunds]] · [[Database Index]]
