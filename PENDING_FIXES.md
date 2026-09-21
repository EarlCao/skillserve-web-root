# Pending Fixes — SkillServe (Backend, Admin Web, Mobile, Deployment)

Last full audit: 2026-09-21, against `SkillServe_Admin_Web_Functionalities.pdf`,
`SkillServe_User_Mobile_Functionalities_Flutter.pdf`, the code in `backend/`, `frontend/` and the
Flutter repo, and the Render deployment. This is the master list; the Flutter repo's
`PENDING_FIXES.md` repeats the items that touch the app.

Each item has an ID, the requirement it satisfies (Admin **A x.y** / Mobile **M x.y**), where the
problem is, the fix, and how to verify it. Work top to bottom: **Critical** items break a core flow
or leave a requirement unmet; the system is not defensible until they are done.

Tags: **[BE]** Laravel backend · **[AW]** React admin web · **[MB]** Flutter app · **[DEP]** deployment
· **[DOC]** defense material.

---

## Critical — a core flow is broken or a requirement is not met

### C1. Providers cannot submit verification documents [BE][MB]
- **Requirement:** M 9.3 Submit Verification, M 9.5 Respond to Information Request, M 9.4, A 4.3.
- **Where:** no API creates a `VerificationRequest` or `VerificationDocument` (only
  `database/seeders/ProviderSeeder.php` does). In the app,
  `lib/features/provider/views/verification_status_screen.dart` and step 2 of
  `provider_onboarding_screen.dart` only add a record to local state and show "Document submitted
  for review" — nothing is uploaded.
- **Why it matters:** `ProviderServiceService::verifiedProfile()` refuses service creation until the
  provider is verified, so in production **no new provider can ever list a service**. Only seeded
  demo providers work.
- **Fix:**
  - [BE] `GET /api/client/v1/provider/verification` — current request status (`pending`,
    `approved`, `rejected`, `info_requested`), the admin's rejection reason / requested info, and
    the submitted documents (no storage paths).
  - [BE] `POST /api/client/v1/provider/verification` (multipart) — `documents[]` with
    `document_type` (`government_id`, `certificate`, `other`), JPG/PNG/PDF up to 10 MB each, stored
    on the private `verification` disk; creates or reopens the request as `pending`. Refuse while a
    request is already pending review. Resubmitting after `rejected`/`info_requested` is the M 9.5
    response. Log it and notify admins (A 11.1).
  - [BE] Feature tests: ownership, file validation, state rules, admin download of the new file.
  - [MB] Replace both screens with the real flow (camera/gallery via `image_picker`, PDF via
    `file_picker`), upload progress, and the status/reason from the API; pull-to-refresh.
- **Verify:** register a new provider on the phone → upload ID → admin opens it in Provider
  Profile → approve → provider can create a service.

### C2. Booking times shift by 8 hours [BE][MB]
- **Requirement:** M 5.1–5.4, A 7.2 (correct schedules).
- **Where:** `backend/config/app.php` `'timezone' => 'UTC'`; the app sends
  `scheduledDate.toIso8601String()` of a local `DateTime`, which has **no offset**
  (`lib/features/booking/services/booking_service.dart`). The server reads 09:00 as 09:00 UTC and
  returns `09:00+00:00`; the app converts that to 17:00 on a phone set to Philippine time. Provider
  hours are also compared in UTC.
- **Fix:** set `'timezone' => env('APP_TIMEZONE', 'Asia/Manila')` (add to `.env.example` and
  Render), send times from the app with their offset (e.g. a helper that formats local time as
  `2026-10-05T09:00:00+08:00`, or `toUtc()`), and add a backend test that a `+08:00` start is stored
  and returned unchanged and passes the provider-hours check. Check the admin tables show the same
  times.
- **Verify:** book 9:00 AM on the phone → booking details, provider app and admin all show 9:00 AM.

### C3. System Settings are saved but not enforced [BE][MB][AW]
- **Requirement:** A 17.2 Marketplace, A 17.3 Booking (incl. cancellation policies), A 17.4
  Notification, A 17.6 System settings; M 5.6 "cancel according to the configured rules".
