---
type: adr
adr: 20
status: accepted
tags: [adr, architecture, payments, commissions]
---
# ADR-020 PayMongo Collects Into the Platform Account

| | |
|---|---|
| Status | **Superseded in part** by [[ADR-021 Direct Payment with Provider-Remitted Commission]] (2026-09-25). Its finding — that PayMongo settles into the platform's account — still holds and is *why* ADR-021 was decided; its consequence, that SkillServe would collect booking totals, no longer applies |
| First evidence | 2026-09-25 |

## Context

[[ADR-019 Payment Gateway Abstraction with PayMongo Deferred]] left one question open: can PayMongo
split SkillServe's commission off automatically, or must it be reconciled afterwards?

Checking PayMongo's current documentation before implementing answered it. A standard PayMongo
merchant integration settles the **whole** amount into the merchant's own account. Splitting to
another party is a separate product, *PayMongo Platforms*, which requires onboarding each recipient
as a linked sub-account with its own KYC and a commercial arrangement.

SkillServe has no provider sub-accounts, no onboarding flow for them, and no such agreement.

## Decision

Integrate PayMongo as an ordinary merchant. The full booking total settles into **SkillServe's**
account. GCash uses Payment Intents (create intent → create `gcash` payment method → attach → redirect
→ webhook), which is the flow PayMongo currently documents.

## Consequences

This **inverts who owes whom**, compared with an on-hand job:

| | On-hand | GCash via PayMongo |
|---|---|---|
| Who receives the money | the provider, in cash | SkillServe |
| Commission | provider owes it back → `outstanding` | already retained → `settled` on payment |
| Net to the provider | they already hold it | **SkillServe owes it to them** |

The commission side is handled: `CommissionLedger` asks the gateway whether the platform collected,
so a GCash booking settles its commission the moment the webhook lands and the provider is never
blocked over it.

> [!success] Resolved by ADR-021
> This was the largest open gap: a GCash booking would have left SkillServe holding the provider's
> net with nothing tracking the obligation. It is closed by
> [[ADR-021 Direct Payment with Provider-Remitted Commission]], which removes the cause — the
> customer now pays the provider directly and SkillServe never holds the money.

Other consequences:

- The **webhook** marks a booking paid, never the customer's return redirect, which is a browser
  navigation anyone can forge.
- Webhooks are verified against the raw body: `Paymongo-Signature` is `t=<unix>,te=<test>,li=<live>`,
  the signed string is `<t>.<raw body>`, HMAC-SHA256 under the *webhook* secret, compared timing-safe
  against the segment matching the configured key mode, inside a 5-minute tolerance.
- Events are deduplicated by event id, because PayMongo redelivers. Double-crediting a booking is
  the failure that guards against.
- GCash is limited by PayMongo to ₱1–₱100,000, checked before the call so the customer gets a clear
  message rather than a provider error code.
- With no `PAYMONGO_SECRET_KEY` configured, `config/payments.php` routes GCash back to the manual
  gateway, so a deployment without credentials behaves exactly as it did before.

## Related

[[ADR-019 Payment Gateway Abstraction with PayMongo Deferred]] · [[Payments and Refunds]] ·
[[Commission Tiers and Settlement]] · [[payment_intents]] · [[ADR-007 Payments Recorded Not Processed]]
