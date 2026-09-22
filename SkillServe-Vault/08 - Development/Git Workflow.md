---
type: guide
tags: [development, git, workflow]
sources: [CLAUDE.md, DEPLOYMENT.md, git logs of all repos]
---
# Git Workflow

| Rule | Detail |
|---|---|
| Repos | root, `backend/`, `frontend/` (all `github.com/EarlCao/*`), mobile (separate GitHub account) — run git **inside the repo you changed** |
| Branch | work directly on `main` (no `dev` branch) |
| Deploys | Render auto-deploys every push to `main` of backend and frontend → **a push is a release** |
| Commit style | conventional commits: `feat(bookings): …`, `fix(frontend): …`, `docs(api): …` |
| Before pushing | run checks ([[Quality Gates]]); if endpoints changed regenerate api-docs and copy to mobile; if a migration was added confirm it is additive or has a rollback |
| Order | deploy the backend before a frontend/app build that depends on it |
| Rollback | redeploy the previous successful deploy in Render; migrations stay applied |

## Observed history

Commit messages are mixed: many recent ones follow conventional style (`feat: …`, `docs: …`), many
are terse (`fix`, `latest fix`, `add`). See [[Commit Timeline]].

## This vault

The vault lives in the **root repo** (`SkillServe-Vault/`). Commit vault updates with
`docs(vault): …` messages.

> [!warning] Needs Verification
> Whether the team wants `.obsidian/` workspace files committed (only minimal config files were
> created: `app.json`, `core-plugins.json`, `templates.json`, `bookmarks.json`). Obsidian will add
> `workspace.json` on first open — consider ignoring it.

Related: [[Release Workflow]] · [[Documentation Sync Procedure]]
