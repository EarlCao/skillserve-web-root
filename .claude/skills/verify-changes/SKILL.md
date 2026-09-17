---
name: verify-changes
description: Run the SkillServe "before finishing" checks (frontend lint/build, backend tests/pint) on the repos that changed, then do a read-only senior review per AGENT_REVIEW.md. Use after implementing a feature or before committing.
---

Verify the current changes the way AGENT.md requires. Optional focus: $ARGUMENTS

1. Find what changed. Root, `backend/` and `frontend/` are separate git repos, so run `git status --short` in each of them.

2. Frontend (only if `frontend/` changed), in `frontend/`:
   - `npm run lint`
   - `npm run build`

3. Backend (only if `backend/` changed), from the repo root:
   - Make sure the stack is up: `docker compose ps`. If `backend` isn't running, start it with `docker compose up -d` and wait for it to be ready.
   - `docker compose exec backend composer test` (for a quick check, run `php artisan test --filter=<Name>` first, then the full suite)
   - `docker compose exec backend ./vendor/bin/pint --dirty`
   - If controllers or Swagger attributes changed, the API docs are out of date. Tell the user to run `/sync-api-docs`.

4. Review. Follow `AGENT_REVIEW.md` as a read-only senior review of the changed code only: don't edit anything during this step. Rank findings CRITICAL/HIGH/MEDIUM/LOW with evidence (file:line), impact and a recommendation. If nothing is found, say exactly: "No findings identified after reviewing the inspected scope."

5. Report:
   - each check you ran and whether it passed or failed, quoting the failing output
   - any check you skipped, and why
   - the review findings

   Don't fix findings unless the user asks.
