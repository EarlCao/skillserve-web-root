---
type: table
tags: [database, table, payments]
domain: Bookings
soft_deletes: false
sources:
  - backend/database/migrations/2026_10_14_000003_create_booking_payment_proofs.php
  - backend/app/Modules/Bookings/Models/BookingPaymentProof.php
  - backend/app/Modules/Bookings/Services/BookingPaymentProofService.php
---
# booking_payment_proofs

A customer's proof of a GCash payment to the provider — a downpayment or the rest — with a
screenshot, for the provider to confirm or reject. See [[Payments and Refunds#GCash payment proofs (downpayment and the rest)]].

- **Model:** `backend/app/Modules/Bookings/Models/BookingPaymentProof.php`
- **Soft deletes:** no
- **Migration:** `2026_10_14_000003_create_booking_payment_proofs`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `booking_id` | FK bookings | cascade on delete |
| `submitted_by` | FK users null | the customer; null on delete |
| `amount` | decimal(10,2) | 1 … the balance at the time |
| `reference` | string(100) null | GCash reference number |
| `image_path` | string | screenshot on the private `payment_proofs` disk; never exposed — read via `image_url` / `download_path` |
| `status` | string(20) default 'pending' | pending / confirmed / rejected |
| `reviewed_by` | FK users null | the provider; null on delete |
| `reviewed_at` | timestamp null |  |
| `review_note` | text null | why it was rejected (shown to the customer) |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- index(booking_id, status) — "is one waiting?" and the booking's list

## Rules

- One `pending` proof per booking at a time (checked under the booking's row lock).
- Confirming adds `amount` to [[bookings]] `amount_paid` via `BookingPaymentService::receive()`.
- A force-deleted booking takes its screenshot files with it (`Booking::forceDeleting`); deleting a
  proof row removes its file after commit.

## Related

[[bookings]] · [[Payments and Refunds]] · [[Database Index]]
