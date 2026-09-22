---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Profile

Mobile requirement(s): **M2** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `Profile tab`, `/edit-profile`, `/change-password`, `/activity-history` |
| Code (Flutter `lib/`) | `features/profile/ (services/profile_service.dart, views/edit_profile_screen.dart, account_status_card.dart)`<br>`features/settings/views/activity_history_screen.dart` |
| Endpoints | [[API - Client Authentication]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 2.1 | View Profile | `GET /auth/me` | implemented |
| M 2.2 | Edit Profile | `PATCH /auth/me` | implemented |
| M 2.3 | Profile Photo Management | `POST/DELETE /auth/me/photo` (JPG/PNG/WebP ≤5 MB, `public` disk) | implemented |
| M 2.4 | View Account Status | account status card in Settings/Profile from `/auth/me` `account` | implemented |
| M 2.5 | View Activity History | `/activity-history` combines the user's bookings (customer or provider list) and reports (no reviews) | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`user_account_profile_test`, `account_status_test`, `security_preferences_test`, `ClientProfileTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- TEST_PLAN M 2.5 expects bookings, reviews and reports; `activity_history_screen.dart` loads only bookings and reports — reviews are not shown there (they are on `/my-reviews`).

## Related

[[Client Data and Account Control]] · [[Client Mobile Features Index]]
