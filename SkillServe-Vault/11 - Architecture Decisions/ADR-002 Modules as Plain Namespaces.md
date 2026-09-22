---
type: adr
adr: 2
status: accepted
tags: [adr, architecture]
---
# ADR-002 Modules as Plain Namespaces

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-08-07 |

## Context

`nwidart/laravel-modules` was installed (commit "Add stubs … in Nwidart modules"), but a lighter structure was wanted.

## Decision

Feature modules are plain PSR-4 namespaces in `app/Modules/<Name>`; routes, policies and listeners are wired manually (routes/api.php, AppServiceProvider, ClientMarketplaceServiceProvider).

## Consequences

- Explicit, greppable wiring; no module auto-discovery.
- Every new module needs manual registration — easy to forget listeners/policies.
- `nwidart/laravel-modules` and `config/modules.php` remain installed but unused for layout.

## Evidence

- `CLAUDE.md ("nwidart/laravel-modules is not used for layout")`
- `composer.json autoload`
- `backend/routes/api.php`

## Related

[[Backend Architecture]] · [[ADR Index]]
