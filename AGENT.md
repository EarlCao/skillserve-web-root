# AI Coding Agent Guide

## Project context

- This repository is a **monolith**: the React frontend lives in `frontend/` and the Laravel backend lives in `backend/`.
- Keep changes within this architecture. Do not split services, introduce microservices, or add a new application/package unless the task explicitly requires it.
- The database is PostgreSQL. Treat database changes as backward-compatible, reviewed application changes.

## General engineering rules

- Before changing any code, inspect the relevant existing implementation and understand how the current flow works, including its callers, data flow, dependencies, and tests where available.
- Do not assume that a file, component, endpoint, model, utility, hook, service, schema, route, or database table exists. Search and verify the current codebase before referencing, extending, importing, or creating it.
- Read the relevant existing code before editing it, and follow the established module, naming, styling, and error-handling patterns.
- Make the smallest complete change that solves the requested problem. Do not modify unrelated behavior, files, dependencies, configuration, or generated assets.
- Do not create files, abstractions, or dependencies unless they have a clear purpose and cannot be served by an existing file, component, utility, hook, or package.
- Reuse verified existing implementations—components, utilities, hooks, services, schemas, layouts, endpoints, and patterns—whenever possible before creating new ones.
- Keep functions, classes, and components small, focused, and named for their responsibility.
- Keep business rules in one authoritative place; do not duplicate business logic, validation rules, constants, or API behavior.
- Prefer clear, maintainable code over clever or overly generic abstractions.
- Preserve public APIs and existing contracts unless the task explicitly calls for a breaking change. When a contract changes, update every affected caller and documentation.
- Never expose secrets, credentials, tokens, or private environment values in code, logs, fixtures, commits, or responses.

## Work AI agents may implement

AI agents may implement or update the following when requested, after inspecting the existing implementation and reusing established project patterns:

- DTOs/data objects, CRUD boilerplate, validation schemas/Form Requests, migrations, API controllers, service classes/functions, API client functions, React components, forms, tests, documentation, types, constants, Swagger/OpenAPI annotations, refactors, and repetitive UI error handling.
- For backend CRUD work, create only the layers the existing feature architecture actually uses. Keep validation in Form Requests/schemas, business logic in services, controllers thin, authorization explicit, responses consistent, and Swagger documentation complete.
- For frontend CRUD work, put HTTP requests in the relevant API/service module; use React Query and feature hooks for server state; reuse shared UI/form/feedback components; and provide loading, error, empty, and success states.
- For migrations, follow the database rules below and explain the migration, data impact, deployment order, rollback plan, and backfill needs before making schema changes.
- For refactors, preserve behavior unless a behavior change is explicitly requested. Update tests, callers, types/constants, and documentation that the refactor affects.
- For repetitive error handling, centralize only genuinely shared behavior through existing error utilities/components or a small reusable addition; do not hide feature-specific errors or introduce a broad abstraction prematurely.
- For tests, cover the relevant happy path, validation, authorization, error/failure paths, and regressions. Prefer focused unit tests for isolated logic and feature/integration tests for HTTP, database, and UI flows.

## Backend rules (`backend/` — Laravel)

### Architecture and responsibility

- Follow Laravel conventions and the existing `App` / `App\\Modules` organization.
- Keep controllers thin: controllers should coordinate the request, authorization, service call, and response only.
- Put complex or reusable business workflows in service classes. Do not put business logic, multi-model workflows, or persistence orchestration in controllers, Form Requests, Eloquent models, or Blade views.
- Use Form Request classes (or established equivalent request validation) to validate and normalize all incoming data. Never trust client input.
- Use policies, gates, middleware, and permission checks for authorization. Authentication alone is not authorization; enforce access control on every protected action.
- Scope queries to the authorized resource and user/tenant context so identifiers cannot be used to access another user's data.
- Avoid N+1 queries; eager-load known relationships and select only the data needed.
- Use database transactions for operations that update multiple related records or must succeed/fail as one unit. Handle failures predictably and avoid partial writes.
- Use Laravel's dependency injection, route model binding where appropriate, Eloquent relationships, and existing project helpers instead of reinventing framework behavior.

### REST API standards

