---
type: guide
tags: [development, conventions, rules]
sources: [AGENT.md, CLAUDE.md, AGENT_REVIEW.md, skill-serve-mobile-application/AGENT.md]
---
# Coding Conventions

Distilled from the project rulebooks. The originals win if they differ: `AGENT.md` (web),
`CLAUDE.md`, `AGENT_REVIEW.md`, and the mobile repo's `AGENT.md`.

## General

- Monolith: backend in `backend/`, admin web in `frontend/`; **don't split services or add apps**.
- Inspect existing code, callers and tests before changing anything; never assume a file, route,
  model or table exists — verify.
- Smallest complete change; reuse existing components/services/utilities; no new dependencies or
  abstractions without clear need.
- One authoritative place for each business rule (services / `BookingRules` / config).
- Preserve public API contracts; if one changes, update every caller and the docs.
- Never expose secrets.

## Backend (Laravel)

- Thin controllers: authorize → Form Request → service → Resource → envelope.
- Business logic in **services** (and single-purpose **actions**), not controllers/requests/models.
- Validate every input in Form Requests; whitelist sort/filter params.
- Authorization via policies/gates/permission checks on every protected action; scope queries to
  the owner.
- Avoid N+1 (eager-load, select needed columns); transactions for multi-row writes; lock rows for
  state transitions.
- REST: plural resources, correct verbs, proper status codes; the `{success,message,data,errors,meta}`
  envelope with `meta.pagination`.
- **Swagger with PHP 8 attributes only**; regenerate docs after endpoint changes.
- Tests: every test extends `Tests\TestCase` (forces SQLite); module tests in
  `app/Modules/<Name>/Tests/Feature`.
- Format with Pint (`./vendor/bin/pint --dirty`; a Claude Code hook runs it on edited PHP files).
- Migrations: backward-compatible, explain data impact / deploy order / rollback / backfill.
- Money in pesos (`PHP`).

## Frontend (React)

- Plain JS/JSX, relative imports, React Compiler on.
- Feature code calls `src/services/api.js`, not raw axios. Query keys in `QUERY_KEYS`.
- Server state in React Query; invalidate after mutations.
- Forms: react-hook-form + zod schemas in `modules/*/schemas`.
- Gate UI with `hasCapability`/`hasAnyCapability` and routes with `RequirePermission`; permission
  strings identical to Spatie.
- Every data screen has loading/error/empty/success states; reuse `Skeleton`, `ErrorState`,
  `EmptyState`, `Spinner`; never show raw backend errors.
- Money: `formatCurrency` + `DEFAULT_CURRENCY`.
- `npm run lint` + `npm run build` must pass (a hook runs ESLint on edited files). No test framework.

## Mobile (Flutter)

- MVC-ish: models, services, `ChangeNotifier` controllers, views.
- **No mock data** — services call the API via `ApiClient`; undocumented endpoints → throw
  `UnsupportedError` instead of faking.
- Use only `/api/client/v1/*`; never admin endpoints; no admin features in the app.
- Keep customer and provider UIs separate and role-guarded.
- Controllers catch service errors and show empty/error states.
- `flutter analyze` and relevant tests before completion.

## Review standard

After implementing a feature: run checks, then a **read-only** senior review per `AGENT_REVIEW.md`
(CRITICAL/HIGH/MEDIUM/LOW with evidence, impact, recommendation). Report checks run and any
skipped.

> [!warning] Mobile AGENT.md is partly stale
> Its "Deferred Scope" and "API Integration Status" sections still list as *not implemented*
> things that now exist (dispute evidence upload, provider support tickets, presence/typing,
> closed-app notifications via WorkManager, review and message reporting, profile update).
> Trust the code and [[Client Mobile Features Index]]. See [[Known Issues and Gaps]].

Related: [[AI Agent Guide]] · [[Backend Development Guide]] · [[Frontend Development Guide]]
