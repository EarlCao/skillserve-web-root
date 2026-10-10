---
type: changelog
tags: [change-management, changelog]
sources: [PENDING_FIXES.md, git logs, ADMIN_WEB_MOBILE_READINESS_AUDIT.md]
---
# Changelog

Newest first. Entries before 2026-09-22 are reconstructed from `PENDING_FIXES.md` ("Resolved on
2026-09-21"), the 2026-09-08 readiness audit, and commit messages. Add new entries at the top with
[[Template - Change Entry]].

## 2026-10-10 — The health check asks Brevo whether codes are delivered

Brevo answers *accepted* even from an account it will not deliver for, which is how the first
account's suspension went unnoticed. `GET /api/health` → `services.otp` now asks Brevo
(`BrevoAccountCheck`: `GET /v3/account` and the last two days' transactional statistics, cached 5
minutes) and reports `down` with a plain `error` when Brevo refuses the key or the server's IP, the
sending allowance is used up, or emails were accepted but none delivered. Brevo's own messages go
to the log only. Sign-up, resend and forgot-password codes are unchanged; their tests (repeated
sends, retry after a failure) still pass. See [[Registration and OTP Flow]].

## 2026-10-07 — Back to Brevo, on a new account

The owner chose **Brevo** again (`MAIL_MAILER=brevo-api`), on a new account sending from a domain
authenticated in Brevo. The first account had been suspended by Brevo, which kept answering
*accepted* — so codes worked at first, then silently stopped. Changes: sign-up refuses an email
whose domain cannot receive mail (`client-auth.check_email_domain`, fewer bounces); a failed
resend answers 503 with a retry message instead of a 500, and starts no cooldown; Brevo's refusal
reason (`code`, `message`) and message id reach the log. Tests prove repeated resends and
forgot-password codes all go out through Brevo. Setup and the suspension checklist:
DEPLOYMENT.md → "Email codes". See [[Registration and OTP Flow]], [[External Integrations]].

## 2026-10-07 — Codes and mail by Resend

The codes and every email now go out through **Resend** (`MAIL_MAILER=resend-api`,
`ResendApiTransport`, free 3,000/month and 100/day). Resend sends to other people only from a
verified domain, so the setup adds a free DigitalPlat domain with its DNS on Cloudflare's free plan
(DEPLOYMENT.md → "Email codes"). A refusal raises Resend's reason into the server log;
`GET /api/health` → `services.otp` checks `RESEND_API_KEY`. The Gmail API mailer stays as the
no-domain alternative. See [[Registration and OTP Flow]], [[External Integrations]].

## 2026-10-06 — Codes and mail sent as Gmail (Gmail API)

Mailjet blocked the new account ("Your account has been temporarily blocked"), the second email
service after Brevo to refuse a new free account sending from a Gmail address. Mail now goes out
**as the owner's Gmail through the Gmail API** (`MAIL_MAILER=gmail-api`, `GmailApiTransport`):
free, no third party to approve the account, about 500 emails a day. Also fixed: Render never
showed these failures because `start.sh` discarded every background process's stderr; errors now
reach the log, without the PHP server's per-request lines.

## 2026-10-06 — Codes and mail by Mailjet

Brevo is replaced by **Mailjet** (`MAIL_MAILER=mailjet-api`, `MailjetApiTransport`, free 200/day):
the sign-up, resend and forgot-password codes and every other email. A refused email raises
Mailjet's error code into the server log. `GET /api/health` reports `services.otp` (driver, mailer,
keys present). Twilio Verify (`OTP_DRIVER=twilio`) and a SendGrid transport were built the same day
and kept, but Twilio has no free trial in the Philippines and SendGrid has no free plan.
See [[Registration and OTP Flow]], [[External Integrations]].

## 2026-10-06 — Sign-up survives the camera, adults only, Philippine phone numbers, audit gaps closed

