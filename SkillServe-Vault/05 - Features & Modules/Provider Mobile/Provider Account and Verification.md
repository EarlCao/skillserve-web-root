---
type: feature
platform: provider-mobile
status: implemented
tags: [feature, mobile]
---
# Provider Account and Verification

Mobile requirement(s): **M9.2–9.6** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/provider (dashboard)`, `provider Settings`, `/verification-status`, `/provider-badges` |
| Code (Flutter `lib/`) | `features/provider/ (controllers/verification_controller.dart, services/verification_service.dart, provider_service_service.dart, views/verification_status_screen.dart, verification_upload_panel.dart, badges_screen.dart, settings_screen.dart)` |
| Endpoints | [[API - Provider Account (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 9.2 | Manage Provider Profile | `GET/PATCH /provider/profile` (skills, experience, bio…) | implemented |
| M 9.3 | Submit Verification | upload panel: camera, gallery, PDF; 1–5 docs, progress | implemented |
| M 9.4 | View Verification Status | pending / verified / rejected / additional info required + reviewer reason | implemented |
| M 9.5 | Respond to Information Request | re-upload reopens the same request | implemented |
| M 9.6 | Provider Account Restrictions | suspension/verification changes shown + notified | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`verification_test`, `provider_account_test`, `account_status_test`, `ProviderVerificationTest`, `ProviderAccountTest`, `AccountStatusTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Provider Verification Lifecycle]] · [[Provider Portfolio and Badges]] · [[Provider Mobile Features Index]]
