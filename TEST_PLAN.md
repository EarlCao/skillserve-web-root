# SkillServe Test Plan — Admin Web and API

User acceptance test (UAT) plan and requirements traceability matrix for the admin web
(`SkillServe_Admin_Web_Functionalities.pdf`). The mobile app has its own plan in the Flutter repo's
`TEST_PLAN.md`. Open defects are tracked in `PENDING_FIXES.md`; a row that depends on one says
so (for example "Open: C3").

## How to use this document

1. Run the automated checks (below) and record the totals and date.
2. Walk through every UAT row on the **deployed** system, signed in as `admin@skillserve.test`
   (super-admin) unless the row says otherwise, and fill in **Result** (Pass / Fail + date, and the
   defect ID if it fails).
3. A requirement is done when its automated tests pass **and** its UAT row passes.

## Automated checks

| Suite | Command (from the repo root) | Covers |
|-------|------------------------------|--------|
| Backend feature tests | `docker compose exec backend composer test` | Every API module: validation, authorization, state rules, notifications, audit logging (in-memory SQLite) |
| Backend code style | `docker compose exec backend ./vendor/bin/pint --test` | PSR-12 / Laravel style |
| Admin web lint | `cd frontend && npm run lint` | ESLint, React hooks rules |
| Admin web build | `cd frontend && npm run build` | Compiles every page; no chunk over 500 kB |
| Dependency audit | `docker compose exec backend composer audit`, `cd frontend && npm audit` | Known vulnerabilities (Open: H3) |

The admin web has no component-test framework; its behaviour is verified by the UAT rows below
together with the backend tests of the endpoints each page calls.

| Run date | Backend tests | Pint | Lint | Build | Audit |
|----------|---------------|------|------|-------|-------|
| | | | | | |

## Design decisions to defend

- **No account deactivation (A 15.4 applies to administrators only; mobile M 15.2).** Mobile
  accounts are either active or deleted. Self-service deletion is a *soft* delete: the account
  disappears from the platform at once, an administrator can restore it from Data Management,
  and it is purged after 30 days only if nothing references it. A separate "deactivated" state
  would duplicate that without adding a user-visible benefit, so the requirement is met by
  deletion + restore. Administrators, by contrast, *can* be activated/deactivated (A 15.4),
  because staff access must be revocable without losing their audit trail.
- **Payments are recorded, not processed.** Customers pay providers off-platform (cash, GCash…).
  The provider confirms "Payment received"; admins can mark bookings paid and record refunds;
  every change is audited. No card data ever touches SkillServe.
- **Realtime without Firebase.** Laravel Reverb (WebSockets) delivers admin dashboard updates and
  mobile notifications instantly; closed-app mobile notifications use a periodic background check
  with a read-only token.
- **Uploads on a Render persistent disk**, not a third-party bucket; private files (verification
  documents, dispute evidence) are only ever streamed to authorized admins.
- **Monolith + separate mobile client.** One Laravel API serves both the admin web
  (`/api/*`, Sanctum admin tokens) and the app (`/api/client/v1/*`, rotating refresh tokens).

## Traceability matrix — Admin Web

Columns: **Page** in the admin web · **API** endpoints · **Tests** (backend feature test classes) ·
**UAT** steps → expected result.

### 1. Admin Authentication

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 1.1 | Admin login | `/login` | `POST /auth/login` | AuthenticationTest | Valid credentials → dashboard; wrong password → "Invalid email or password"; 6 fast attempts → rate-limited | |
| A 1.2 | Admin logout | Header → Sign out | `POST /auth/logout` | AuthenticationTest | Sign out → login page; old token rejected (reload stays logged out) | |
| A 1.3 | Role-based access control | All pages | Spatie permissions on every route | AuthenticationTest, UserRolesTest, RoleManagementTest | Sign in as `system@skillserve.test` → only permitted menu items; opening a forbidden URL shows "not authorized" | |
| A 1.4 | Password management | `/admin/change-password`, `/forgot-password`, `/reset-password` | `POST /auth/change-password`, `/auth/forgot-password`, `/auth/reset-password` | AuthenticationTest, AdminPasswordResetTest | Change password → other sessions end; "Forgot password?" → email link → new password works, old one does not | |
| A 1.5 | Session management | — | token expiry = Settings → System → Session timeout | AuthenticationTest | Set timeout to 5 min, wait → next action returns to login | |

