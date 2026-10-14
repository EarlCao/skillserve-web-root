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
| A 14.5 | Respond to Support Ticket | a chat in the request dialog (`SupportChat`): the user's messages on the left, staff on the right, Enter to send, up to 5 photos (`POST …/responses`, JSON or multipart `images[]`) → user notified and the app's open thread updates live; new user replies arrive through the live admin updates |
| A 14.6 | Assign Support Ticket | `PATCH …/assign` to an active administrator (`GET …/assignees`) |
| A 14.7 | Resolve Support Ticket | `PATCH …/resolve` → user notified |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`SupportTicketManagementTest`, `ProviderSupportTicketTest` — see [[Backend Test Suite]].

## Notes

- Module was entirely missing in the 2026-09-08 readiness audit; added 2026-09-08.
- **Photos from the requester** show as thumbnails under the request and under each reply that
  carried them (`PrivatePhotos`); click one for full size.

- **Named *Customer Support*** in both apps since 2026-10-14 (sidebar, page, dialog, permission area, app
  screens and notifications). Routes, tables and permission names keep `support ticket`.
- New requests and the user's replies also raise [[Admin Inbox]] alerts (a reply on an assigned
  request alerts only its assignee).

## Related

[[Support Ticket Lifecycle]] · [[support_tickets]] · [[Admin Web Features Index]]

## Sidebar count badge

The sidebar shows how many support tickets still `open` (nobody has replied) next to this page, from `GET /api/dashboard/attention`
(null when the viewer may not open the list). It lives under the `dashboard` query key, so every
realtime change refetches it: a ticket or report filed in the app shows up at once. A closed
sidebar group shows the total of its items; the collapsed icon rail shows a dot.
