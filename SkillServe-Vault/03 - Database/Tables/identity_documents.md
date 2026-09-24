---
type: table
tags: [database, table, identity, security]
domain: IdentityVerification
soft_deletes: false
---
# identity_documents

National ID images backing a submission, on the private `identity` disk. Never served directly;
administrators open them through an authorised, audited download.

- **Model:** `backend/app/Modules/IdentityVerification/Models/IdentityDocument.php`
- **Soft deletes:** no — rows are deleted outright when images are purged or replaced
- **Migrations:** `2026_09_24_000005_create_identity_verification_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | |
| `identity_verification_id` | FK, indexed | |
| `document_type` | string | id_front / id_back / selfie |
| `file_name` | string | the holder's original filename, for display only |
| `file_path` | string | random UUID name on the private disk; `#[Hidden]` from serialisation |
| `file_mime_type` | string | |
| `file_size` | bigint | |
| `created_at, updated_at` | | |

Filenames on disk are random UUIDs: the uploaded name is attacker-controlled and must never decide
where a file lands.

## Lifecycle

Rows are removed when the images are replaced by a resubmission, when retention expires
(`identity:purge-documents`), or when the ID is released on permanent account deletion. The
verification record and its history are kept in every case.

## Foreign keys

- identity_verification_id → identity_verifications cascade on delete

## Related

[[identity_verifications]] · [[Identity Verification Lifecycle]] · [[File Storage Architecture]] · [[Database Index]]
