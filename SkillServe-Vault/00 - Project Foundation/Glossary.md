---
type: reference
tags: [foundation, glossary]
---
# Glossary

| Term | Meaning in SkillServe |
|---|---|
| **Admin Web** | The React SPA in `frontend/` used by staff. |
| **Client / Customer** | A mobile account with `role_id = 4` that books services. The API and code use "client" and "customer" interchangeably (`client_id`, `EnsureClient`, `isClientAccount`). |
| **Provider** | A mobile account with `role_id = 3` **and** a `provider_profiles` row. Offers services. |
| **Provider profile** | `provider_profiles` row: business name, bio, skills, rating aggregates, verification state, featured flag. Bookings and services point at the profile id, not the user id. |
| **Staff / Administrator** | Any account whose role is not provider/customer (super-admin, admin, custom roles). |
| **Super-admin** | Role id 1; bypasses every gate. |
| **Service** | A provider's listing (`services`), with `status` (draft/published/archived) and `approval_status` (pending/approved/rejected). |
| **Booking** | A customer's request for a service at a time (`bookings`). Also *is* the chat conversation and the dispute record. |
| **Booking number** | Human-readable unique `bookings.booking_number`. |
| **Dispute** | Columns on a booking (`dispute_status`, `dispute_reason`, `dispute_evidence`, …); raised from the app, managed in Admin → Disputes. |
| **Report** | A complaint against a user, review or message (`reports`, polymorphic `reportable`). |
| **Moderation action** | warning / suspend / ban / hide / remove applied from a report. |
| **Verification request** | A provider's submission of documents for admin review (`verification_requests`, `verification_documents`). |
| **Badge** | Admin-defined recognition (`provider_badges`) assigned to providers. |
| **Featured** | `services.is_featured` or `provider_profiles.is_featured`; shown in the app's featured rails. |
| **Announcement** | Admin broadcast to all / customers / providers / selected users, optionally scheduled. |
| **Platform fee** | SkillServe's commission on a booking, stored in `bookings.platform_fee`. The rate comes from the matching `commission_tiers` band (`marketplace.commission_rate` is only the fallback when no band is configured) and is snapshotted onto the booking as `commission_rate`. |
| **Inclusive commission** | The commission is contained *within* the price the provider advertises: the customer pays that price, and the provider receives it less the commission. It is never added on top. |
| **Outstanding commission** | `bookings.commission_status = outstanding` — the provider has been paid and holds SkillServe's share until they remit it. While anything is outstanding they cannot accept new bookings or publish services. |
| **Cancellation window / late fee** | Cancelling a *confirmed* booking inside `booking.cancellation_window_hours` records a fee on the booking. |
| **Business time** | `BUSINESS_TIMEZONE` (Asia/Manila). Storage is UTC. |
| **Envelope** | The JSON response shape `{ success, message, data, errors, meta }`. |
| **client-access token** | Mobile Sanctum access token (ability `client:auth`, 60 min). |
| **Refresh token** | Rotating mobile refresh token in `client_refresh_tokens` (family-based reuse detection). |
| **Background token** | Read-only mobile token (ability `client:notifications`) used by WorkManager while the app is closed. |
| **admin-session token** | Admin Sanctum token, lifetime = System Settings → session timeout. |
| **Reverb** | Laravel's WebSocket server (Pusher protocol). |
| **`admin.data` channel** | Private channel on which the backend signals which admin resources changed. |
| **Pending registration** | A sign-up waiting for OTP verification (`pending_registrations`); becomes a user only after OTP. |
| **OTP** | 6-digit email one-time password used to verify registration. |
| **Maintenance mode** | `system.maintenance_mode` setting; mobile API returns 503 with `meta.maintenance`. |
| **Starter / admin-only / demo** | `SEED_MODE` values ([[Seeding and Demo Data]]). |
| **NeonDB pooler / direct host** | Neon's pgBouncer endpoint (`-pooler`) for queries vs the direct host for migrations. |
| **A x.y / M x.y** | Requirement ids from the admin / mobile PDFs. |
| **PENDING_FIXES IDs** | C1–C4 (critical), H1–H5 (high), M1–M7, L1–L6, D1–D3 used in `PENDING_FIXES.md`. |
