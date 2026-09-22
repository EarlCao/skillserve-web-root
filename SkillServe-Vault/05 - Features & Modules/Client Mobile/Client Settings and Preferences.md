---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Settings and Preferences

Mobile requirement(s): **M14** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/notification-preferences`, `/privacy-settings`, `/application-preferences`, `/terms`, `/privacy`, `/community-guidelines`, `/help-center`, `/about`, `/contact` |
| Code (Flutter `lib/`) | `features/settings/ (controllers/preferences_controller.dart, services/preferences_service.dart, platform_service.dart, views/*)`<br>`features/notifications/views/preferences_screens.dart` |
| Endpoints | [[API - Client Preferences and Platform]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 14.1 | Notification Preferences | booking / service / message / announcement toggles (server-side; muted categories are not stored) | implemented |
| M 14.2 | Privacy Settings | private profile (hides provider from discovery), activity personalization | implemented |
| M 14.3 | Application Preferences | theme light/dark/system, reduce motion | implemented |
| M 14.4 | View Platform Policies | terms, privacy, community guidelines from `/platform`; bundled fallback offline | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`preferences_controller_test`, `security_preferences_test`, `platform_test`, `ClientPreferencesTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[client_preferences]] · [[System Settings Catalog]] · [[Client Mobile Features Index]]
