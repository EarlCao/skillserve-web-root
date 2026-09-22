---
type: feature
platform: client-mobile
status: implemented
tags: [feature, mobile]
---
# Client Reviews

Mobile requirement(s): **M6** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/write-review/:bookingId`, `/my-reviews`, `/reviews/:providerId` |
| Code (Flutter `lib/`) | `features/reviews/ (controllers/review_controller.dart, services/review_service.dart, views/*)` |
| Endpoints | [[API - Client Reviews]], [[API - Client Reports]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 6.1 | Submit Review | completed bookings only, once | implemented |
| M 6.2 | Submit Rating | 1–5 | implemented |
| M 6.3 | View Reviews | provider's published reviews | implemented |
| M 6.4 | Report Review | review card → Report (`POST /reports {review_id}`) | implemented |
| M 6.5 | View My Reviews | own reviews with moderation state; editable | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`notifications_reviews_test`, `reports_support_test`, `ClientMarketplaceTest`, `ClientReportTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Reviews and Ratings Rules]] · [[Client Mobile Features Index]]
