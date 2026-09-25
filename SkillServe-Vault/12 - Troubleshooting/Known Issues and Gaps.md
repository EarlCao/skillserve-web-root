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
| **KI-01** | HIGH | Mobile background (closed-app) token is rejected once older than `system.session_timeout_minutes` | `AppServiceProvider::boot` Sanctum callback exempts only tokens named `client-access`; background token is `client-background` (`BackgroundNotificationService::TOKEN_NAME`); app requests a new token only if none is stored and on 401 just cancels the WorkManager task (`background_notifications.dart`) | Closed-app notifications stop ~1 day after sign-in (default 1440 min; 8 h with the recommended 480) until the user signs out and in | exempt `client-background` from the admin timeout (or check abilities), and/or clear the stored token on 401 so `enable()` re-issues it |
| **KI-02** | HIGH | Mobile password recovery cannot be completed | `ClientPasswordResetNotification` links to `config('client-auth.password_reset_url')` = default `APP_URL/client/reset-password`; no such route in `backend/routes/web.php`, no page in the admin SPA, and the app never calls `POST /client/v1/auth/reset-password`; `CLIENT_PASSWORD_RESET_URL` is undocumented | M 1.4 "recover account access" fails; UAT row M 1.4 will fail | add a reset screen (deep link or in-app token entry) or a small web page, and document the env var |
| KI-03 | MEDIUM (Needs Verification) | Rejected dispute leaves the booking `disputed` forever and cannot be closed | `DisputeService::reject` changes only `dispute_status`; `close` requires `resolved` | booking stuck in `disputed`; dashboards count it as disputed | confirm intended outcome; possibly restore the previous status on reject or allow closing rejected disputes |
| KI-04 | MEDIUM | Service reports (A 9.2) can't be created by users | `ClientReportService::SUBJECT_TYPES = [User, Review, Message]`; only `ReportSeeder` creates `Service` reports | admin "service reports" view is empty on real data | allow `service_id` in `StoreClientReportRequest`, or document the gap |
| KI-05 | MEDIUM (Needs Verification) | Verification upload may exceed the production body limit | nginx `client_max_body_size 20m`; request allows 5 × 10 MB | large submissions could get HTTP 413 before Laravel validates | align limits (e.g. raise nginx limit or lower per-file max) |
| KI-06 | LOW | Reverb key defaults disagree | `.env.example` `skillserve-local-key`; `frontend/src/app/config.js` fallback `5854c89d…`; mobile default `skillserve` | realtime silently fails if an env var is missing | make the key required everywhere |
| KI-07 | LOW | `/api/health` returns raw DB exception text publicly | `backend/routes/api.php` | minor info disclosure | return generic status |

## Code / consistency

| ID | Sev. | Issue | Evidence |
|---|---|---|---|
| KI-08 | LOW | Feature code imports raw axios (rule says use `services/api.js`) | `frontend/src/modules/analytics/api/analyticsApi.js`, `dataManagement/api/dataManagementApi.js` (CSV blobs) |
| KI-09 | LOW | Unused files/packages | `frontend/src/components/feedback/OfflineBanner.jsx` (only `common/OfflineBanner` imported), `frontend/src/assets/hero.png`; backend packages with config but no app usage: dompdf, laravel-backup, medialibrary (`media` table), spatie settings classes (`app/Settings/` empty), nwidart modules; `s3` disk |
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
| KI-26 | **Flutter app is behind the API (2026-09-24).** It offers six payment methods and defaults to `cash`; the alias keeps that default working, but Card, Bank transfer and PayPal now return **422**, and there is no label for `on_hand`. It also has no screen for National ID submission (`/client/v1/identity-verification`), for transaction eligibility, or for an outstanding commission — so a blocked account currently sees a bare 403. See [[Payments and Refunds]] · [[Identity Verification Lifecycle]] |
| KI-28 | **Provider payouts are not built (2026-09-25).** A GCash booking settles into SkillServe's PayMongo account, so SkillServe holds the provider's net (₱180 of a ₱200 job). There is no payout ledger and no payout mechanism — the money must be transferred by hand and nothing tracks the obligation. Largest open gap in the payment design; see [[ADR-020 PayMongo Collects Into the Platform Account]] |
| KI-27 | Commission enforcement has **no threshold**: a provider owing ₱20 is blocked exactly like one owing ₱5,000, and every on-hand job creates a small debt an administrator must clear by hand. Raised with the owner, who chose the simple rule; revisit if it proves too blunt in practice |

When an item is fixed: update the code, move the row to [[Changelog]] with the date, and update the
affected notes.

Related: [[Security Findings]] · [[Project Status]] · [[Needs Verification Register]]
