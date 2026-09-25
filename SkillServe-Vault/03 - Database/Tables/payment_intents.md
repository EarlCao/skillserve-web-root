---
type: table
tags: [database, table, payments]
domain: Payments
soft_deletes: false
---
# payment_intents

One row per attempt to collect a booking's total through a payment gateway. A customer may abandon a
GCash redirect and start again, so a booking can have several attempts and only one succeeds.

- **Model:** `backend/app/Modules/Payments/Models/PaymentIntent.php`
- **Soft deletes:** no
- **Migrations:** `2026_09_25_000002_create_payment_intents_table`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | |
| `booking_id` | FK, indexed with status | |
| `gateway` | string default `paymongo` | so a later provider needs no second table |
| `external_id` | string null, **unique** | PayMongo's `pi_…`; lets a webhook resolve exactly one attempt |
| `client_key` | string null | `#[Hidden]` — returned once to the paying customer, never logged or listed |
| `status` | string | awaiting_payment_method / awaiting_next_action / processing / succeeded / failed |
| `amount_minor` | bigint | centavos, as the gateway counts them |
| `currency` | char(3) default PHP | |
| `idempotency_key` | string **unique** | sent as PayMongo's `Idempotency-Key`; a retry resumes rather than duplicates |
| `redirect_url` | text null | where the customer authorises |
| `last_event_id` | string null | the last webhook applied, so a redelivery is a no-op |
| `paid_at` | timestamp null | |
| `failure_reason` | text null | |
| `created_at, updated_at` | | |

## Why the duplicate guards

PayMongo retries webhook delivery, and idempotency is a hard requirement for anything touching money.
Three separate guards stop a booking being credited twice: the unique `idempotency_key`, the
`last_event_id` check inside a row lock, and `BookingPaymentService::markPaid` refusing a booking
that is not `unpaid`.

## Foreign keys

- booking_id → bookings cascade on delete

## Related

[[Payments and Refunds]] · [[ADR-020 PayMongo Collects Into the Platform Account]] · [[bookings]] · [[Database Index]]