### 2. Admin Dashboard

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 2.1 | User summary | `/admin` | `GET /dashboard` | DashboardTest | Counts of clients, providers, active, suspended match the Users page | |
| A 2.2 | Service summary | `/admin` | `GET /dashboard` | DashboardTest | Total / approved / pending / reported match the Services page | |
| A 2.3 | Booking summary | `/admin` | `GET /dashboard` | DashboardTest | Counts per status match the Bookings filters | |
| A 2.4 | Verification summary | `/admin` | `GET /dashboard` | DashboardTest | Pending / approved / rejected match the Providers page | |
| A 2.5 | Reports summary | `/admin` | `GET /dashboard` | DashboardTest | Pending / investigating / resolved / rejected match the Reports page | |
| A 2.6 | Recent activities | `/admin` | `GET /dashboard` | DashboardTest, RealtimeAdminUpdatesTest | Suspend a user in another tab → activity appears without reload | |
| A 2.7 | Platform analytics | `/admin` | `GET /dashboard` | DashboardTest | Charts render with data; empty ranges show an empty state | |

### 3. User Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 3.1 | View all users | `/admin/users` | `GET /users` | UserManagementTest | Paginated list with name, email, type, status | |
| A 3.2 | Search users | `/admin/users` | `GET /users?search=` | UserManagementTest | Search by name, email and ID each find the user | |
| A 3.3 | Filter users | `/admin/users` | `GET /users?type=&status=` | UserManagementTest | Type / status / verification filters narrow the list | |
| A 3.4 | View user profile | `/admin/users/:id` | `GET /users/{id}`, `/users/{id}/moderation-history` | UserManagementTest | Profile shows details, services, bookings, ratings, activity | |
| A 3.5 | Edit user information | `/admin/users/:id` | `PATCH /users/{id}` | UserManagementTest | Edit phone → saved, audit log entry | |
| A 3.6 | Suspend user | `/admin/users` | `PATCH /users/{id}/suspend` | UserManagementTest | Suspend with reason → user cannot use the app (Open: C4, H1 for the user-facing notice) | |
| A 3.7 | Activate user | `/admin/users` | `PATCH /users/{id}/activate` | UserManagementTest | Activate → user can sign in again | |
| A 3.8 | Ban user | `/admin/users` | `PATCH /users/{id}/ban`, `/unban` | UserManagementTest | Ban (days / forever) → ban email sent; expired ban lifts automatically | |
| A 3.9 | Delete user | `/admin/users` | `DELETE /users/{id}` | UserManagementTest | Delete → gone from list, listed in Data Management → Deleted | |

### 4. Service Provider Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 4.1 | View providers | `/admin/providers` | `GET /providers` | ProviderSecurityTest | List with business name, verification status | |
| A 4.2 | View provider profile | `/admin/providers/:id` | `GET /providers/{id}` | ProviderSecurityTest | Skills, experience, portfolio, services, ratings, bookings shown | |
| A 4.3 | Review verification request | `/admin/providers/:id` | `GET /providers/{id}/verification-documents/{doc}/download` | ProviderSecurityTest | "View" opens the uploaded document (Open: C1 — providers cannot upload yet) | |
| A 4.4 | Approve verification | `/admin/providers/:id` | `PATCH /providers/{id}/verification/approve` | ProviderSecurityTest | Approve → provider verified, can create services | |
| A 4.5 | Reject verification | `/admin/providers/:id` | `PATCH …/verification/reject` | ProviderSecurityTest | Reject with reason → status rejected (Open: H1 notification) | |
| A 4.6 | Request additional info | `/admin/providers/:id` | `PATCH …/verification/request-info` | ProviderSecurityTest | Request info → status "info requested" (Open: C1, H1) | |
| A 4.7 | Suspend provider | `/admin/providers/:id` | `PATCH /providers/{id}/suspend`, `/activate` | ProviderSecurityTest | Suspend → provider hidden from marketplace | |
| A 4.8 | Remove verification | `/admin/providers/:id` | `PATCH …/verification/remove` | ProviderSecurityTest | Remove → provider unverified, services not bookable | |

