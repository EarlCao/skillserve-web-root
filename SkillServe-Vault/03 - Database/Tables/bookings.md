---
type: table
tags: [database, table, bookings]
domain: Bookings
soft_deletes: true
---
# bookings

Customer bookings. Also the chat thread and the dispute record.

- **Model:** `backend/app/Modules/Bookings/Models/Booking.php`
- **Soft deletes:** yes
- **Migrations:** `2026_08_22_000001_create_bookings_table`, `2026_09_05_000001_add_dispute_management_fields_to_bookings_table`, `2026_09_05_000002_add_disputed_at_index_to_bookings_table`, `2026_09_08_000006_add_client_idempotency_to_bookings`, `2026_09_08_000007_add_client_marketplace_indexes`, `2026_09_17_000001_use_philippine_peso_as_default_currency`, `2026_09_20_000007_add_service_location_to_bookings`, `2026_09_21_000002_add_rescheduled_at_to_bookings`, `2026_09_21_000003_add_payment_settlement_to_bookings`, `2026_09_22_000001_add_cancellation_fee_to_bookings`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `service_id` | FK services |  |
| `client_id` | FK users |  |
| `provider_id` | FK provider_profiles |  |
| `booking_number` | string unique | `BK-` + 12 chars |
| `status` | string default 'pending' | pending / confirmed / active / completed / cancelled / disputed |
| `payment_status` | string default 'unpaid' | unpaid / paid / partially_refunded / refunded |
| `total_price, service_price` | decimal(10,2) |  |
| `platform_fee` | decimal(10,2) default 0 | commission |
| `currency` | string(3) default 'PHP' |  |
| `payment_method, payment_reference` | string null |  |
| `paid_at, payment_recorded_by` |  | settlement |
| `refunded_amount` | decimal(10,2) default 0 |  |
| `refunded_at, refund_reason` |  |  |
| `client_notes, provider_notes` | text null |  |
| `service_address` | string null |  |
| `contact_phone` | string(32) null |  |
| `cancellation_reason` | text null |  |
| `cancellation_fee` | decimal(10,2) null | late cancellation |
| `cancelled_by` | FK users null |  |
| `scheduled_date, scheduled_end_date` | timestamp null | UTC |
| `confirmed_at, started_at, completed_at, cancelled_at, rescheduled_at` | timestamp null |  |
| `dispute_reason` | text null |  |
| `disputed_at` | timestamp null, indexed |  |
| `dispute_status` | string null, indexed | pending / investigated / resolved / rejected / closed |
| `dispute_resolution` | text null |  |
| `dispute_evidence, dispute_notes` | json null |  |
| `dispute_closed_at, dispute_closed_by` |  |  |
| `is_reviewed` | bool default false |  |
| `client_idempotency_key` | string(100) null |  |
| `created_at, updated_at` |  |  |
| `deleted_at, deleted_by` | soft delete |  |

## Indexes & constraints

- unique(booking_number)
- unique(client_id, client_idempotency_key) `bookings_client_idempotency_unique`
- index(status)
- index(payment_status)
- index(booking_number)
- index(client_id, status)
- index(provider_id, status)
- index(service_id, status)
- index(scheduled_date)
- index(created_at)
- index(dispute_status)
- index(disputed_at)
- index(client_id, created_at) `bookings_client_created_index`

## Foreign keys

- service_id → services **cascade**
- client_id → users **cascade**
- provider_id → provider_profiles **cascade**
- cancelled_by, deleted_by, dispute_closed_by, payment_recorded_by → users null on delete

## Notes

- Cascading FKs mean a *hard* delete of a user/service/profile would delete bookings; Data Management blocks force-deletes that have dependents.

## Related

[[Booking Lifecycle]] · [[Payments and Refunds]] · [[Disputes Lifecycle]] · [[Cancellation and Fees]] · [[reviews]] · [[messages]] · [[Database Index]]
