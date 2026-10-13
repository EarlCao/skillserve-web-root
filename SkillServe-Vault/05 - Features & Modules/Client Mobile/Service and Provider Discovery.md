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
| M 3.2 | Search Services | `search` — every word, across title, description, location, category, subcategory and provider ([[Search and Personalized Discovery]]) | implemented |
| M 3.3 | Filter Services | filter sheet: category, subcategory, min rating, availability | implemented |
| M 3.4 | View Service Details | price in ₱ (or "On quote"), category and area, **Offered by** tile → provider profile, Book button, **Report this service** | implemented |
| M 3.5 | View Featured Services | home rail (suppressed when featured services disabled) | implemented |
| M 3.6 | View Service Categories | enabled categories + subcategories | implemented |
| M 4.1 | Browse Service Providers | verified, active, public providers | implemented |
| M 4.2 | Search Service Providers | display name (business or account name), specialization, bio, location, skills, and their public services' titles and categories | implemented |
| M 4.3 | Filter Service Providers | category, rating, featured, available, weekday | implemented |
| M 4.4 | View Provider Profile | photo, name, category, area; rating, jobs, years; verification; about, skills, recognition, hours; services (tap → details, Book); portfolio thumbnails → gallery; reviews; Message, favorite, **Report this provider** | implemented |
| M 4.5 | View Provider Verification Status | `VerificationSeal` | implemented |
| M 4.6 | View Provider Recognition | badges, featured, top-rated | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`discovery_test`, `marketplace_models_test`, `ClientMarketplaceTest`, `ProviderRecognitionTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- **Display name**: the API's `display_name` is the business name, or the account holder's name
  when the provider registered without one (`ProviderProfile::displayName()`); `profile_photo_url`
  is their account photo. Before this, a provider without a business name showed as a blank and
  could not be found by name.
- **Home** (`/client`) lists, under the category chips: Featured Pros, **Latest services** (the 8
  newest published services in the selected category — a newly published service appears here),
  and Available providers. Each list loads on its own, so one failed request no longer blanks Home.
- **Live**: Home, Explore, the provider profile and service details refetch silently when the
  catalog changes ([[Realtime Architecture]] → marketplace channel).
- Tapping a provider's name on any service card opens their profile.

- Visibility rules: [[Marketplace Visibility Rules]]. Providers are redirected away from the marketplace except `/provider-preview/:id` and `/reviews/:providerId`.

## Related

[[Search and Personalized Discovery]] · [[Client Favorites]] · [[Client Mobile Features Index]]
