# Pending Fixes — SkillServe (Backend, Admin Web, Mobile, Deployment)

Last full audit: 2026-09-21, against `SkillServe_Admin_Web_Functionalities.pdf`,
`SkillServe_User_Mobile_Functionalities_Flutter.pdf`, the code in `backend/`, `frontend/` and the
Flutter repo, and the Render deployment. This is the master list; the Flutter repo's
`PENDING_FIXES.md` repeats the items that touch the app.

Each item has an ID, the requirement it satisfies (Admin **A x.y** / Mobile **M x.y**), where the
problem is, the fix, and how to verify it. All Critical, High, Medium and Low items are resolved (below); what remains are the owner
actions before go-live and the defense material.

Tags: **[BE]** Laravel backend · **[AW]** React admin web · **[MB]** Flutter app · **[DEP]** deployment
· **[DOC]** defense material.

---

## Critical

Nothing open.

---

## High

Nothing open.

### Owner actions before go-live (cannot be done from the code)
1. **Render:** a paid backend instance with the persistent disk, and the environment from
   `DEPLOYMENT.md`, including `SEED_MODE=starter` on the first deploy, then `admin-only`.
   After that, follow `DEPLOYMENT.md` → "Go-live checklist".
2. **Android signing:** create the upload keystore and `android/key.properties` (Flutter repo
   `README.md` → "Building a release"). Back up the keystore and its passwords.
3. **Google sign-in:** register an Android OAuth client for `com.skillserve.mobile` with the debug
   and release SHA-1 fingerprints (Flutter repo `SETUP_CREDENTIALS.md`, section 2).
4. **Admin content:** in Settings, write the Terms of Service, Privacy Policy and Community
   Guidelines, and review the booking rules. Then add categories, badges and a support-staff role.
5. **Evidence:** run the smoke test (D2) on the deployed stack and fill in the Result columns of
   both `TEST_PLAN.md` files.

---

## Medium

Nothing open.

---

## Low

Nothing open.

---

## Defense readiness

- **D1. Requirements traceability matrix.** Done: `TEST_PLAN.md` (admin web) and the Flutter repo's
  `TEST_PLAN.md` (mobile) map every requirement to its page/screen, endpoint, automated tests and
  UAT steps. Fill in the Result column on the deployed system; every row must pass before the
  defense.
- **D2. Demo script and data.** A short end-to-end scenario on the deployed system: customer books →
  provider accepts → reschedule → job done → provider records payment → review → report → admin
  moderates → dispute → admin resolves → notifications on both phones. Use `scripts/fresh-demo.sh`
  only on a **local/demo** database (it wipes data).
- **D3. Architecture and security talking points.** Monolith (Laravel API + React admin) plus Flutter
  client; Sanctum tokens with rotating refresh tokens; role/permission model (Spatie); realtime via
  Reverb (no Firebase — and why); closed-app notifications via WorkManager polling with a read-only
  token; uploads on a Render persistent disk; audit logging of admin actions.

---

## Resolved on 2026-09-21

**Critical and High from the full audit:**
- **C1 — Provider verification upload (M 9.3, M 9.5, A 4.3).**
  - `GET` and `POST /api/client/v1/provider/verification`: 1–5 documents (government ID,
    certificate, other; JPG/PNG/PDF up to 10 MB) plus an optional note.
  - Files go to the private `verification` disk. A request in `additional_info_required` is
    reopened, and any other allowed status starts a new one. The profile moves to pending, the
    submission is logged, and admins see it in the existing review screen.
  - The app has an upload panel (camera, gallery, PDF, with progress) on Verification Status and
    in onboarding. It shows the status, the reviewer's reason or request, and the documents sent.
  - Also fixed `LogProviderActivity`, which called a nonexistent method, so every admin decision
    on a provider returned a 500.
  - Tests: `ProviderVerificationTest`, `verification_test`.
