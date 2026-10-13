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
| M 13.1 | Global Search | one box over services, categories and providers (by name too) — see below | implemented |
| M 13.2 | Search Suggestions | from categories and live results | implemented |
| M 13.3 | Recent Searches | stored **on device** (SharedPreferences), clearable — no API | implemented |
| M 13.4 | Featured Providers | `GET /providers?featured=1` rail | implemented |
| M 13.5 | Top-Rated Providers | rail sorted by rating | implemented |

## How a search matches

The same `search` parameter drives `GET /services` and `GET /providers`
(`ClientCatalogService::searchTerms`). The text is split into words (at most 8); **every** word has
to match somewhere, case-insensitively and anywhere inside a field — "electro" finds
"Electronics", "electronics cebu" finds an electronics service in Cebu. `%`, `_` and `!` typed by
the customer are matched literally (escaped with `!`).

| Searching | A word may match |
|---|---|
| Services | title, description, location; category name; subcategory name; the provider's business name, specialization, bio, location, skills or **account name** |
| Providers | business name, specialization, bio, location, skills, **account name**; or the title, description, category or subcategory of one of their public services |

So "electronics" lists every Electronics service *and* the providers who offer one, and a
provider who registered without a business name is found by their own name. Hidden or unapproved
services never make a provider match.

Results update live: when a provider publishes or edits a service, the search on screen re-runs
silently ([[Realtime Architecture]]).

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`discovery_test`, `ClientMarketplaceTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Service and Provider Discovery]] · [[Client Mobile Features Index]]