### 5. Service Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 5.1 | View all services | `/admin/services` | `GET /services` | ServiceManagementTest | List of every provider's services | |
| A 5.2 | Search services | `/admin/services` | `GET /services?search=` | ServiceManagementTest | Search by title, provider, category | |
| A 5.3 | Filter services | `/admin/services` | `GET /services?category_id=&status=&approval_status=` | ServiceManagementTest | Filters narrow the list | |
| A 5.4 | Review submission | `/admin/services` | `GET /services/{id}` | ServiceManagementTest | Details modal shows every field | |
| A 5.5 | Approve service | `/admin/services` | `PATCH /services/{id}/approve` | ServiceManagementTest | Approve → visible in the app; provider notified | |
| A 5.6 | Reject service | `/admin/services` | `PATCH /services/{id}/reject` | ServiceManagementTest | Reject with reason → provider notified with the reason | |
| A 5.7 | Edit service | `/admin/services` | `PUT/PATCH /services/{id}` | ServiceManagementTest | Edit title → saved; provider notified of changed fields | |
| A 5.8 | Hide service | `/admin/services` | `PATCH /services/{id}/hide` | ServiceManagementTest | Hide → disappears from the app; unhide restores | |
| A 5.9 | Feature service | `/admin/services` | `PATCH /services/{id}/feature` | ServiceManagementTest | Feature → appears in the app's featured list | |
| A 5.10 | Delete service | `/admin/services` | `DELETE /services/{id}` | ServiceManagementTest | Delete → gone; restorable from Data Management | |

### 6. Service Category Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 6.1 | View categories | `/admin/service-categories` | `GET /service-categories` | ServiceCategoryManagementTest | Categories with subcategories | |
| A 6.2 | Add category | same | `POST /service-categories` | ServiceCategoryManagementTest | New category saved; duplicate name refused | |
| A 6.3 | Edit category | same | `PUT/PATCH /service-categories/{id}` | ServiceCategoryManagementTest | Rename saved | |
| A 6.4 | Delete category | same | `DELETE /service-categories/{id}` | ServiceCategoryManagementTest | Unused category deleted; one in use is refused | |
| A 6.5 | Manage subcategories | same | `POST/PUT/DELETE …/subcategories` | ServiceCategoryManagementTest | Add / edit / delete a subcategory | |
| A 6.6 | Enable / disable | same | `PATCH /service-categories/{id}/status` | ServiceCategoryManagementTest | Disable → category and its services disappear from the app | |

