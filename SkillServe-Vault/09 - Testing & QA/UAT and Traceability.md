---
type: reference
tags: [testing, uat, traceability, requirements]
sources: [TEST_PLAN.md, skill-serve-mobile-application/TEST_PLAN.md]
---
# UAT and Traceability

Two traceability matrices exist in the repos (created 2026-09-21, PENDING_FIXES D1/M6):

| Document | Rows | Columns |
|---|---|---|
| web root `TEST_PLAN.md` | A 1.1 … A 19.1 + cross-cutting checks (security headers, CORS, rate limiting, health, realtime) | ID · Requirement · Page · API · Tests · UAT → expected · **Result** |
| mobile `TEST_PLAN.md` | M 1.1 … M 17.1 | ID · Requirement · Screen · API · Tests · UAT → expected · **Result** |

**How to use (from the plans):** run the automated checks and record totals/date; walk every UAT row
on the **deployed** system (admin rows as `admin@skillserve.test`); fill *Result* with Pass/Fail +
date (+ defect id). A requirement is done when its automated tests pass **and** its UAT row passes.

## State at audit

- All *Result* cells and both "Run date" tables are **empty** → no recorded UAT evidence yet.
- Rows expected to **fail** today based on this audit:
  - **M 1.4** "reset link email works" — the link targets `APP_URL/client/reset-password`, which does
    not exist (KI-02).
  - Closed-app notification rows (M 8.2 with the app closed for longer than the session timeout)
    — KI-01.
- **M 15.2** is intentionally marked "—" (design decision).

## Where each feature note shows coverage

Every feature note in `05 - Features & Modules` has a *Requirement coverage* table and the test
classes that cover it: [[Admin Web Features Index]], [[Client Mobile Features Index]],
[[Provider Mobile Features Index]]. Summary: [[Module Completion Matrix]].

Related: [[Defense Readiness]] · [[Go-Live Checklist]]
