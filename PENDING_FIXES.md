# Pending Fixes — SkillServe Web (Admin Frontend + Laravel Backend)

Last audited: 2026-09-21. Each item names where the problem is, why it matters,
and a suggested fix. Ordered by priority. The mobile app has its own list in
`skill-serve-mobile-application/PENDING_FIXES.md`; items that span both are
marked **(also mobile)**.

---

## High — affects correctness or data in production

### 1. A booking can never be marked as paid (also mobile)
- **Where:** `backend/app/Modules/ClientMarketplace/Actions/CreateClientBookingAction.php` sets
  `payment_status = 'unpaid'`; nothing anywhere ever writes `paid`, `refunded` or
  `partially_refunded`.
- **Why it matters:** every booking stays "Unpaid" forever. The mobile Payments screen, the
  provider Earnings screen ("not yet marked paid"), and the admin booking/analytics payment
  badges can never show a settled job.
- **Fix:** add a way to record settlement — an admin "Mark as paid" action on a booking
  (permission-gated, audited via `LogBookingActivity`), and/or a provider "Cash received"
  confirmation on a completed job. Refunds need the same once a policy exists.

### 2. Admins cannot open provider verification documents
- **Where:** `frontend/src/modules/providers/pages/ProviderProfilePage.jsx` (the "View" link uses
  `doc.file_url`). No API resource returns `file_url`, so the link has no target.
- **Why it matters:** verifying a provider means looking at the ID they uploaded; right now the
  admin can see the file name but cannot open it.
- **Fix:** the backend already serves it behind auth at
  `GET /api/providers/{provider}/verification-documents/{document}/download`. Fetch it as a blob
  with the admin's token and open it — the same pattern as `useOpenDisputeEvidence` in
  `frontend/src/modules/disputes/hooks/useDisputes.js`.

### 3. Uploaded files do not survive a production deploy
- **Where:** `backend/config/filesystems.php` — the `public`, `verification` and
  `dispute_evidence` disks are all local; the Render free web service has an ephemeral filesystem.
- **Why it matters:** every redeploy deletes profile photos, portfolio images, provider
  verification documents and dispute evidence, while the database still points at them.
- **Fix:** point all file disks at S3-compatible storage through env (only
  `CLIENT_PROFILE_PHOTO_DISK` is configurable today), keeping `verification` and
  `dispute_evidence` private buckets. Alternatively attach a Render persistent disk.

---

## Medium — consistency, maintainability, product gaps

### 4. Report reasons are defined in three places
- **Where:** `frontend/src/modules/reports/pages/ReportsPage.jsx` (`REASONS`),
  `backend/app/Modules/ClientCommunication/Requests/StoreClientReportRequest.php` (`REASONS`),
  `backend/database/seeders/ReportSeeder.php` (`REASONS`).
- **Why it matters:** a reason added in one place silently won't appear as a filter in another.
- **Fix:** expose the reason list from the API (or a shared config) and read it in the admin UI.

### 5. Pre-existing code-style violations
- **Where:** `backend/app/Modules/DataManagement/Services/DataManagementService.php`
  (`unary_operator_spaces`), `backend/app/Shared/Services/BrevoApiTransport.php`
  (`fully_qualified_strict_types`), `backend/app/Modules/ClientAuthentication/Requests/VerifyClientOtpRequest.php`
  (unused import).
- **Fix:** run `./vendor/bin/pint` on those three files in their own commit.

### 6. Booking lifecycle gaps (also mobile)
- A provider can decline a pending request but has no way to cancel after accepting.
- There is no rescheduling; the only route is cancel and rebook.
- **Fix:** product decision first, then `PATCH /api/client/v1/provider/bookings/{booking}/cancel`
  and a reschedule endpoint that re-runs the availability and overlap checks.

### 7. Admin frontend ships one large bundle
- **Where:** `npm run build` warns that a chunk exceeds 500 kB.
- **Fix:** lazy-load route pages (`React.lazy`) so each admin module is its own chunk.

### 8. `render.yaml` is not the live deploy config
- **Where:** its own header explains Render never reads it, because backend and frontend deploy
  from separate repositories.
- **Fix:** move the env documentation into `DEPLOYMENT.md` (or into each deployed repo) so it
  cannot drift from what actually runs.

---

## Low

### 9. Mobile sessions end after 14 idle days (also mobile)
- **Where:** `backend/config/client-auth.php` — `CLIENT_REFRESH_TOKEN_EXPIRATION` defaults to
  20160 minutes. Each app open rotates the refresh token, so an active user stays signed in;
  someone who does not open the app for 14 days must sign in again.
- **Fix:** raise the env value if a longer idle window is wanted.

### 10. Messaging makes two requests per incoming message (also mobile)
- While a conversation is open, each pushed message re-reads the thread (to mark it read) and the
  inbox. Correct, but chatty. A dedicated "mark thread read" endpoint would halve it.

---

## Resolved on 2026-09-21

- Support tickets opened to provider accounts (`/api/client/v1/support/tickets` now uses
  `EnsureMobileAccount`).
- Client reports can now target a published review or a received message, not only the other party
  on a booking. Reporting a review also sets the review's `is_reported` flag, so it appears under
  the admin Reviews "Reported" filter.
- One open report per reporter per subject is now enforced by the database (partial unique index
  `reports_one_open_per_subject`); the demo seeder skips pairs that would collide.
- Dispute evidence: either party can attach up to 5 photos to an open dispute
  (`POST /api/client/v1/bookings/{booking}/dispute/evidence`). Files are private; admins open them
  through `GET /api/disputes/{booking}/evidence/{evidence}` from the dispute details modal.
- Admin report reason filter now includes the reasons the mobile app files.
