---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Mobile Security

Mobile requirement(s): **M16** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `route guards`, `/security-activity` |
| Code (Flutter `lib/`) | `core/services/token_storage.dart`<br>`core/services/api_client.dart`<br>`routes/app_router.dart`<br>`features/notifications/views/security_notifications_screen.dart` |
| Endpoints | [[API - Client Authentication]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 16.1 | Secure Authentication | tokens in flutter_secure_storage (Keystore/Keychain); rate-limited auth endpoints | implemented |
| M 16.2 | Session Expiration Handling | refused refresh → session cleared → login | implemented |
| M 16.3 | Unauthorized Access Protection | `redirectFor` guards + API middleware; background token cannot read anything but its feed | implemented |
| M 16.4 | Security Notifications | `/security-activity` shows **on-device** session events (signed in, signed out by server, credential handling) derived from `AuthController`; server-side security events reach the user as account notifications | implemented (device-local) |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`session_roles_payments_test`, `security_preferences_test`, `ClientAuthenticationTest`, `ClientAuthRateLimitTest`, `BackgroundNotificationTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Token and Session Management]] · [[Mobile App Architecture]] · [[Client Mobile Features Index]]
