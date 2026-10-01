# Pending Fixes — SkillServe (Backend, Admin Web, Mobile, Deployment)

Last updated: **2026-09-30** (M8 threshold built; service-based provider ratings, dashboard commission card and general Excel report added).
Previous full audit: 2026-09-21.

Requirements now live in `SkillServe-Vault/` (Obsidian), which supersedes the two functionality
PDFs — those are kept for the original module numbering (**A x.y** / **M x.y**) only. This is the
master list; the Flutter repo's `PENDING_FIXES.md` repeats the items that touch the app.

Each item has an ID, the requirement it satisfies (Admin **A x.y** / Mobile **M x.y**), where the
problem is, the fix, and how to verify it. Every item that could be fixed in code is resolved
(below). What remains is **owner action only**: turn the
National ID requirement on when ready (**H8**), the go-live list, and the defense material.

Tags: **[BE]** Laravel backend · **[AW]** React admin web · **[MB]** Flutter app · **[DEP]** deployment
· **[DOC]** defense material.

---

## Features in progress

### F1 · ID-first sign-up and the Philippine address picker **[BE][MB]** — in progress
**Asked 2026-10-01:** sign-up starts by photographing the National ID front, then back; the app
reads both and fills the form; addresses use Region → Province → City → Barangay everywhere.
Required for every account; PhilSys card and ePhilID. See vault [[Philippine Addresses]].
- [x] **Phase 1** — PSGC list, `locations:import`, `/api/client/v1/locations/*` (backend).
- [ ] **Phase 2** — structured address columns + validation on users, pending registrations,
  bookings and services (backend; migration explained before it runs).
- [ ] **Phase 3** — ID capture front → back, on-device text + QR reading, pre-filled sign-up,
  ID submitted after the email code (mobile).
- [ ] **Phase 4** — the picker in Edit Profile, the booking form and Add/Edit Service (mobile).
- [ ] **Phase 5** — docs, APK, owner test with a real National ID.
**Server-side enforcement:** turn on System Settings → Identity (**H8**) at launch.

---

## Critical

### ~~C5 · Rotate the exposed PayMongo live secret key~~ — **RESOLVED 2026-09-30**
**Where:** PayMongo dashboard → Developers → API Keys. Nothing in the repositories can do this.
**Problem:** `sk_live_w7xdt7…` was pasted into a chat transcript, so it must be treated as public.
Anyone holding it can charge and refund real money and create webhooks on the account.
**Fix:** remove `PAYMONGO_SECRET_KEY` from Render first (nothing uses it), then switch *Viewing live
data* **on**, regenerate, confirm, enter the OTP. Do **not** put the new key back — see below.
**Verify:** the API Keys page shows a new "last regenerated" timestamp, and
`php artisan paymongo:status --probe-key` answers **401** for the old key.
**Status:** the live account was checked on 2026-09-25 and had **no webhooks**, so the key had not
been used to divert payment events. Rotation is still required.

**Code side, done 2026-09-26** — the blast radius is now closed even before rotation:
  - **A live key cannot be used by accident.** `PayMongoClient` refuses every request while an
    `sk_live_` key is configured unless `PAYMONGO_ALLOW_LIVE=true` is *also* set, logs it as
    `critical`, and never logs the key. One mistyped variable should not be all that stands between
    a deploy and real money. Test: `LiveKeyGuardTest`.
  - **`php artisan paymongo:status`** reports the environment's posture — key present, test or live,
    whether live is allowed, the webhook secret, and the gateway each payment method resolves to.
    "No key is set" is the healthy answer. `--probe` checks the configured key against PayMongo;
    `--probe-key` prompts for one (hidden, never stored), which is how the rotated-out key is
    confirmed dead.
  - **The key is nowhere in the repositories.** All four working trees and their full git history
    were searched for `sk_live_`: only truncated references in documentation. `backend/.env` is
    gitignored and its live key had already been removed by hand.
  - **The docs no longer invite it back.** `.env.example`, `DEPLOYMENT.md` (environment table,
    go-live step 6 and a "Rotating an exposed PayMongo key" runbook) and the vault's
    [[PayMongo Setup]] all said or implied that setting a key switches GCash on. That has been
    untrue since ADR-021 — both methods route to the manual gateway unconditionally — so they now
    say to leave every PayMongo variable unset.

**Rotated 2026-09-30:** the owner regenerated the **live secret key** in PayMongo → Developers →
API keys (the public key and the test keys were left alone). The new key is deliberately stored
nowhere in the project or Render, since nothing uses it. The optional `--probe-key` check was
skipped because the old key is no longer at hand; regeneration itself invalidates it.
`PAYMONGO_SECRET_KEY` and `PAYMONGO_WEBHOOK_SECRET` were **deleted from Render → Environment** the
same day. Closed. Once the backend is pushed, `php artisan paymongo:status` on Render should report
"No key is set".