- **Where:** `config/system-settings.php` defines them; only `system.session_timeout_minutes` and
  `notifications.announcement_notifications_enabled` are read anywhere. The platform fee is
  hard-coded (`CreateClientBookingAction`: `$servicePrice * 0.10`).
- **Fix (one authoritative read through `SettingsService`, with tests for each):**
  - `marketplace.provider_registration_enabled` → `register-provider` / Google provider sign-up
    return 403 with a clear message when off.
  - `marketplace.service_approval_required` → when off, provider-created services publish as
    approved.
  - `marketplace.featured_services_enabled` → when off, the `featured` filter/sections return
    nothing and the admin "Feature" action is disabled.
  - `marketplace.commission_rate` → used for `platform_fee` instead of 10%.
  - `booking.booking_enabled` → booking creation refused (422) when off; the app shows why.
  - `booking.cancellation_window_hours` → a client cannot cancel a confirmed booking inside the
    window (pending is always cancellable); expose the rule in the booking resource so the app's
    cancel dialog explains it.
  - `booking.client_/provider_cancellation_fee_percent` → record the fee on the booking when a
    late cancellation happens (off-platform like payments), or remove these settings if the
    capstone scope has no fees — do not leave dead switches.
  - `notifications.email_notifications_enabled` / `push_notifications_enabled` → gate mail
    notifications and realtime/background delivery respectively.
  - `system.maintenance_mode` → middleware returning 503 on `/api/client/v1/*` (admins unaffected);
    the app shows a maintenance screen.
  - `system.default_page_size` → default `per_page` for list endpoints.
  - `general.platform_name` / `support_email` → used in mail and exposed to the app (see H2).
- **Verify:** toggle each in Admin → Settings and observe the effect in the app/API.

### C4. Account status and restrictions are not shown to users [BE][MB]
- **Requirement:** M 1.6 Account Status Display, M 2.4 View Account Status, M 9.6 Provider Account
  Restrictions, M 15.4 Account Status and Restriction Information, M 16.4.
- **Where:** a suspended/banned user gets only "Your account is not active." at login
  (`ClientAuthenticationService::login`); when a session is refused later, `api_client.dart` just
  ends it. The app has no account-status UI. Moderation **warnings** are recorded on the report only
  (`TakeModerationAction`: "warnings are recorded on the report only").
- **Fix:**
  - [BE] On a refused login/refresh, return `errors.account = {status, reason, until}` (suspended /
    banned / deleted), using the data the Users module already stores.
  - [BE] Include `account_status` (and provider `verification_status`, suspension state) in
    `GET /auth/me`.
  - [BE] Deliver a warning as a notification (`AccountWarningNotification`) and record it in the
    user's moderation history.
  - [MB] An "Account restricted" screen shown instead of the generic error, with the reason, the
    end date and a "Contact support" action; an account-status card on the profile/settings screen.
- **Verify:** suspend a user in Admin → the app shows the restriction screen with the reason;
  issue a warning → the user gets a notification.

---

## High — needed for a complete, deployable system

### H1. Admin decisions do not notify the people affected [BE][MB]
- **Requirement:** M 8.1–8.3, M 9.4, M 9.6, M 11.5 View Dispute Updates, M 6.4/7.5 follow-up.
- **Where:** `AppServiceProvider` only logs these events: `ProviderVerificationApproved/Rejected`,
  `ProviderAdditionalInfoRequested`, `ProviderVerificationRemoved`, `ProviderSuspended/Activated`,
  `UserSuspended/Activated`, `ReportResolved/Rejected`, `BookingDisputeManaged`. Only bans/unbans
  (mail) and service moderation notify anyone. Resolving a dispute also sets the booking to
  `completed`, which sends the misleading "Job completed — you can now leave a review".
- **Fix:** one listener per group extending `BaseNotification` with the right category:
  verification decisions (with the reason / requested info) → provider; suspension/activation →
  user; report resolved/rejected → reporter (no details about the other party); dispute
  investigate/resolve/reject/close → both parties with the resolution; suppress the generic
  "Job completed" message when completion comes from a dispute resolution. Tests with
  `Notification::fake()`.