- Follow REST conventions: resource-oriented, plural nouns, correct HTTP methods, meaningful route parameters, and no action verbs in routes unless an action is genuinely non-CRUD.
- Return appropriate HTTP status codes (for example: `200`/`201` on success, `204` for successful no-content deletion, `401` unauthenticated, `403` unauthorized, `404` absent, `422` validation failure, and `409` conflict where applicable).
- Use the project's established JSON response shape consistently for success, errors, pagination, and validation failures. Do not invent a different response envelope for a single endpoint.
- Return API Resources or dedicated response transformers for externally exposed models; do not accidentally expose model internals, hidden fields, or sensitive data.
- Paginate collection endpoints when results can grow, and keep sorting/filtering parameters validated and documented.
- Provide accurate Swagger/OpenAPI documentation for every changed or new API endpoint, including authentication, parameters, request bodies, success responses, validation errors, and error responses. Keep documentation synchronized with implementation.
- Log meaningful server-side context without logging secrets or sensitive personal data. Do not leak internal exception details to API clients in production.

### Quality and security

- Add or update focused feature/unit tests for changed behavior, authorization, validation, and failure cases.
- Format PHP with Laravel Pint. Use the repository's existing testing approach and fixtures/factories.
- Make queues, events, mail, file uploads, and external side effects idempotent or safely retryable when the workflow requires it.

## Frontend rules (`frontend/` — React)

### Structure and state

- Follow the existing feature-module structure in `src/modules/`: keep feature API clients, hooks, schemas, components, pages, and utilities close to the feature.
- Reuse shared components from `src/components/`, shared hooks from `src/hooks/`, utilities from `src/lib/` or `src/utils/`, and providers/contexts before creating alternatives.
- Keep pages and JSX focused on composition and presentation. Put API access in `api/` or shared `services/` modules; place reusable stateful behavior in hooks; move non-trivial transformations and business rules out of JSX.
- Use the existing Axios configuration, React Query client, authentication context, routing guards, and error helpers. Do not create duplicate HTTP clients, global state stores, or auth flows.
- Validate client-side forms through the existing React Hook Form and Zod schema patterns. Client validation complements, but never replaces, server validation.
- Keep server state in React Query (or the established data-fetching pattern), and invalidate/update relevant queries after mutations rather than manually duplicating cache state.

### User experience and accessibility

- Every data-driven screen must handle loading, error, empty, and success states. Reuse the existing `Skeleton`, `ErrorState`, `EmptyState`, `Spinner`, and feedback components where suitable.
- Use existing modal, dialog, toast, form, table, and UI components to keep behavior and visual language consistent.
- Make interactive controls accessible: use semantic elements, labels, keyboard support, focus management, visible focus states, and descriptive feedback.
- Do not show raw backend errors to users. Map expected errors to useful messages and preserve unexpected errors for the error boundary/logging path.
- Avoid unnecessary re-renders and effects; derive values during render where practical and keep hooks dependency-safe.

### Frontend quality

- Follow the configured ESLint rules and existing formatting/style conventions.
- Add or update focused tests when a test setup exists; otherwise provide a clear manual verification path for the changed UI behavior.
- Do not edit `dist/` output directly; change source files and regenerate build artifacts only when they are intentionally tracked and required by the project workflow.

## Database rules (PostgreSQL)

- Do not modify the database schema without explicitly explaining the migration, its data impact, deployment order, rollback plan, and any required backfill.
- Make schema changes through Laravel migrations only. Do not make undocumented manual database changes.
- Use appropriate PostgreSQL data types, foreign keys, indexes, unique constraints, `NOT NULL` constraints, defaults, and check constraints to protect data integrity.
- Index foreign keys and fields used frequently for joins, filtering, ordering, and uniqueness, while avoiding unnecessary indexes.
- Prevent duplicate data through normalization and database constraints; do not rely only on application-level checks for critical uniqueness or relationships.
- Define foreign-key deletion/update behavior deliberately. Never introduce cascading deletes unless the lifecycle is understood and explicitly intended.
- Write migrations that are safe for existing production data. Use staged/backward-compatible migrations for large or risky changes, and avoid long locks or destructive changes during normal deployments.
- Keep database transactions at the service/workflow boundary and avoid holding transactions open during network, queue, mail, or file operations.

## Before finishing any task

1. Review the diff and confirm only task-related files and logic changed.
2. Run the relevant automated checks:
   - Frontend: `npm run lint` and `npm run build` from `frontend/`.
   - Backend: `composer test` and `./vendor/bin/pint --dirty` from `backend/` when dependencies are available.
   - Run targeted tests as well as the relevant full suite when practical.
3. Check affected flows for regressions, including validation, authorization, loading/error/empty states, API contracts, and migrations when applicable.
4. After implementing a feature, perform a separate, read-only senior code review using [`AGENT_REVIEW.md`](AGENT_REVIEW.md). Do not modify code during that review.
5. Clearly report what changed, tests/checks run and their results, review findings (or that none were found), and any checks not run with the reason.
