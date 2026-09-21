# Pending Fixes — SkillServe Web (Admin Frontend + Laravel Backend)

Last audited: 2026-09-21. Each item names where the problem is, why it matters,
and a suggested fix. Ordered by priority. The mobile app has its own list in
`skill-serve-mobile-application/PENDING_FIXES.md`; items that span both are
marked **(also mobile)**.

---

## High — affects correctness or data in production

Nothing open.

---

## Medium — consistency, maintainability, product gaps

Nothing open.

---

## Low

Nothing open.

---

## Resolved on 2026-09-21

- **Bookings can be marked paid (also mobile).** Payment still happens off-platform; it is now
  recorded. A provider confirms payment on a completed job
  (`PATCH /api/client/v1/provider/bookings/{booking}/payment-received`), and an admin with the new
  `manage booking payments` permission can mark any confirmed/active/completed/disputed booking paid
  (`PATCH /api/bookings/{booking}/mark-paid`) or record a full or partial refund
  (`PATCH /api/bookings/{booking}/refund`) from the booking details modal. Rules live in
  `BookingPaymentService`; every change is audited and notifies the other party. New columns:
  `paid_at`, `payment_recorded_by`, `refunded_amount`, `refunded_at`, `refund_reason`.
- **Admins can open provider verification documents.** The "View" button fetches the file through
  the authorized download endpoint and opens it in a new tab.
- **Uploads survive deploys (Render only).** Uploads stay on Laravel's local disks under
  `storage/app`, which in production is a Render persistent disk (see `DEPLOYMENT.md` → "Uploaded
  files"). `start.sh` prepares a fresh disk and warns if it is not writable; `GET /api/health`
  reports `services.storage`. Needs the backend on a paid Render instance with the disk attached.
- **Favorites are stored on the server (mobile).** `GET /api/client/v1/favorites`,
  `PUT`/`DELETE /api/client/v1/favorites/{provider}` (idempotent) on a new `favorite_providers`
  table; favorites are included in the account data export.

- Report reasons live in one place: `Report::REASONS` (what can be filed) and
  `Report::LEGACY_REASONS` (older keys still on existing reports). The client report request and
  the demo seeder use them, and the admin reason filter reads `GET /api/reports/reasons`.
- Pint is clean across the backend (the three listed files plus `routes/api.php`).
- Booking lifecycle: a provider can cancel an accepted booking before it starts
  (`PATCH /api/client/v1/provider/bookings/{booking}/cancel`, reason required), and a customer can
  move a pending or confirmed booking (`PATCH /api/client/v1/bookings/{booking}/reschedule`). The
  new time re-runs the provider-hours and overlap checks, a confirmed booking returns to pending,
  the provider is notified, and `bookings.rescheduled_at` records it. The Flutter app has both.
- Admin frontend bundle: route pages are lazy-loaded (`src/routes/lazyPages.jsx`) and React and
  the realtime client are split into their own chunks; no chunk exceeds 500 kB any more.
- `render.yaml` is removed; `DEPLOYMENT.md` now documents the dashboard configuration of the
  backend Docker service and the frontend static site that actually run.

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
- Mobile sessions no longer end after 14 idle days: the refresh-token window
  (`CLIENT_REFRESH_TOKEN_EXPIRATION`, counted from last use) defaults to one year and is now in
  `backend/.env.example`. A password change, suspension, deletion or reuse of a rotated token still
  ends a session.
- Messaging: `POST /api/client/v1/bookings/{booking}/messages/read` marks a thread read and returns
  the remaining unread total, so an open conversation no longer re-reads the thread and the inbox
  for every incoming message.
