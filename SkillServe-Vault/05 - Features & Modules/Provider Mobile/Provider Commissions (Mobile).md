---
type: feature
platform: provider-mobile
status: implemented
tags: [feature, mobile, commissions, payments]
---
# Provider Commissions (Mobile)

Mobile requirement(s): **(extra)** ([[Requirements Sources]]).

| | |
|---|---|
| Screens / routes | `/commissions`, `/commissions/pay`, `/gcash-details` |
| Code (Flutter `lib/`) | `features/provider/ (models/commission_model.dart, services/commission_service.dart, views/commissions_screen.dart, views/pay_commission_screen.dart, views/gcash_details_screen.dart)` |
| Endpoints | `GET /api/client/v1/provider/commissions`, `POST /api/client/v1/provider/commission-remittances`, `PATCH /api/client/v1/provider/profile` |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | See what is owed | the outstanding total and each unremitted booking: the service, the booking number, the commission, its rate against the job's price, and when the customer paid | implemented |
| — | Understand the block | while anything is outstanding the provider cannot accept or start jobs or publish services; declining and cancelling stay open, and the screen says so | implemented |
| — | Settle it | **I've paid** (`/commissions/pay`): SkillServe's GCash number, name and the amount, each copyable; then the GCash reference number, the amount sent and an optional receipt screenshot. A payment waiting for confirmation, or a rejected one with its reason, is shown on `/commissions`. Without SkillServe's GCash configured the screen falls back to contacting support | implemented |
| — | Hear the decision | a `commission_remittance` notification (confirmed or rejected) opens `/commissions`, and on arrival reloads the balance (`CommissionController`) and the eligibility banner, so the block lifts on screen at once | implemented |
| — | Receive GCash payments | `/gcash-details` saves `gcash_number` and `gcash_name`, which is what makes `payment_instructions` useful to the customer | implemented |

## Tests

`identity_test` covers `CommissionSummary` — the balance, the block, the bookings behind it, and a
provider whose block is actually an identity one. `commission_remittance_test` covers the payment
account and the latest payment (pending, rejected, and an older API without either);
`notifications_reviews_test` the notification route; both sweeps render `/commissions/pay`;
`commission_remittance_test` also covers `CommissionController` reloading and clearing on sign-out.

## Notes

- **The commission is inside the advertised price, not added to it.** The customer pays the
  provider the whole amount, and the platform's share stays with the provider until they remit it
  ([[ADR-021 Direct Payment with Provider-Remitted Commission]], [[Commission Tiers and Settlement]]).
- **The app never takes the money.** SkillServe is never in the payment path: the provider sends
  GCash outside the app and submits the reference, and nothing is settled until an administrator
  confirms it arrived — so new work stays paused while a payment waits. See
  [[Commission Tiers and Settlement#Paying it by GCash]].
- Money amounts stay exactly as the API formatted them. Re-parsing a decimal for display only
  invites rounding differences between the app and the ledger.
- A provider blocked on **identity** is sent to [[Mobile Identity Verification]] instead — the API
  reports identity first, because it is the more fundamental block and the commission screen offers
  them nothing to act on.
- `gcash_name` is asked for so the customer can compare it against the recipient name GCash shows
  before sending, which is what catches a mistyped or swapped number.

## Related

[[Commission Tiers and Settlement]] · [[Provider Earnings and Statistics]] ·
[[Mobile Identity Verification]] · [[Provider Mobile Features Index]]