### ~~C7 · Production holds the demo dataset, with guessable passwords~~ — **RESOLVED 2026-10-01**
**Verified 2026-10-01:** after the second wipe with backend `051089a` live, the public catalog reports 0
services, 0 providers and 0 categories, and the owner signs in as the seeded super-admin.

**History:**
**Reopened 2026-09-30:** after the seeding fix (`924cf14`) the next deploy seeded the **demo** dataset
again (18 services, 11 providers, 7 categories), because `SEED_MODE` was not `admin-only` on Render
and the default was `demo`. Backend `051089a` makes production refuse demo seeding outright.
**To do:** once `051089a` is live on Render, wipe the Neon schema again and redeploy; verify the
catalog reports 0 services, providers and categories, and `users` holds one row.

**First attempt:**
**Done:** `SEED_MODE=admin-only` set on Render, Neon schema wiped, backend redeployed. Verified from
outside: `/api/health` up, and the public catalog reports 0 services, 0 providers, 0 categories.
The first rebuild created **no** super-admin: `db:seed-if-empty` mistook the roles the migrations
insert for a seeded database. Fixed in backend `924cf14`; the following deploy seeds the super-admin
from `ADMIN_EMAIL`. **Left:** delete the Neon
`backup-before-reset` branch once the super-admin login and the new setup are confirmed.

<details><summary>Original entry</summary>

### C7 · Production holds the demo dataset, with guessable passwords **[DEP]** — decided: wipe, owner action
**Found 2026-09-30** (read-only check of the public catalog): the live marketplace lists the
`ProviderSeeder` / `ServiceSeeder` data (e.g. "Garcia Plumbing Solutions", "Calculus Tutoring",
20 services, 8 categories), so production was seeded with `SEED_MODE=demo` at some point.
**Problem:** demo accounts are active and email-verified with the password **`password`** —
providers are `firstname.lastname@example.com`, customers are on `example.com/.org/.net` — and the
provider names are public. Anyone can guess an address and sign in as that account on the live
system.
**Fix — decide first:**
  a. *Keep the demo catalogue, lock the accounts* (recommended for the defense): a one-off data
     migration gives every mobile account on an `example.*` address a random password and revokes
     its tokens. The catalogue stays for browsing; nobody can sign in as a seeded account.
  b. *Remove the demo data*: delete the seeded accounts and their services, bookings and reviews
     (a data migration), or wipe and reseed with `SEED_MODE=starter` — loses any real sign-ups.
**Decision (owner, 2026-09-30): wipe everything and start from the super-admin only.**
Cause: `DatabaseSeeder` defaults `SEED_MODE` to `demo` when the variable is unset, so a Render
environment without it seeds the demo dataset on a fresh database.
Procedure (no code change; `start.sh` rebuilds an empty database on boot):
  1. Render → Environment: `SEED_MODE=admin-only`, a real `ADMIN_EMAIL`, a strong `ADMIN_PASSWORD`.
  2. Push the backend, so the rebuilt schema is the current one.
  3. Neon → Branches → create a backup branch from `main` (the undo button).
  4. Neon → SQL Editor on `main` / `neondb`: `DROP SCHEMA public CASCADE; CREATE SCHEMA public;`
  5. Render → Manual Deploy → Restart: `migrate` recreates every table, `db:seed-if-empty` finds
     no roles and seeds roles, permissions and the super-admin only.
  6. Verify: `/api/health` up, `/api/client/v1/services` total 0, the super-admin can sign in.
Consequences: every account, booking, review, report and setting is deleted, every session ends,
and there are **no service categories** until an administrator creates them. Uploaded files on the
disk become orphans (harmless). Delete the Neon backup branch once the new setup is confirmed.

</details>
**Verify:** signing in as a seeded address with `password` fails.

### ~~C6 · Provider payouts do not exist~~ — **RESOLVED 2026-09-25**
**Decision:** the customer pays the provider **directly** (GCash to the provider's own number, or
cash), and the provider remits the commission to keep their account active. SkillServe is never in
the payment path and never holds customer money, so there is no payout obligation to build.
**Done:** both payment methods route to the manual gateway unconditionally; `provider_profiles`
gained `gcash_number` / `gcash_name`; the customer sees `payment_instructions` on an unpaid GCash
booking. See `ADR-021`.
**Trade accepted:** no escrow and no payment guarantee — a customer who pays and gets nothing is a
dispute, not something the platform can reverse.

<details><summary>Original entry</summary>

