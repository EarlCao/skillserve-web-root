---
type: feature
platform: provider-mobile
status: implemented
tags: [feature, mobile]
---
# Provider Portfolio and Badges

Mobile requirement(s): **M9.2, M4.6** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/portfolio`, `/upload-portfolio`, `/provider-badges` |
| Code (Flutter `lib/`) | `features/provider/ (controllers/portfolio_controller.dart, services/portfolio_service.dart, views/portfolio_screen.dart, upload_portfolio_screen.dart, badges_screen.dart)` |
| Endpoints | [[API - Provider Account (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Portfolio | `GET/POST /provider/portfolio` (image ≤5 MB + title/description), `DELETE …/{item}` | implemented |
| — | Badges | `GET /provider/badges` — admin-assigned recognition | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`provider_account_test`, `ProviderAccountTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[provider_portfolio_items]] · [[Provider Recognition]] · [[Provider Mobile Features Index]]
