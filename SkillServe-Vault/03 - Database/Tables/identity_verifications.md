---
type: table
tags: [database, table, identity, security]
domain: IdentityVerification
soft_deletes: false
---
# identity_verifications

One row per account, holding its Philippine National ID verification state. Created on first read,
so every account that has looked at the feature has a record.

- **Model:** `backend/app/Modules/IdentityVerification/Models/IdentityVerification.php`
- **Soft deletes:** no — a record is *released*, never deleted (see below)
- **Migrations:** `2026_09_24_000005_create_identity_verification_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | |
| `user_id` | FK null, **unique** | **nullOnDelete by design** — the record outlives the account as its audit trail |
| `status` | string, indexed | unverified / pending / verified / rejected |
| `id_number_hash` | string(64) null | HMAC-SHA256 of the 16 normalised digits under a server pepper; the only column compared |
| `id_number_encrypted` | text null | Laravel `encrypted` cast; cleared on release |
| `id_number_last4` | string(4) null | the only part ever displayed |
| `full_name` | string null | as printed on the card, for the reviewer to match |
| `birthdate` | date null | as printed on the card |
| `submitted_at, reviewed_at` | timestamp null | |
| `reviewed_by` | FK users nullOnDelete | |
| `rejection_reason` | text null | shown to the holder so they can resubmit |
| `released_at` | timestamp null | set on **permanent** account deletion; frees the ID for reuse |
| `documents_purge_after` | timestamp null, indexed | retention clock, started by a decision |
| `created_at, updated_at` | | |

`id_number_hash` and `id_number_encrypted` are `#[Hidden]` on the model, so even a stray `toArray()`
cannot leak them.

## Indexes & constraints

- unique(user_id)
- index(status), index(documents_purge_after)
- **`identity_verifications_active_id_number`** — partial unique on `(id_number_hash)`
  `WHERE id_number_hash IS NOT NULL AND released_at IS NULL`. This is the database-level enforcement
  of *one National ID = one active account*; see [[ADR-018 Blind Index for National ID Uniqueness]].

## Foreign keys

- user_id → users **null on delete** (deliberate: the record survives the account)
- reviewed_by → users null on delete

## Related

[[Identity Verification Lifecycle]] · [[identity_documents]] · [[identity_verification_events]] ·
[[ADR-018 Blind Index for National ID Uniqueness]] · [[Database Index]]
