---
type: feature
platform: admin-web
status: implemented
tags: [feature, admin-web]
sources:
  - backend/app/Modules/Notifications/Listeners/NotifyAdministrators.php
  - backend/app/Modules/Notifications/Services/AdminAlertService.php
  - backend/app/Modules/Notifications/Notifications/AdminAlertNotification.php
  - backend/app/Modules/Notifications/Controllers/AdminInboxController.php
  - frontend/src/modules/inbox
---
# Admin Inbox

What users do in the app that waits for an administrator arrives as an alert: a bell in the top bar
(unread count + the six latest) and the **Inbox** page (`/admin/inbox`, All / Unread, mark read, mark
all read). Opening an alert marks it read and goes to the page that handles it. Alerts arrive live
(`.admin.notification.created`, with a toast) and the list also refetches when the socket is down.

Not the same as [[Notifications and Announcements]], which sends announcements *to app users*.

| | |
|---|---|
| Backend | `App\Modules\Notifications` — `AdminAlertNotification` (database channel, type `admin_alert`), `AdminAlertService`, listener `NotifyAdministrators`, `BroadcastAdminNotification` |
| Frontend | `frontend/src/modules/inbox` (`InboxBell`, `InboxPage`, `AlertItem`) |
| Admin route | `/admin/inbox` — every administrator (no permission needed: each sees only their own alerts) |
| Endpoints | [[API - Admin Inbox]] (gate `use admin inbox` = `User::isAdministrator()`; app accounts get 403) |
| Storage | the existing Laravel `notifications` table — no migration |

## What raises an alert, and who gets it

Recipients are active administrators who pass the ability that the target page's list endpoint
checks — so an alert never points at a page its reader cannot open. The person who caused it is
never alerted, and alerts are sent after the surrounding transaction commits (`DB::afterCommit`); a
failure is logged and never fails the user's action.

| Kind | Event | Recipients (ability) | Opens |
|---|---|---|---|
| `provider_verification` | `ProviderVerificationSubmitted` (new request or requested info) | `viewAny` ProviderProfile → `view providers` | `/admin/providers/{id}` |
| `identity_verification` | `IdentityVerificationSubmitted` | `viewAny` IdentityVerification | `/admin/identity-verifications` |
| `service_review` | `ServiceCreated` / `ServiceUpdated` by a provider, when the service is `pending` approval | `viewAny` Service → `view services` | `/admin/services` |
| `report` | `ReportSubmitted` (new; `ClientReportService::create`) | `viewAny` Report → `view reports` | `/admin/reports` |
| `dispute` | `BookingStatusChanged` → `disputed` (raised by a party); `BookingDisputeEvidenceAdded` (new) | `viewDisputes` → `view bookings` | `/admin/disputes` |
| `support_ticket` | `SupportTicketCreated` (new); `SupportTicketResponseAdded` by the requester — **only the assignee** when the ticket is assigned | `viewAny` SupportTicket → `view support` | `/admin/support` |
| `commission_payment` | `CommissionRemittanceFlagged` (new): a QR payment PayMongo reported with the wrong amount, or paid after it was rejected | `view commissions` | `/admin/commissions?tab=payments` |

`manage …` permissions and `super-admin` pass these checks too.

## Tests

`AdminInboxTest` (recipient scoping per kind, assignee-only replies, live push, inbox endpoints,
another admin's alert → 404, app account → 403) — see [[Backend Test Suite]].

## Notes

- An alert stays unread for the other administrators after one of them handles the item; the
  sidebar count badges (`/api/dashboard/attention`) remain the measure of what is still waiting.

Related: [[Admin Web Features Index]] · [[Realtime Channels and Events]] · [[Notifications and Announcements]]
