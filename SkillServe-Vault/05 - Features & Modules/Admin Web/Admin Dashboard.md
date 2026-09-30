---
type: feature
platform: admin-web
status: implemented
module_number: 2
tags: [feature, admin-web]
---
# Admin Dashboard

Admin requirement module **2** ([[Requirements Sources]]).

| | |
|---|---|
| Backend module | `backend/app/Modules/Dashboard`  |
| Frontend module | `frontend/src/modules/dashboard` |
| Admin route(s) | `/admin` |
| Endpoints | [[API - Dashboard]] |
| Permissions | `view dashboard` |

## Requirement coverage

| ID | Functionality | Implementation |
|---|---|---|
| A 2.1 | User Summary | `user_summary`: total_clients, total_providers, active_users, suspended_users |
| A 2.2 | Service Summary | `service_summary`: total_services, approved, pending, reported_services |
| A 2.3 | Booking Summary | `booking_summary` per status (pending, confirmed, active, completed, cancelled, disputed) |
| A 2.4 | Verification Summary | `verification_summary`: pending, approved, rejected (+ additional_info_required) |
| A 2.5 | Reports Summary | `reports_summary`: pending, investigating, resolved, rejected |
| A 2.6 | Recent Activities | `recent_activities` from `activity_log`; live refresh via `admin.data` |
| A 2.7 | Platform Analytics | `analytics.monthly_activity` charts (recharts) |
| — | Commission | `commission_summary` — see [[#Commission card]] |

**Status:** code present for every functionality above. UAT result columns in `TEST_PLAN.md` are
still empty (not yet executed on the deployed system) — see [[UAT and Traceability]].

## Automated tests

`DashboardTest` (incl. the commission summary), `RealtimeAdminUpdatesTest` — see [[Backend Test Suite]].

## Commission card

Shown only to administrators who may read commissions (`view commissions` or `manage commissions`);
the API leaves `commission_summary` out for everyone else.

| Field | Meaning |
|---|---|
| `collected` | Settled commission, ₱ |
| `collected_booking_value` | What customers paid on those settled bookings, ₱ |
| `collected_rate` | `collected ÷ collected_booking_value × 100` — the effective percentage actually collected. It differs from a single tier's rate when bookings fell in different bands or predate a rate change (each booking keeps its snapshot). |
| `outstanding`, `waived` | Same totals as the Commission Management ledger header |
| `rate_source` | `tiers`, or `fallback` when no tier is active and the flat `marketplace.commission_rate` applies |
| `tiers` | Active bands, lowest first |

With `manage commissions` the card also lets an administrator change a band's percentage in place
(the existing `PATCH /api/commission-tiers/{id}`), apply a preset such as **Standard** or **Flat 10%**
after a confirmation listing the new bands ([[Commission Tiers and Settlement#Presets]]), or open
Commission Management (**Custom…**) to edit ranges.

## Notes

- Dashboard queries are aggregate reads over existing tables (`DashboardService`); no dedicated table.

## Related

[[Realtime Architecture]] · [[Admin Web Features Index]]