### 7. Booking Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 7.1 | View all bookings | `/admin/bookings` | `GET /bookings` | BookingListTest | List with client, provider, service | |
| A 7.2 | Booking details | `/admin/bookings` (modal) | `GET /bookings/{id}` | BookingPaymentTest | Details: client, provider, service, schedule, status, payment (Open: C2 for times) | |
| A 7.3 | Search bookings | `/admin/bookings` | `GET /bookings?search=` | BookingListTest | Search by booking number, client, provider, service | |
| A 7.4 | Filter bookings | `/admin/bookings` | `GET /bookings?status=&payment_status=&date_from=` | BookingListTest | Status, payment, dispute, date filters | |
| A 7.5 | Monitor status | `/admin/bookings` | same | ProviderBookingTest | A booking moves pending → confirmed → active → completed as the provider acts | |
| A 7.6 | Booking history | modal → Activity History | `GET /bookings/{id}/history` | BookingRescheduleTest, BookingPaymentTest | Every status change, reschedule and payment appears with actor and time | |
| A 7.7 | Cancel booking | `/admin/bookings` | `PATCH /bookings/{id}/cancel` | BookingCancellationTest | Cancel with reason → both parties notified | |
| A 7.8 | Manage disputes | `/admin/bookings`, `/admin/disputes` | `PATCH /bookings/{id}/dispute` | DisputeManagementTest | See module 10 | |
| — | Record payment / refund | modal → Mark as Paid / Record Refund | `PATCH /bookings/{id}/mark-paid`, `/refund` | BookingPaymentTest | Mark paid → both notified; partial then full refund; over-refund refused | |

### 8. Reviews and Ratings Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 8.1 | View reviews | `/admin/reviews` | `GET /reviews` | ReviewListTest | List with rating, reviewer, provider | |
| A 8.2 | Search reviews | `/admin/reviews` | `GET /reviews?search=` | ReviewListTest | Search by user, provider, service | |
| A 8.3 | Filter reviews | `/admin/reviews` | `GET /reviews?rating=&is_reported=&status=` | ReviewListTest | Rating, reported, status filters | |
| A 8.4 | Review reported feedback | `/admin/reviews` (Reported) | `GET /reviews?is_reported=1` | ClientReportTest, ReviewListTest | A review reported from the app appears under Reported | |
| A 8.5 | Hide review | `/admin/reviews` | `PATCH /reviews/{id}/hide` | ReviewRemovalTest | Hide → gone from the app; reviewer notified | |
| A 8.6 | Remove review | `/admin/reviews` | `DELETE /reviews/{id}` | ReviewRemovalTest | Remove → reviewer notified; restorable from Data Management | |
| A 8.7 | Restore review | `/admin/reviews` | `PATCH /reviews/{id}/hide` (is_hidden=false) | ReviewRemovalTest | Restore → visible again; reviewer and provider notified | |

### 9. Reports and Moderation

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 9.1–9.4 | View user / service / review / message reports | `/admin/reports` | `GET /reports?type=`, `GET /reports/reasons` | ReportsAndModerationTest, ClientReportTest | Each type filter lists reports filed from the app; reason filter lists every reason | |
| A 9.5 | Investigate | `/admin/reports` | `PATCH /reports/{id}/investigate` | ReportsAndModerationTest | Status → investigating, audit entry | |
| A 9.6 | Investigation notes | `/admin/reports` | `PATCH /reports/{id}/notes` | ReportsAndModerationTest | Note appended with author and time | |
| A 9.7 | Resolve | `/admin/reports` | `PATCH /reports/{id}/resolve` | ReportsAndModerationTest | Resolved with note (Open: H1 reporter notification) | |
| A 9.8 | Reject | `/admin/reports` | `PATCH /reports/{id}/reject` | ReportsAndModerationTest | Rejected with reason | |
| A 9.9 | Moderation action | `/admin/reports` | `PATCH /reports/{id}/action` | ReportsAndModerationTest | Warning / suspend / ban / hide / remove applied to the target (Open: C4 warning delivery) | |

### 10. Dispute Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 10.1 | View disputes | `/admin/disputes` | `GET /disputes` | DisputeManagementTest | Disputes raised from the app | |
| A 10.2 | Dispute details | `/admin/disputes` (modal) | `GET /disputes/{booking}` | DisputeManagementTest | Parties, booking, statement, evidence | |
| A 10.3 | Review evidence | modal → evidence | `GET /disputes/{booking}/evidence/{id}` | DisputeManagementTest, BookingDisputeTest | Photos uploaded from the app open | |
| A 10.4 | Dispute history | modal | `GET /disputes/{booking}/history` | DisputeManagementTest | Every action listed | |
| A 10.5 | Dispute notes | modal | `PATCH /disputes/{booking}/notes` | DisputeManagementTest | Internal note saved | |
| A 10.6 | Resolve | modal | `PATCH /disputes/{booking}/resolve`, `/reject` | DisputeManagementTest | Decision saved (Open: H1 notifications to both parties) | |
| A 10.7 | Close | modal | `PATCH /disputes/{booking}/close` | DisputeManagementTest | Resolved dispute closed | |

