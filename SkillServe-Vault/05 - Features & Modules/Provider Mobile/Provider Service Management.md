---
type: feature
platform: provider-mobile
status: implemented
tags: [feature, mobile]
---
# Provider Service Management

Mobile requirement(s): **M10.1–10.5** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/my-services`, `/add-service`, `/edit-service/:id` |
| Code (Flutter `lib/`) | `features/provider/ (controllers/provider_services_controller.dart, services/provider_service_service.dart, views/my_services_screen.dart, add_service_screen.dart, edit_service_screen.dart, service_form.dart)` |
| Endpoints | [[API - Provider Services (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 10.1 | Create Service | verified providers only | implemented |
| M 10.2 | View My Services | with approval status filter | implemented |
| M 10.3 | Edit Service | snapshot-field edits return to review when approval is required | implemented |
| M 10.4 | Submit Service for Review | implicit on create/edit | implemented |
| M 10.5 | View Service Approval Status | pending / approved / rejected / hidden | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`provider_services_test`, `ProviderServiceTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Service Approval Lifecycle]] · [[Provider Mobile Features Index]]
