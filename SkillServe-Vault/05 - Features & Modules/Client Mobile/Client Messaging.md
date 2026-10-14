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
| M 7.2 | Send Message | optimistic send with retry, `Idempotency-Key`; photos from camera or gallery with an optional caption (multipart `image`) | implemented |
| M 7.3 | Receive Messages | realtime `client.message.created`; presence ("in this chat") and typing on `presence-booking-chat.{id}` | implemented |
| M 7.4 | Message History | `GET /bookings/{id}/messages`; `POST …/messages/read` | implemented |
| M 7.5 | Report Message | long-press → Report message (`message_id`) | implemented |
| — | Copy and paste | long-press any message with text → **Copy text** (clipboard); paste into the message box from its own long-press menu | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`messaging_test`, `chat_realtime_test`, `presence_background_test`, `reports_support_test`, `ConversationTest`, `ClientCommunicationTest`, `ClientReportTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

- **Provider profile from the chat (customers):** tapping the provider's photo or name in the chat
  header, the person icon in its top bar, or the provider's photo in the Messages list opens
  `/provider-profile/:id`. The inbox's `counterpart.provider_id` (customer's view only) carries the
  profile id; providers see no link (customers have no public profile). A chat opened from a
  notification or a booking before the inbox loaded fetches the inbox, so the header always has the
  participant.

- **Photos:** private; the app loads them through the API client with the user's token
  (`core/widgets/misc/private_image.dart`, small in-memory cache) and opens them full screen with
  zoom. A failed photo send keeps the local file so Retry re-uploads it.

- Messaging exists only inside a booking: you cannot message a provider before booking.

## Related

[[Realtime Channels and Events]] · [[messages]] · [[Client Mobile Features Index]]
