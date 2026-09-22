---
type: reference
tags: [testing, backend]
sources: [backend/tests, backend/app/Modules/*/Tests/Feature]
---
# Backend Test Suite

Counted by static inspection (`public function test…` / `#[Test]`), audit 2026-09-22:
**59 files, ≈449 test methods**.

| Module / area | Test class (methods) |
|---|---|
| Administrators | AdministratorManagementTest (23), RoleManagementTest (14) |
| Analytics | AnalyticsTest (7) |
| Audit | AuditLogTest (4) |
| Authentication | AuthenticationTest (12), AdminPasswordResetTest (3) |
| Bookings | BookingCancellationTest (2), BookingListTest (3), BookingPaymentTest (8), DisputeManagementTest (6) |
| ClientAuthentication | AccountDataTest (10), AccountStatusTest (6), CancelRegistrationTest (7), ClientAuthRateLimitTest (2), ClientAuthenticationTest (14), ClientEmailOtpTest (7), ClientGoogleAuthTest (14), ClientProfileTest (10), ClientProviderRegistrationTest (6) |
| ClientCommunication | BackgroundNotificationTest (7), ClientCommunicationTest (4), ClientReportTest (15), ConversationTest (11), ProviderSupportTicketTest (3) |
| ClientMarketplace | BookingDisputeTest (14), BookingRescheduleTest (7), ClientMarketplaceTest (18), FavoriteProviderTest (6), ProviderAccountTest (12), ProviderBookingTest (14), ProviderServiceTest (10), ProviderVerificationTest (6) |
| ClientPreferences | ClientPreferencesTest (10) |
| Dashboard | DashboardTest (3) |
| DataManagement | DataManagementTest (4) |
| Notifications | AnnouncementsMigrationTest (1), NotificationsTest (5) |
| ProviderRecognition | ProviderRecognitionTest (4) |
| Providers | ProviderSecurityTest (1) |
| ReportsAndModeration | ReportsAndModerationTest (24) |
| Reviews | ReviewListTest (2), ReviewRemovalTest (4) |
| ServiceCategories | ServiceCategoryManagementTest (15) |
| Services | ServiceManagementTest (8) |
| Settings | SettingsTest (3) |
| Support | SupportTicketManagementTest (6) |
| Users | UserManagementTest (29) |
| `tests/Feature` | AdminDecisionNotificationTest (4), ApiFoundationTest (7), CorsTest (3), DemoAccountSeederTest (3), ExampleTest (1), HealthCheckTest (1), RealtimeAdminUpdatesTest (6), RolePermissionSeederTest (2), SettingsEnforcementTest (9), StarterSeedTest (1), UserRolesTest (7) |
| `tests/Unit` | ExampleTest (1) |

## Thin spots (by count)

`ProviderSecurityTest` has a single method that checks verification documents are not exposed and
that downloads are scoped — yet `TEST_PLAN.md` cites it for A 4.1–4.8. Approve/reject/request-info
and suspend/activate are exercised (with notifications) by `AdminDecisionNotificationTest`, but no
test calling `PATCH /api/providers/{id}/verification/remove` was found; Dashboard (3), Data Management (4), Audit (4),
Provider Recognition (4), Settings (3) are lightly covered compared with their surface.

Run: `docker compose exec backend composer test` or `php artisan test --filter=ClassName`.

Related: [[Testing Strategy]] · [[UAT and Traceability]]
