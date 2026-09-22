---
type: changelog
tags: [change-management, changelog]
sources: [PENDING_FIXES.md, git logs, ADMIN_WEB_MOBILE_READINESS_AUDIT.md]
---
# Changelog

Newest first. Entries before 2026-09-22 are reconstructed from `PENDING_FIXES.md` ("Resolved on
2026-09-21"), the 2026-09-08 readiness audit, and commit messages. Add new entries at the top with
[[Template - Change Entry]].

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
