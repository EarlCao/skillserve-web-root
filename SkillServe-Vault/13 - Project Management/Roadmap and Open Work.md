---
type: plan
tags: [project-management, roadmap]
sources: [PENDING_FIXES.md, skill-serve-mobile-application/PENDING_FIXES.md, DEPLOYMENT.md]
---
# Roadmap and Open Work

Only work that is **recorded** in the repos or **found** by the audit. No new features are proposed
here.

## A. Owner actions before go-live (from PENDING_FIXES)

1. Render: paid backend instance + persistent disk; environment per DEPLOYMENT.md;
   `SEED_MODE=starter` on first deploy, then `admin-only`; follow the Go-live checklist.
2. Android signing: upload keystore + `android/key.properties`; back them up.
3. Google sign-in: Android OAuth client for `com.skillserve.mobile` with debug and release SHA-1.
4. Admin content: Terms, Privacy, Community Guidelines; review booking rules; add categories,
   badges and a support-staff role.
5. Evidence: run the smoke test (D2) on the deployed stack; fill both `TEST_PLAN.md` Result columns.

→ tracked in [[Go-Live Checklist]].

## B. Audit findings to schedule (from [[Known Issues and Gaps]])

| Priority | Items |
|---|---|
| Before UAT | KI-01 background token vs session timeout; KI-02 mobile password reset |
| Decide | KI-03 rejected-dispute outcome; KI-04 service reports from the app; KI-05 upload size limit |
| Cleanup | KI-06…KI-14 code/consistency; KI-15…KI-23 stale docs |

## C. Defense preparation

D1 traceability (done, needs results), D2 demo script and data, D3 talking points →
[[Defense Readiness]].

## D. Documentation upkeep

Keep this vault synchronized ([[Documentation Sync Procedure]]).

Related: [[Project Status]] · [[Change Management Index]]
