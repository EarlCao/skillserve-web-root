---
type: reference
tags: [testing, mobile]
sources: [skill-serve-mobile-application/test]
---
# Mobile Test Suite

26 test files (+ `flutter_test_config.dart`), ≈203 `test`/`testWidgets` cases (static count).

| File | Cases | Area |
|---|---|---|
| booking_test | 23 | booking model/controller, UTC times, cancel/reschedule |
| session_roles_payments_test | 22 | sessions, secure storage, role routing, payments |
| discovery_test | 18 | search, filters, featured/top-rated, recent searches |
| notifications_reviews_test | 18 | notification feed, reviews |
| reports_support_test | 15 | reports, disputes, evidence, support |
| overflow_diag2_test / overflow_diag_test / overflow_repro_test | 14 / 9 / 1 | layout overflow at phone sizes |
| provider_account_test | 13 | provider profile, availability, onboarding |
| preferences_controller_test | 10 | preferences |
| marketplace_models_test | 9 | catalog JSON parsing |
| messaging_test | 9 | conversations, send/retry |
| google_registration_screen_test | 5 | Google sign-up |
| presence_background_test | 5 | presence channel, background task |
| account_status_test | 4 | restricted accounts |
| favorites_test | 4 | favorites |
| provider_services_test | 4 | provider services |
| verification_test | 4 | verification upload |
| auth_form_locking_test | 3 | form states |
| chat_realtime_test | 3 | realtime chat |
| user_account_profile_test | 3 | profile, password |
| api_error_test | 2 | error messages incl. 429 |
| platform_test | 2 | `/platform` policies, maintenance |
| app_sweep_test | 1 | screen sweep |
| security_preferences_test | 1 | security/privacy screens |
| widget_test | 1 | smoke |

Run from WSL: `tool/wsl-flutter.sh test` (or a single file). Static analysis:
`tool/wsl-flutter.sh analyze`.

Related: [[Testing Strategy]] · [[Mobile Development Guide]]
