---
type: domain
tags: [domain, reviews]
sources: [backend/app/Modules/ClientMarketplace/Services/ClientReviewService.php, backend/app/Modules/Reviews/Actions/RecalculateRatingAggregatesAction.php, backend/app/Modules/Reviews]
---
# Reviews and Ratings Rules

`reviews.status` ∈ `active, hidden, removed` (+ `deleted_at` soft delete). `is_reported` flag.

## Writing (mobile, customers only — `EnsureClient`)

| Rule | Source |
|---|---|
| Only for **completed** bookings the customer owns (else 404 / 422 "Reviews can only be created or updated for completed bookings.") | `ClientReviewService` |
| One review per booking — DB unique on `reviews.booking_id`; second attempt → **409** | migration + service |
| `rating` integer 1–5, `comment` ≤2000 | `StoreClientReviewRequest` |
| Editable later (`PUT/PATCH /api/client/v1/reviews/{id}`) | `UpdateClientReviewRequest` |
| Ratings recalculated on create and edit — see [[#How ratings are calculated]] | `RecalculateRatingAggregatesAction` |
| `bookings.is_reviewed` marks reviewed bookings | `bookings` column |

`GET /api/client/v1/reviews` = the customer's own reviews (with moderation state). Public reviews
appear in provider/service detail from the catalog endpoints.

## How ratings are calculated

Customers rate a **booking of a service**; nobody rates a provider directly. The provider's rating
is built from its services' ratings.

| Stored value | Rule |
|---|---|
| `services.average_rating` | Average of the service's **active** reviews, rounded to 2 decimals. `0.00` with no active review. |
| `services.total_reviews` | Count of the service's active reviews. |
| `provider_profiles.average_rating` | Average of the provider's **rated services'** ratings, each service counting **once** however many reviews it has. |
| `provider_profiles.total_reviews` | Count of all the provider's active reviews. |

Worked example — five services rated 3.50, 5.00, 4.60, 3.30 and 3.50:
(3.50 + 5.00 + 4.60 + 3.30 + 3.50) / 5 = **3.98**. With 2, 1, 5, 10 and 2 reviews, a plain average
of all 20 reviews would have been 3.85 — the 10-review service would have outweighed the rest.

- **Services with no active review are left out**, not counted as zero, so a new service never
  drags the provider down.
- **Deleted and hidden services still count.** Their reviews were earned on real bookings, and a
  provider must not be able to lift their rating by deleting a poorly rated service.
- Hidden and removed reviews count for nothing, in either figure.

`RecalculateRatingAggregatesAction` (Reviews module) is the only code that writes these values. It
runs whenever a review's rating or active state changes: customer create/edit, admin
hide/restore/remove (directly or through a report moderation action), and a Data Management restore
of a removed review. Every screen — mobile catalog, admin Provider Management, Provider
Recognition's list and Top Rated — reads the stored `provider_profiles.average_rating`; none
computes its own average. Before 2026-09-30 the provider figure was the plain average of all
reviews, admin screens computed it themselves, and admin moderation did not recalculate at all;
the `2026_09_30_000001_recalculate_ratings_from_service_ratings` migration rewrote the stored values.

## Moderation (admin)

| Action | Endpoint | Effect | Permission |
|---|---|---|---|
| Hide | `PATCH /api/reviews/{r}/hide` `{is_hidden: true}` | `status hidden`, `hidden_by/at` | `edit reviews` |
| Restore | same with `is_hidden: false` | `status active` | `edit reviews` |
| Remove | `DELETE /api/reviews/{r}` | `status removed`, `removed_by/at` + soft delete (restorable in Data Management) | `delete reviews` |

Every row above recalculates the service and provider ratings. `manage reviews` grants all. Notifications (`NotifyReviewModeration`): reviewer on hide/remove/restore;
provider when a hidden review is restored. Reviews can also be hidden/removed via a report
moderation action.

Related: [[Reviews and Ratings Management]] · [[Client Reviews]] · [[reviews]] · [[provider_profiles]] ·
[[services]] · [[Provider Recognition]]
