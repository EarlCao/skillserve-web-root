---
type: feature
platform: admin-web
status: implemented
module_number: 6
tags: [feature, admin-web]
---
# Service Category Management

Admin requirement module **6** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/ServiceCategories`  |
| Frontend module | `frontend/src/modules/serviceCategories` |
| Admin route(s) | `/admin/service-categories` |
| Endpoints | [[API - Service Categories]] |
| Permissions | `view|create|edit|delete service categories` (or `manage service categories`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 6.1 | View Service Categories | paginated list with search, status filter, sort (name, created_at) |
| A 6.2 | Add Service Category | `POST /api/service-categories` (unique name) |
| A 6.3 | Edit Service Category | `PUT /api/service-categories/{id}` |
| A 6.4 | Delete Service Category | `DELETE` soft delete — blocked while it has subcategories |
| A 6.5 | Manage Subcategories | nested `POST/PUT/DELETE …/subcategories` inside the details modal (unique per category) |
| A 6.6 | Enable or Disable Category | `PATCH …/status` enabled/disabled → disappears from the app |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`ServiceCategoryManagementTest` — see [[Backend Test Suite]].

## Notes

- Starter seed (`ServiceCategorySeeder`): 8 categories, 25 subcategories.
- Audit log names `service_categories`, `service_subcategories`.

## Related

[[service_categories]] · [[service_subcategories]] · [[Admin Web Features Index]]