### C6 · Provider payouts do not exist **[BE]** — needs a decision, then building
**Where:** the whole payment flow. See `ADR-020` and Known Issues **KI-28**.
**Problem:** PayMongo settles into **SkillServe's** account, not the provider's. A ₱200 GCash
booking leaves SkillServe holding the provider's ₱180 with **nothing recording that it is owed**.
The commission half is handled (it settles automatically); the payout half is missing entirely.
**Fix — decide first:**
  a. *Manual payouts* — add a provider payout ledger (what is owed, what has been paid, by whom)
     and settle by bank/GCash transfer by hand. Smallest change; a person must do the transfers.
  b. *PayMongo Platforms* — onboard every provider as a linked sub-account so splits are automatic.
     Needs per-provider KYC, an onboarding flow and a commercial agreement with PayMongo.
**Verify:** a completed GCash booking shows the provider what they are owed, and an administrator
can mark it paid.
**Until then:** do not take real GCash bookings — money would arrive with no record of the debt.

</details>

---

## High

### ~~H6 · Flutter app is behind the API~~ — **RESOLVED 2026-09-26**
The app predated the September API work: six payment methods defaulting to `cash`, no National ID
screens, no eligibility check and no commission screen, so a blocked account saw a bare 403.
**Done:**
  - Payment methods trimmed to **On-hand** and **GCash**, the only two the API accepts. Codes on
    older bookings still read back with a label, because the API does not rewrite them.
  - National ID capture is reachable at `/identity-verification` — on the Profile tab for both
    roles, and where registration lands straight after the OTP (a provider carries on to business
    onboarding). Skipping is offered only while the platform does not require it of that account.
  - `EligibilityBanner` on the customer home and provider dashboard renders
    `GET /transaction-eligibility` as a prompt that opens the screen which fixes it, and draws
    nothing when the account is eligible.
  - `/commissions` shows a provider what they owe, per booking, and what the block stops them doing.
  - `/gcash-details` lets a provider save the number and account name customers pay.
  - A "How to pay" card on an unpaid GCash booking shows the provider's GCash details, the amount
    and the booking reference, from the API's `payment_instructions`.
**Verify:** register a new account, capture both sides of the ID, and make a GCash booking — the
booking shows the provider's GCash details, and the provider sees the commission become outstanding
once they confirm the payment.
**Tests:** `identity_test` (new), `booking_test`, `app_sweep_test`; 270 Flutter tests pass.

### ~~H7 · GCash has never been run end to end~~ — **SUPERSEDED 2026-09-26**
**Why:** H7 asked for a ₱1 payment through the PayMongo redirect. Since `ADR-021` there is no such
path: `config/payments.php` routes **both** methods to the manual gateway, so
`POST /bookings/{booking}/pay` refuses every booking with a 422 and no payment intent is ever
created. The integration stays in the codebase, tested but unused for bookings; its one defensible
future use is a provider paying their **own** outstanding commission, which is not built.
**What replaces it** — verify the *direct* payment flow on the deployed system, as part of the D2
demo script: a customer makes a GCash booking, sees the provider's GCash details, pays, the provider
confirms the payment, the commission becomes outstanding and blocks new work, and an administrator
settles it. No real card or gateway is involved, so this costs nothing to rehearse.
**Also done:** the stale comments in `config/payments.php` and the pay endpoint's Swagger
description (which still claimed a GCash booking could be paid online) now match ADR-021.

### H8 · Identity enforcement is switched off **[DEP]** — owner action
**Where:** Admin web → System Settings → **Identity**.
**Problem:** National ID verification is built but **not enforced**: it ships off deliberately so
deploying changed nothing.
**Fix:** when ready, set *Require National ID verification to transact* on, and set *Require it for
accounts created from* to the cutover date. Leaving that date **empty applies the rule to every
existing account**, which freezes the marketplace until the review queue is cleared — set a date.
**Verify:** an account created after the date cannot book until verified; one created before still
can.
**Code side done 2026-09-26:** the Identity tab did not exist. `SettingsPage.jsx` builds its tabs
from its own list, not from the API's groups, so the `identity` group was returned by the API and
rendered nowhere — this owner action could not be performed at all. The tab is now there, the
cutover date is a date picker, and turning the switch on with the date empty raises a warning about
freezing every existing account.

### ~~H9 · Push the outstanding 401 fix~~ — **RESOLVED**
Commit `6f4c46c` (`redirectGuestsTo(fn () => null)` plus a regression test) is on `origin/main`;
the entry was stale. `curl https://skillserve-web-backend.onrender.com/api/bookings` should return
401, not 500 — worth confirming once against the deployed backend.
**Pushed 2026-09-30:** all four repos are on `origin/main`. The backend deploy ran the two new
migrations and went live (the new `/api/commission-tiers/presets` answers 401 unauthenticated;
`/api/health` up); the frontend was pushed after it.

### Owner actions before go-live (cannot be done from the code)
1. **Render:** a paid backend instance with the persistent disk, and the environment from
   `DEPLOYMENT.md`, including `SEED_MODE=starter` on the first deploy, then `admin-only`.
   After that, follow `DEPLOYMENT.md` → "Go-live checklist".
