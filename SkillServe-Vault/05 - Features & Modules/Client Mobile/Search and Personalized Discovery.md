---
type: feature
platform: client-mobile
status: implemented
tags: [feature, mobile]
---
# Search and Personalized Discovery

Mobile requirement(s): **M13** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/search (Explore)` |
| Code (Flutter `lib/`) | `features/marketplace/views/search_screen.dart`<br>`features/marketplace/services/recent_searches_service.dart` |
| Endpoints | [[API - Client Catalog]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 13.1 | Global Search | one box over services and providers | implemented |
| M 13.2 | Search Suggestions | from categories and live results | implemented |
| M 13.3 | Recent Searches | stored **on device** (SharedPreferences), clearable — no API | implemented |
| M 13.4 | Featured Providers | `GET /providers?featured=1` rail | implemented |
| M 13.5 | Top-Rated Providers | rail sorted by rating | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`discovery_test`, `ClientMarketplaceTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Service and Provider Discovery]] · [[Client Mobile Features Index]]
