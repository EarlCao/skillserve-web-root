---
type: reference
tags: [api, mobile, mapping]
sources: [skill-serve-mobile-application/lib/features/*/services, lib/core/services]
---
# Mobile-to-API Map

Extracted from the Flutter services (paths relative to `/api`). All go through `ApiClient`
(except the background task, which uses its own Dio with the background token).

| Mobile feature | Service file(s) | Endpoints |
|---|---|---|
| Auth & session | `features/auth/services/auth_service.dart` | `POST /client/v1/auth/register`, `register-provider`, `verify-otp`, `resend-otp`, `cancel-registration`, `login`, `google`, `google/register`, `refresh`, `logout`, `forgot-password`; `GET /client/v1/auth/me` |
| Profile | `features/profile/services/profile_service.dart` | `GET/PATCH /client/v1/auth/me`, `POST/DELETE /client/v1/auth/me/photo`, `POST /client/v1/auth/change-password` |
| Account data & deletion | `features/profile/services/account_data_service.dart` | `GET /client/v1/auth/me`, `GET /client/v1/auth/me/data-export`, `DELETE /client/v1/auth/me` |
| Catalog / discovery | `features/marketplace/services/service_service.dart` | `GET /client/v1/categories`, `/services`, `/services/{id}`, `/providers`, `/providers/{id}` |
| Favorites | `features/marketplace/services/favorites_service.dart` | `GET /client/v1/favorites`, `PUT/DELETE /client/v1/favorites/{provider}` |
| Customer bookings & payments | `features/booking/services/booking_service.dart`, `features/payments/services/payment_service.dart` | `GET/POST /client/v1/bookings`, `GET …/{id}`, `PATCH …/{id}/cancel`, `PATCH …/{id}/reschedule` |
| Provider jobs | `features/booking/services/booking_service.dart` (used by `ProviderBookingController`) | `GET /client/v1/provider/bookings[/{id}]`, `PATCH …/confirm|decline|cancel|start|complete|payment-received` |
| Provider services, profile, availability, badges | `features/provider/services/provider_service_service.dart` | `GET/POST /client/v1/provider/services`, `GET/PUT/DELETE …/{id}`, `GET/PATCH /client/v1/provider/profile`, `GET/PUT /client/v1/provider/availability`, `GET /client/v1/provider/badges`, `GET /client/v1/categories` |
| Portfolio | `features/provider/services/portfolio_service.dart` | `GET/POST /client/v1/provider/portfolio`, `DELETE …/{item}`, `GET /client/v1/providers/{id}` |
| Verification | `features/provider/services/verification_service.dart` | `GET/POST /client/v1/provider/verification` (multipart with progress) |
| Messaging | `features/messaging/services/message_service.dart` | `GET /client/v1/conversations`, `GET …/unread-count`, `GET/POST /client/v1/bookings/{id}/messages`, `POST …/messages/read` |
| Notifications | `features/notifications/services/notification_service.dart` | `GET /client/v1/notifications`, `GET …/unread-count`, `PATCH …/{id}/read`, `POST …/read-all` |
| Background notifications | `core/services/background_notifications.dart` | `POST /client/v1/notifications/background-token`, `GET /client/v1/notifications/background` |
| Reviews | `features/reviews/services/review_service.dart` | `GET/POST /client/v1/reviews`, `PATCH /client/v1/reviews/{id}`, `GET /client/v1/providers/{id}` |
| Reports & disputes | `features/reports/services/report_service.dart` | `GET/POST /client/v1/reports`, `GET …/{id}`, `GET /client/v1/disputes`, `PATCH /client/v1/bookings/{id}/dispute`, `POST …/dispute/evidence` |
| Support | `features/support/services/support_service.dart` | `GET/POST /client/v1/support/tickets`, `GET …/{id}`, `POST …/{id}/replies` |
| Preferences | `features/settings/services/preferences_service.dart` | `GET/PUT /client/v1/preferences` |
| Platform info / policies / maintenance | `features/settings/services/platform_service.dart` | `GET /client/v1/platform` |
| Realtime | `core/services/realtime_client.dart` | `POST /broadcasting/auth` |

## Client endpoints the app does not call

| Endpoint | Note |
|---|---|
| `POST /client/v1/auth/reset-password` | the app only requests the reset email; completing the reset has no app screen **and** the emailed link points to a non-existent page — KI-02 in [[Known Issues and Gaps]] |
| `POST /client/v1/auth/verification-notification`, `GET /client/v1/auth/verify-email/{user}/{hash}` | legacy signed-link verification; the app uses OTP |
| `GET /client/v1/categories/{category}` | the app loads the full category list instead |

Related: [[Mobile App Architecture]] · [[Endpoints Index]]
