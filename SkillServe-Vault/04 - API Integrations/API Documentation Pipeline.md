---
type: guide
tags: [api, documentation, swagger]
sources: [backend/app/Shared/Swagger/OpenApi.php, backend/config/l5-swagger.php, api-docs/generate.php, .claude/skills/sync-api-docs/SKILL.md, CLAUDE.md]
---
# API Documentation Pipeline

```mermaid
flowchart LR
  A["PHP 8 OA attributes<br/>on controllers"] -->|php artisan l5-swagger:generate| B[backend/storage/api-docs/api-docs.json]
  B -->|php api-docs/generate.php| C[api-docs/openapi.json<br/>api-docs/modules/*.md<br/>api-docs/MODULES.md]
  C -->|rsync (exclude README.md)| D[mobile repo api-docs/]
  B --> E[Swagger UI /api/documentation]
  R[vault script generate_endpoint_notes.py] -->|php artisan route:list| F[SkillServe-Vault/04 - API Integrations/Endpoints]
```

## Rules

- **PHP 8 attributes only** (`#[OA\Post(...)]`). l5-swagger v11's analyser ignores `@OA` docblocks
  — an endpoint missing from the spec almost always has docblocks or no attributes.
- Global info and shared schemas: `app/Shared/Swagger/OpenApi.php` (e.g. `ApiEnvelope`).
- `L5_SWAGGER_GENERATE_ALWAYS=true` locally regenerates on every docs request.
- In production Swagger UI and `/docs` are hidden by `EnsureSwaggerUiEnabled` unless
  `SWAGGER_UI_ENABLED=true`.

## Commands (from the web root)

```bash
docker compose exec backend php artisan l5-swagger:generate
php api-docs/generate.php
rsync -a --delete --exclude README.md api-docs/ /mnt/c/Users/earlf/OneDrive/Desktop/skill-serve-mobile-application/api-docs/
python3 "SkillServe-Vault/99 - Meta/Scripts/generate_endpoint_notes.py"
```

The Claude Code skill `/sync-api-docs` performs the first three steps (it doesn't commit).
`generate.php` also calls `php artisan route:list` on the host to check route methods; if that
fails (e.g. `backend/.env` doesn't parse) the method check is skipped.

## State at audit (2026-09-22)

- `api-docs/openapi.json` documents **201** operations; the route table has **212** API operations
  (excluding Swagger's own). The difference is only: the `PATCH` aliases of 8 update routes
  (documented as `PUT`), `GET /api/health`, and `GET|POST /api/broadcasting/auth`. No documented
  operation is missing from the code.
- The mobile repo's `api-docs/` matches the root copy except `README.md` (intentionally different).

> [!bug] Stale text in `api-docs/README.md`
> Its "What is NOT yet implemented (gaps for Flutter)" section says Reverb is only connected to the
> web admin and recommends FCM — both outdated (the app has a Reverb client and WorkManager
> polling). See [[Known Issues and Gaps]].

Related: [[Documentation Sync Procedure]] · [[Endpoints Index]]
