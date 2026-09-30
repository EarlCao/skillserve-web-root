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
| Screens / routes | `/commissions`, `/gcash-details` |
| Code (Flutter `lib/`) | `features/provider/ (models/commission_model.dart, services/commission_service.dart, views/commissions_screen.dart, views/gcash_details_screen.dart)` |
| Endpoints | `GET /api/client/v1/provider/commissions`, `PATCH /api/client/v1/provider/profile` |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | See what is owed | the outstanding total and each unremitted booking: the service, the booking number, the commission, its rate against the job's price, and when the customer paid | implemented |
| — | Understand the block | while anything is outstanding the provider cannot accept or start jobs or publish services; declining and cancelling stay open, and the screen says so | implemented |
| — | Settle it | there is nothing to pay in the app — the screen explains the remittance and links to support, with the platform's support address when the API returns one | implemented |
| — | Receive GCash payments | `/gcash-details` saves `gcash_number` and `gcash_name`, which is what makes `payment_instructions` useful to the customer | implemented |

## Tests

`identity_test` covers `CommissionSummary` — the balance, the block, the bookings behind it, and a
provider whose block is actually an identity one.

## Notes

- **The commission is inside the advertised price, not added to it.** The customer pays the
  provider the whole amount, and the platform's share stays with the provider until they remit it
  ([[ADR-021 Direct Payment with Provider-Remitted Commission]], [[Commission Tiers and Settlement]]).
- **The screen is read-only by design.** SkillServe is never in the payment path, so there is
  nothing to charge: a remittance is arranged outside the platform and an administrator records it
  against the ledger.
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
