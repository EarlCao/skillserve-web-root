---
type: table
tags: [database, table, providers]
domain: Providers
soft_deletes: false
---
# verification_documents

Files attached to a verification request (private `verification` disk).

- **Model:** `backend/app/Modules/Providers/Models/VerificationDocument.php`
- **Soft deletes:** no
- **Migrations:** `2026_08_20_000003_create_verification_documents_table`, `2026_09_08_000010_move_verification_documents_to_private_storage (data move)`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `verification_request_id` | FK |  |
| `document_type` | string, indexed | government_id / certificate / other |
| `file_name, file_path, file_mime_type` | string |  |
| `file_size` | bigint |  |
| `description` | text null |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(verification_request_id)
- index(document_type)

## Foreign keys

- verification_request_id → verification_requests cascade on delete

## Related

[[verification_requests]] · [[File Storage Architecture]] · [[Database Index]]
