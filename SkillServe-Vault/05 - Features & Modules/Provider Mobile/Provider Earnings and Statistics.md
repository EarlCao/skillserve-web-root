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
| Code (Flutter `lib/`) | `features/provider/views/earnings_screen.dart`<br>`statistics_screen.dart` (+ `controllers/statistics_controller.dart`, `models/provider_statistics_model.dart`)<br>`dashboard_screen.dart` |
| Endpoints | [[API - Provider Bookings (Mobile)]], [[API - Provider Account (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Earnings | derived client-side from the provider's bookings (price, platform fee, paid status) — no balance/payout | implemented |
| — | Statistics | `GET /client/v1/provider/statistics` (since 2026-10-13): this month's earnings; rating, completion rate, completed bookings, reviews; monthly chart of completed bookings or earnings over 3/6/12 months ending with the **current month in Asia/Manila**; bookings by status (tap through to the lists); star breakdown; top services. Live: refetched when the provider's bookings change, when a review lands (marketplace channel) and every 60 s | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`provider_account_test` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Earnings on the Earnings screen are computed in the app from the bookings; Statistics reads the
  same definition (total price − SkillServe's fee, completed bookings) from the API.
- Until 2026-10-13 the Statistics screen showed **hard-coded** numbers (a Feb–Jul chart and fixed
  rating percentages) — the reason its months were wrong. `ProviderStatisticsService` replaced them;
  test `ProviderStatisticsTest` (incl. a UTC/Manila month boundary).

## Related

[[Payments and Refunds]] · [[Provider Mobile Features Index]]
