---
type: table
tags: [database, table, providers]
domain: Providers
soft_deletes: false
---
# verification_requests

A provider's verification submission and the admin decision.

- **Model:** `backend/app/Modules/Providers/Models/VerificationRequest.php`
- **Soft deletes:** no
- **Migrations:** `2026_08_20_000002_create_verification_requests_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `provider_profile_id` | FK provider_profiles |  |
| `status` | string default 'pending' | pending / approved / rejected / additional_info_required |
| `notes` | text null | provider's note |
| `admin_notes, rejection_reason, additional_info_request` | text null |  |
| `submitted_at, reviewed_at` | timestamp null |  |
| `reviewed_by` | FK users null |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(status)
- index(provider_profile_id, status)

## Foreign keys

- provider_profile_id → provider_profiles cascade on delete

## Related

[[verification_documents]] · [[provider_profiles]] · [[Provider Verification Lifecycle]] · [[Database Index]]
