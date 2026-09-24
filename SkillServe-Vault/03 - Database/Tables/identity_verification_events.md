---
type: table
tags: [database, table, identity, audit]
domain: IdentityVerification
soft_deletes: false
---
# identity_verification_events

Append-only history of every submission and decision on an identity verification. Nothing in the
application updates or deletes a row here: it is the record of a decision the platform made about a
person, and it survives the account itself.

- **Model:** `backend/app/Modules/IdentityVerification/Models/IdentityVerificationEvent.php`
  (`UPDATED_AT = null` — only `created_at` is meaningful for an append-only log)
- **Soft deletes:** no
- **Migrations:** `2026_09_24_000005_create_identity_verification_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | |
| `identity_verification_id` | FK | |
| `action` | string | submitted / approved / rejected / released |
| `actor_id` | FK users nullOnDelete | null for a system action such as release |
| `reason` | text null | the rejection reason, or the approval note |
| `created_at` | timestamp null | |

## Indexes & constraints

- index(identity_verification_id, id) — the history is always read in order for one record

## Note on duplication with the activity log

Decisions are *also* written to the Spatie activity log (`identity_verifications`), which is what the
Security and Audit module reads. This table is the domain-owned history shown on the submission
itself and is kept deliberately: the activity log is a cross-cutting, prunable stream, while this is
part of the verification record.

## Related

[[identity_verifications]] · [[Identity Verification Lifecycle]] · [[activity_log]] · [[Database Index]]
