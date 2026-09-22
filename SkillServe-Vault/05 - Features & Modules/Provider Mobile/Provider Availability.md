---
type: feature
platform: provider-mobile
status: implemented
tags: [feature, mobile]
---
# Provider Availability

Mobile requirement(s): **M10.6** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/availability`, `/calendar` |
| Code (Flutter `lib/`) | `features/provider/views/availability_screen.dart`<br>`features/provider/views/calendar_screen.dart`<br>`features/provider/models/provider_availability_model.dart` |
| Endpoints | [[API - Provider Account (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 10.6 | Manage Service Availability | `GET/PUT /provider/availability`: weekly hours (one window per weekday, Manila time) + "taking new bookings"; calendar shows booking density per day | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`provider_account_test`, `ProviderAccountTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Empty schedule = no published hours = bookings unrestricted by time.

## Related

[[provider_availabilities]] · [[Time and Timezone Rules]] · [[Provider Mobile Features Index]]
