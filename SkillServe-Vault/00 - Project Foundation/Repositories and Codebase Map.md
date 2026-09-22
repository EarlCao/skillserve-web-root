---
type: reference
tags: [foundation, repositories, git]
---
# Repositories and Codebase Map

SkillServe is **four separate git repositories**. The root repo's `.gitignore` excludes `/backend`
and `/frontend`, which are cloned *inside* it.

| Repo | Local path | Remote | Branch | Commits (audit) | First commit |
|---|---|---|---|---|---|
| Root (docs, compose, scripts, api-docs, **this vault**) | `web-project-bsit3blk3group6/` | `github.com/EarlCao/skillserve-web-root` | `main` | 29 | 2026-08-07 |
| Backend | `…/backend/` | `github.com/EarlCao/skillserve-web-backend` | `main` | 79 | 2026-07-26 |
| Frontend (admin web) | `…/frontend/` | `github.com/EarlCao/skillserve-web-frontend` | `main` | 56 | 2026-07-28 |
| Mobile | `/mnt/c/Users/earlf/OneDrive/Desktop/skill-serve-mobile-application` | `github.com/boylesjohndominique-netizen/skill-serve-mobile-application` | `main` | 33 | 2026-07-29 |

All work happens directly on `main`; Render auto-deploys `main` of backend and frontend
([[Git Workflow]]).

## Root repo layout

```
web-project-bsit3blk3group6/
├── AGENT.md, AGENT_REVIEW.md, CLAUDE.md     # agent rulebook, review format, Claude Code guide
├── README.md, DEPLOYMENT.md                 # setup and Render/Neon deployment
├── PENDING_FIXES.md, TEST_PLAN.md           # open work, UAT traceability
├── ADMIN_WEB_MOBILE_READINESS_AUDIT.md      # historical audit (2026-09-08)
├── IMPLEMENTATION_PROMPT_TEMPLATE.md
├── SkillServe_Admin_Web_Functionalities.pdf # admin requirements
├── docker-compose.yml                       # local stack (db, backend, frontend, reverb)
├── scripts/fresh-demo.sh, fresh-admin.sh    # migrate:fresh + seed (WIPES the DB)
├── api-docs/                                # generated OpenAPI + per-module markdown
├── .claude/                                 # Claude Code settings (hooks) and skills
├── SkillServe-Vault/                        # this Obsidian vault
├── backend/   (own repo)
└── frontend/  (own repo)
```

## Backend layout (`backend/`)

```
app/
├── Console/Commands/     PurgeExpiredDeletedRecords, SeedIfEmpty, UnbanExpiredUsers
├── Models/User.php       the only model outside modules
├── Modules/<Name>/       21 feature modules (Actions, Controllers, Events, Listeners, Models,
│                         Notifications, Policies, Requests, Resources, Routes, Services, Tests)
├── Providers/AppServiceProvider.php   policies, gates, event listeners, rate limiters
└── Shared/               base classes, ApiResponder, middleware, realtime tracker, helpers
bootstrap/app.php         middleware aliases, exception → envelope rendering, broadcasting
config/                   incl. client-auth, system-settings, data-management, cors, api-cache
database/migrations       69 migrations (see [[Migrations Timeline]])
database/seeders          11 seeders (see [[Seeding and Demo Data]])
deploy/render/            start.sh, nginx.conf (production container)
routes/                   api.php, channels.php, console.php, web.php
tests/                    Feature + Unit (plus module tests under app/Modules/*/Tests)
Dockerfile, Dockerfile.render
```

Size at audit: 555 files under `app/`, ≈46,400 lines of PHP. Details: [[Backend Architecture]].

## Frontend layout (`frontend/src/`)

```
app/config.js        API base URL + Reverb config resolution
components/          common/, feedback/, forms/, tables/, ui/
constants/index.js   QUERY_KEYS, STORAGE_KEYS, APP_EVENTS, DEFAULT_CURRENCY
contexts/, providers/ Auth and Theme context + providers
hooks/               useDebounce, useDisclosure, useLocalStorage, useNetworkStatus, usePagination
layouts/             AdminLayout, AuthLayout, BlankLayout
lib/                 errors, queryClient, utils
modules/<name>/      18 feature folders (api/, components/, hooks/, pages/, schemas/)
routes/              index.jsx (router), lazyPages.jsx
services/            api.js (envelope helpers), axios.js, echo.js, liveUpdates.js
utils/               index.js (formatCurrency…), permissions.js
```

183 files. Details: [[Admin Web Frontend Architecture]].

## Mobile layout (`lib/`)

```
core/      config, constants, models, services (api_client, token_storage, realtime_client,
           background_notifications, maintenance_state), theme, utils, widgets
features/  auth, booking, marketplace, messaging, notifications, payments, profile, provider,
           reports, reviews, settings, support  (controllers/ models/ services/ views/)
routes/app_router.dart   go_router table + role guard
main.dart
```

187 Dart files, ≈29,200 lines. Other folders: `test/` (27 files), `api-docs/` (copy of the root
one), `env/local.json` + `env/production.json` (only `API_BASE_URL`), `android/`, `branding/`,
`assets/`, `tool/wsl-flutter.sh`. Details: [[Mobile App Architecture]].

## Related

[[Tech Stack]] · [[Git Workflow]] · [[Commit Timeline]]
