---
type: feature
platform: client-mobile, provider-mobile
status: partial
tags: [feature, mobile]
---
# Client Authentication and Account

Mobile requirement(s): **M1** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/splash`, `/onboarding`, `/welcome`, `/login`, `/register`, `/google-register`, `/verify-email`, `/forgot-password` |
| Code (Flutter `lib/`) | `features/auth/ (controllers/auth_controller.dart, services/auth_service.dart, views/*)`<br>`core/services/api_client.dart`<br>`core/services/token_storage.dart` |
| Endpoints | [[API - Client Authentication]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 1.1 | User Registration | customer or provider sign-up → 6-digit email OTP → account created on verify; Google sign-in / Google registration; cancel pending sign-up | implemented |
| M 1.2 | User Login | email/password or Google; lands on `/client` or `/provider` by role | implemented |
| M 1.3 | User Logout | see [[Logout (Mobile)]] | implemented |
| M 1.4 | Password Management | change password implemented; **forgot password only sends the email — the reset link targets a page that does not exist and the app has no reset screen (KI-02)** | partial |
| M 1.5 | Session Management | 60-min access token auto-refreshed from a rotating refresh token; signed in until sign-out | implemented |
| M 1.6 | Account Status Display | suspended/banned → session ended, login screen shows reason and end date (`AccountRestrictionCard`) | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`auth_form_locking_test`, `google_registration_screen_test`, `session_roles_payments_test`, `account_status_test`, `ClientAuthenticationTest`, `ClientEmailOtpTest`, `ClientGoogleAuthTest`, `CancelRegistrationTest`, `ClientAuthRateLimitTest`, `AccountStatusTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Unverified users are held on `/verify-email` by the router.

## Related

[[Registration and OTP Flow]] · [[Authentication Flows]] · [[Mobile Security]] · [[Client Mobile Features Index]]
