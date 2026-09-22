---
type: feature
platform: provider-mobile
status: implemented
tags: [feature, mobile]
---
# Provider Onboarding and Registration

Mobile requirement(s): **M9.1** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/register (provider role)`, `/verify-email`, `/provider-onboarding` |
| Code (Flutter `lib/`) | `features/auth/views/widgets/provider_details_fields.dart`<br>`features/provider/views/provider_onboarding_screen.dart` |
| Endpoints | [[API - Client Authentication]], [[API - Provider Account (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 9.1 | Become a Service Provider | `POST /auth/register-provider` (business name, specialization, experience, bio) → OTP → provider profile `unverified`; onboarding: 1 profile · 2 upload documents · 3 status seal | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`provider_account_test`, `ClientProviderRegistrationTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Provider sign-up can be closed by System Settings → provider registration.

## Related

[[Registration and OTP Flow]] · [[Provider Account and Verification]] · [[Provider Mobile Features Index]]
