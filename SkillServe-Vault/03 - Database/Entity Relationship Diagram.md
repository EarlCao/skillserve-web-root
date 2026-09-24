---
type: architecture
tags: [database, erd]
sources: [backend/database/migrations]
---
# Entity Relationship Diagram

Core business tables (framework, cache, queue and RBAC pivots omitted). FK delete behaviour in
brackets.

```mermaid
erDiagram
  roles ||--o{ users : "role_id [restrict]"
  users ||--o| provider_profiles : "user_id [cascade]"
  users ||--o| client_preferences : "user_id [cascade]"
  users ||--o{ client_refresh_tokens : "user_id [restrict]"
  users ||--o{ bookings : "client_id [cascade]"
  users ||--o{ reviews : "reviewer_id [restrict]"
  users ||--o{ messages : "sender_id/receiver_id [restrict]"
  users ||--o{ reports : "reporter_id [null]"
  users ||--o{ support_tickets : "requester_id [null]"
  users ||--o{ favorite_providers : "user_id [cascade]"
  provider_profiles ||--o{ favorite_providers : "[cascade]"
  provider_profiles ||--o{ verification_requests : "[cascade]"
  verification_requests ||--o{ verification_documents : "[cascade]"
  provider_profiles ||--o{ provider_availabilities : "[cascade] one per weekday"
  provider_profiles ||--o{ provider_portfolio_items : "[cascade]"
  provider_profiles ||--o{ provider_badge_assignments : "[cascade]"
  provider_badges ||--o{ provider_badge_assignments : "[cascade]"
  provider_profiles ||--o{ services : "provider_id [cascade]"
  service_categories ||--o{ service_subcategories : "[cascade]"
  service_categories ||--o{ services : "category_id [cascade]"
  service_subcategories ||--o{ services : "subcategory_id [null]"
  services ||--o{ bookings : "service_id [cascade]"
  provider_profiles ||--o{ bookings : "provider_id [cascade]"
  bookings ||--o| reviews : "booking_id unique [restrict]"
  services ||--o{ reviews : "[restrict]"
  provider_profiles ||--o{ reviews : "[restrict]"
  bookings ||--o{ messages : "booking_id [null]"
  support_tickets ||--o{ support_ticket_messages : "[cascade]"
  commission_tiers ||--o{ bookings : "commission_tier_id [null]"
  bookings ||--o| commission_settlements : "booking_id unique [cascade]"
  provider_profiles ||--o{ commission_settlements : "[cascade]"
  users ||--o| identity_verifications : "user_id unique [null, survives deletion]"
  identity_verifications ||--o{ identity_documents : "[cascade]"
  identity_verifications ||--o{ identity_verification_events : "[cascade]"

  users {
    bigint id PK
    bigint role_id FK
    string email UK
    string status
    timestamp deleted_at
  }
  provider_profiles {
    bigint id PK
    bigint user_id FK
    string verification_status
    bool is_featured
    bool is_accepting_bookings
  }
  services {
    bigint id PK
    bigint provider_id FK
    bigint category_id FK
    string status
    string approval_status
    bool is_hidden
  }
  commission_tiers {
    bigint id PK
    decimal min_amount
    decimal max_amount "null = open ended"
    decimal percentage
    bool is_active
    timestamp deleted_at
  }
  commission_settlements {
    bigint id PK
    bigint booking_id FK "unique"
    decimal amount
    string method
    timestamp settled_at
  }
  identity_verifications {
    bigint id PK
    bigint user_id FK "unique; null once purged"
    string status
    string id_number_hash "HMAC, partial UK"
    string id_number_last4
    timestamp released_at
  }
  bookings {
    bigint id PK
    string booking_number UK
    string status
    string payment_status
    string commission_status
    decimal platform_fee
    string dispute_status
    timestamp scheduled_date
  }
  reviews {
    bigint id PK
    bigint booking_id UK
    tinyint rating
    string status
  }
  reports {
    bigint id PK
    string reportable_type
    bigint reportable_id
    string status
  }
```

Polymorphic links (not drawn): `reports.reportable` → users / reviews / messages / services;
`notifications.notifiable` → users; `activity_log.subject` and `.causer`; `personal_access_tokens.tokenable` → users;
`media.model`.

Related: [[Domain Model Overview]] · [[Database Index]]
