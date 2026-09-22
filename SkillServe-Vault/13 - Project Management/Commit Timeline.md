---
type: history
tags: [project-management, history, git]
sources: [git log of root, backend, frontend, mobile repos]
---
# Commit Timeline

Derived from `git log` of the four repos (dates are commit dates).

```mermaid
gantt
  dateFormat YYYY-MM-DD
  title SkillServe development (commit activity)
  section Backend
  Initial + infra, auth, admins, users, bans      :2026-07-26, 2026-08-07
  Service categories                              :2026-08-12, 1d
  Granular permissions, providers, services, bookings :2026-08-19, 2026-08-20
  Reviews → audit, recognition, analytics (bulk add commits) :2026-09-03, 2026-09-05
  Settings, data mgmt, support, client API        :2026-09-08, 2026-09-09
  Registration, OTP, Brevo, cancel-registration   :2026-09-11, 2026-09-13
  Role-based accounts, realtime push, discovery   :2026-09-17, 2026-09-20
  Verification upload, account status, settings enforcement :2026-09-21, 1d
  section Frontend
  Scaffold, auth, admins, users                   :2026-07-28, 2026-08-07
  Categories, permissions, providers, services    :2026-08-12, 2026-08-20
  Remaining modules                               :2026-09-03, 2026-09-09
  Live updates, moderation-only services, fees    :2026-09-17, 2026-09-21
  section Mobile
  UI prototype + redesigns (mock data)            :2026-07-29, 2026-08-07
  API integration (no more mockup data)         :2026-09-10, 2026-09-13
  Realtime, role accounts, discovery              :2026-09-17, 2026-09-20
  Verification, status, maintenance, release      :2026-09-21, 1d
  section Root docs
  README, AGENT.md, PDFs, api-docs, scripts       :2026-08-07, 2026-09-21
```

## Milestone commits

| Date | Repo | Commit |
|---|---|---|
| 2026-07-26 | backend | Initial Commit; "change into mysql database" (later PostgreSQL) |
| 2026-08-07 | backend | PostgreSQL + Dockerfile; API infrastructure; authentication; administrators; users; bans |
| 2026-08-07 | frontend | Tailwind/daisyUI; routing; auth; role & permission management; user management |
| 2026-08-12 | both | service category management |
| 2026-08-20 | both | provider management; services |
| 2026-09-05 | both | bulk module work (reviews, reports, disputes, notifications, dashboard, analytics, recognition, audit) — terse "add"/"fix" messages |
| 2026-09-08 | both | `feat/system-settings`, `feat/data-management` |
| 2026-09-11 | mobile | "switch to api and connect to backend no more mockup data" |
| 2026-09-12 | backend | registration, SMTP, Brevo API transport, CORS for Vercel |
| 2026-09-17 | all | role-based accounts, provider services, realtime push, live admin updates |
| 2026-09-20 | backend/mobile | discovery filters, provider availability, global search |
| 2026-09-21 | all | verification upload, account status, decision notifications, enforced settings, release setup; docs: go-live checklist |

Totals at audit: root 29, backend 79, frontend 56, mobile 33 commits.

Related: [[Changelog]] · [[Team and Ownership]]
