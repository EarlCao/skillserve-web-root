---
name: sync-api-docs
description: Regenerate SkillServe OpenAPI docs from backend Swagger attributes, rebuild api-docs/ module markdown, and copy api-docs/ into the Flutter mobile app. Use after adding or changing backend endpoints or their Swagger attributes.
---

Regenerate the API docs and keep the mobile app's copy in sync.

1. From the repo root, make sure the backend container is running (`docker compose ps`; start it with `docker compose up -d` if needed).

2. Generate the spec: `docker compose exec backend php artisan l5-swagger:generate`
   - This reads PHP 8 `#[OA\...]` attributes only. An endpoint that is missing from the output almost always has `@OA` docblocks or no attributes at all.

3. Rebuild the docs from the root: `php api-docs/generate.php`
   - This copies `backend/storage/api-docs/api-docs.json` to `api-docs/openapi.json` and rebuilds `api-docs/modules/*.md` and `api-docs/MODULES.md`.
   - It calls `php artisan route:list` on the host. If that fails because `backend/.env` doesn't parse, route method checks are skipped. Mention this in the report.

4. Sync to the mobile app:
   `rsync -a --delete api-docs/ /mnt/c/Users/earlf/OneDrive/Desktop/skill-serve-mobile-application/api-docs/`
   - First check that the mobile `api-docs/` has no files missing from the root copy, because `--delete` would remove them. The mobile `README.md` there differs from the root one, so exclude it: `--exclude README.md`.

5. Report:
   - `git diff --stat` for `api-docs/` in the root repo and in the mobile repo
   - any endpoints that were added or removed under `/api/client/v1`, since those affect the Flutter app

   Don't commit.
