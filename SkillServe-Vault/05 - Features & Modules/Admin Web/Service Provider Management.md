---
type: feature
platform: admin-web
status: implemented
module_number: 4
tags: [feature, admin-web]
---
# Service Provider Management

Admin requirement module **4** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Providers`  |
| Frontend module | `frontend/src/modules/providers` |
| Admin route(s) | `/admin/providers`, `/admin/providers/:providerId` |
| Endpoints | [[API - Providers]] |
| Permissions | `view providers`, `verify providers`, `reject providers`, `suspend providers`, `activate providers` (or `manage providers`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 4.1 | View Service Providers | `GET /api/providers` (business name, verification status, rating…) |
| A 4.2 | View Provider Profile | `GET /api/providers/{id}` — skills, experience, portfolio, services, ratings, bookings |
| A 4.3 | Review Verification Request | documents streamed via `…/verification-documents/{doc}/download` (blob → new tab); `verification-history` |
| A 4.4 | Approve Verification | `PATCH …/verification/approve` → verified |
| A 4.5 | Reject Verification | `PATCH …/verification/reject` with reason |
| A 4.6 | Request Additional Information | `PATCH …/verification/request-info`; provider re-uploads, same request back to pending |
| A 4.7 | Suspend Service Provider | `PATCH …/suspend` / `…/activate` (hidden from marketplace) |
| A 4.8 | Remove Provider Verification | `PATCH …/verification/remove` → unverified |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`ProviderSecurityTest`, `ProviderVerificationTest`, `AdminDecisionNotificationTest` — see [[Backend Test Suite]].

## Notes

- `LogProviderActivity` previously called a nonexistent method (every decision 500'd) — fixed 2026-09-21 (PENDING_FIXES C1).

## Related

[[Provider Verification Lifecycle]] · [[provider_profiles]] · [[Admin Web Features Index]]
