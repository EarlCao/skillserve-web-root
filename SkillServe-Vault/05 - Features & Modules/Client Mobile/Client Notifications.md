---
type: feature
platform: client-mobile, provider-mobile
status: implemented
tags: [feature, mobile]
---
# Client Notifications

Mobile requirement(s): **M8** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/notifications`, `in-app banners`, `Android system notifications` |
| Code (Flutter `lib/`) | `features/notifications/ (controllers/notification_controller.dart, services/notification_service.dart, views/notification_poller.dart, notifications_screen.dart)`<br>`core/services/background_notifications.dart` |
| Endpoints | [[API - Client Notifications]] |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| M 8.1 | View Notifications | feed with category filters, mark read / read all, tap-through | implemented |
| M 8.2 | Receive Booking Notifications | realtime + 30 s polling + WorkManager when closed | implemented |
| M 8.3 | Receive Service Notifications | service moderation notifications | implemented |
| M 8.4 | View Announcements | announcement category | implemented |
| M 8.5 | Targeted Notifications | admin targeting all/customers/providers/selected | implemented |
| M 8.6 | Notification History | paginated feed | implemented |

UAT result columns in the mobile `TEST_PLAN.md` are still empty — see [[UAT and Traceability]].

## Tests

`notifications_reviews_test`, `presence_background_test`, `ClientCommunicationTest`, `BackgroundNotificationTest`, `NotificationsTest` (Flutter tests in snake_case, backend tests in PascalCase — [[Mobile Test Suite]], [[Backend Test Suite]]).

## Notes

> [!bug] KI-01
> Closed-app notifications stop after `session_timeout_minutes` because the background token is subject to the admin session timeout. See [[Known Issues and Gaps]].

## Related

[[Notifications Catalog]] · [[ADR-006 Closed-App Notifications via WorkManager]] · [[Client Mobile Features Index]]
