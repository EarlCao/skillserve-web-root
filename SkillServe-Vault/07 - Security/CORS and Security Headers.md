---
type: guide
tags: [security, cors, headers]
sources: [backend/config/cors.php, frontend/vite.config.js, DEPLOYMENT.md, backend/deploy/render/nginx.conf]
---
# CORS and Security Headers

## CORS (`backend/config/cors.php`)

- Paths: `api/*`, `sanctum/csrf-cookie`; all methods and headers; `supports_credentials: true`;
  `max_age: 0`.
- **Allowed origins** (exact): `https://skillserve-admin-side.vercel.app`,
  `https://skillserve-web-admin.vercel.app`, `https://skillserve-frontend.onrender.com`,
  `http://localhost:5173`, `http://localhost:3000`, `http://127.0.0.1:5173`, plus `FRONTEND_URL` and
  comma-separated `FRONTEND_URLS`.
- Pattern: any `http://localhost:*` / `127.0.0.1:*` **only when `APP_ENV=local`** (for
  `flutter run -d chrome`).
- Wildcards like `*.vercel.app` / `*.onrender.com` were removed on 2026-09-21 (PENDING_FIXES M7;
  test `CorsTest`).
- Native mobile apps are not subject to CORS.

## Admin web headers

| Control | Where | Status |
|---|---|---|
| Content-Security-Policy `<meta>` (`default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https:; font-src 'self' data:; connect-src 'self' https: wss:; worker-src 'self'; manifest-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'`) | injected by a Vite plugin in production builds | in code |
| `X-Frame-Options: DENY`, `Content-Security-Policy: frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()` | Render static-site **Headers** tab (dashboard) | documented in `DEPLOYMENT.md`; **Needs Verification** that they are configured |
| Zod without `eval` | frontend config | done (M5) |

> [!note] Local dev
> The CSP is not applied in `vite` dev mode (HMR needs inline scripts and a local websocket). The
> production CSP's `connect-src 'self' https: wss:` would block a plain `http://` API — production
> must use HTTPS.

## Backend

- `ForceJsonResponse` on every API route; exceptions never leak stack traces or SQL
  ([[Backend Architecture]]).
- Swagger hidden in production unless `SWAGGER_UI_ENABLED=true`.
- nginx (production) sets `client_max_body_size 20m` and turns 502/504 into a JSON 503.

Related: [[Frontend Hosting]] · [[Security Findings]]
