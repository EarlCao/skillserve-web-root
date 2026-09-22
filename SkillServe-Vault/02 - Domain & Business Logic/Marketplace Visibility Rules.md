---
type: domain
tags: [domain, marketplace, catalog]
sources: [backend/app/Modules/ClientMarketplace/Services/ClientCatalogService.php]
---
# Marketplace Visibility Rules

What the public catalog (`/api/client/v1/categories|services|providers`) shows, from
`ClientCatalogService`.

## A service is public / bookable when

- `services.status = published`
- `services.approval_status = approved`
- `services.is_hidden = false`
- its category has `status = enabled`
- its provider profile is `verification_status = verified`, `suspended_at IS NULL`
- the provider's user is `status = active` (and discoverable)

## A provider is listed when

- `verification_status = verified`, not suspended, active user
- private profiles are excluded where `client_preferences.private_profile = true`
  (discoverable-user filter)

## Discovery filters (query params)

| Param | Applies to | Meaning |
|---|---|---|
| `search` | services, providers | text search (title, provider, category, keywords / name, skills) |
| `category_id`, `subcategory_id` | both | via public services |
| `min_rating` | both | minimum `average_rating` |
| `featured` | providers | `is_featured` |
| `available` | providers | `is_accepting_bookings = true` **and** has a bookable service (false = the opposite) |
| `available_day` | providers | has an availability window on weekday 0–6 |
| `sort`, `direction` | both | `created_at, title, price, average_rating, business_name` |

- Categories/subcategories: only `enabled`.
- Badges shown: only `provider_badges.is_active = true`.
- `featured` service flags are suppressed when `marketplace.featured_services_enabled` is off.

Related: [[Service and Provider Discovery]] · [[Service Approval Lifecycle]] ·
[[Provider Verification Lifecycle]]
