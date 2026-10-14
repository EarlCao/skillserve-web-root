---
type: table
tags: [database, table, communication]
domain: Communication
soft_deletes: false
sources:
  - backend/database/migrations/2026_10_14_000002_create_inquiries_and_link_messages.php
  - backend/app/Modules/ClientCommunication/Models/Inquiry.php
---
# inquiries

A customer's conversation with a provider **before any booking** ("chat before booking"). One row per
customer–provider pair; its messages live in [[messages]] with `inquiry_id` set (and `booking_id`
null).

- **Model:** `backend/app/Modules/ClientCommunication/Models/Inquiry.php`
- **Soft deletes:** no
- **Migration:** `2026_10_14_000002_create_inquiries_and_link_messages`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK | addresses the thread: `/api/client/v1/inquiries/{id}/messages` |
| `customer_id` | FK users | the customer who started it |
| `provider_profile_id` | FK provider_profiles | the provider asked |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(customer_id, provider_profile_id) — one conversation per pair (also serves customer lookups)
- index(provider_profile_id)

## Foreign keys

- customer_id → users **restrict**; provider_profile_id → provider_profiles **restrict** — an
  account with a conversation is never hard-deleted under it ([[Data Management]] lists it as a
  dependent).

## Rules

- Only a **customer** starts one (`POST /inquiries`, throttled 30/hour), and only with a provider the
  marketplace lists ([[Marketplace Visibility Rules]]); asking again returns the same row.
- Either party then reads and writes like a booking chat (`InquiryPolicy`, same rules as
  `BookingMessagePolicy`); presence/typing on `presence-inquiry-chat.{id}`.
- Listed in the Messages inbox once someone has written in it, and only for app builds that ask with
  `include_inquiries=1`.

## Related

[[Client Messaging]] · [[messages]] · [[Database Index]]