- **Sign-up after the ID photo** no longer restarts the app on low-memory phones: ML Kit is released
  before the camera opens, and the photos taken are kept for an hour so a restart resumes the scan
  ([[Mobile Sign-up with National ID Scan]]).
- **18+ only; experience ≤ age − 16** at sign-up, profile edit and ID review
  (`App\Shared\Helpers\AgeRequirement`).
- **Approving a provider's National ID verifies the provider** in Provider Management
  ([[Identity Verification]]).
- **Phone numbers are Philippine mobile numbers, 11 digits starting with 09** — the profile phone,
  booking contact phone, GCash number and the admin's user edit. `+63 912 345 6789`, `639…` and
  `9…` are accepted and stored as `09123456789` (`App\Shared\Helpers\PhilippineMobileNumber`;
  the app's `PhMobileNumber` formatter stops the field at 11 digits). The GCash screen explains the
  account name: the name registered on the GCash account, which GCash shows partly hidden to the
  sender.
- **Audit gaps KI-01, 03–23 closed** ([[Known Issues and Gaps]]): closed-app notifications, rejected
  disputes, service reports, upload limits, unused packages, permission drift, API docs, CI, docs.

## 2026-10-03 — A reset database starts with the default setup

`SEED_MODE=starter` (now production's default, and what `scripts/fresh-admin.sh` seeds) gives the
super-admin plus the service categories, the Standard commission tiers and the provider badges — no
sample people. Fixed the reset script's container check. See [[Seeding and Demo Data]].

## 2026-10-03 — Password after the code, Google needs the password, readable light and dark mode

- **Sign-up order:** National ID → details → 6-digit code → password + confirmation → account, for
  email and Google sign-ups alike (`POST /auth/complete-registration`, `registration_token`).
  Migration `2026_10_03_000001_add_password_step_to_pending_registrations`. Older app versions that
  send the password up front still complete on the code.
- **Google sign-in needs the account password** (`password_required`, then `/auth/google` with
  `password`). Google-created accounts from before this set theirs with Forgot password.
- **Forgot password by code, in the app** (`/auth/verify-reset-code`): closes KI-02. The link email
  and `CLIENT_PASSWORD_RESET_URL` were removed.
- **Mobile readability:** lime is no longer used as text/icon colour on light surfaces, and fixed
  light-mode colours no longer vanish in dark mode (`app_palette.dart`, theme fixes, 66 files);
  `contrast_sweep_test` guards 49 screens in both modes. See [[Mobile UI System]].
- See [[Registration and OTP Flow]]. Backend: 86 client-auth tests, full suite green; app: 407 tests.

## 2026-10-02 — The National ID is captured automatically, and reading never gets stuck

The first test on a real phone failed with "Your ID could not be read" and no way forward. Fixed:
R8 keep rules for ML Kit (release builds strip it otherwise); the camera is ML Kit's Document
Scanner, which detects, auto-captures, crops and cleans the card like KYC apps; a failed read no
longer blocks; the back scanner opens by itself; QR is read on both sides; misread labels on blurry
print are still recognised. See [[Mobile Sign-up with National ID Scan]]. Flutter `7fdb2d5`;
305 app tests pass.

## 2026-10-02 — The address picker everywhere (F1 phase 4)

Edit Profile, the booking form's service address and Add/Edit Service's service area use the
Region → Province → City → Barangay picker instead of a free-text box. The booking starts from the
customer's saved address; a service area needs a city or municipality (barangay optional).
Addresses typed before the picker existed are shown as a reminder to pick them. Flutter `7a55b03`.

**Tests:** `address_picker_test` (6); 302 app tests pass.

## 2026-10-02 — Sign-up starts by scanning the National ID (F1 phase 3)

Email and Google sign-up open on the camera: the front of the PhilSys card or ePhilID, then — by
itself — the back. Google ML Kit reads both on the phone (text on the front, QR on the back, the QR
correcting the camera), the printed address is matched to Region → Province → City → Barangay, and
the form arrives pre-filled for the user to check. After the email code (or Google sign-up) the
scanned card is submitted for review automatically; the National ID screen opens pre-filled only as
a fallback. See [[Mobile Sign-up with National ID Scan]]. Flutter `4bd904a`.

**Tests:** 20 new app tests; 296 pass. **Not yet verified:** a release APK build and a real card.

## 2026-10-02 — Philippine address picker, Phase 2: structured addresses

Sign-up (email, provider and Google), Edit Profile, bookings and services accept a structured
address — the client sends a barangay (or, for a service area, a city) and the server derives the
rest — and store it as PSGC codes plus a formatted copy in the existing text field, so older app
versions and the admin web are unaffected. Sign-up also accepts `birthday`, read from the National
ID. Migration `2026_10_01_000002` (additive). See [[Philippine Addresses]].

**Tests:** `StructuredAddressTest` (6); 637 backend tests pass.

## 2026-10-01 — Philippine address picker, Phase 1: the location list

First phase of the ID-first sign-up the owner asked for. The PSA PSGC (43,778 regions, provinces,
cities/municipalities and barangays) ships as a 318 KB snapshot and is loaded by
`php artisan locations:import` on start. Three public endpoints feed the picker and match a
National ID's printed address to codes (`GET /api/client/v1/locations/regions`,
`/{code}/children`, `/match?address=`). Matching was tuned against the real list: "Quezon City" is
not Quezon province, a province decides between same-named municipalities, and an ambiguous
address is left for the user. See [[Philippine Addresses]].

**Tests:** `PhLocationTest` (11, real PSGC codes), `ImportPhLocationsTest` (3, including a full
check of the shipped snapshot, run in its own process for memory); 631 backend tests pass.

## 2026-10-01 — "Verified" no longer means two different things

Customer Management showed **Verified** for any account that had confirmed its email, so a customer
whose National ID was still pending looked verified. User responses now carry `identity_status`
(backend `40a8c87`); the list has separate **Email** and **National ID** columns and the profile
shows both (frontend `1853d82`).

## 2026-10-01 — Missing upload files explain themselves

Opening a National ID image in the admin web failed with a vague error. The rows existed but the
files did not: without a Render persistent disk every deploy deletes `storage/app` (see
[[Render Persistent Disk]]). The three private downloads (ID images, provider verification
documents, dispute evidence) now answer 404 with a message saying the file is no longer stored and
log a warning (`App\Shared\Helpers\StoredFile`, backend `01e2c61`), and the admin web reads error
messages from blob downloads instead of losing them (frontend `1db2573`). Production also refuses
demo seeding (`051089a`).

## 2026-09-30 — A reset database now gets its super-admin

After the production reset nobody could sign in: `users` was empty. `db:seed-if-empty` treated any
row in `roles` as "already seeded", and the 2026_09_18 migration inserts the fixed roles, so a freshly
migrated database was always skipped. The marker is now the super-admin account itself (backend
`924cf14`, `SeedIfEmptyTest`); the next start seeds it from `ADMIN_EMAIL` / `ADMIN_PASSWORD`.

## 2026-09-30 — Production reset to the super-admin only (C7 closed)

Production had been seeded with the demo dataset (`SEED_MODE` defaults to `demo` when unset), which
left about 170 active accounts with the password `password`. The owner set `SEED_MODE=admin-only`,
wiped the Neon schema and redeployed; `start.sh` migrated the empty database and seeded only roles,
permissions and the super-admin. The catalog now reports 0 services, providers and categories.
The same day, a crash in the new dashboard commission card was fixed (frontend `2e55e67`).

## 2026-09-30 — The leaked PayMongo key is rotated (C5 closed)

The owner regenerated the **live secret key** in PayMongo → Developers → API keys, so the key pasted
into a chat no longer works, and deleted `PAYMONGO_SECRET_KEY` and `PAYMONGO_WEBHOOK_SECRET` from
Render. The new key is stored nowhere in the project, because nothing uses it (ADR-021). The optional
`--probe-key` check was skipped because the old key was no longer at hand.

## 2026-09-30 — The app's catch-up is committed, and providers see their commission split (M10, L2 / KI-31)

- **M10.** The 2026-09-26 app work (identity verification, provider Commissions and GCash details
  screens, the two-method booking form, payment recording) was verified with `flutter analyze` (no
  issues) and `flutter test` (270 passed), then committed as `d79e1a6`.
- **L2.** The service form shows SkillServe's share and what the provider keeps as they type a
  price, and My Services shows each service's earnings (`0434a02`). 5 new tests; 275 pass.
- Flutter now runs from WSL through a Linux SDK of the same version against a copy of the app — see
  [[Mobile Test Suite]].

## 2026-09-30 — Providers hear when their commission is settled (L1 / KI-30)

Settling or waiving a commission from the admin web used to unblock the provider silently. A
`CommissionSettlementNotification` now tells them the amount, the booking and what they still owe.
It uses the `booking` preference category and the type `booking_commission` with a `booking_id`, so
the current app already files it with booking updates and opens the booking on tap — no app release
needed.

**Tests:** 1 new in `CommissionLedgerTest`; 611 backend tests pass.

## 2026-09-30 — Commission blocking gets a threshold (M8 / KI-27)

A provider owing ₱20 was blocked exactly like one owing ₱5,000. Two System Settings → Marketplace
values now decide when the block starts: a minimum unpaid total (₱, 0 = any debt) and a grace period
after which even a small debt blocks (days, 0 = off). Whichever is reached first applies. The
defaults keep the original behaviour, so the deploy changes nothing until an administrator sets
them. The provider commission and transaction-eligibility endpoints also return `block_threshold`
and `block_deadline` (additive). The admin Settings page explains both fields.

**Tests:** 3 new in `CommissionLedgerTest`; 610 backend tests pass.

## 2026-09-30 — Commission on the dashboard, and a general Excel report

- **Dashboard commission card.** Collected commission in pesos and as a percentage of the settled
  bookings it came from (e.g. ₱350 = 17.5% of ₱2,000), outstanding and waived totals, and the rates
  in force. Administrators with `manage commissions` can edit a band's percentage in place or apply
  a preset — **Standard** (5/10/15/20%) or **Flat 10%** — which retires the active tiers and creates
  the preset's bands in one transaction. The block is omitted from `GET /api/dashboard` for viewers
  without a commission permission. See [[Admin Dashboard#Commission card]].
- **Presets** live in `config/commissions.php`; new endpoints `GET /api/commission-tiers/presets`
  and `POST /api/commission-tiers/presets/{preset}/apply`. See
  [[Commission Tiers and Settlement#Presets]].
- **Commission report category** (`type=commissions`) on the Reports page and in CSV export.
- **General report.** `GET /api/analytics/reports/general/export` builds one Excel workbook: a
  Summary sheet plus a sheet for each of the seven categories, over the selected date range. The
  CSV formula-injection guard moved into `ReportService::exportCell` so both exports share it. See
  [[Reports and Analytics#General report]].

**Tests:** 4 preset tests in `CommissionTierTest`, 3 in `DashboardTest`, 4 in `AnalyticsTest` (the
workbook is opened with PhpSpreadsheet and checked sheet by sheet); 607 backend tests pass.
Frontend `npm run lint` and `npm run build` pass. No schema change.

## 2026-09-30 — A provider's rating is the average of its services' ratings

Customers rate services; the provider's rating is now built from those. Five services rated 3.50,
5.00, 4.60, 3.30 and 3.50 give the provider **3.98**, each service counting once however many
reviews it has. It used to be the plain average of every review, so one busy service outweighed the
rest. Full rule in [[Reviews and Ratings Rules]].

- **One place calculates ratings.** `RecalculateClientReviewAggregatesAction` moved to the Reviews
  module as `RecalculateRatingAggregatesAction`. Unrated services are left out rather than counted
  as zero; deleted and hidden services still count, so deleting a poorly rated service cannot lift
  a provider.
- **Admin moderation now recalculates.** Hiding, restoring or removing a review — from the Reviews
  page or a report moderation action — and restoring a removed review from Data Management used to
  leave both ratings stale until the next customer review. They now update at once.
- **Admin screens read the stored rating.** Provider Management and Provider Recognition (list,
  sort, Top Rated and its `min_rating` filter) computed their own review average, so they could
  disagree with the mobile app. They now read `provider_profiles.average_rating`.
- **Migration `2026_09_30_000001_recalculate_ratings_from_service_ratings`** rewrites the stored
  ratings on deploy. Data only; see [[Migrations Timeline]].
- **No change to service ownership.** Providers already create their own services from the app and
  administrators only moderate them (approve, reject, edit, hide, feature, delete) — see
  [[Service Approval Lifecycle]]. API response shapes are unchanged.

**Tests:** `RatingAggregatesTest` (5 new); 596 backend tests pass.

## 2026-09-26 — A leaked PayMongo key can no longer be spent by accident

Code side of **C5**. The rotation itself is a dashboard action with an OTP, which nothing in the
repositories can perform — what could be built is everything that makes the leak harmless and the
rotation checkable.

- **`PayMongoClient` refuses a live key.** An `sk_live_` key is rejected before the HTTP call unless
  `PAYMONGO_ALLOW_LIVE=true` is set as well, with a `critical` log line that never contains the key
  and a deliberately vague 502 to the caller. One mistyped environment variable should not be all
  that stands between a deploy and real money — and under
  [[ADR-021 Direct Payment with Provider-Remitted Commission]] nothing is supposed to reach PayMongo
  at all, so a live key in the environment is a misconfiguration by definition.
- **`php artisan paymongo:status`** reports the posture of any environment: whether a key is set and
  whether it is test or live, whether live is allowed, whether a webhook secret is set, and which
  gateway each payment method resolves to. "No key is set" is the healthy answer.
- **`--probe` / `--probe-key`** ask PayMongo to read a payment intent that cannot exist. A rejected
  key answers 401 whatever it is asked for, so this is how a rotated-out key is confirmed dead. The
  prompted key is hidden, not logged and not stored.
- **The key is in no repository.** All four working trees and their full git history were searched
  for `sk_live_`; only truncated references in documentation. `backend/.env` is gitignored and its
  live key had already been removed by hand.
- **The documentation stopped inviting it back.** `.env.example`, `DEPLOYMENT.md` and
  [[PayMongo Setup]] all said, in one form or another, that setting a key switches GCash on. That
  has been untrue since ADR-021: both methods route to the manual gateway unconditionally. They now
  say to leave every PayMongo variable unset, and `DEPLOYMENT.md` gained a "Rotating an exposed
  PayMongo key" runbook and a go-live step that checks the posture.

**Tests:** `LiveKeyGuardTest` (11 new); 591 backend tests pass.

## 2026-09-26 — The app catches up with the API, and Identity is reachable from the admin web

Closes **H6** (KI-26) and the part of **H8** that was not an owner action at all.

- **Mobile payment methods trimmed to the two the API accepts.** The booking form offered six and
  defaulted to `cash`; Card, Bank transfer and PayPal had been returning **422** since the methods
  were trimmed. It now offers `on_hand` and `gcash` only. Codes on older bookings (`cash`,
  `credit_card`, `paypal`, …) still read back with a label, because the API deliberately does not
  rewrite them.
- **National ID capture is wired up.** The screen existed but no route reached it. It is now
  `/identity-verification`, on the Profile tab for both roles, and is where registration lands —
  after the OTP for an email sign-up, and after "Finish signing up" for a Google one, which has no
  OTP step because Google verifies the address. A provider carries on to business onboarding
  afterwards. It can be skipped while the platform does not require verification of that account.
- **A blocked account is told why, before it is stopped.** `EligibilityBanner` renders
  `GET /transaction-eligibility` on the customer home and the provider dashboard and sends the
  person to the screen that fixes it. It draws nothing at all when the account is eligible, so a
  verified user never sees it. Previously the first sign of a block was a bare 403 at the moment of
  booking.
- **Providers can see what they owe.** `/commissions` lists each unremitted booking, the total, and
  what the block stops them doing — and says plainly that there is nothing to pay in the app,
  because SkillServe never handles the money.
- **Providers can save their GCash details** (`/gcash-details`), which is what makes
  `payment_instructions` useful. Without them the customer is only told to message the provider.
- **The customer sees where to pay.** A "How to pay" card on an unpaid GCash booking shows the
  provider's number, the name GCash will display, the amount and the booking reference, with a copy
  button — straight from `payment_instructions`, never guessed at by the app.
- **The admin web had no Identity tab.** System Settings rendered six of the seven setting groups,
  so the switch H8 asks the owner to turn on was not reachable in the UI at all. The tab is now
  there, the cutover date is a real date picker, and turning the requirement on with the date empty
  raises a warning that it freezes every existing account.
- `payment_instructions` and `cancellation_policy` are now in the OpenAPI schema; the pay endpoint's
  description no longer claims a booking can be paid online, which has not been true since
  [[ADR-021 Direct Payment with Provider-Remitted Commission]].

**Tests:** 270 Flutter tests pass (23 new), `flutter analyze` clean; 579 backend tests pass; admin
web lint and build clean.

## 2026-09-25 — Direct payment: SkillServe never holds the money

Reverses the money flow decided earlier the same day, after the owner chose it against two
alternatives ([[ADR-021 Direct Payment with Provider-Remitted Commission]]).

- The customer pays the **provider directly** — GCash to the provider's own number, or cash — and
  the provider then remits the commission to keep taking work. A GCash booking now behaves exactly
  like a cash one, with no special case in the ledger.
- `config/payments.php` routes **both** methods to the manual gateway unconditionally, even with
  PayMongo credentials present. This matters operationally: the keys were already in Render, so
  without this change production would have started collecting booking totals into SkillServe's
  account.
- `provider_profiles` gained `gcash_number` and `gcash_name`. Shown to a customer only on their own
  unpaid GCash booking, never in the public catalog.
- **KI-28 (provider payouts) is closed by removing the cause**, not by building a payout system.
- The PayMongo integration stays, tested but unused for bookings. Its defensible future use is the
  provider paying their own outstanding commission — SkillServe collecting its own revenue.
- Trade accepted: no escrow, no payment guarantee. A customer who pays and receives nothing is a
  dispute, not something the platform can reverse.

**Tests:** 579 backend tests pass (10 new).

## 2026-09-25 — GCash live through PayMongo

- `PayMongoGateway` is now a real integration, replacing the throwing stub: Payment Intent → `gcash`
  Payment Method → attach → redirect → webhook, the flow PayMongo currently documents (checked
  against their live docs first — the previous docs site had been restructured and the Sources API
  is no longer the recommended path).
- New `POST /api/client/v1/bookings/{booking}/pay` and `POST /api/webhooks/paymongo`, plus the
  `payment_intents` table.
- The **webhook** marks a booking paid, never the customer's return redirect. Signature verification
  runs on the raw body with a 5-minute replay tolerance, and events are deduplicated by event id
  because PayMongo redelivers.
- Credentials come from the environment only; `config/payments.php` routes GCash back to manual
  settlement when no key is configured.
- **PayMongo settles into SkillServe's account**, so a GCash commission settles on payment instead of
  becoming outstanding — and SkillServe then owes the provider their net, which is **not built**
  (KI-28). See [[ADR-020 PayMongo Collects Into the Platform Account]].

**Tests:** 568 backend tests pass (19 new), none of which touch a real PayMongo account.

## 2026-09-25 — Seeding reduced to the super-admin only

- `RolePermissionSeeder` now creates **only** `admin@skillserve.test` (super-admin). The second
  seeded administrator (`system@skillserve.test` / `SYSTEM_ADMIN_*`) is gone, so a deployment starts
  with exactly one way in and every further staff account is created by hand in Administrator
  Management.
- Migration **`2026_09_25_000001_remove_seeded_system_administrator`** soft-deletes that account on
  existing databases, revoking its tokens and detaching its staff role. A seeder change alone would
  not have touched production: `db:seed-if-empty` skips once roles exist, whereas migrations run on
  every deploy.
- `SYSTEM_ADMIN_EMAIL` / `SYSTEM_ADMIN_PASSWORD` are retired; production seeding now only requires a
  non-default `ADMIN_PASSWORD`.
- The removal is a soft delete, so it is restorable from Data Management for 30 days before the
  scheduled purge removes it for good. Administrator accounts created by hand are untouched.

## 2026-09-24 — Commission tiers, National ID verification, two payment methods

Added on the project owner's instruction; none of this is in the requirements PDFs
([[Requirements Sources]]).

### Commission
- **Tiered rates** (`commission_tiers`) replace the flat `marketplace.commission_rate`, which stays
  as the fallback so an unconfigured deployment behaves exactly as before. Overlapping active bands
  are refused by the service on every driver and by a PostgreSQL exclusion constraint.
- **The commission is inclusive** — it comes out of the price the provider advertises, so the
  customer pays that price and the provider receives the rest. `bookings.total_price` keeps its
  meaning and the mobile booking contract is unchanged. This **supersedes** the owner's earlier
  written example of adding the commission on top.
- Each booking snapshots its rate and tier, so changing the tiers never moves an existing booking.
- Providers see the split before publishing a price, and on every booking.
- A paid on-hand job leaves the provider holding SkillServe's share; it is tracked as outstanding
  until an administrator records the remittance. While anything is outstanding they cannot accept
  new bookings or publish services — work already agreed to is never blocked.
  See [[Commission Tiers and Settlement]].

### Identity
- **Philippine National ID verification** for customers and providers through one pipeline, separate
  from provider business verification so existing verified providers are untouched.
- The card number is never stored in the clear: an HMAC blind index is the only column compared and
  a partial unique index enforces one active account per ID
  ([[ADR-018 Blind Index for National ID Uniqueness]]).
- An ID is released for reuse only on **permanent** deletion, never on soft deletion.
- Admin review queue with separate view/approve/reject permissions and an audited document download.
- **Enforcement ships switched off** and grandfathers accounts created before a configurable date.
  See [[Identity Verification Lifecycle]].

### Payments
- Narrowed to **`on_hand` and `gcash`**. `cash` is accepted as a deprecated alias; `credit_card`,
  `debit_card`, `bank_transfer` and `paypal` are removed and now return 422.
- `PaymentGateway` abstraction with a manual implementation (today's behaviour) and a PayMongo
  **stub that throws**. No credentials, no webhook route, no payment_intents table — those land with
  the integration ([[ADR-019 Payment Gateway Abstraction with PayMongo Deferred]]).

### Admin web
- [[Commission Management]] (`/admin/commissions`) and [[Identity Verification]]
  (`/admin/identity-verifications`).

### Follow-up
> [!warning] The Flutter app must be updated
> It offers all six old payment methods and **defaults to `cash`**. The alias keeps that default
> working, but Card, Bank transfer and PayPal now fail with 422, and there is no label for
> `on_hand`. The app also has no screen for National ID submission or for an outstanding commission.

**Tests:** 549 backend tests pass (85 new). `npm run lint` and `npm run build` pass.

## 2026-09-22 — Knowledge base created
- Created `SkillServe-Vault/` (this Obsidian vault) from a read-only audit of all four repos.
- Added generator `99 - Meta/Scripts/generate_endpoint_notes.py` (221 routes → 33 endpoint notes).
- Recorded audit findings KI-01…KI-25 ([[Known Issues and Gaps]]) and open questions
  ([[Needs Verification Register]]). No application code was changed.

## 2026-09-21 — Critical/High/Medium/Low items resolved (per PENDING_FIXES.md)
- **C1** provider verification upload (API + app); fixed `LogProviderActivity` 500 on every admin
  provider decision.
- **C2** booking times: UTC storage, Manila business time, app sends UTC.
- **C3** settings enforced: commission → platform fee, booking pause, late-cancellation fee
  (`bookings.cancellation_fee`, migration `2026_09_22_000001`), service approval, featured toggle,
  email/push switches, default page size, provider sign-up switch, maintenance mode (mobile 503).
- **C4** account status: 403 + `meta.account` everywhere; `UserWarned` notification.
- **H1** decision notifications (verification, account, report outcome, dispute).
- **H2** policies served by `GET /client/v1/platform`.
- **H3** dependency updates (`league/commonmark` 2.10.1, `maatwebsite/excel` 3.1.70).
- **H4** mobile release setup (app id, icon, splash, signing, tracked `pubspec.lock`).
- **H5** `SEED_MODE=starter`, env docs, go-live checklist.
- **M1** admin forgot/reset password; **M2** deactivation decision documented; **M3** `client-auth`
  rate limiter; **M4** review moderation notifications; **M5** admin CSP + headers doc; **M6** test
  plans and extra tests; **M7** CORS wildcard removal.
- **L1–L6** cleanup (empty folders removed, env example additions, release workflow doc, READMEs,
  read-only timezone setting).
- Earlier the same day: closed-app notifications (background token + WorkManager), chat presence and
  typing, booking payments and refunds (`manage booking payments`), admin opening verification
  documents, uploads on Render disk, server-side favorites, report reasons in one place, provider
  cancel, customer reschedule, frontend lazy routes/chunking, `render.yaml` removed, provider support
  tickets, reporting reviews/messages, one-open-report index, dispute evidence, 1-year refresh
  window, mark-thread-read endpoint.

## 2026-09-20
- Discovery filters and provider availability (backend + mobile); pending registrations, profile
  photos, client preferences, portfolio items, availability tables.

## 2026-09-17 → 09-18
- Role-based accounts (`users.role_id`, `user_type` dropped), provider services, realtime push,
  live admin updates, moderation-only service management; PHP currency default.

## 2026-09-12 → 09-13
- Mobile registration with email OTP, Google sign-in, SMTP → Brevo API transport, cancel-registration,
  CORS for the Vercel frontend.

## 2026-09-08 → 09-11
- 2026-09-08 readiness audit (≈62 % admin completion; Support missing; super-admin escalation;
  broken `POST /api/services`; no client API).
- System Settings, Data Management, Support modules; client refresh tokens, idempotency keys,
  private verification storage; api-docs generator; mobile switched from mock data to the API.

## 2026-09-03 → 09-05
- Reviews, messages, reports & moderation, dispute management, announcements & notifications,
  dashboard, analytics, provider recognition, audit logs.

## 2026-08-12 → 08-22
- Service categories; granular permissions; provider management & verification; services; bookings.

## 2026-07-26 → 08-07
- Repos created; MySQL briefly, then PostgreSQL + Docker; API foundation (envelope, middleware,
  exceptions); Swagger; admin authentication; administrator management; user management with
  bans; React admin scaffold; Flutter UI prototype with mock data.