- **Verify:** each admin action produces one notification on the right phone.

### H2. Platform policies are hard-coded in the app [BE][MB]
- **Requirement:** M 14.4 View Platform Policies, A 17.5 Manage Platform Policies.
- **Where:** `lib/features/settings/views/terms_screen.dart` and `privacy_screen.dart` are static
  text; there is no Community Guidelines screen; no public endpoint exposes
  `policies.*` settings.
- **Fix:** [BE] public `GET /api/client/v1/platform` returning `platform_name`, `support_email`,
  `terms_of_service`, `privacy_policy`, `community_guidelines` (cached, invalidated on settings
  save). [MB] one policy screen that renders the admin text (fallback to the bundled copy when
  empty/offline) for Terms, Privacy and a new Community Guidelines entry; link them from
  registration ("By signing up you agree…"). [DEP] write the real policy texts in Admin → Settings.
- **Verify:** edit the privacy policy in Admin → reopen it in the app.

### H3. Backend dependencies with known vulnerabilities [BE]
- **Where:** `composer audit`: `league/commonmark` (4 high advisories, fixed in ≥ 2.10.0) and
  `maatwebsite/excel` (CVE-2026-84374, fixed in ≥ 3.1.70); `doctrine/annotations` is abandoned.
- **Fix:** `composer update league/commonmark maatwebsite/excel --with-dependencies`, run the full
  suite and an analytics export; find what still requires `doctrine/annotations`
  (`composer why doctrine/annotations`) and drop or replace it if possible.
- **Verify:** `composer audit` reports no advisories. (`npm audit` for the admin web is clean.)

### H4. Mobile app is not release-ready [MB][DEP]
- **Where:** `android/app/build.gradle.kts` — `applicationId = "com.example.skilllink_mobile"`,
  release builds signed with the **debug** key; `AndroidManifest.xml` label `skilllink_mobile`;
  default launcher icon; `flutter_01.log` is committed.
- **Fix:** app label "SkillServe"; a real `applicationId` (e.g. `com.skillserve.mobile`) — this
  needs a **new Google OAuth Android client** with the release SHA-1 (see
  `SETUP_CREDENTIALS.md`) or Google sign-in breaks; a release keystore with `key.properties`
  (gitignored) and a `signingConfigs.release`; launcher icon and splash
  (`flutter_launcher_icons`, `flutter_native_splash`); a monochrome notification icon
  (`@drawable/ic_stat_notification`) for closed-app notifications; bump `version`; delete
  `flutter_01.log` and ignore `*.log`. Build with
  `flutter build apk --release --dart-define-from-file=env/production.json` (and pass
  `REVERB_APP_KEY` if production's key is not `skillserve`).
- **Verify:** install the release APK on a clean phone: name/icon correct, Google sign-in works,
  realtime connects, notifications show the icon.

### H5. Production setup checklist [DEP]
Do these once, in order, and record the results for the defense:
1. Backend on a **paid Render instance with the persistent disk** at `/var/www/html/storage/app`
   (`DEPLOYMENT.md` → "Uploaded files"); confirm `GET /api/health` shows `storage: up`. A paid
   instance also stops the free-tier sleep that delays the first request and pauses the queue,
   scheduler and closed-app notification checks.
2. Environment: `APP_KEY`, `APP_URL`, `FRONTEND_URL` (CORS), `APP_TIMEZONE=Asia/Manila` (C2),
   Neon `DB_*`, `REVERB_APP_ID/KEY/SECRET` (the app's `REVERB_APP_KEY` must match), mail (Brevo) for
   OTP and password reset, `GOOGLE_CLIENT_ID`, `SEED_MODE=admin-only` with strong
   `ADMIN_PASSWORD`/`SYSTEM_ADMIN_PASSWORD`, `SWAGGER_UI_ENABLED` off unless needed for the panel.
3. Frontend static site env (`VITE_API_BASE_URL`, `VITE_REVERB_*`) and the `/* → /index.html`
   rewrite.
4. Production data an admin must enter: service categories and subcategories, recognition badges,
   policy texts (H2), settings (C3), at least one support-staff role.
5. Smoke test end to end on the deployed stack (see D2).

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
