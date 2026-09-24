---
type: adr
adr: 19
status: accepted
tags: [adr, architecture, payments]
---
# ADR-019 Payment Gateway Abstraction with PayMongo Deferred

| | |
|---|---|
| Status | **Accepted** |
| First evidence | 2026-09-24 |

## Context

SkillServe is to support exactly two payment methods — GCash and on-hand payment — and eventually
collect GCash through PayMongo. The integration is explicitly **not** to be built yet.

The risk in "prepare for it later" work is building either too little (so the eventual integration
rewrites the commission and booking code) or too much (dead schema and unimplemented public
endpoints shipped to production).

## Decision

Introduce a `PaymentGateway` contract with two implementations: `ManualGateway`, which is the real
behaviour today, and `PayMongoGateway`, which is scaffolding and **throws** on every call that would
move money. A `PaymentGatewayManager` resolves the gateway per payment method from
`config/payments.php`.

The commission ledger asks the *gateway* — not the payment method — whether the platform collected
the money. Pointing `gcash` at `paymongo` in configuration is therefore the single switch that makes
GCash commissions settle on payment instead of becoming outstanding.

Deliberately **not** built yet:

- no `payment_intents` table — it would be empty until the integration exists, and unused schema
  still has to be migrated in production;
- no public webhook route — an unimplemented, unauthenticated public endpoint is a liability, and
  the signature check is the only thing protecting it;
- no credentials — `config/payments.php` has empty placeholders and no keys have been issued.

## Consequences

- The rest of the platform is written against the contract, so adding PayMongo does not mean editing
  the booking or commission code.
- A misconfigured gateway name raises rather than falling back to `manual`, because the fallback
  would silently change who holds the money.
- `PayMongoGateway::collect()` throwing is intentional: a gateway that quietly returned success would
  let a booking be marked paid with nothing collected, which is the worst failure this subsystem can
  have. `verifyWebhook()` returns false rather than throwing, so an unverifiable webhook is refused
  instead of becoming a retryable server error.
- Whether PayMongo can split the commission off automatically, or whether it must be reconciled
  afterwards, is **still open**. Nothing in the codebase assumes an answer, and the current API and
  supported Philippine flows must be verified before implementation begins.

## Related

[[Payments and Refunds]] · [[Commission Tiers and Settlement]] · [[ADR-007 Payments Recorded Not Processed]] · [[ADR Index]]
