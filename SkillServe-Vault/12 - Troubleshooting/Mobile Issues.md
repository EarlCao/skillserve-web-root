---
type: troubleshooting
tags: [troubleshooting, mobile]
sources: [skill-serve-mobile-application/README.md, SETUP_CREDENTIALS.md, lib/core/config/app_config.dart]
---
# Mobile Issues

| Symptom | Cause | Fix |
|---|---|---|
| `flutter` fails from WSL | Windows SDK entry script has CRLF line endings | use `tool/wsl-flutter.sh <args>` |
| First request after idle times out | Render free-tier cold start (~60–75 s) | app already uses 120 s receive / 90 s connect timeouts and a wake-up ping at start; keep-alive or paid instance |
| Google sign-in fails | Android OAuth client/SHA-1 not registered, or `GOOGLE_CLIENT_ID` ≠ `GOOGLE_WEB_CLIENT_ID` | `SETUP_CREDENTIALS.md` §2; backend checks token `aud` |
| No OTP email | mail not configured on Render | `SETUP_CREDENTIALS.md` §1/§3 (Brevo) |
| "Too many attempts…" | `client-auth`/`login` limiter or OTP limits | wait a minute; OTP: 5 tries, 60 s resend cooldown |
| Full-screen "under maintenance" | System Settings maintenance mode on | turn it off in admin; app rechecks `/platform` |
| Signed out with a reason | account suspended/banned (403 `meta.account`) | admin activates/unbans |
| Signed out unexpectedly on two devices | refresh token reused (family revoked) or password changed | sign in again |
| Forgot-password link opens a 404 | KI-02 | no workaround in-app; the admin API has no password-reset endpoint for customer/provider accounts (only `PATCH /api/administrators/{id}/password` for staff) |
| Release build signed with debug key | `android/key.properties` missing | create keystore + properties ([[Mobile Release Build]]) |
| App points at production when testing locally | no define file | `--dart-define-from-file=env/local.json` |

Related: [[Mobile App Architecture]] · [[Mobile Development Guide]]
