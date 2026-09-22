---
type: guide
tags: [deployment, release, workflow]
sources: [DEPLOYMENT.md, CLAUDE.md]
---
# Release Workflow

No `dev` branch: each repo is developed on `main`, and Render deploys every push to `main` of the
backend and frontend repos — **a push is a release**.

1. Develop locally with Docker (local Postgres on 5433).
2. Run the checks in the repo you changed ([[Quality Gates]]).
3. Try it at `http://localhost:5173` / `http://localhost:8000/api` and from the app
   (`--dart-define-from-file=env/local.json`).
4. If endpoints changed: `l5-swagger:generate` → `php api-docs/generate.php` → copy `api-docs/` into
   the Flutter repo → regenerate vault endpoint notes.
5. If a migration was added: confirm it is additive or has a rollback (the container runs
   `migrate --force` on start). **Deploy the backend before** a frontend or app build that depends on
   it.
6. Commit and push to `main` (conventional commits). Watch the Render deploy log, then check
   `GET /api/health` (database and storage `up`).

**Rollback:** Render dashboard → redeploy the previous successful deploy of that service. Migrations
that already ran stay applied → they must be backward-compatible.

Mobile releases are separate: build a signed APK against production ([[Mobile Release Build]]).

Related: [[Git Workflow]] · [[Go-Live Checklist]] · [[Change Management Index]]
