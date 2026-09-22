---
type: feature
platform: client-mobile
status: implemented
tags: [feature, mobile]
---
# Client Favorites

Mobile requirement(s): **(extra)** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/favorites`, `favorite toggle on provider rows/profile` |
| Code (Flutter `lib/`) | `features/marketplace/ (controllers/favorites_controller.dart, services/favorites_service.dart, views/favorites_screen.dart, favorite_toggle.dart)` |
| Endpoints | [[API - Client Favorites]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Save providers | server-side favorites: `GET /favorites`, idempotent `PUT/DELETE /favorites/{provider}`; included in data export | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`favorites_test`, `FavoriteProviderTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Not a PDF requirement; added 2026-09-21 (moved from local storage to the server).

## Related

[[favorite_providers]] · [[Client Mobile Features Index]]
