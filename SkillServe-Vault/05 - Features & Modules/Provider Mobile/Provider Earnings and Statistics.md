---
type: feature
platform: provider-mobile
status: implemented
tags: [feature, mobile]
---
# Provider Earnings and Statistics

Mobile requirement(s): **(extra)** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/earnings`, `/statistics`, `/provider (dashboard)` |
| Code (Flutter `lib/`) | `features/provider/views/earnings_screen.dart`<br>`statistics_screen.dart`<br>`dashboard_screen.dart` |
| Endpoints | [[API - Provider Bookings (Mobile)]], [[API - Provider Account (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Earnings | derived client-side from the provider's bookings (price, platform fee, paid status) — no balance/payout | implemented |
| — | Statistics | completed-jobs trend and rating breakdown from services/profile data | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`provider_account_test` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- No backend earnings endpoint exists; figures are computed in the app.

## Related

[[Payments and Refunds]] · [[Provider Mobile Features Index]]
