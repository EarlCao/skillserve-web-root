---
type: feature
platform: client-mobile (guests too)
status: implemented
tags: [feature, mobile]
---
# Service and Provider Discovery

Mobile requirement(s): **M3, M4** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/client (home)`, `/browse`, `/categories`, `/service-details/:id`, `/provider-profile/:id`, `/provider-preview/:id`, `/portfolio-gallery/:id`, `/reviews/:providerId` |
| Code (Flutter `lib/`) | `features/marketplace/ (controllers/marketplace_controller.dart, discovery_controller.dart, services/service_service.dart, views/*)` |
| Endpoints | [[API - Client Catalog]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 3.1 | Browse Services | only approved, visible services of verified providers | implemented |
| M 3.2 | Search Services | `search` | implemented |
| M 3.3 | Filter Services | filter sheet: category, subcategory, min rating, availability | implemented |
| M 3.4 | View Service Details | price in ₱, provider, ratings, Book button | implemented |
| M 3.5 | View Featured Services | home rail (suppressed when featured services disabled) | implemented |
| M 3.6 | View Service Categories | enabled categories + subcategories | implemented |
| M 4.1 | Browse Service Providers | verified, active, public providers | implemented |
| M 4.2 | Search Service Providers | name, skills, services | implemented |
| M 4.3 | Filter Service Providers | category, rating, featured, available, weekday | implemented |
| M 4.4 | View Provider Profile | skills, experience, portfolio, services, ratings, badges, hours | implemented |
| M 4.5 | View Provider Verification Status | `VerificationSeal` | implemented |
| M 4.6 | View Provider Recognition | badges, featured, top-rated | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`discovery_test`, `marketplace_models_test`, `ClientMarketplaceTest`, `ProviderRecognitionTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Visibility rules: [[Marketplace Visibility Rules]]. Providers are redirected away from the marketplace except `/provider-preview/:id` and `/reviews/:providerId`.

## Related

[[Search and Personalized Discovery]] · [[Client Favorites]] · [[Client Mobile Features Index]]