- **C2 — Booking times.**
  - Storage stays UTC. `BUSINESS_TIMEZONE=Asia/Manila` (`BusinessTime`) is the wall clock for
    provider hours and for times written in notifications.
  - Booking and reschedule requests are normalised to UTC. The app sends UTC ISO-8601 times.
  - Tests: `ClientMarketplaceTest` (instant and hours), `BookingRescheduleTest`, `booking_test`.
- **C3 — Settings enforced (A 17.2–17.6).**
  - Commission sets `platform_fee`.
  - `booking_enabled` pauses new bookings.
  - The cancellation window records a late-cancellation fee on the booking
    (`bookings.cancellation_fee`, migration `2026_09_22_000001`, nullable and additive). The fee
    is shown to the client and provider before they confirm, on the booking, and in the admin
    modal.
  - `service_approval_required` and `featured_services_enabled` are enforced, along with the
    email and push switches.
  - `default_page_size` applies to every list (`PageSize`), and provider sign-ups can be closed.
  - Maintenance mode returns a 503 with `meta.maintenance` to the mobile API. The app shows a
    maintenance screen and retries. The admin web and `GET /api/client/v1/platform` stay open.
  - Tests: `SettingsEnforcementTest`, `platform_test`.
- **C4 — Account status (M 1.6, M 2.4, M 9.6, M 15.4, M 16.4).**
  - Every refusal of a suspended or banned account (login, Google, OTP, refresh, middleware) is a
    403 with `meta.account` {status, reason, since, until}. `/auth/me` carries `account` and the
    provider's suspension details.
  - The app ends the session and explains why on the login screen. Settings shows an account
    status card.
  - Moderation warnings now reach the user as a `UserWarned` event, with a notification and a
    log entry.
  - Tests: `AccountStatusTest`, `account_status_test`.
