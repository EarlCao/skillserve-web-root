---
type: domain
tags: [domain, reviews]
sources: [backend/app/Modules/ClientMarketplace/Services/ClientReviewService.php, backend/app/Modules/ClientMarketplace/Actions/RecalculateClientReviewAggregatesAction.php, backend/app/Modules/Reviews]
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
| Aggregates recalculated from **active** reviews for the service and provider (`average_rating`, `total_reviews`) | `RecalculateClientReviewAggregatesAction` |
| `bookings.is_reviewed` marks reviewed bookings | `bookings` column |

`GET /api/client/v1/reviews` = the customer's own reviews (with moderation state). Public reviews
appear in provider/service detail from the catalog endpoints.

## Moderation (admin)

| Action | Endpoint | Effect | Permission |
|---|---|---|---|
| Hide | `PATCH /api/reviews/{r}/hide` `{is_hidden: true}` | `status hidden`, `hidden_by/at` | `edit reviews` |
| Restore | same with `is_hidden: false` | `status active` | `edit reviews` |
| Remove | `DELETE /api/reviews/{r}` | `status removed`, `removed_by/at` + soft delete (restorable in Data Management) | `delete reviews` |

`manage reviews` grants all. Notifications (`NotifyReviewModeration`): reviewer on hide/remove/restore;
provider when a hidden review is restored. Reviews can also be hidden/removed via a report
moderation action.

Related: [[Reviews and Ratings Management]] · [[Client Reviews]] · [[reviews]]