### 11. Notifications and Announcements

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 11.1 | View notifications | `/admin/notifications` | `GET /notifications` | NotificationsTest | Admin alerts listed | |
| A 11.2 | Send announcement | `/admin/notifications` | `POST /notifications/announcements` | NotificationsTest | Send → arrives on phones instantly | |
| A 11.3 | Target notifications | same | `GET /notifications/recipients` | NotificationsTest | All / clients / providers / selected users each reach only that group | |
| A 11.4 | Schedule announcement | same | `POST …/announcements` with `scheduled_at` | NotificationsTest | Schedule 2 min ahead → delivered at that time | |
| A 11.5 | Notification history | same | `GET /notifications` | NotificationsTest, AnnouncementsMigrationTest | Past and scheduled announcements listed; a scheduled one can be deleted | |

### 12. Provider Recognition

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 12.1 | Manage badges | `/admin/provider-recognition` | `GET/POST/PUT/DELETE /provider-recognition/badges` | ProviderRecognitionTest | Create / edit / delete a badge | |
| A 12.2 | Assign badge | same | `POST /provider-recognition/providers/{id}/badges` | ProviderRecognitionTest | Assigned badge shows on the provider's app profile | |
| A 12.3 | Remove badge | same | `DELETE …/badges/{badge}` | ProviderRecognitionTest | Badge disappears from the profile | |
| A 12.4 | Featured providers | same | `PATCH /provider-recognition/providers/{id}/featured` | ProviderRecognitionTest | Featured provider appears in the app's featured list | |
| A 12.5 | Top-rated providers | same | `GET /provider-recognition/top-rated` | ProviderRecognitionTest | Highest-rated providers listed | |

### 13. Reports and Analytics

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 13.1–13.6 | User / provider / service / booking / review / system activity reports | `/admin/analytics` | `GET /analytics/reports?type=` | AnalyticsTest | Each report type renders with filters and totals | |
| A 13.7 | Export reports | `/admin/analytics` | `GET /analytics/reports/export` | AnalyticsTest | Export downloads a file with the same rows | |

### 14. Support Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 14.1 | View tickets | `/admin/support` | `GET /support/tickets` | SupportTicketManagementTest | Tickets from customers and providers | |
| A 14.2 | Search tickets | same | `GET /support/tickets?search=` | SupportTicketManagementTest | Search by ticket number, user, subject | |
| A 14.3 | Filter tickets | same | `GET /support/tickets?category=&status=` | SupportTicketManagementTest | Category and status filters | |
| A 14.4 | Ticket details | same | `GET /support/tickets/{id}` | SupportTicketManagementTest | Concern, replies, history | |
| A 14.5 | Respond | same | `POST /support/tickets/{id}/responses` | SupportTicketManagementTest, ProviderSupportTicketTest | Reply → user notified in the app | |
| A 14.6 | Assign | same | `PATCH /support/tickets/{id}/assign`, `GET …/assignees` | SupportTicketManagementTest | Assign to staff → shown as assigned | |
| A 14.7 | Resolve | same | `PATCH /support/tickets/{id}/resolve` | SupportTicketManagementTest | Resolve → user notified | |

