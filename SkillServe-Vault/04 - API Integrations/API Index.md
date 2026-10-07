---
type: index
tags: [index, api]
---
# API Integrations Index

- [[API Conventions]] — envelope, errors, pagination, headers, rate limits, idempotency
- [[Authentication Flows]] — admin tokens, mobile access/refresh tokens, background token
- [[Realtime Channels and Events]] — Reverb contract for clients
- [[API Documentation Pipeline]] — Swagger attributes → OpenAPI → `api-docs/` → mobile copy
- [[Frontend-to-API Map]] — which admin page calls which endpoint
- [[Mobile-to-API Map]] — which mobile feature calls which endpoint
- [[External Integrations]] — NeonDB, Render, Brevo, Google, Reverb

## Endpoint reference (generated)

[[Endpoints Index]] — 221 route entries in 33 groups, regenerated from `php artisan route:list` by
`99 - Meta/Scripts/generate_endpoint_notes.py`. Each group lists method, path, controller action,
middleware and the permission checked.

## Base URLs

| Environment | Admin API | Client API |
|---|---|---|
| Local | `http://localhost:8000/api` | `http://localhost:8000/api/client/v1` |
| Production | `https://<backend>.onrender.com/api` | `…/api/client/v1` |

> [!warning] Needs Verification — production hostname
> The mobile app defaults to `https://skillserve-web-backend.onrender.com/api`
> (`lib/core/config/app_config.dart`, `env/production.json`), while `DEPLOYMENT.md` uses
> `skillserve-backend.onrender.com` in its examples. The CORS list names
> `skillserve-frontend.onrender.com`, `skillserve-admin-side.vercel.app` and
> `skillserve-web-admin.vercel.app`. Confirm the real live hosts in the Render/Vercel dashboards.

Swagger UI: `/api/documentation`, raw spec `/docs` (hidden in production unless
`SWAGGER_UI_ENABLED=true`).

Back to [[Home]]
