---
type: reference
tags: [foundation, stack, backend, frontend, mobile]
sources: [backend/composer.json, backend/composer.lock, frontend/package.json, frontend/package-lock.json, skill-serve-mobile-application/pubspec.yaml]
---
# Tech Stack

Versions are the **installed** ones from lock files at audit time.

## Backend — `backend/`

| Area | Technology | Version | Notes |
|---|---|---|---|
| Language | PHP | ^8.3 (Docker `php:8.3-cli-alpine`) | |
| Framework | laravel/framework | 13.21.1 | |
| API auth | laravel/sanctum | 4.3.3 | bearer tokens only ([[Token and Session Management]]) |
| RBAC | spatie/laravel-permission | 8.3.0 | guard `web` ([[Authorization and RBAC]]) |
| Realtime | laravel/reverb | 1.11.0 | Pusher protocol on port 8080 ([[Realtime Architecture]]) |
| Audit log | spatie/laravel-activitylog | 4.12.3 | `activity_log` table |
| API docs | darkaonline/l5-swagger | 11.1.0 | PHP 8 attributes only ([[API Documentation Pipeline]]) |
| Excel/CSV | maatwebsite/excel | 3.1.70 | |
| PDF | barryvdh/laravel-dompdf | 3.1.2 | installed |
| Media | spatie/laravel-medialibrary 11.23.3, intervention/image 4.2.0 | | `media` table migrated |
| Backups | spatie/laravel-backup | 10.3.1 | installed |
| Settings pkg | spatie/laravel-settings | 3.9.0 | `settings` table; values read by `SettingsService` |
| Modules pkg | nwidart/laravel-modules | 13.0.0 | installed but **not** used for layout ([[ADR-002 Modules as Plain Namespaces]]) |
| Other | laravel/tinker, ramsey/uuid | | |
| Dev | phpunit 12, laravel/pint, mockery, faker, collision, pail, pao | | |
| Database | PostgreSQL 17 (`postgres:17-alpine`) locally; NeonDB in production | | tests: in-memory SQLite |
| Mail | log mailer locally; Brevo HTTP API transport (`brevo-api`) or SMTP in production | | `app/Shared/Services/BrevoApiTransport.php` |

> [!warning] Needs Verification — unused packages
> No application code was found using DomPDF, laravel-backup, laravel-medialibrary models or the
> spatie settings classes (`app/Settings/` is empty). They are installed and configured, but
> whether they are used anywhere indirectly is unconfirmed.

## Admin Web — `frontend/`

| Area | Technology | Version |
|---|---|---|
| Language | JavaScript/JSX (no TypeScript) | |
| UI | React / react-dom | 19.2.8 |
| Build | Vite | 8.1.5 (rolldown), `@vitejs/plugin-react` 6 + React Compiler (`babel-plugin-react-compiler`) |
| Styling | Tailwind CSS 4.3.3 + daisyUI 5.7.16 | `tailwind-merge` |
| Routing | react-router-dom | 7.18.2 |
| Server state | @tanstack/react-query | 5.101.4 (+ devtools) |
| Tables | @tanstack/react-table | ^9.0.0 |
| Forms | react-hook-form 7 + zod 4.4.3 + @hookform/resolvers | |
| HTTP | axios | 1.19.0 |
| Realtime | laravel-echo 2.4.0 + pusher-js 8 | |
| Charts | recharts | 3.10.1 |
| Misc | date-fns, lucide-react, sonner (toasts), react-dropzone, react-loading-skeleton, react-intersection-observer | |
| Lint | ESLint 10 (react-hooks, react-refresh) | Prettier installed, no config |
| Node | 22 (Docker `node:22-alpine`) | |

## Mobile — Flutter app

| Area | Technology |
|---|---|
| SDK | Dart `>=3.3.0 <4.0.0` (pubspec); lock requires Dart ≥3.12, Flutter ≥3.44 |
| State | provider 6 (`ChangeNotifier` controllers) |
| Navigation | go_router 14 |
| HTTP | dio 5 |
| Realtime | web_socket_channel 3 (hand-written Pusher-protocol client) |
| Secure storage | flutter_secure_storage 11 |
| Local storage | shared_preferences |
| Background | workmanager 0.10 + flutter_local_notifications 22 |
| Auth | google_sign_in 6.2.1 |
| Media | image_picker, file_picker, cached_network_image |
| UI | google_fonts, hugeicons, flutter_animate, shimmer, lottie, flutter_svg, flutter_screenutil, responsive_framework |
| Other | connectivity_plus, intl |
| Lint | flutter_lints 4 |

> [!bug] Stale package metadata
> `pubspec.yaml` still says *"Frontend only — ready for future REST API integration"* and
> *"Media (UI only — no upload logic)"*; the app is fully API-integrated and uploads files. The
> package name is `skilllink_mobile`. See [[Known Issues and Gaps]].

## Infrastructure

Docker Compose (local), Render (backend Docker web service + frontend static site), NeonDB
(PostgreSQL), Render persistent disk for uploads, Brevo (mail), Google Cloud OAuth (sign-in).
See [[Deployment Index]] and [[External Integrations]].
