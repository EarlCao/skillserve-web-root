---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Reports

Mobile requirement(s): **M5.7, M6.4, M7.5** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/file-report`, `/my-reports`, report sheet on reviews, messages, service details and the provider profile |
| Code (Flutter `lib/`) | `features/reports/ (controllers/report_controller.dart, services/report_service.dart, views/*)` |
| Endpoints | [[API - Client Reports]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | File and follow reports | against the other party of a booking, a review or a received message; status + outcome visible, notes hidden | implemented |
| — | Report a service | flag icon and **Report this service** button on Service Details (`service_id`); reasons: misleading, spam, inappropriate, safety, other | implemented |
| — | Photos as proof | up to 5 (camera or gallery) on the Report an Issue screen and the report sheet; shown in My Reports | implemented |
| — | Report a provider | flag icon and **Report this provider** button on the provider profile (`provider_id`), no booking needed; the report is about the provider's account (`reportable_type` User), so moderators can warn, suspend or ban; reasons exclude booking-only ones (no-show, service quality, payment) | implemented |

Customers only: guests have no account, and a provider cannot report themself (422) or a provider the
public cannot see (404). One open report per subject (409).

In *My Reports* a reported provider is named as the marketplace names them (business name, else
account name — `ClientReportResource::personName`), so filing a report never reveals the personal
name behind a business. Customers and message senders keep their account name.

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`reports_support_test`, `ClientReportTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Reports and Moderation Lifecycle]] · [[Client Mobile Features Index]]
