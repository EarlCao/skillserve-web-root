---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Support

Mobile requirement(s): **M12** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/support/tickets`, `/support/new`, `/support/tickets/:ticketId`, `/help-center` |
| Code (Flutter `lib/`) | `features/support/ (controllers/support_controller.dart, services/support_service.dart, views/*)` |
| Endpoints | [[API - Client Support]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 12.1 | Create Support Ticket | subject, description, category, up to 5 photos | implemented |
| M 12.2 | View My Support Tickets | own tickets | implemented |
| M 12.3 | View Ticket Details | thread with staff | implemented |
| M 12.4 | Reply to Support Ticket | text and/or up to 5 photos; refused once resolved | implemented |
| M 12.5 | View Ticket Status | open / in_progress / resolved (no separate *assigned* status) | implemented |

Shown to users as **Customer Support** (Settings tile, screen titles, *Contact support*), a chat with
the team: staff replies can carry photos too, and the thread updates live. Notifications read
*Customer Support replied* / *Customer Support resolved your request*.

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`reports_support_test`, `ClientCommunicationTest`, `ProviderSupportTicketTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Related

[[Support Ticket Lifecycle]] · [[Client Mobile Features Index]]
