---
type: meta
tags: [meta, needs-verification]
audited_on: 2026-09-22
---
# Needs Verification Register

Questions the code could not answer during the 2026-09-22 audit. Resolve each by checking the
source named in *How to verify*, then edit the linked note and move the row to **Resolved**.

## Open

| ID | Question | Where it matters | How to verify |
|---|---|---|---|
| NV-01 | What are the real production hostnames (backend `skillserve-web-backend.onrender.com` vs `skillserve-backend.onrender.com`; admin web on Render and/or Vercel)? | [[API Index]], [[Frontend Hosting]], [[Render Backend Service]] | Render / Vercel dashboards |
| NV-02 | Is the backend on a paid instance with the persistent disk attached? Is a keep-alive ping configured? | [[Render Persistent Disk]], [[External Integrations]] | Render dashboard |
| NV-03 | Are the admin web security headers (`X-Frame-Options`, `frame-ancestors`, nosniff, Referrer/Permissions-Policy) configured on the live host? | [[CORS and Security Headers]], SF-1 | `curl -I` the live admin URL |
| NV-04 | Effective permissions of the `admin` role in production (migrations vs seeder `syncPermissions`) | [[User Types and Roles]], [[Permission Catalog]] | `select p.name from role_has_permissions rp join permissions p on p.id = rp.permission_id where rp.role_id = 2` |
| NV-05 | Is a rejected dispute meant to leave the booking `disputed` and un-closable? (KI-03) | [[Disputes Lifecycle]], [[Dispute Management]] | product owner decision |
| NV-06 | Does the app send all verification documents in one request (5 × 10 MB > nginx 20 MB)? (KI-05) | [[File Upload Security]] | inspect `verification_service.dart` request building; try a 5-file upload in production |
| NV-07 | Are DomPDF, laravel-backup, medialibrary (`media` table), spatie settings classes and nwidart modules used anywhere? | [[Tech Stack]], [[media]] | search for usages; remove or document |
| NV-08 | Can anything generate signed temporary URLs for the `local` disk that shares `storage/app/private` with verification documents? (SF-4) | [[File Storage Architecture]] | search for `temporaryUrl` / `Storage::disk('local')` |
| NV-09 | Do any clients use the signed-link email verification routes (`verify-email/{user}/{hash}`, `verification-notification`)? | [[Registration and OTP Flow]] | app + admin code search (none found), server logs |
| NV-10 | Is GitHub Actions enabled for the backend repo and does the daily `tests.yml` run pass? | [[Quality Gates]] | GitHub → Actions |
| NV-11 | Behaviour of unknown admin-web URLs in production (no catch-all route) | [[Admin Web Navigation Map]] | open a bogus `/admin/...` URL on the deployed site |
| NV-12 | Is `/help-center` intentionally reachable signed out in the app? | [[Mobile Navigation Map]] | product decision |
| NV-13 | How do developers point a physical device/emulator at the local backend (repo only ships `localhost`)? | [[Local Setup]] | ask the team |
| NV-14 | Neon plan in use; are Neon branches used for dev/staging? | [[NeonDB]] | Neon console |
| NV-15 | Mobile distribution channel (Play Store vs direct APK) | [[Mobile Release Build]] | team |
| NV-16 | Team roster, roles, adviser; identities behind git handles | [[Team and Ownership]] | team |
| NV-17 | Defense date, panel, rubric; go-live date | [[Defense Readiness]], [[Project Status]] | team / course |
| NV-18 | Should `.obsidian/workspace*.json` be committed or ignored? | [[Git Workflow]] | team preference |
| NV-19 | Purpose of the empty root `.kimchi/ferments/` folder | [[Claude Code Tooling]] | team |
| NV-20 | Go-live checklist steps 1–9 done? | [[Go-Live Checklist]] | owner |

## Resolved during the audit

| Question | Answer | Source |
|---|---|---|
| Does activity history include reviews? | No — bookings and reports only | `activity_history_screen.dart` |
| Does the partial unique report index run on SQLite? | Yes, unguarded; SQLite supports partial indexes | migration `2026_09_21_000001` |
| Are `target notifications` / `schedule announcements` enforced? | Yes — `NotificationController@store` / `@recipients` | controller |
| Does the migration `link_users_to_roles` roll back cleanly? | Lossy: restores `user_type` as customer/provider only | migration `down()` |
| Do tests cover provider suspend/activate? | Yes (`AdminDecisionNotificationTest`); remove-verification is not covered | tests |
| Can admins reset a customer's password? | No endpoint exists (staff only via `/administrators/{id}/password`) | route list |

Related: [[Known Issues and Gaps]] · [[Vault Guide]]