2. ~~**Android signing**~~ — keystore and `android/key.properties` created 2026-09-30 (Flutter repo
   `PENDING_FIXES.md`). **Still to do: back both up.** Release SHA-1
   `20:30:88:71:1E:64:1B:EE:90:9B:E5:0C:7E:FE:E1:9D:75:E3:36:1A`.
3. **Google sign-in:** register an Android OAuth client for `com.skillserve.mobile` with the debug
   and release SHA-1 fingerprints (Flutter repo `SETUP_CREDENTIALS.md`, section 2).
4. **Admin content:** in Settings, write the Terms of Service, Privacy Policy and Community
   Guidelines, and review the booking rules. Then add categories, badges and a support-staff role.
5. **Evidence:** run the smoke test (D2) on the deployed stack and fill in the Result columns of
   both `TEST_PLAN.md` files.

---

## Medium

### ~~M8 · Commission blocking has no threshold~~ — **RESOLVED 2026-09-30**
**Done:** two System Settings → Marketplace values decide when unpaid commission blocks a provider:
*Block providers once unpaid commission reaches (₱)* and *Also block when a commission stays unpaid
for (days)*. Whichever is reached first blocks. Defaults (₱0, 0 = off) keep the original behaviour —
any debt blocks at once — so deploying changes nothing until an administrator sets them.
`GET /api/client/v1/provider/commissions` and `/transaction-eligibility` now also return
`block_threshold` and `block_deadline`. Tests in `CommissionLedgerTest`.
**Owner action:** pick the values (for example ₱200 and 7 days) in the admin web when ready.
**Optional mobile follow-up:** the app already obeys `eligible`; it could also show "remit by
{block_deadline}" to warn a provider before the block. Not required for correctness.

<details><summary>Original entry</summary>

### M8 · Commission blocking has no threshold **[BE]** — decision taken, worth revisiting
**Where:** `CommissionLedger` / `TransactionEligibility`. Known Issues **KI-27**.
**Problem:** a provider owing **₱20** is blocked from new work exactly like one owing ₱5,000, and
every on-hand job creates a small debt an administrator must clear by hand.
**Fix if it proves too blunt:** a minimum balance and/or an age before blocking starts, as System
Settings values. The ledger and eligibility service already funnel through one place, so this is a
small change.
**Verify:** a provider owing less than the threshold can still accept work.

</details>

### ~~M9 · Mobile `api-docs/` is synced but uncommitted~~ — **RESOLVED 2026-09-30**
Committed in the Flutter repo as `43496cf docs(api): sync api-docs with the backend`.

<details><summary>Original entry</summary>

### M9 · Mobile `api-docs/` is synced but uncommitted **[MB]**
**Where:** Flutter repo, `api-docs/`.
**Fix:** `git add api-docs && git commit` in that repo. It is regenerated by the `sync-api-docs`
skill and was left uncommitted because the mobile repo is the owner's to commit.

</details>

### ~~M10 · The app's 2026-09-26 catch-up is still uncommitted~~ — **RESOLVED 2026-09-30**
Verified with `flutter analyze` (no issues) and `flutter test` (270 passed) on Flutter 3.44.2, then
committed in the Flutter repo as `d79e1a6`.

---

## Low

### ~~L1 · (KI-30) A provider is not told when their commission is settled or waived~~ — **RESOLVED 2026-09-30**
`NotifyProviderOfCommissionSettlement` sends `CommissionSettlementNotification` on both events,
with the amount, the booking and what is still owed. Type `booking_commission` + `booking_id`, so the
current app files it under booking updates and opens the booking on tap. Test in
`CommissionLedgerTest`.

### ~~L2 · (KI-31) The app does not show SkillServe's share when a provider prices a service~~ — **RESOLVED 2026-09-30**
The service form shows "SkillServe 15% · ₱75.00 · you keep ₱425.00" as the price is typed, and My
Services shows each service's earnings. Flutter repo `0434a02`; `commission_split_test` (5 tests),
275 app tests pass.

---

## Defense readiness

- **D1. Requirements traceability matrix.** Done: `TEST_PLAN.md` (admin web) and the Flutter repo's
  `TEST_PLAN.md` (mobile) map every requirement to its page/screen, endpoint, automated tests and
  UAT steps. Fill in the Result column on the deployed system; every row must pass before the
  defense.
- **D2. Demo script and data.** Written 2026-09-30: `DEMO_SCRIPT.md` — preparation, then booking →
  reschedule → accept → job → GCash payment → commission block and settlement → review → report and
  moderation → dispute → admin wrap-up, with the expected result of every step. **Owner action:**
  rehearse it on the deployed system and record results in both `TEST_PLAN.md` files. Use
  `scripts/fresh-demo.sh` only on a **local/demo** database (it wipes data).
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
