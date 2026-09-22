---
type: guide
tags: [testing, strategy]
sources: [TEST_PLAN.md, skill-serve-mobile-application/TEST_PLAN.md, backend/phpunit.xml, backend/tests/TestCase.php]
---
# Testing Strategy

| Layer | Tooling | Scope | Gaps |
|---|---|---|---|
| Backend API | PHPUnit 12 feature tests (`RefreshDatabase`, in-memory **SQLite**) | every module: validation, authorization, state rules, notifications, audit logging, settings enforcement, realtime signals | PostgreSQL-only behaviour (CHECK constraints, partial indexes, pgBouncer) not exercised |
| Backend style | Laravel Pint | PSR-12/Laravel style | — |
| Admin web | ESLint + `vite build` | lint, compile, chunk size | **no component/unit/E2E test framework** — verified by UAT rows + backend tests of each endpoint |
| Mobile | `flutter analyze`, `flutter test` (widget + unit) | models, controllers, route guards, token storage, realtime presence, background checks, overflow sweeps at phone sizes | no integration tests against a live backend in the repo |
| Dependencies | `composer audit`, `npm audit` | known CVEs | results reported 2026-09-21 (composer clean); not re-run in this audit |
| UAT | `TEST_PLAN.md` (admin + mobile) | every requirement on the **deployed** system | Result columns empty |
| End-to-end smoke | `DEPLOYMENT.md` → Go-live checklist step 6 | two phones, full lifecycle | not yet recorded |

## Test infrastructure details

- `phpunit.xml` suites: `Unit` (`tests/Unit`), `Feature` (`tests/Feature`), `Modules`
  (`app/Modules/**/Tests/*Test.php`).
- `tests/TestCase.php` forces `DB_CONNECTION=sqlite`, `DB_DATABASE=:memory:` in `putenv`, `$_ENV`
  and `$_SERVER` **before** boot, so Docker's pgsql env can never make `RefreshDatabase` wipe the
  live database ([[ADR-013 In-Memory SQLite for Tests]]).
- `composer test` = `config:clear` + `artisan test`.
- Flutter `test/flutter_test_config.dart` mocks secure storage per test and resets
  `TokenStorage`.

Related: [[Quality Gates]] · [[UAT and Traceability]]
