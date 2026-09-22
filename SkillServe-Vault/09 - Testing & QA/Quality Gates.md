---
type: guide
tags: [testing, quality, ci]
sources: [AGENT.md, CLAUDE.md, TEST_PLAN.md, DEPLOYMENT.md]
---
# Quality Gates

**CI:** only the backend repo has `.github/workflows/` — the four files inherited from the Laravel
skeleton (`tests.yml`, `issues.yml`, `pull-requests.yml`, `update-changelog.yml`). `tests.yml` runs
`php artisan test` on PHP 8.3/8.4/8.5 with SQLite for pushes to **`master`** or `*.x`, for pull
requests, and on a daily cron — the project pushes to `main`, so pushes do not trigger it.
**Needs Verification:** whether GitHub Actions is enabled and the daily run passes. Frontend, root
and mobile repos have no CI. In practice gates are run manually (or with `/verify-changes`) before
pushing to `main`, which deploys.

| Repo changed | Must pass | Command |
|---|---|---|
| backend | feature tests | `docker compose exec backend composer test` |
| backend | style | `docker compose exec backend ./vendor/bin/pint --dirty` (or `--test`) |
| backend | dependency audit (periodic) | `docker compose exec backend composer audit` |
| frontend | lint | `cd frontend && npm run lint` |
| frontend | build (no chunk > 500 kB) | `cd frontend && npm run build` |
| frontend | dependency audit (periodic) | `npm audit` |
| mobile | analyze | `tool/wsl-flutter.sh analyze` |
| mobile | tests | `tool/wsl-flutter.sh test` |
| mobile (release) | build | `flutter build apk --release --dart-define-from-file=env/production.json` |
| any endpoint change | docs regenerated + copied to mobile + vault endpoint notes | [[API Documentation Pipeline]] |
| any migration | additive or rollback documented | [[Migrations Timeline]] |
| any feature | read-only senior review per `AGENT_REVIEW.md` | `/verify-changes` |

After deploy: `GET /api/health` → database `up`, storage `up`.

Related: [[Release Workflow]] · [[Testing Strategy]]
