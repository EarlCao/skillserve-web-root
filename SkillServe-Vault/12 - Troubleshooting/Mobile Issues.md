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
| Google sign-in fails (`ApiException: 10`, "not set up for this version") | Android OAuth client/SHA-1 not registered, or `GOOGLE_CLIENT_ID` ≠ `GOOGLE_WEB_CLIENT_ID` | `SETUP_CREDENTIALS.md` §2; backend checks token `aud` |
| Google sign-in fails (`network_error` / `ApiException: 7`, "Google could not be reached") | the phone's Google Play services cannot reach Google: offline, wrong date/time, VPN or Private DNS (ad-blocking DNS), outdated Play services, or an emulator without Play Store. Nothing reaches the backend, so no code is emailed | app retries once; then fix the phone's connection/settings and try again. Email sign-up is unaffected |
| No OTP email, but the code screen opened | `GET /api/health` → `services.otp`: `down` means `RESEND_API_KEY` is missing on Render. If `up`: Render's log has `Failed to send registration OTP` with Resend's reason (`domain is not verified` / `only send testing emails to your own email address` = no verified domain or `MAIL_FROM_ADDRESS` on another domain; `daily_quota_exceeded` = 100 emails today). Each email is listed in Resend → *Emails* | Render → Environment: `MAIL_MAILER=resend-api`, `RESEND_API_KEY`, `MAIL_FROM_ADDRESS=no-reply@<verified domain>`; finish verifying the domain in Resend (DEPLOYMENT.md → "Email codes"). Ask the user to check Spam |
| "Too many attempts…" | `client-auth`/`login` limiter or OTP limits | wait a minute; OTP: 5 tries, 60 s resend cooldown |
| Full-screen "under maintenance" | System Settings maintenance mode on | turn it off in admin; app rechecks `/platform` |
| Signed out with a reason | account suspended/banned (403 `meta.account`) | admin activates/unbans |
| Signed out unexpectedly on two devices | refresh token reused (family revoked) or password changed | sign in again |
| ~~Forgot-password link opens a 404~~ | ~~KI-02~~ | resolved 2026-10-03: reset is now done in the app with an emailed 6-digit code |
| Release build signed with debug key | `android/key.properties` missing | create keystore + properties ([[Mobile Release Build]]) |
| App points at production when testing locally | no define file | `--dart-define-from-file=env/local.json` |

Related: [[Mobile App Architecture]] · [[Mobile Development Guide]]
