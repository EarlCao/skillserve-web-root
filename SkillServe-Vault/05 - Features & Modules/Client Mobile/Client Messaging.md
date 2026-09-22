---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Messaging

Mobile requirement(s): **M7** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `Messages tab (chat list)`, `/chat-conversation/:bookingId` |
| Code (Flutter `lib/`) | `features/messaging/ (controllers/chat_controller.dart, services/message_service.dart, views/*)`<br>`core/services/realtime_client.dart` |
| Endpoints | [[API - Client Messaging]], [[API - Client Reports]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 7.1 | View Conversations | one thread per booking (`GET /conversations`), unread counts | implemented |
| M 7.2 | Send Message | optimistic send with retry, `Idempotency-Key` | implemented |
| M 7.3 | Receive Messages | realtime `client.message.created`; presence ("in this chat") and typing on `presence-booking-chat.{id}` | implemented |
| M 7.4 | Message History | `GET /bookings/{id}/messages`; `POST …/messages/read` | implemented |
| M 7.5 | Report Message | long-press → Report (`message_id`) | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`messaging_test`, `chat_realtime_test`, `presence_background_test`, `reports_support_test`, `ConversationTest`, `ClientCommunicationTest`, `ClientReportTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- Messaging exists only inside a booking: you cannot message a provider before booking.

## Related

[[Realtime Channels and Events]] · [[messages]] · [[Client Mobile Features Index]]
