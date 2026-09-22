---
type: feature
platform: admin-web
status: implemented
module_number: 17
tags: [feature, admin-web]
---
# System Settings

Admin requirement module **17** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Settings`  |
| Frontend module | `frontend/src/modules/settings` |
| Admin route(s) | `/admin/settings` |
| Endpoints | [[API - System Settings]] |
| Permissions | `manage settings` |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 17.1 | General Settings | platform name, description, support email; timezone read-only |
| A 17.2 | Marketplace Settings | provider registration, service approval, featured services, commission — all enforced |
| A 17.3 | Booking Settings | booking pause, cancellation window, client/provider fee % |
| A 17.4 | Notification Settings | email, push, announcement switches |
| A 17.5 | Platform Policies | terms, privacy, community guidelines → shown in the app via `/platform` |
| A 17.6 | System Settings | maintenance mode (mobile 503), session timeout, default page size |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`SettingsTest`, `SettingsEnforcementTest`, `AuthenticationTest` — see [[Backend Test Suite]].

## Notes

- Full key list: [[System Settings Catalog]].

## Related

[[settings]] · [[Admin Web Features Index]]
