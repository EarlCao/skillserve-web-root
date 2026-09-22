---
type: feature
platform: admin-web
status: implemented
module_number: 12
tags: [feature, admin-web]
---
# Provider Recognition

Admin requirement module **12** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/ProviderRecognition`  |
| Frontend module | `frontend/src/modules/providerRecognition` |
| Admin route(s) | `/admin/provider-recognition` |
| Endpoints | [[API - Provider Recognition]] |
| Permissions | `view provider recognition`, `manage provider badges`, `assign provider badges`, `manage featured providers`, `view top rated providers` |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 12.1 | Manage Provider Badges | CRUD `/api/provider-recognition/badges` |
| A 12.2 | Assign Provider Badge | `POST …/providers/{p}/badges` → shown on the app profile |
| A 12.3 | Remove Provider Badge | `DELETE …/providers/{p}/badges/{b}` |
| A 12.4 | Manage Featured Providers | `PATCH …/providers/{p}/featured` |
| A 12.5 | Manage Top-Rated Providers | `GET …/top-rated` |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`ProviderRecognitionTest` — see [[Backend Test Suite]].

## Notes

- Changes fire `ProviderRecognitionChanged` → audit log.

## Related

[[provider_badges]] · [[provider_badge_assignments]] · [[Admin Web Features Index]]
