---
type: adr
adr: 22
status: accepted
tags: [adr, architecture, payments, commissions, qrph]
sources: [backend/app/Shared/Helpers/QrPh.php, backend/app/Modules/Commissions/Services/CommissionQrPaymentService.php, backend/app/Modules/Payments/Services/PayMongoWebhookProcessor.php]
---
# ADR-022 Payment QR Codes Without Holding Customer Money

| | |
|---|---|
| Status | **Accepted** — builds on [[ADR-021 Direct Payment with Provider-Remitted Commission]] |
| First evidence | 2026-10-11 |

## Context

The owner asked for a QR code with the exact amount in two places: when a customer pays a provider
for a booking, and when a provider pays SkillServe its commission. PayMongo's dynamic QR Ph does
exactly that, but it settles the money into **SkillServe's** PayMongo account — which for a booking
is the escrow position ADR-021 rejected (a payout obligation to every provider, and licensing
exposure for holding other people's money).

## Decision

The two payments get different QR codes, chosen by the owner on 2026-10-11:

| Payment | QR code | Who confirms it |
|---|---|---|
| Customer → provider (booking) | The **provider's own** GCash "Receive via QR" code, with the booking's exact amount written into it by the API (`QrPh::withAmount`) | The provider, as before ("payment received") |
| Provider → SkillServe (commission) | A **PayMongo dynamic QR Ph** code for the exact outstanding total | PayMongo, by its signed `payment.paid` webhook |

- **Bookings stay out of PayMongo.** The provider's QR Ph code carries their own account; the API
  only copies it with the amount (EMV tag `54`), marks it dynamic and re-computes the CRC. The money
  goes straight from customer to provider and SkillServe never sees it. `config/payments.php` still
  maps both booking methods to the manual gateway.
- **The commission is SkillServe's own money**, so collecting it through PayMongo is not escrow.
  It is the only way to pay the commission in the app (the GCash-reference way was retired the
  same day); without PayMongo keys the provider is told to contact support.

## Consequences

- Whether GCash honours a written-in amount on a personal P2P code is a property of GCash, not of
  this code; it must be checked on a real phone. Without it the customer types the amount as before.
- PayMongo charges a fee per QR Ph payment and requires a verified merchant account; live keys need
  `PAYMONGO_ALLOW_LIVE=true` as a deliberate step after a test-mode rehearsal.
- A QR on the phone that must scan it cannot be scanned, so the app saves it to the gallery for
  GCash's "Upload QR".

Related: [[Commission Tiers and Settlement]] · [[PayMongo Setup]] · [[ADR-021 Direct Payment with Provider-Remitted Commission]] · [[ADR Index]]
