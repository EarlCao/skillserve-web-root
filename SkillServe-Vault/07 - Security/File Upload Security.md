---
type: guide
tags: [security, uploads, storage]
sources: [backend/app/Modules/ClientMarketplace/Requests/SubmitProviderVerificationRequest.php, StoreDisputeEvidenceRequest.php, StorePortfolioItemRequest.php, backend/app/Modules/ClientAuthentication/Requests/UpdateClientProfilePhotoRequest.php, backend/config/filesystems.php]
---
# File Upload Security

| Upload | Endpoint | Validation | Disk / visibility | Who can read |
|---|---|---|---|---|
| Profile photo | `POST /client/v1/auth/me/photo` | `image`, jpg/jpeg/png/webp, ≤5 MB | `public` (`profile-photos/`) | anyone with the URL |
| Portfolio image | `POST /client/v1/provider/portfolio` | `image`, jpg/jpeg/png/webp, ≤5 MB; title ≤255, description ≤2000 | `public` (`portfolio/`) | anyone |
| Verification documents | `POST /client/v1/provider/verification` | 1–5 files, jpg/jpeg/png/pdf, ≤10 MB each; type ∈ government_id/certificate/other | `verification` (private) | admins with `view providers`, via streaming endpoint |
| National ID images | `POST /client/v1/identity-verification` | 1–3 files, jpg/jpeg/png/pdf, ≤10 MB each; type ∈ id_front/id_back/selfie | `identity` (private) | admins with `view identity verifications`, via streaming endpoint; **every open is audited**, and the document must belong to the submission in the path |
| Dispute evidence | `POST /client/v1/bookings/{id}/dispute/evidence` | `image`, jpg/jpeg/png/webp, ≤5 MB; ≤5 per dispute; caption ≤500 | `dispute_evidence` (private) | admins with `view bookings`, via streaming endpoint |

- Files are stored with generated names (`store` / `storeAs`), outside the web root for private
  disks; old files are deleted on replacement (profile photo) or failed submission cleanup
  (verification).
- nginx `client_max_body_size 20m` bounds request size in production (five 10 MB PDFs in one
  verification request would exceed it — **Needs Verification** whether the app sends documents
  in one request; the app's upload panel sends a multipart `POST` with all selected documents).
- Government IDs live on a private disk; the historical public copies were moved by migration
  `2026_09_08_000010`.

Related: [[File Storage Architecture]] · [[Render Persistent Disk]]
