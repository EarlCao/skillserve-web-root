---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Authentication and Account

Mobile requirement(s): **M1** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/splash`, `/onboarding`, `/welcome`, `/login`, `/register`, `/google-register`, `/verify-email`, `/create-password`, `/forgot-password` |
| Code (Flutter `lib/`) | `features/auth/ (controllers/auth_controller.dart, services/auth_service.dart, views/*)`<br>`core/services/api_client.dart`<br>`core/services/token_storage.dart` |
| Endpoints | [[API - Client Authentication]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 1.1 | User Registration | starts by scanning the National ID front and back, which fills names, birthday, card number and the Region → Barangay address ([[Mobile Sign-up with National ID Scan]]); customer or provider sign-up (email, or Google) → 6-digit email OTP → password + confirmation → account created, ID submitted for review; the Google path takes the same code and password steps; cancel pending sign-up ([[Registration and OTP Flow]]) | implemented |
| M 1.2 | User Login | email + password, or Google **+ the account password** (a prompt after the Google picker); lands on `/client` or `/provider` by role | implemented |
| M 1.3 | User Logout | see [[Logout (Mobile)]] | implemented |
| M 1.4 | Password Management | change password; forgot password in the app: email → 6-digit code → new password + confirmation (KI-02 fixed 2026-10-03) | implemented |
| M 1.5 | Session Management | 60-min access token auto-refreshed from a rotating refresh token; signed in until sign-out | implemented |
| M 1.6 | Account Status Display | suspended/banned → session ended, login screen shows reason and end date (`AccountRestrictionCard`) | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`auth_form_locking_test`, `google_registration_screen_test`, `sign_up_password_step_test`, `session_roles_payments_test`, `account_status_test`, `ClientAuthenticationTest`, `ClientEmailOtpTest`, `ClientGoogleAuthTest`, `SignUpPasswordStepTest`, `CancelRegistrationTest`, `ClientAuthRateLimitTest`, `AccountStatusTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- The router holds a sign-up on `/verify-email` until the code is confirmed, then on `/create-password` until the password is set.

## Related

[[Registration and OTP Flow]] · [[Authentication Flows]] · [[Mobile Security]] · [[Client Mobile Features Index]]