- **H1 — Decision notifications.** In-app, realtime and closed-app notifications now go out for:
  - verification approved, rejected or needing more info, and provider suspended or reinstated;
  - account warned, suspended or reinstated;
  - report outcomes, to the reporter;
  - dispute investigate, resolve, reject and close, to both parties (without a duplicate "job
    completed").

  Tapping a notification opens the matching screen. Tests: `AdminDecisionNotificationTest`,
  `notifications_reviews_test`.
- **H2 — Policies from the admin (M 14.4).**
  - Public `GET /api/client/v1/platform` returns the platform name, support email, sign-up and
    booking rules, and the three policy texts.
  - The app renders them on Terms, Privacy and the new Community Guidelines screen, falling back
    to the bundled text when offline. Registration links all three.
- **H3 — Dependency audit.** `league/commonmark` 2.10.1 and `maatwebsite/excel` 3.1.70;
  `composer audit` is clean.
- **H4 — Mobile release.**
  - App ID `com.skillserve.mobile`, label "SkillServe", launcher icon (`branding/app_icon.png`),
    branded splash, monochrome notification icon.
  - Release signing via a gitignored `key.properties`, falling back to the debug key with a
    warning. `pubspec.lock` is now tracked, and `flutter_01.log` was removed.
  - `flutter build apk --release` succeeds.
- **H5 — Production setup.**
  - `SEED_MODE=starter` gives roles and permissions plus the default service categories, with no
    demo users (`StarterSeedTest`).
  - `.env.example` and `DEPLOYMENT.md` cover the timezones and the full environment.
  - A "Go-live checklist" was added to `DEPLOYMENT.md`.

**Medium and Low from the full audit:**
- **M1 — Admin forgot password (A 1.4).** "Forgot password?" on the admin login;
  `POST /api/auth/forgot-password` (same answer for every address) and `POST /api/auth/reset-password`
  on a separate `admins` password broker; the emailed link opens `/reset-password` on the admin web
  (`FRONTEND_URL`, now read as `config('app.frontend_url')`); a reset signs the admin out everywhere
  and is audited. Tests: `AdminPasswordResetTest`.
- **M2 — Account deactivation decision.** Documented in both `TEST_PLAN.md` files ("Design decisions to
  defend") and the Flutter README: accounts are active or deleted; deletion is a restorable soft
  delete.
- **M3 — Rate limits on public mobile auth endpoints.** New `client-auth` limiter (20/min per IP via
  `CLIENT_AUTH_RATE_LIMIT`, 10/min per email) on register, register-provider, cancel-registration,
  verify-otp, resend-otp, forgot-password and reset-password. The admin web and the app show a clear
  "Too many attempts…" message on 429. Tests: `ClientAuthRateLimitTest`, `api_error_test.dart`.
- **M4 — Review moderation notifications.** The reviewer is notified when a review is hidden, removed
  or restored, and the provider when a hidden review is restored (`NotifyReviewModeration`). Test in
  `ReviewRemovalTest`.
- **M5 — Admin web hardening.** Production builds ship a strict Content-Security-Policy (scripts from
  the site itself only; `frontend/vite.config.js`), Zod runs without `eval`, and `DEPLOYMENT.md` lists
  the Render headers (`X-Frame-Options`, `frame-ancestors`, `nosniff`, `Referrer-Policy`) plus a
  short session timeout. Verified in headless Chrome: login, forgot and reset pages render with no
  CSP violations.
- **M6 — Test evidence.** `TEST_PLAN.md` (admin web) and the Flutter repo's `TEST_PLAN.md`: every
  requirement → page/screen → endpoint → tests → UAT steps. Gaps in automated coverage were closed:
  `DataManagementTest` (export, archive, restore), `BookingListTest` (search/filter), `ReviewListTest`
  (search/filter/reported), `SettingsTest`, `CorsTest`, `HealthCheckTest`.
- **M7 (found during this work) — CORS trusted every `*.vercel.app` and `*.onrender.com` site.**
  `config/cors.php` now allows only the admin web's own origins plus `FRONTEND_URL` / `FRONTEND_URLS`
  (local dev keeps its localhost pattern). Test: `CorsTest`.
- **L1** Empty `frontend/src/modules/systemSettings/` and `backend/app/Modules/SystemSettings/`
  folders removed.
- **L2** `APP_TIMEZONE`, `CLIENT_BACKGROUND_TOKEN_EXPIRATION` and `CLIENT_AUTH_RATE_LIMIT` added to
  `backend/.env.example`; `config/app.php` reads `APP_TIMEZONE` (default still UTC — switching to
  Asia/Manila is C2).
- **L3** `DEPLOYMENT.md` "Step 3 — Release Workflow" now describes the real main-only flow, checks,
  migrations and rollback.
- **L4** Flutter `README.md` rewritten for the current app; root `README.md` gained a module map,
  related documents and a complete project layout.
- **L5** `general.timezone` in System Settings is read-only and shows the server timezone
  (`meta.read_only` in `GET /api/settings`; sending it returns 422). Test: `SettingsTest`.
- **L6** `workmanager` is already the latest release; the Kotlin Gradle Plugin warning comes from
  upstream and does not affect the build. Nothing further to do until a new release ships.

**Earlier on 2026-09-21:**

- **Mobile closed-app notifications (no Firebase).** A read-only background token
  (`POST /api/client/v1/notifications/background-token`, ability `client:notifications`) lets the
  app's WorkManager task call `GET /api/client/v1/notifications/background` and nothing else; it is
  refused by every other route, the chat policy and the user's broadcast channel, and ends on
  logout or password change.
- **Chat presence and typing.** Presence channel `booking-chat.{booking}` in `routes/channels.php`,
  joinable only by the booking's two participants (reuses `BookingMessagePolicy`); typing uses
  client events, which Reverb accepts from members by default.
- `BookingMessagePolicy` now requires a full client session token for providers too, not only for
  customers.

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
