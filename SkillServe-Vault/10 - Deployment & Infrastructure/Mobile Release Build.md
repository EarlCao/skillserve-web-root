---
type: guide
tags: [deployment, mobile, android, release]
sources: [skill-serve-mobile-application/README.md, SETUP_CREDENTIALS.md, android/app/build.gradle.kts, PENDING_FIXES.md]
---
# Mobile Release Build

| Item | Value |
|---|---|
| Application id | `com.skillserve.mobile` |
| Launcher label | SkillServe |
| Version | `1.0.0+1` (pubspec) |
| Icon source | `branding/app_icon.png`; branded splash; monochrome notification icon |
| Signing | `android/key.properties` (gitignored) → upload keystore; **falls back to the debug key with a warning** if missing |
| Lock file | `pubspec.lock` tracked |

## Steps

1. Create the upload keystore once (`keytool -genkey … -alias upload`) and **back it up** with its
   passwords — a lost key means the installed app can never be updated.
2. Write `android/key.properties` (`storePassword`, `keyPassword`, `keyAlias=upload`, `storeFile`).
3. Register the keystore's SHA-1 on the Android OAuth client (Google sign-in).
4. `flutter build apk --release --dart-define-from-file=env/production.json`
   (+ `--dart-define=REVERB_APP_KEY=<key>` if the backend key isn't `skillserve`).
5. Output `build/app/outputs/flutter-apk/app-release.apk`; check on a clean phone: name/icon,
   email + Google sign-in, realtime chat, a closed-app notification.

PENDING_FIXES H4 (2026-09-21) reports `flutter build apk --release` succeeds (not re-run in this
audit). Distribution channel (Play Store vs direct APK): **Needs Verification**.

Related: [[Go-Live Checklist]] · [[Mobile Development Guide]]
