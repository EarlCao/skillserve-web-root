---
type: reference
tags: [troubleshooting, known-issue, audit]
audited_on: 2026-09-22
---
# Known Issues and Gaps

Master list of defects, gaps and inconsistencies **found by the 2026-09-22 audit** (code reading, no
runtime testing). The repos' own `PENDING_FIXES.md` files list nothing open; these are additional.
Severity uses the `AGENT_REVIEW.md` scale. Open questions without a confirmed defect are in
[[Needs Verification Register]].

## Functional

| ID | Sev. | Issue | Evidence | Impact | Direction |
|---|---|---|---|---|---|
| ~~KI-01~~ | **Resolved 2026-10-06.** The background token is exempt from the admin session timeout, `config/sanctum.php` has no global expiry (it ended every token after a day), and the app forgets a refused background token so the next sign-in issues a new one. Was: HIGH — Mobile background (closed-app) token is rejected once older than `system.session_timeout_minutes` |
| ~~KI-02~~ | ~~HIGH~~ | **Resolved 2026-10-03.** Forgot password now runs in the app: email → 6-digit code (`POST /auth/verify-reset-code` returns a reset token) → new password + confirmation (`POST /auth/reset-password`); the link email and `CLIENT_PASSWORD_RESET_URL` were removed ([[Registration and OTP Flow#Forgot password (mobile)]]). Was: Mobile password recovery cannot be completed | `ClientPasswordResetNotification` links to `config('client-auth.password_reset_url')` = default `APP_URL/client/reset-password`; no such route in `backend/routes/web.php`, no page in the admin SPA, and the app never calls `POST /client/v1/auth/reset-password`; `CLIENT_PASSWORD_RESET_URL` is undocumented | M 1.4 "recover account access" fails; UAT row M 1.4 will fail | add a reset screen (deep link or in-app token entry) or a small web page, and document the env var |
| ~~KI-03~~ | **Resolved 2026-10-06.** Rejecting returns the booking to `completed` (if `completed_at` is set) or `active`, and a rejected dispute can be closed. The older `PATCH /api/bookings/{booking}/dispute` also stored the action name ("reject") as the status; fixed, and migration `2026_10_06_000001` corrects existing rows (data only). Was: MEDIUM (Needs Verification) — Rejected dispute leaves the booking `disputed` forever and cannot be closed |
| ~~KI-04~~ | **Resolved 2026-10-06.** `POST /api/client/v1/reports` accepts `service_id` (any listed service except your own); the app has a flag on the service page. Was: MEDIUM — Service reports (A 9.2) can't be created by users |
| ~~KI-05~~ | **Resolved 2026-10-06.** Worse than recorded: PHP ran on its defaults (2 MB per file, 8 MB per request). `deploy/php/uploads.ini` (10M / 55M) is in both images and nginx allows 55m. Was: MEDIUM (Needs Verification) — Verification upload may exceed the production body limit |
| ~~KI-06~~ | **Resolved 2026-10-06.** Production Reverb accepts `skillserve` (probed 2026-10-06); every default is now `skillserve`. Was: LOW — Reverb key defaults disagree |
| ~~KI-07~~ | **Resolved 2026-10-06.** The error goes to the log; the endpoint returns only `down`. Was: LOW — `/api/health` returns raw DB exception text publicly |

## Code / consistency

| ID | Sev. | Issue | Evidence |
|---|---|---|---|
| ~~KI-08~~ | **Resolved 2026-10-06.** Both downloads go through `services/api.js`. Was: LOW — Feature code imports raw axios (rule says use `services/api.js`) |
| KI-09 | LOW | Unused files/packages — **frontend files removed 2026-10-06; the five backend packages are still installed (removal awaits the owner's go-ahead)** | `frontend/src/components/feedback/OfflineBanner.jsx` (only `common/OfflineBanner` imported), `frontend/src/assets/hero.png`; backend packages with config but no app usage: dompdf, laravel-backup, medialibrary (`media` table), spatie settings classes (`app/Settings/` empty), nwidart modules; `s3` disk |
| KI-10 | LOW | Seeder vs migrations permission drift | seeder omits the 7 granular service permissions (created by migration) and re-syncs `admin` to a short list while later migrations grant more ([[Permission Catalog]]) |
| KI-11 | LOW | OpenAPI spec omits `PATCH` aliases, `/api/health`, `/api/broadcasting/auth` | [[API Documentation Pipeline]] |
| KI-12 | LOW | Backend `tests.yml` workflow (Laravel skeleton) triggers on `master`, not `main` | `backend/.github/workflows/tests.yml` |
| KI-13 | LOW | No test for `PATCH /api/providers/{id}/verification/remove`; several admin modules have ≤4 tests | [[Backend Test Suite]] |
| KI-14 | LOW | Flutter package still named `skilllink_mobile`; pubspec description says "Frontend only — ready for future REST API integration" and "Media (UI only — no upload logic)" | `pubspec.yaml` |

## Stale documentation

| ID | Document | What is outdated |
|---|---|---|
| KI-15 | mobile `AGENT.md` | "Deferred Scope" lists as missing: review reporting, message reporting, dispute evidence upload, provider support tickets, presence/typing, closed-app notifications, admin announcements, info-request response; "API Integration Status" says profile update throws `UnsupportedError` — all now implemented |
| KI-16 | mobile `README.md` → Design system | claims Ink Navy/Brass/Warm Slate and Space Grotesk/Inter/IBM Plex Mono; code uses charcoal/lime and Outfit ([[Mobile UI System]]) |
| KI-17 | `api-docs/README.md` → "What is NOT yet implemented" | says Reverb is web-only and recommends FCM |
| KI-18 | `DEPLOYMENT.md` → Troubleshooting | "The mobile app has no WebSocket connection; it checks unread-count every 30 seconds" |
| KI-19 | `AdminDataChanged` docblock | "production runs no queue worker" — `start.sh` runs one |
| KI-20 | `primary_button.dart` doc comment | describes a brass gradient; button renders lime |
| KI-21 | `ADMIN_WEB_MOBILE_READINESS_AUDIT.md` | dated 2026-09-08 (62% estimate, Support missing, etc.) — superseded; keep as history |
| KI-22 | `backend/README.md`, `frontend/README.md` | framework boilerplate (Laravel / React+Vite), not project docs |
| KI-23 | Root `README.md` | Swagger table's first row shows a stray "user`" instead of the `/api/documentation` URL; says `nwidart/laravel-modules` gives the "modular structure under `Modules/`" (it doesn't) |

## Process

| ID | Issue |
|---|---|
| KI-24 | UAT Result columns and automated-check run tables in both `TEST_PLAN.md` files are empty — no recorded acceptance evidence |
| KI-25 | Go-live owner actions (paid Render + disk, signing keystore, Google OAuth SHA-1, admin content, smoke test) are not recorded as done ([[Go-Live Checklist]]) |
| ~~KI-29~~ | **Resolved 2026-09-26.** System Settings in the admin web rendered six of the seven setting groups: the `identity` group had no tab, so the National ID requirement and its cutover date could not be reached from the UI at all — the setting H8 asks the owner to turn on. Found while working through H8 |
| ~~KI-26~~ | **Resolved 2026-09-26.** The app offered six payment methods and defaulted to `cash`, and had no screen for National ID submission, transaction eligibility or an outstanding commission, so a blocked account saw a bare 403. It now offers `on_hand` and `gcash` only, captures the National ID at registration and from Settings, shows an eligibility banner on both homes, lists what a provider owes, and shows the customer where to send a GCash payment. See [[Changelog]] 2026-09-26 |
| ~~KI-28~~ | **Resolved 2026-09-25.** Provider payouts were the largest open gap while PayMongo collected booking totals. Closed by removing the cause: the customer now pays the provider directly and SkillServe never holds the money. See [[ADR-021 Direct Payment with Provider-Remitted Commission]] |
| ~~KI-27~~ | ~~Commission enforcement has no threshold~~ — **resolved 2026-09-30**: a minimum unpaid amount and a grace period in days are now System Settings; see [[Commission Tiers and Settlement#What an outstanding commission blocks]] |
| ~~KI-30~~ | ~~No notification when a commission is settled or waived~~ — **resolved 2026-09-30**: `CommissionSettlementNotification` (**L1**) |
| ~~KI-31~~ | ~~No commission split in the service form~~ — **resolved 2026-09-30** (**L2**) |
| ~~KI-32~~ | **Resolved 2026-09-30 — production wiped and reseeded `admin-only`.** Was: production held the demo dataset: seeded providers and customers on `example.*` addresses, active and verified, with the password `password` — guessable, since provider names are public. Cause: `SEED_MODE` defaults to `demo` when unset. Decided 2026-09-30: wipe production and reseed with `admin-only` (**C7**) |

When an item is fixed: update the code, move the row to [[Changelog]] with the date, and update the
affected notes.

> [!info] This note describes; `PENDING_FIXES.md` acts
> The root `PENDING_FIXES.md` is the working to-do list: each entry there says what to *do* about a
> gap, who it is for, and how to verify the fix. This note is the reference description. Keep the
> two in step — a gap recorded in one belongs in the other.
>
> | Here | There |
> |---|---|
> | ~~KI-26~~ Flutter app behind the API — resolved | ~~H6~~ |
> | ~~KI-27~~ no commission threshold — resolved | ~~M8~~ |
> | ~~KI-28~~ provider payouts — resolved | ~~C6~~ |
> | ~~KI-30~~ no settlement notification — resolved | ~~L1~~ |
> | ~~KI-31~~ no commission preview — resolved | ~~L2~~ |
> | ~~KI-32~~ demo data in production — resolved | ~~C7~~ |

Related: [[Security Findings]] · [[Project Status]] · [[Needs Verification Register]]
