---
type: changelog
tags: [change-management, changelog]
sources: [PENDING_FIXES.md, git logs, ADMIN_WEB_MOBILE_READINESS_AUDIT.md]
---
# Changelog

Newest first. Entries before 2026-09-22 are reconstructed from `PENDING_FIXES.md` ("Resolved on
2026-09-21"), the 2026-09-08 readiness audit, and commit messages. Add new entries at the top with
[[Template - Change Entry]].

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
