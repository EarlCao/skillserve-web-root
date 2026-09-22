---
type: reference
tags: [deployment, frontend, render]
sources: [DEPLOYMENT.md, frontend/vercel.json, frontend/vite.config.js, backend/config/cors.php]
---
# Frontend Hosting

## Render static site (documented target)

| Setting | Value |
|---|---|
| Repo | `skillserve-web-frontend`, `main`, auto-deploy |
| Build | `npm install && npm run build` → publish `dist` |
| Rewrite | `/*` → `/index.html` (deep links like `/admin/bookings`) |
| Headers (`/*`) | `X-Frame-Options: DENY`, `Content-Security-Policy: frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()` |
| Env (build-time) | `VITE_API_BASE_URL`, `VITE_REVERB_APP_KEY` (= backend `REVERB_APP_KEY`), `VITE_REVERB_HOST` (backend host), `VITE_REVERB_PORT=443`, `VITE_REVERB_SCHEME=https` |

The build injects a CSP `<meta>` tag; frame-blocking must come from real headers.

## Vercel config also present

`frontend/vercel.json` rewrites `/assets/*` and everything else to `/index.html`, and the backend
CORS list includes `https://skillserve-admin-side.vercel.app` and
`https://skillserve-web-admin.vercel.app` (backend commit "Fix CORS config for Vercel frontend",
2026-09-12).

> [!warning] Needs Verification
> Which host serves the live admin web (Render static site, Vercel, or both) and whether the
> security headers are configured there.

Also recommended: keep System Settings → session timeout short (e.g. 480 min).

Related: [[CORS and Security Headers]] · [[Admin Web Frontend Architecture]]
