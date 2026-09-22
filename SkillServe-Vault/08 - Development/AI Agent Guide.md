---
type: guide
tags: [development, ai-agent, meta]
---
# AI Agent Guide

How an AI coding agent (Claude Code or similar) should use this vault and the repositories.

## 1. Orient in this order

1. [[Home]] → [[Architecture Overview]] → [[Repositories and Codebase Map]].
2. The feature note for the module you are touching (e.g. [[Booking Management]],
   [[Client Booking]]).
3. The domain lifecycle it depends on (e.g. [[Booking Lifecycle]]) and the tables
   ([[Database Index]]).
4. The generated endpoint group ([[Endpoints Index]]) for exact routes and permissions.
5. [[Known Issues and Gaps]] and [[Needs Verification Register]] — don't "fix" something that is a
   documented decision ([[ADR Index]]), and don't rely on a fact marked Needs Verification.

## 2. Treat the vault as a map, the code as the territory

- Every note cites source files. **Re-read the cited code before editing** (AGENT.md: never assume a
  file/route/table exists).
- If code and vault disagree, trust the code and update the vault in the same change
  ([[Documentation Sync Procedure]]).

## 3. Hard rules for this project

| Rule | Source |
|---|---|
| Follow `AGENT.md` (web) / mobile `AGENT.md`; review format `AGENT_REVIEW.md` | repos |
| Backend commands via `docker compose exec backend …` | CLAUDE.md |
| Never run `scripts/fresh-*.sh` or `migrate:fresh` without asking — they wipe the DB | CLAUDE.md |
| Tests extend `Tests\TestCase` (SQLite) | CLAUDE.md |
| Swagger = PHP 8 attributes; regenerate docs and copy to mobile after endpoint changes (`/sync-api-docs`) | CLAUDE.md |
| Explain data impact, deploy order and rollback for migrations | CLAUDE.md / AGENT.md |
| Commit on `main` with conventional commits; pushing deploys | CLAUDE.md |
| Uploads stay on Render's persistent disk — no S3/external buckets | owner decision ([[ADR-008 Uploads on Render Persistent Disk]]) |
| Realtime on Reverb, not Firebase | owner decision ([[ADR-005 Realtime with Reverb instead of Firebase]]) |
| No account deactivation — active or deleted | owner decision ([[ADR-009 No Account Deactivation]]) |
| Customer and provider mobile UIs stay separate and role-guarded | owner decision ([[ADR-017 Separate Customer and Provider Shells]]) |
| Mobile users stay signed in until they sign out | owner decision ([[ADR-003 Sanctum Bearer Tokens with Rotating Mobile Refresh]]) |
| Finish a module end-to-end (API, UI, tests, docs) before starting the next; no proxy implementations | owner working style |

## 4. After a change

1. Run [[Quality Gates]] for the repos you touched (`/verify-changes` skill).
2. If routes changed: `/sync-api-docs`, then
   `python3 "SkillServe-Vault/99 - Meta/Scripts/generate_endpoint_notes.py"`.
3. Update the affected feature/domain/table notes; add a [[Changelog]] entry; close or add rows in
   [[Known Issues and Gaps]] / [[Needs Verification Register]].
4. Report checks run, skipped checks and review findings.

## 5. Stale sources to be careful with

`ADMIN_WEB_MOBILE_READINESS_AUDIT.md` (2026-09-08, superseded), the mobile `AGENT.md` deferred-scope
list, the mobile README design-system section, `api-docs/README.md` "not yet implemented" section,
and one DEPLOYMENT.md troubleshooting line about mobile polling. Details in
[[Known Issues and Gaps]].

Related: [[Claude Code Tooling]] · [[Coding Conventions]] · [[Vault Guide]]
