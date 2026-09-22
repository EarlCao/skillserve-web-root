---
type: domain
tags: [domain, bookings, settings]
sources: [backend/app/Modules/Bookings/Services/BookingRules.php, backend/config/system-settings.php, backend/database/migrations/2026_09_22_000001_add_cancellation_fee_to_bookings.php]
---
# Cancellation and Fees

Implemented in `App\Modules\Bookings\Services\BookingRules` (settings-driven).

| Setting (System Settings → Booking) | Default | Effect |
|---|---|---|
| `cancellation_window_hours` | 24 (0–720) | a cancellation is **late** if the booking is `confirmed` and starts in less than this many hours |
| `client_cancellation_fee_percent` | 0 (0–100) | fee recorded when the **customer** cancels late |
| `provider_cancellation_fee_percent` | 0 (0–100) | fee recorded when the **provider** cancels an accepted booking late |
| `booking_enabled` | true | pauses **new** bookings only |

`fee = round(total_price × percent / 100, 2)`; stored in `bookings.cancellation_fee` (nullable,
`null` when zero). Only `confirmed` bookings can be late — cancelling a `pending` one is always free.

| Who cancels | Fee side | Code |
|---|---|---|
| Customer | `client` | `ClientBookingService::cancel` |
| Provider (`…/cancel`, confirmed only) | `provider` | `ProviderBookingService::transition('cancel')` |
| Provider decline (pending) | none | — |
| Admin | none | `BookingService::cancel` |

The app shows the policy **before** confirming: booking resources expose
`cancellation_policy {window_hours, fee_percent, is_late, fee_if_cancelled_now}`
(`BookingRules::policyFor`). The admin booking modal shows the recorded fee.

> [!info] Recorded, not charged
> The fee is a number on the booking. No payment is taken or deducted
> ([[ADR-007 Payments Recorded Not Processed]]).

Payment state on cancellation: `Booking::cancellationPaymentPolicy()` →
`unpaid_no_refund_due`, `already_refunded`, or `payment_unchanged_refund_not_processed` (refunds are
recorded separately by an admin — [[Payments and Refunds]]).

Related: [[Booking Lifecycle]] · [[System Settings Catalog]]