### 15. Admin Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 15.1 | View administrators | `/admin/administrators` | `GET /administrators` | AdministratorManagementTest | Admin list | |
| A 15.2 | Add administrator | same | `POST /administrators` | AdministratorManagementTest | New admin can sign in with the given role | |
| A 15.3 | Edit administrator | same | `PUT/PATCH /administrators/{id}` | AdministratorManagementTest | Changes saved | |
| A 15.4 | Activate / deactivate | same | `PATCH /administrators/{id}/status` | AdministratorManagementTest | Deactivated admin cannot sign in | |
| A 15.5 | Manage roles | `?tab=roles` | `GET/POST/PUT/DELETE /roles` | RoleManagementTest | Create / edit / delete a role | |
| A 15.6 | Manage permissions | `?tab=permissions` | `GET /permissions`, `PUT /roles/{id}/permissions` | RoleManagementTest, RolePermissionSeederTest | Granting a permission reveals the matching menu item | |

### 16. Security and Audit Logs

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 16.1 | View audit logs | `/admin/audit-logs` | `GET /audit-logs` | AuditLogTest | Admin actions listed with actor and time | |
| A 16.2 | Search logs | same | `GET /audit-logs?search=` | AuditLogTest | Search finds an action | |
| A 16.3 | Filter logs | same | `GET /audit-logs?administrator_id=&module=&action=&from=&to=` | AuditLogTest | Filters narrow the list | |
| A 16.4 | Login activity | same → Login view | `GET /audit-logs?view=login` | AuditLogTest | Logins, logouts, failed logins listed | |
| A 16.5 | Security events | same → Security view | `GET /audit-logs?view=security` | AuditLogTest | Failed logins, password changes, bans listed | |

### 17. System Settings

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 17.1 | General settings | `/admin/settings` → General | `GET/PUT /settings` | SettingsTest | Name, description, support email saved; timezone shown read-only | |
| A 17.2 | Marketplace settings | → Marketplace | same | SettingsTest | Saved (Open: C3 — not enforced yet) | |
| A 17.3 | Booking settings | → Booking | same | SettingsTest | Saved (Open: C3 — cancellation window not enforced yet) | |
| A 17.4 | Notification settings | → Notifications | same | NotificationsTest | Announcement switch blocks sending (Open: C3 for email/push switches) | |
| A 17.5 | Platform policies | → Platform policies | same | SettingsTest | Saved (Open: H2 — not shown in the app yet) | |
| A 17.6 | System settings | → System | same | AuthenticationTest | Session timeout enforced (Open: C3 for maintenance mode, page size) | |

### 18. Data Management

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 18.1 | Export data | `/admin/data-management` | `GET /data-management/export` | DataManagementTest | Export downloads the selected records | |
| A 18.2 | Archive records | same | `POST /data-management/archives` | DataManagementTest | Archive → hidden from active lists | |
| A 18.3 | Restore archived | same | `POST /data-management/archives/{id}/restore` | DataManagementTest | Restored record reappears | |
| A 18.4 | Manage deleted records | same | `GET /data-management/deleted`, restore, permanent delete | ReviewRemovalTest | Restore a deleted review; permanent delete refused while related data exists; purge after 30 days | |

### 19. Logout

| ID | Requirement | Page | API | Tests | UAT → expected | Result |
|----|-------------|------|-----|-------|----------------|--------|
| A 19.1 | Admin logout | Header → Sign out | `POST /auth/logout` | AuthenticationTest | Returns to login; Back button does not re-open the admin | |

## Cross-cutting checks

| Check | How | Expected | Result |
|-------|-----|----------|--------|
| Security headers | Browser dev tools on the deployed admin → Network → document | CSP meta present; `X-Frame-Options: DENY` header (DEPLOYMENT.md) | |
| CORS | `CorsTest`; request from another origin | Only the admin web's origins allowed | |
| Rate limiting | `ClientAuthRateLimitTest`, 6 fast admin logins | 429 after the limit | |
| Health | `GET /api/health` on production | database and storage `up` | |
| Realtime | Two admin tabs; act in one | Other tab updates without reload | |
