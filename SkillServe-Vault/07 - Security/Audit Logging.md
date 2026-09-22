---
type: guide
tags: [security, audit]
sources: [backend/app/Modules/*/Listeners/Log*Activity.php, backend/app/Modules/Audit, backend/config/activitylog.php]
---
# Audit Logging

All audit entries go to the spatie `activity_log` table through `Log…Activity` listeners registered
in `AppServiceProvider`.

| Log name | Written by | Examples |
|---|---|---|
| `authentication` | `LogAuthenticationActivity` | `administrator_logged_in`, `administrator_logged_out`, `administrator_login_failed`, password changed (with IP, user agent) |
| `administrators`, `roles` | `LogAdministratorActivity` | admin created/updated/status/password (`administrators`); role created/updated/deleted/permissions synced (`roles`) |
| `users` | `LogUserActivity` | user updated/suspended/activated/banned/unbanned/deleted/warned, `user_self_deleted` |
| `service_categories`, `service_subcategories` | `LogServiceCategoryActivity` | category/subcategory CRUD, status |
| `provider` | `LogProviderActivity` | verification submitted/approved/rejected/info requested/removed, suspended/activated |
| `provider_recognition` | `LogProviderRecognitionActivity` | badge CRUD, assign/remove, featured |
| `services` | `LogServiceActivity` | created/updated/approved/rejected/hidden/featured/deleted |
| `bookings` | `LogBookingActivity` | `booking_status_changed`, `booking_cancelled`, dispute actions, reschedules, payments |
| `reviews` | `LogReviewActivity` | hidden/restored/removed |
| `reports` | `LogReportActivity` | investigated, note added, resolved, rejected, action taken |
| `support` | `LogSupportTicketActivity` | `support_ticket_assigned`, `support_ticket_response_added`, `support_ticket_resolved` |
| `system_settings` | Settings service | settings updated |
| `data_management` | Data Management service | data-management actions (archive, restore, delete…) |

## Reading the log

- Admin → Security & Audit (`GET /api/audit-logs`): search, filter by administrator/module/action/
  date; `view=login` (login/logout/failed) and `view=security` (authentication + administrators
  logs).
- Booking and dispute history, user moderation history and provider verification history are also
  read from `activity_log`.
- Indexed for these queries (`created_at`, causer+date, description+date, log_name+subject+date).

Related: [[Security and Audit Logs]] · [[activity_log]]
