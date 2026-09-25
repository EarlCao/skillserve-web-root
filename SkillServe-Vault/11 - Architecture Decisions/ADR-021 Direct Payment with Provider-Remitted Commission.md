---
type: adr
adr: 21
status: accepted
tags: [adr, architecture, payments, commissions]
---
# ADR-021 Direct Payment with Provider-Remitted Commission

| | |
|---|---|
| Status | **Accepted** — supersedes the money-flow conclusion of [[ADR-020 PayMongo Collects Into the Platform Account]] |
| First evidence | 2026-09-25 |

## Context

[[ADR-020 PayMongo Collects Into the Platform Account]] established that a standard PayMongo
merchant integration settles the whole booking total into **SkillServe's** account, and left the
resulting problem open: SkillServe would then hold each provider's share with no payout ledger and
no mechanism to send it on. Every provider has their own GCash account, and the platform stored
none of them.

Three ways out were put to the project owner:

1. collect through PayMongo and pay providers out afterwards (needs payout details, a ledger, and
   disbursement — PayMongo has a Disbursements product for this);
2. onboard every provider as a PayMongo linked sub-account so the gateway splits automatically
   (needs per-provider KYC and a commercial agreement);
3. keep payment directly between the two people.

## Decision

**Option 3.** The customer pays the provider directly — GCash to the provider's own number, or cash
on the job — and the provider then owes SkillServe its commission, which they must remit to keep
their account able to take new work.

SkillServe is **never in the payment path** and never holds customer money.

`config/payments.php` therefore routes **both** payment methods to the manual gateway
unconditionally. That is deliberate and must not be changed to `paymongo` for a booking, even when
credentials are present.

## Consequences

- A GCash booking behaves exactly like a cash one. The provider receives the full advertised price,
  and the commission becomes `outstanding` until settled — the mechanism already built in
  [[Commission Tiers and Settlement]] now covers both methods with no special case.
- **No payout obligation, no payout ledger, no escrow.** The gap recorded as KI-28 is closed by
  removing the cause rather than by building a payout system.
- The platform avoids holding other people's money, which in the Philippines can carry BSP
  licensing exposure for a real business. (Noted as a factor in the decision, not as legal advice.)
- The customer needs the provider's GCash details, so `provider_profiles` now carries
  `gcash_number` and `gcash_name`. These are personal payment details: they are shown only to a
  customer with an actual booking, on an unpaid GCash booking, and never through the public catalog.
- `gcash_name` is stored alongside the number so the customer can compare it against the recipient
  name GCash shows before confirming a transfer — that is what catches a mistyped or swapped number.
- **There is no payment guarantee and no escrow.** A customer who pays and receives nothing, or a
  provider who works and is not paid, is a dispute, not something the platform can reverse. That is
  the trade accepted for not handling the money.

## What happens to the PayMongo integration

It stays in the codebase, fully tested, but **unused for bookings**. It is not dead weight: the
defensible use for it is the provider paying their **own outstanding commission** to SkillServe,
which is SkillServe collecting its own revenue rather than handling a third party's money. That is
not built yet.

## Related

[[ADR-020 PayMongo Collects Into the Platform Account]] · [[Commission Tiers and Settlement]] ·
[[Payments and Refunds]] · [[provider_profiles]] · [[ADR-007 Payments Recorded Not Processed]]
