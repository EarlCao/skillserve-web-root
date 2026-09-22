---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Logout (Mobile)

Mobile requirement(s): **M17** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `Settings → Sign out (customer and provider)` |
| Code (Flutter `lib/`) | `features/auth/controllers/auth_controller.dart` |
| Endpoints | [[API - Client Authentication]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 17.1 | User Logout | confirm → `POST /auth/logout` (revokes all tokens incl. refresh and background) → tokens cleared → realtime closed → WorkManager task cancelled → auth screen | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`session_roles_payments_test`, `ClientAuthenticationTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Client Authentication and Account]] · [[Client Mobile Features Index]]
