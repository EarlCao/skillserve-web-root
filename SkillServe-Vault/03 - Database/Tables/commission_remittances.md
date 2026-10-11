---
type: table
tags: [database, table, commissions, payments]
domain: Commissions
soft_deletes: false
sources: [backend/database/migrations/2026_10_11_000001_create_commission_remittances_table.php, backend/app/Modules/Commissions/Models/CommissionRemittance.php, backend/app/Modules/Commissions/Services/CommissionRemittanceService.php]
---
# commission_remittances

A provider's claim that they sent SkillServe its commission by GCash. The provider pays
SkillServe's GCash outside the app and submits the GCash reference number; an administrator finds
that reference in SkillServe's GCash history and confirms it, which settles every booking the claim
covers. See [[Commission Tiers and Settlement#Paying it by GCash]].

- **Model:** `backend/app/Modules/Commissions/Models/CommissionRemittance.php`
- **Soft deletes:** no
- **Migrations:** `2026_10_11_000001_create_commission_remittances_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | |
| `provider_profile_id` | FK, indexed | who paid |
| `amount_due` | decimal(10,2) | what the covered bookings owed at submission |
| `amount_sent` | decimal(10,2) | what the provider says they sent; must be ≥ `amount_due` |
| `reference` | string(40) | GCash reference number, stored without spaces or dashes, upper-cased |
| `proof_path` | string null | receipt screenshot on the private `commission_remittances` disk; cleared when `commissions:purge-receipts` deletes it after the retention period |
| `proof_mime_type` | string(100) null | |
| `status` | string(20) default `pending` | `pending` / `confirmed` / `rejected` |
| `reviewed_by` | FK users nullOnDelete | the administrator who decided |
| `reviewed_at` | timestamp null | |
| `review_notes` | text null | the rejection reason, or the reviewer's note on a confirmation |
| `created_at, updated_at` | | `created_at` is the submission time |

## commission_remittance_bookings

The outstanding bookings the payment was for, fixed at submission so a commission that becomes
outstanding while the claim waits is never settled by money that was not sent for it.

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | |
| `commission_remittance_id` | FK cascade | |
| `booking_id` | FK cascade, indexed | |
| `amount` | decimal(10,2) | the booking's `platform_fee` at submission |
| `created_at, updated_at` | | |

unique(commission_remittance_id, booking_id).

## Indexes & constraints

- index(provider_profile_id), index(status, created_at) — the review queue
- **`commission_remittances_one_pending_per_provider`** — partial unique on `provider_profile_id`
  `WHERE status = 'pending'`: a provider has at most one claim waiting
- **`commission_remittances_reference_confirmed`** — partial unique on `reference`
  `WHERE status = 'confirmed'`: a GCash receipt pays once. Pending claims may share a reference, so
  someone typing another provider's receipt first cannot lock the payer out; the reviewer is shown
  the clash (`other_claims_count`)
- index(reference) — finding the other claims on a reference

Both back the service's own checks, closing the races between two submissions, or two
confirmations, landing together.
PostgreSQL and SQLite (tests) both support partial indexes.

## Foreign keys

- provider_profile_id → provider_profiles cascade on delete
- reviewed_by → users null on delete
- [[commission_settlements]]`.commission_remittance_id` → this table null on delete

## Related

[[Commission Tiers and Settlement]] · [[commission_settlements]] · [[bookings]] ·
[[Provider Commissions (Mobile)]] · [[Commission Management]] · [[Database Index]]
