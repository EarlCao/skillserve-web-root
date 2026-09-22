---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Data and Account Control

Mobile requirement(s): **M15** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/account-data`, `/account-deletion`, `login & Settings restriction info` |
| Code (Flutter `lib/`) | `features/profile/ (services/account_data_service.dart, views/account_data_screen.dart, account_deletion_screen.dart)` |
| Endpoints | [[API - Client Authentication]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 15.1 | View Account Data | `GET /auth/me/data-export` (copied to clipboard as JSON) | implemented |
| M 15.2 | Request Account Deactivation | **not implemented by design** — active or deleted only ([[ADR-009 No Account Deactivation]]) | deliberately omitted |
| M 15.3 | Request Account Deletion | `DELETE /auth/me` with password; refused with open bookings; soft delete restorable by admin | implemented |
| M 15.4 | Account Status and Restriction Information | reason, since, until shown | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`security_preferences_test`, `account_status_test`, `AccountDataTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Data Retention and Deletion]] · [[Client Mobile Features Index]]
