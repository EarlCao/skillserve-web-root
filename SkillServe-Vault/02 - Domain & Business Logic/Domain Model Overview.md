---
type: domain
tags: [domain, model]
sources: [backend/database/migrations, backend/app/Models/User.php, backend/app/Modules/*/Models]
---
# Domain Model Overview

```mermaid
classDiagram
  class User {
    +role_id
    +status
    +email_verified_at
    +deleted_at
  }
  class Role
  class ProviderProfile {
    +business_name
    +verification_status
    +is_featured
    +is_accepting_bookings
    +average_rating
  }
  class VerificationRequest {
    +status
  }
  class VerificationDocument {
    +document_type
    +file_path
  }
  class ProviderAvailability {
    +day_of_week
    +start_time
    +end_time
  }
  class ProviderPortfolioItem
  class ProviderBadge
  class ServiceCategory {
    +status
  }
  class ServiceSubcategory {
    +status
  }
  class Service {
    +status
    +approval_status
    +is_hidden
    +is_featured
    +price
    +currency
  }
  class Booking {
    +status
    +payment_status
    +dispute_status
    +scheduled_date
  }
  class Review {
    +rating
    +status
    +is_reported
  }
  class Message {
    +status
    +read_at
  }
  class Report {
    +reportable
    +reason
    +status
    +moderation_action
  }
  class SupportTicket {
    +status
    +priority
    +category
  }
  class SupportTicketMessage
  class Announcement {
    +target
    +status
    +scheduled_at
  }
  class Notification
  class ClientPreference
  class ClientRefreshToken
  class FavoriteProvider

  User "1" --> "1" Role : role_id
  User "1" --> "0..1" ProviderProfile
  User "1" --> "0..1" ClientPreference
  User "1" --> "*" ClientRefreshToken
  User "1" --> "*" Booking : client_id
  User "*" --> "*" ProviderProfile : favorite_providers
  ProviderProfile "1" --> "*" VerificationRequest
  VerificationRequest "1" --> "*" VerificationDocument
  ProviderProfile "1" --> "*" ProviderAvailability : one per weekday
  ProviderProfile "1" --> "*" ProviderPortfolioItem
  ProviderProfile "*" --> "*" ProviderBadge : provider_badge_assignments
  ProviderProfile "1" --> "*" Service : provider_id
  ServiceCategory "1" --> "*" ServiceSubcategory
  ServiceCategory "1" --> "*" Service
  Service "1" --> "*" Booking
  ProviderProfile "1" --> "*" Booking : provider_id
  Booking "1" --> "0..1" Review
  Booking "1" --> "*" Message
  Report --> User : reportable
  Report --> Review : reportable
  Report --> Message : reportable
  Report --> Service : reportable (admin/seed only)
  User "1" --> "*" SupportTicket : requester_id
  SupportTicket "1" --> "*" SupportTicketMessage
  User "1" --> "*" Notification : notifiable
```

## Key modelling choices

- **Provider identity is the profile, not the user.** `services.provider_id`, `bookings.provider_id`,
  `reviews.provider_id` reference `provider_profiles.id`.
- **A booking is also the conversation and the dispute.** `messages.booking_id` threads chat;
  dispute fields live on `bookings` ([[Disputes Lifecycle]]).
- **Reports are polymorphic** (`reportable_type/id`). The mobile API files reports against
  `User`, `Review` or `Message` only (`ClientReportService::SUBJECT_TYPES`); `Service` reports exist
  in the admin moderation matrix and in the demo `ReportSeeder`, but the app cannot create them.
- **Soft deletes** on users, service categories/subcategories, services, bookings, reviews, messages,
  reports and support tickets ([[Data Retention and Deletion]]).
- **Aggregates are denormalised:** `provider_profiles.average_rating/total_reviews/total_bookings/
  completed_bookings`, `services.average_rating/total_reviews/total_bookings/completed_bookings`
  (review aggregates recalculated by `RecalculateClientReviewAggregatesAction`).
- **Money:** `decimal(10,2)`; `currency` char(3) default `PHP` since migration
  `2026_09_17_000001` ([[ADR-011 Philippine Peso Currency]]).
- **Audit trail:** `activity_log` (spatie) written by `Log…Activity` listeners.

Table-level detail: [[Database Index]] · [[Entity Relationship Diagram]].
