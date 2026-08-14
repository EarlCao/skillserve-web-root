# Senior Implementation Review Guide

## Purpose

Use this guide after an AI agent implements a feature or significant change. Act as a senior software developer performing an independent review.

This is a **read-only review**: do not modify code, create files, run destructive commands, or apply fixes. Inspect the implementation, its relevant existing code, tests, routes, API contracts, migrations, and callers before reporting findings.

## Review prompt

Use the following task prompt, replacing the feature name as needed:

> Review the `<feature name>` implementation as a senior software developer. Do not modify anything. Inspect the current implementation and relevant existing code. Look specifically for security issues, authorization issues, validation gaps, race conditions, database problems, duplicated logic, unnecessary complexity, poor error handling, Swagger/OpenAPI documentation gaps, performance issues, and architectural inconsistencies. Rank findings as CRITICAL, HIGH, MEDIUM, or LOW, and explain the reason, impact, affected code, and recommended remediation for each finding.

## Required review areas

- **Security:** authentication, authorization, data exposure, injection risks, mass assignment, insecure uploads, sensitive-data handling, rate limiting, and unsafe logging.
- **Authorization:** policies, gates, middleware, permission checks, and resource/user/tenant query scoping for every protected action.
- **Validation:** server-side validation for every input source, validation consistency, allowed values, pagination/filter/sort validation, and client/server schema alignment where relevant.
- **Concurrency and transactions:** concurrent requests, duplicate submission, lost updates, idempotency, transaction boundaries, side effects before commit, locking, and retry safety.
- **Database:** migration safety, PostgreSQL data types, constraints, foreign keys, indexes, N+1 queries, query shape, duplicate data, and data-integrity risks.
- **Design and architecture:** adherence to the monolith and feature-module structure, controller/service boundaries, duplicated business logic, unnecessary abstractions, reuse of existing implementations, and separation of concerns.
- **API and Swagger:** REST conventions, status codes, consistent responses, error responses, pagination, exposed fields, Swagger/OpenAPI accuracy, request/response schemas, and authentication documentation.
- **Frontend:** API calls in service modules, data-fetching/caching behavior, form validation, loading/skeleton/error/empty states, accessibility, large JSX/business logic, and shared component/hook reuse.
- **Performance and reliability:** N+1 queries, missing indexes, inefficient loops or payloads, unnecessary renders/effects, caching implications, timeouts, background work, and error recovery.
- **Tests and regressions:** meaningful coverage of happy paths, validation, authorization, failure cases, and potentially affected existing behavior.

## Finding severity

- **CRITICAL:** Exploitable security issue, unauthorized data/action access, data loss/corruption, outage risk, or a defect that blocks a core production workflow.
- **HIGH:** Serious correctness, security, integrity, or reliability risk that is likely to affect users or important workflows, but has a narrower impact or prerequisite.
- **MEDIUM:** Material maintainability, performance, consistency, or edge-case issue that should be addressed before the feature grows or is broadly relied upon.
- **LOW:** Minor robustness, clarity, documentation, test, style, or maintainability improvement with limited current impact.

## Report format

Return only the review report. Do not claim an issue without evidence, and do not list speculative findings as facts.

For each finding, include:

1. **Severity:** `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.
2. **Title:** a short, precise description.
3. **Location:** file path and relevant line(s), endpoint, component, service, migration, or flow.
4. **Evidence and reason:** what the implementation does and why it is a problem.
5. **Impact:** the concrete security, correctness, data, performance, or maintenance consequence.
6. **Recommendation:** a focused, practical remediation that respects existing architecture and reuse opportunities.

End with:

- A short summary grouped by severity with finding counts.
- Any assumptions, unverified areas, or checks that could not be completed.
- If no findings are identified, explicitly state: `No findings identified after reviewing the inspected scope.`
