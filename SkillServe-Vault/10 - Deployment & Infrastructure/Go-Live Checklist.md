---
type: guide
tags: [deployment, go-live, project-management]
sources: [DEPLOYMENT.md, PENDING_FIXES.md, skill-serve-mobile-application/PENDING_FIXES.md]
---
# Go-Live Checklist

From `DEPLOYMENT.md` → "Go-live checklist" and the owner actions in both `PENDING_FIXES.md` files.
Status unknown at audit time (these are dashboard/owner actions) — record date and result as each is
done.

| # | Step | Status |
|---|---|---|
| 1 | Backend service on a **paid** Render instance with the persistent disk at `/var/www/html/storage/app`; full environment incl. `APP_KEY`, `APP_URL`, `FRONTEND_URL`, Neon `DB_*`, `REVERB_*`, `BUSINESS_TIMEZONE`, Brevo mail, `GOOGLE_CLIENT_ID`, `SEED_MODE=starter`, strong admin passwords; Swagger off | Needs Verification |
| 2 | Deploy and verify: migrations + seeding in the log; `/api/health` database + storage `up`; `/api/client/v1/platform` answers | Needs Verification |
| 3 | Frontend static site: `VITE_*` vars (Reverb key = backend key), `/* → /index.html` rewrite, security headers; add its URL to `FRONTEND_URLS` if new | Needs Verification |
| 4 | Sign in as super-admin: Settings → General (name, support email), Platform policies (terms, privacy, community guidelines), Marketplace/Booking (commission, cancellation window & fees), System (session timeout ≈480, maintenance **off**); review starter categories; create badges; create staff accounts and a support role | Needs Verification |
| 5 | After first deploy switch `SEED_MODE` to `admin-only` | Needs Verification |
| 6 | Android signing: upload keystore + `android/key.properties` (backed up) | Needs Verification |
| 7 | Google sign-in: Android OAuth client for `com.skillserve.mobile` with debug + release SHA-1 | Needs Verification |
| 8 | Release APK built against production and checked on a clean phone | Needs Verification |
| 9 | End-to-end smoke test with two phones: register customer + provider → provider verification upload → admin approves → provider adds service → admin approves → customer books → provider accepts → chat → reschedule → start → complete → payment received → review → report → admin moderates → notifications on both phones incl. app closed; record in both `TEST_PLAN.md` files | Needs Verification |

> [!warning] Known blockers found by this audit
> Step 9 "notifications with the app closed" can fail after the session timeout (KI-01); the mobile
> password-reset UAT will fail (KI-02). See [[Known Issues and Gaps]].

Related: [[Release Workflow]] · [[Defense Readiness]] · [[Project Status]]
