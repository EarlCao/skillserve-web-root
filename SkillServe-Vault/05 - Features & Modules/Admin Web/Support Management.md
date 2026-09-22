---
type: feature
platform: admin-web
status: implemented
module_number: 14
tags: [feature, admin-web]
---
# Support Management

Admin requirement module **14** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Support`  |
| Frontend module | `frontend/src/modules/support` |
| Admin route(s) | `/admin/support` |
| Endpoints | [[API - Support Tickets (Admin)]] |
| Permissions | `view support`, `assign support tickets`, `respond to support tickets`, `resolve support tickets` (or `manage support`) |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 14.1 | View Support Tickets | `GET /api/support/tickets` |
| A 14.2 | Search Support Tickets | ticket number, user, subject |
| A 14.3 | Filter Support Tickets | category, status, priority, assignee |
| A 14.4 | View Ticket Details | concern, replies, history |
| A 14.5 | Respond to Support Ticket | `POST …/responses` → user notified in app |
| A 14.6 | Assign Support Ticket | `PATCH …/assign` to an active administrator (`GET …/assignees`) |
| A 14.7 | Resolve Support Ticket | `PATCH …/resolve` → user notified |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`SupportTicketManagementTest`, `ProviderSupportTicketTest` — see [[Backend Test Suite]].

## Notes

- Module was entirely missing in the 2026-09-08 readiness audit; added 2026-09-08.

## Related

[[Support Ticket Lifecycle]] · [[support_tickets]] · [[Admin Web Features Index]]
