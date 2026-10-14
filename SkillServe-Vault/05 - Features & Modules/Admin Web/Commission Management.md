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
| Admin route(s) | `/admin/commissions` (tabs: `?tab=ledger`, `?tab=payments` — *Provider payments*, `?tab=rules` — *Rules*) |
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

The dashboard's commission card offers the quick path: change a band's percentage in place, or
apply a preset (**Standard** 5/10/15/20%, **Flat 10%**) that replaces the active tiers in one step —
see [[Admin Dashboard#Commission card]] and [[Commission Tiers and Settlement#Presets]]. Its
**Custom…** button leads here for range changes.

### Commissions & Payments tab

One row per booking: what the customer paid, what the provider received, the commission and its
rate, the payment method and date, and the commission status. Header cards total the outstanding,
settled and waived amounts for the current filters.

`Settle` records a remittance (method, reference, notes); `Waive` writes the debt off and always
requires a reason. **The amount is never entered** — it is shown read-only, because it always comes
from the booking.

### Provider payments tab

The providers' commission payments ([[Commission Tiers and Settlement#Paying it by GCash]],
[[Commission Tiers and Settlement#Paying it by QR Ph]]). Each row says how it was paid: *GCash
reference* (a reviewer confirms it) or *QR Ph (PayMongo)* (PayMongo confirms it by itself — such a
payment appears in the waiting list only when it needs a decision, e.g. PayMongo reported a
different amount, shown in red with the PayMongo payment id).
It opens on the payments **waiting for confirmation**, oldest first; each row shows the GCash
reference, the provider and their own GCash number (the expected sender), and the amount sent
against the amount owed (shown in red when short).

`Confirm` opens the reference, both amounts, the receipt screenshot when one was attached, and the
bookings a confirmation settles with each one's current status; confirming settles them all with
method `gcash`. Two warnings guard it: **another provider also claimed this reference** (a reference
can be confirmed once, so only the claim whose sender matches GCash should be), and **some bookings
are no longer outstanding** (settled by hand, waived or voided since — the provider may have paid
for them twice and is owed the difference). Opening a receipt is written to the audit log. `Reject` requires a
reason, which the provider is shown. Both need `settle commissions`.

The sidebar's **Commissions** item carries a live count of waiting payments and links straight to
this tab while any are waiting. Providers now pay by QR Ph only, so GCash-reference payments come
only from older app versions.

### Rules tab

The fallback commission rate (used when no tier matches) and when unpaid commission blocks a
provider (₱ threshold, 0 = any debt; days, 0 = off). Moved here from System Settings → Marketplace
on 2026-10-14: `GET /api/commission-settings` (`view commissions`), `PUT` (`manage commissions`).
The values are still the `marketplace.commission_*` settings (flagged `managed_by: commissions`);
System Settings no longer shows them and refuses them with "Change this on the Commission page."

> [!info] Why there is no separate Payments page
> `/api/commissions` already returns the payment status, method, reference and date alongside the
> commission, so this tab is the payment view. Marking a booking paid and refunding it stay on
> [[Booking Management]], where those actions already live, rather than being duplicated here.

## Automated tests

`CommissionTierTest`, `CommissionSettingsTest`, `CommissionCalculationTest`, `CommissionLedgerTest`, `CommissionRemittanceTest`,
`PaymentGatewayTest` —
see [[Backend Test Suite]]. There is no frontend test framework; the UI is verified by
`npm run lint` and `npm run build`.

## Related

[[Commission Tiers and Settlement]] · [[Payments and Refunds]] · [[commission_tiers]] ·
[[commission_settlements]] · [[commission_remittances]] · [[Booking Management]] · [[Admin Web Features Index]]
