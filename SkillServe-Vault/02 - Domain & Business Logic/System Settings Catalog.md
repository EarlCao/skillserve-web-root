---
type: domain
tags: [domain, settings]
sources: [backend/config/system-settings.php, backend/app/Modules/Settings/Services/SettingsService.php, backend/app/Modules/Settings/Controllers/PlatformController.php]
---
# System Settings Catalog

Defined in `backend/config/system-settings.php`; stored in the `settings` table (group + name +
JSON payload); read everywhere through `SettingsService::value(group, name)`; edited via
`GET/PUT /api/settings` (permission `manage settings`); audit log name `system_settings`.

| Group | Key | Type | Default | Enforced by (code) |
|---|---|---|---|---|
| general | `platform_name` | string ≤120 | `SkillServe` | `/platform` endpoint |
| general | `platform_description` | text ≤1000 | `''` | `/platform` |
| general | `support_email` | email | `''` | `/platform` |
| general | `timezone` | **read-only** | from `app.business_timezone` (`Asia/Manila`) | sending it → 422 (`meta.read_only`) |
| marketplace | `provider_registration_enabled` | bool | true | `ProviderSignups` (provider sign-up closed) |
| marketplace | `service_approval_required` | bool | true | `ProviderServiceService` (new/edited services → pending) |
| marketplace | `featured_services_enabled` | bool | true | `ServiceService` refuses featuring; catalog hides featured flag |
| marketplace | `commission_rate` | 0–100 % | 10 | **Fallback only** — used by `CommissionCalculator` when no active `commission_tiers` row exists. Configured tiers take precedence; see [[Commission Tiers and Settlement]] |
| identity | `identity_verification_required` | bool | **false** | `IdentityGate` — master switch for National ID enforcement; see [[Identity Verification Lifecycle]] |
| identity | `identity_verification_enforced_from` | date | `''` | `IdentityGate` — accounts created before this date are grandfathered; empty applies the rule to everyone |
| identity | `identity_document_retention_days` | int 1–3650 | 90 | `identity:purge-documents` (daily) |
| booking | `booking_enabled` | bool | true | `BookingRules::assertBookingEnabled` (new bookings only) |
| booking | `cancellation_window_hours` | int 0–720 | 24 | [[Cancellation and Fees]] |
| booking | `client_cancellation_fee_percent` | 0–100 | 0 | same |
| booking | `provider_cancellation_fee_percent` | 0–100 | 0 | same |
| notifications | `email_notifications_enabled` | bool | true | moderation mail |
| notifications | `push_notifications_enabled` | bool | true | `BroadcastClientNotification`, background feed |
| notifications | `announcement_notifications_enabled` | bool | true | `AnnouncementService` refuses create/delete when off |
| policies | `terms_of_service`, `privacy_policy`, `community_guidelines` | text ≤50000 | `''` | `/platform` → app policy screens |
| system | `maintenance_mode` | bool | false | `EnsurePlatformAvailable` (mobile API 503) |
| system | `session_timeout_minutes` | int 5–43200 | 1440 | admin token `expires_at` + Sanctum validity check |
| system | `default_page_size` | int 1–100 | 15 | `PageSize::from` |

## Public projection — `GET /api/client/v1/platform`

No auth, outside maintenance mode. Returns platform name, support email, sign-up and booking rules,
and the three policy texts (the app falls back to bundled text offline).

> [!bug] Session timeout also limits the mobile background token
> The Sanctum check applies `session_timeout_minutes` to every token not named `client-access`,
> which includes the mobile background token (`client-background`). See
> [[Known Issues and Gaps]] (KI-01).

Related: [[System Settings]] · [[settings]]
