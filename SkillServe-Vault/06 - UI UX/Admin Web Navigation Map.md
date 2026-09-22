---
type: reference
tags: [ui, navigation, frontend]
sources: [frontend/src/routes/index.jsx, frontend/src/layouts/AdminLayout.jsx]
---
# Admin Web Navigation Map

## Sidebar (as labelled in `AdminLayout.jsx`)

| Group | Label | Route | Visible if user has any of |
|---|---|---|---|
| Main | Dashboard | `/admin` | (always shown; route needs `view dashboard`) |
| User Management | Customer Management | `/admin/users` | manage/view/edit/delete/suspend/activate/ban users |
| User Management | Provider Management | `/admin/providers` | manage/view/edit/delete/suspend/activate/verify/reject providers |
| User Management | Admin Management | `/admin/administrators` | manage/view/create/edit administrators |
| Services & Categories | Services | `/admin/services` | manage/view/create/edit/delete/approve/reject/feature services |
| Services & Categories | Service Categories | `/admin/service-categories` | manage/view/create/edit/delete service categories |
| Bookings & Disputes | Bookings | `/admin/bookings` | manage/view/cancel bookings, manage booking disputes |
| Bookings & Disputes | Dispute Management | `/admin/disputes` | manage/view bookings, manage booking disputes |
| Reviews & Moderation | Reviews and Ratings | `/admin/reviews` | manage/view/edit/delete reviews |
| Reviews & Moderation | Reports and Moderation | `/admin/reports` | manage/view/investigate/resolve reports, manage moderation |
| Reviews & Moderation | Provider Recognition | `/admin/provider-recognition` | recognition permissions |
| — | Support Management | `/admin/support` | support permissions |
| — | Reports (= Analytics)¹ | `/admin/analytics` | view/export analytics |
| — | Notifications | `/admin/notifications` | notification permissions |
| — | Data Management | `/admin/data-management` | data permissions |
| — | Security & Audit | `/admin/audit-logs` | audit permissions |
| — | System Settings | `/admin/settings` | manage settings |
| footer | Sign out | — | — |

¹ Label from the **uncommitted** working tree at audit time; the committed `main` says "Reports & Analytics".

Top bar user menu: Change password (`/admin/change-password`), Sign out.

## All routes

| Path | Guard | Page component |
|---|---|---|
| `/` | — | redirect → `/login` |
| `/login`, `/forgot-password`, `/reset-password` | `GuestOnly` | LoginPage, ForgotPasswordPage, ResetPasswordPage |
| `/admin` | `RequireAuth` + `view dashboard` | DashboardPage |
| `/admin/change-password` | `RequireAuth` | ChangePasswordPage |
| `/admin/administrators` (`?tab=roles`, `?tab=permissions`) | administrator permissions | AdministratorManagementPage |
| `/admin/roles`, `/admin/permissions` | same | redirects to the tabs |
| `/admin/users`, `/admin/users/:userId` | user permissions | UsersPage, UserProfilePage |
| `/admin/service-categories` | category permissions | ServiceCategoriesPage |
| `/admin/services` | service permissions | ServicesPage |
| `/admin/bookings` | booking permissions | BookingsPage |
| `/admin/disputes` | booking/dispute permissions | DisputesPage |
| `/admin/reviews` | review permissions | ReviewsPage |
| `/admin/reports` | report permissions | ReportsPage |
| `/admin/notifications` | notification permissions | NotificationsPage |
| `/admin/providers`, `/admin/providers/:providerId` | provider permissions | ProvidersPage, ProviderProfilePage |
| `/admin/provider-recognition` | recognition permissions | ProviderRecognitionPage |
| `/admin/analytics` | analytics permissions | AnalyticsPage |
| `/admin/audit-logs` | audit permissions | AuditLogsPage |
| `/admin/settings` | `manage settings` | SettingsPage |
| `/admin/support` | support permissions | SupportTicketsPage |
| `/admin/data-management` | data permissions | DataManagementPage |

Unknown paths: no catch-all route is defined in `routes/index.jsx` (React Router's default error
element handles them). **Needs Verification** of the exact behaviour in production.

Related: [[Admin Web Frontend Architecture]] · [[Admin Web Features Index]]
