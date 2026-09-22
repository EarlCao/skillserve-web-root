---
type: reference
tags: [api, frontend, mapping]
sources: [frontend/src/modules/*/api/*.js]
---
# Frontend-to-API Map

Extracted from every `frontend/src/modules/*/api/*Api.js` (paths relative to `/api`).

| Admin page (route) | API module file | Endpoints called |
|---|---|---|
| Login / Forgot / Reset (`/login`, `/forgot-password`, `/reset-password`), Change password | `authentication/api/authApi.js` | `POST /auth/login`, `/auth/logout`, `GET /auth/me`, `POST /auth/change-password`, `/auth/forgot-password`, `/auth/reset-password` |
| Dashboard (`/admin`) | `dashboard/api/dashboardApi.js` | `GET /dashboard` |
| Administrators (`/admin/administrators`, tabs roles/permissions) | `administrators/api/{administratorApi,roleApi,permissionApi}.js` | `GET/POST /administrators`, `PUT /administrators/{id}`, `PATCH …/status`, `PATCH …/password`; `GET/POST /roles`, `PUT/DELETE /roles/{id}`, `PUT /roles/{id}/permissions`; `GET /permissions` |
| Users (`/admin/users`, `/admin/users/:userId`) | `users/api/userApi.js` | `GET /users`, `GET/PUT/DELETE /users/{id}`, `PATCH …/suspend`, `/activate`, `/ban`, `/unban`, `GET …/moderation-history` |
| Service Categories | `serviceCategories/api/serviceCategoryApi.js` | `GET/POST /service-categories`, `GET/PUT/DELETE /service-categories/{id}`, `PATCH …/status`, `POST/PUT/DELETE …/subcategories[/{sub}]` |
| Providers (`/admin/providers`, `/:providerId`) | `providers/api/providerApi.js` | `GET /providers`, `GET /providers/{id}`, `PATCH …/verification/approve|reject|request-info|remove`, `GET …/verification-history`, `GET …/verification-documents/{doc}/download` (blob), `PATCH …/suspend`, `/activate` |
| Services | `services/api/serviceApi.js` | `GET /services`, `GET/PUT/DELETE /services/{id}`, `PATCH …/approve`, `/reject`, `/hide`, `/feature` |
| Bookings | `bookings/api/bookingApi.js` | `GET /bookings`, `GET /bookings/{id}`, `GET …/history`, `PATCH …/cancel`, `/mark-paid`, `/refund`, `/dispute` |
| Disputes | `disputes/api/disputeApi.js` | `GET /disputes`, `GET /disputes/{id}`, `GET …/history`, `PATCH …/investigate|notes|resolve|reject|close`, evidence via `download_path` (blob) |
| Reviews | `reviews/api/reviewApi.js` | `GET /reviews`, `GET /reviews/{id}`, `PATCH …/hide`, `DELETE /reviews/{id}` |
| Reports | `reports/api/reportApi.js` | `GET /reports`, `GET /reports/reasons`, `GET /reports/{id}`, `PATCH …/investigate|notes|resolve|reject|action` |
| Notifications | `notifications/api/notificationApi.js` | `GET /notifications`, `GET /notifications/recipients`, `POST /notifications/announcements`, `DELETE /notifications/announcements/{id}` |
| Provider Recognition | `providerRecognition/api/providerRecognitionApi.js` | `GET/POST /provider-recognition/badges`, `PUT/DELETE …/badges/{id}`, `GET …/providers`, `GET …/top-rated`, `POST/DELETE …/providers/{p}/badges[/{b}]`, `PATCH …/providers/{p}/featured` |
| Analytics | `analytics/api/analyticsApi.js` | `GET /analytics/reports`, `GET /analytics/reports/export` (blob, **raw axios**) |
| Audit Logs | `audit/api/auditApi.js` | `GET /audit-logs`, `GET /audit-logs/administrators` |
| Settings | `settings/api/settingsApi.js` | `GET /settings`, `PUT /settings` |
| Data Management | `dataManagement/api/dataManagementApi.js` | `GET/POST /data-management/archives`, `POST …/archives/{id}/restore`, `GET …/deleted`, `POST …/deleted/{type}/{id}/restore`, `DELETE …/deleted/{type}/{id}`, `GET …/export` (blob, **raw axios**) |
| Support | `support/api/supportTicketApi.js` | `GET /support/tickets`, `GET …/{id}`, `GET …/assignees`, `PATCH …/assign`, `POST …/responses`, `PATCH …/resolve` |
| (global) | `services/echo.js` | `POST /broadcasting/auth` (Echo) |

## Admin endpoints with no direct caller in the SPA

Checked by matching every admin route against the path strings in `frontend/src` (audit script):

| Endpoint | Why it is not called |
|---|---|
| `GET /administrators/{id}`, `GET /roles/{id}` | no caller found (the pages appear to use list data for details — inference, not verified) |
| `PATCH` aliases of `/administrators/{id}`, `/roles/{id}`, `/users/{id}`, `/services/{id}`, `/service-categories/{id}`, `…/subcategories/{sub}` | the SPA uses `PUT` |
| `GET /disputes/{booking}/evidence/{evidence}` | called indirectly through each evidence item's `download_path` |

Every other admin route has a caller.

Related: [[Admin Web Frontend Architecture]] · [[Endpoints Index]]
