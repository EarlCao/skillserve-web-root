---
type: architecture
tags: [architecture, queue, scheduler]
sources: [backend/routes/console.php, backend/app/Console/Commands, backend/app/Modules/Notifications/Jobs/SendAnnouncementJob.php, backend/Dockerfile, backend/deploy/render/start.sh]
---
# Background Jobs and Scheduling

## Queue

- Driver: `QUEUE_CONNECTION=database` (`jobs`, `job_batches`, `failed_jobs` tables — [[Queue Tables]]).
- Worker: local `php artisan queue:work --queue=default --sleep=3 --tries=3 --timeout=90` (backend
  container CMD); production `queue:work --queue=default --sleep=1 --tries=3 --timeout=90
  --max-time=3600`, restarted by `supervise` in `start.sh`.

| Queued work | Class | Notes |
|---|---|---|
| Announcement delivery | `Notifications\Jobs\SendAnnouncementJob` | dispatched with `->delay(scheduled_at ?? now())` — scheduling relies on the delayed job, not the scheduler |
| Mobile realtime broadcasts | `ClientNotificationCreated`, `ClientMessageCreated` (`ShouldBroadcast`) | without a worker these never reach phones |
| Admin data-changed signal | `AdminDataChanged` | `ShouldBroadcastNow` — **not** queued |

## Scheduler (`routes/console.php`)

| Schedule | Command | Class | What it does |
|---|---|---|---|
| every minute | `users:unban-expired` | `App\Console\Commands\UnbanExpiredUsers` | lifts temporary bans whose `banned_until` passed; fires `UserUnbanned` (actor null) for audit + email |
| daily | `data-management:purge-expired` | `App\Console\Commands\PurgeExpiredDeletedRecords` | force-deletes soft-deleted records older than `data-management.retention_days` (30) unless dependents exist |

Run by `php artisan schedule:work` in both the local backend container and the production
container.

## Other commands

| Command | Used by |
|---|---|
| `db:seed-if-empty {--fresh}` (`SeedIfEmpty`) | production start-up: seeds only if `roles` is empty, so cold starts don't re-seed |
| `inspire` | framework default |

## Free-tier caveat

On Render's free tier the service sleeps; queue and scheduler sleep with it. A scheduled
announcement whose time passes while idle is sent on the next wake-up (`DEPLOYMENT.md`).

## Related

[[Realtime Architecture]] · [[Data Retention and Deletion]] · [[Render Backend Service]]
