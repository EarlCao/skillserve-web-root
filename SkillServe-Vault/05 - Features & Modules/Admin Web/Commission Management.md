---
type: feature
platform: admin-web
status: implemented
module_number: null
tags: [feature, admin-web, commissions]
---
# Commission Management

> [!note] Beyond the original requirements
> This module is **not** in `SkillServe_Admin_Web_Functionalities.pdf`, which has no commission or
> payment module. It was added later on the project owner's instruction. See
> [[Requirements Sources]].

| | |
|---|---|
| Backend module | `backend/app/Modules/Commissions` |
| Frontend module | `frontend/src/modules/commissions` |
| Admin route(s) | `/admin/commissions` (tabs: `?tab=ledger`) |
| Permissions | `view commissions` to read · `manage commissions` to configure tiers · `settle commissions` to record or waive |

## What it does

The commission is **inclusive**: it comes out of the price the provider advertises, so the customer
pays that price and the provider receives the rest. See [[Commission Tiers and Settlement]] for the
rules.

### Tiers tab

Create, edit and retire the bands that decide the rate. The form states that both bounds are
inclusive and that an empty maximum makes the band open-ended, and previews the split on the band's
own lower bound so the effect of a rate is visible before saving.

Overlap with another active band is a cross-row rule decided by the server, so a clash arrives as a
422 naming the band it collides with rather than being guessed at in the browser. Retiring a tier
warns that bookings already charged under it keep their own snapshotted rate.

### Commissions & Payments tab

One row per booking: what the customer paid, what the provider received, the commission and its
rate, the payment method and date, and the commission status. Header cards total the outstanding,
settled and waived amounts for the current filters.

`Settle` records a remittance (method, reference, notes); `Waive` writes the debt off and always
requires a reason. **The amount is never entered** — it is shown read-only, because it always comes
from the booking.

> [!info] Why there is no separate Payments page
> `/api/commissions` already returns the payment status, method, reference and date alongside the
> commission, so this tab is the payment view. Marking a booking paid and refunding it stay on
> [[Booking Management]], where those actions already live, rather than being duplicated here.

## Automated tests

`CommissionTierTest`, `CommissionCalculationTest`, `CommissionLedgerTest`, `PaymentGatewayTest` —
see [[Backend Test Suite]]. There is no frontend test framework; the UI is verified by
`npm run lint` and `npm run build`.

## Related

[[Commission Tiers and Settlement]] · [[Payments and Refunds]] · [[commission_tiers]] ·
[[commission_settlements]] · [[Booking Management]] · [[Admin Web Features Index]]
