---
type: feature
platform: admin-web
status: implemented
module_number: 11
tags: [feature, admin-web]
---
# Notifications and Announcements

Admin requirement module **11** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Notifications`  |
| Frontend module | `frontend/src/modules/notifications` |
| Admin route(s) | `/admin/notifications` |
| Endpoints | [[API - Notifications and Announcements]] |
| Permissions | `view notifications` (list); `send announcements` (create/delete); `schedule announcements` when `scheduled_at` is set; `target notifications` when target ≠ `all` and for `GET /recipients` |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 11.1 | View Notifications | `GET /api/notifications` (announcement history; filters status/target) |
| A 11.2 | Send Announcement | `POST /api/notifications/announcements` → `SendAnnouncementJob` |
| A 11.3 | Target Notifications | target all / customers / providers / selected; `GET …/recipients` searches selectable users |
| A 11.4 | Schedule Announcement | `scheduled_at` → delayed job |
| A 11.5 | View Notification History | list includes past and scheduled; scheduled/pending can be deleted |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`NotificationsTest`, `AnnouncementsMigrationTest`, `SettingsEnforcementTest` — see [[Backend Test Suite]].

## Notes

- Blocked entirely when System Settings → announcement notifications is off.
- Delivery is a delayed queued job — a queue worker must be running (see [[Background Jobs and Scheduling]]).

## Related

[[Notifications Catalog]] · [[announcements]] · [[Admin Web Features Index]]
