---
type: domain
tags: [domain, time]
sources: [backend/app/Shared/Helpers/BusinessTime.php, backend/config/app.php, backend/.env.example]
---
# Time and Timezone Rules

| Concern | Rule |
|---|---|
| Storage | **UTC** (`APP_TIMEZONE=UTC`, default). Timestamps are stored without zone. |
| Business wall clock | `BUSINESS_TIMEZONE=Asia/Manila` (`config('app.business_timezone')`) |
| Incoming schedule times | `BusinessTime` converts to UTC; a value **without an offset** is read as Manila wall-clock time |
| Mobile app | sends UTC ISO-8601 for create and reschedule (`BookingModel.apiDateTime`) |
| Provider weekly hours | `provider_availabilities.start_time/end_time` are Manila wall clock; booking fit is checked after converting the booking to Manila time |
| Text in notifications | formatted in business time, e.g. "Oct 5, 2026 9:00 AM" |
| System Settings timezone | shown read-only (source `app.business_timezone`) |
| Admin web | displays "Manila time" in booking details (TEST_PLAN A 7.2) |

`day_of_week` uses 0 = Sunday … 6 = Saturday (`ProviderAvailability::DAYS`, discovery filter
`available_day`).

Related: [[ADR-010 UTC Storage with Manila Business Time]] · [[Booking Lifecycle]]
