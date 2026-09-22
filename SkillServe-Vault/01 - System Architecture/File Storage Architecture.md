---
type: architecture
tags: [architecture, storage, uploads]
sources: [backend/config/filesystems.php, backend/config/client-auth.php, DEPLOYMENT.md, backend/deploy/render/start.sh]
---
# File Storage Architecture

All uploads use Laravel **local disks under `storage/app`**. In production that folder is a
**Render persistent disk** mounted at `/var/www/html/storage/app` — never an external bucket
([[ADR-008 Uploads on Render Persistent Disk]]).

## Disks (`config/filesystems.php`)

| Disk | Root | Public? | Holds | Written by |
|---|---|---|---|---|
| `public` | `storage/app/public`, URL `APP_URL/storage` | yes (via `storage:link`) | profile photos (`profile-photos/`), portfolio images (`portfolio/`) — JPG/PNG/WebP ≤5 MB | `ClientProfileService`, `ProviderAccountService` |
| `verification` | `storage/app/private` | no (`serve: false`) | provider ID / certificate / other documents (JPG/PNG/PDF ≤10 MB, 1–5 per submission) | `ProviderVerificationService` |
| `dispute_evidence` | `storage/app/private/dispute-evidence` | no | dispute photos — JPG/PNG/WebP ≤5 MB, ≤5 per dispute, optional caption ≤500 chars | `BookingDisputeService` |
| `local` | `storage/app/private` | `serve: true` (signed temporary URLs only) | default disk (`FILESYSTEM_DISK=local`) | — |
| `s3` | — | — | configured by the framework default; **not used** | — |

The profile-photo disk is configurable: `CLIENT_PROFILE_PHOTO_DISK` (default `public`).

## Private file access

| File | Endpoint | Authorization |
|---|---|---|
| Verification document | `GET /api/providers/{provider}/verification-documents/{document}/download` | `ProviderPolicy::view` → `view providers` |
| Dispute evidence | `GET /api/disputes/{booking}/evidence/{evidence}` | `BookingPolicy::viewDisputes` → `view bookings` |

The admin web fetches these as blobs and opens them in a new tab. Migration
`2026_09_08_000010_move_verification_documents_to_private_storage` moved older documents from the
public disk to the private one.

> [!warning] Needs Verification — `local` and `verification` share a root
> Both disks point at `storage/app/private`, and `local` has `serve: true` (the framework's
> `/storage/{path}` route pair appears in `route:list`). Laravel only serves `local` files through
> signed temporary URLs, so this is not public by default, but no code was found that creates
> such URLs. Confirm that nothing can sign a URL for a verification document.

## Production start-up (`deploy/render/start.sh`)

- Creates `storage/app/public` and `storage/app/private/dispute-evidence` on a fresh disk.
- Writes a probe file; logs a warning if `storage/app` is not writable.
- Runs `php artisan storage:link --force` so `public/storage` exists in the new container.
- `GET /api/health` reports `services.storage` = `down` if `storage/app` is not writable.

Only `storage/app` is persistent; logs, caches and compiled views are rebuilt on each start.
The disk needs a paid Render instance and pins the service to one instance.

## Related

[[Render Persistent Disk]] · [[File Upload Security]] · [[Provider Verification Lifecycle]]
