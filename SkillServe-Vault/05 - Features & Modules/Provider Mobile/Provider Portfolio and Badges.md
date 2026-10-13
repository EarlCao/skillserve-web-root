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
| Screens / routes | `/portfolio`, `/upload-portfolio`, `/edit-portfolio/:itemId`, `/my-portfolio/:itemId`; customer `/portfolio-gallery/:providerId`, `/portfolio-item/:providerId/:itemId`; `/provider-badges` |
| Code (Flutter `lib/`) | `features/provider/ (controllers/portfolio_controller.dart, services/portfolio_service.dart, views/portfolio_screen.dart, upload_portfolio_screen.dart, badges_screen.dart)` |
| Endpoints | [[API - Provider Account (Mobile)]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Portfolio | a piece of work = title, optional description, **1–10 photos** (first = cover). `GET/POST /provider/portfolio` (`images[]`, ≤5 MB each; legacy single `image` still accepted), `PATCH …/{item}` (text), `POST …/{item}/images`, `DELETE …/{item}/images/{image}` (never the last), `DELETE …/{item}` | implemented |
| — | Delete several | the Portfolio app bar's trash button selects pieces of work (tick boxes) and deletes them after one confirmation; adding is the floating *Add work* button only | implemented |
| — | Portfolio details | one screen for both roles (`PortfolioItemScreen`): swipeable photos with full-screen zoom, title, date, description; the provider gets Edit/Delete, the customer a link to the provider. Cards (`PortfolioCard`) look the same on Portfolio, the customer gallery and the profile. Customer screens are live (marketplace channel) | implemented |
| — | Badges | `GET /provider/badges` — admin-assigned recognition | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`provider_account_test`, `ProviderAccountTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[provider_portfolio_items]] · [[Provider Recognition]] · [[Provider Mobile Features Index]]
