---
type: feature
platform: admin-web
status: implemented
module_number: 18
tags: [feature, admin-web]
---
# Data Management

Admin requirement module **18** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/DataManagement`  |
| Frontend module | `frontend/src/modules/dataManagement` |
| Admin route(s) | `/admin/data-management` |
| Endpoints | [[API - Data Management]] |
| Permissions | `export system data`, `archive records`, `restore archived records`, `manage deleted records`, `restore deleted records` (list archives: `manage data` or `restore archived records`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 18.1 | Export System Data | `GET …/export?type=users|providers|services|bookings|reviews|activity` → CSV |
| A 18.2 | Archive Records | `POST …/archives` (services only) |
| A 18.3 | Restore Archived Records | `POST …/archives/{id}/restore` |
| A 18.4 | Manage Deleted Records | `GET …/deleted`, restore, permanent delete (refused with dependents), auto-purge after 30 days |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`DataManagementTest`, `ReviewRemovalTest` — see [[Backend Test Suite]].

## Notes

- The SPA downloads CSV exports with the raw axios instance.

## Related

[[Data Retention and Deletion]] · [[data_archives]] · [[Admin Web Features Index]]
