---
type: reference
tags: [development, ai-agent, tooling]
sources: [.claude/settings.json, .claude/skills/sync-api-docs/SKILL.md, .claude/skills/verify-changes/SKILL.md, CLAUDE.md]
---
# Claude Code Tooling

Project-level Claude Code configuration in the root repo's `.claude/`.

## Skills

| Skill | What it does |
|---|---|
| `/sync-api-docs` | ensures the backend container runs → `php artisan l5-swagger:generate` → `php api-docs/generate.php` → `rsync -a --delete --exclude README.md` into the mobile repo's `api-docs/` (after checking nothing would be deleted) → reports `git diff --stat` in both repos and any `/api/client/v1` endpoint changes. Doesn't commit. |
| `/verify-changes [focus]` | finds changed repos (`git status` in root, backend, frontend) → frontend `npm run lint` + `npm run build` → backend `composer test` + `pint --dirty` (via Docker) → read-only review per `AGENT_REVIEW.md` → reports passes/failures/skips and findings. Doesn't fix unless asked. |

## Hooks (`.claude/settings.json`, PostToolUse on Write|Edit)

| Hook | Trigger | Action |
|---|---|---|
| Pint | edited `backend/**/*.php` (not `vendor/`) | `./vendor/bin/pint --quiet <file>` |
| ESLint | edited `frontend/**/*.js|jsx` (not `node_modules/`, `dist/`) | `eslint --no-warn-ignored <file>`; failure blocks with exit 2 |

## Other agent aids in the repos

- `CLAUDE.md` (root) — short operational guide pointing to `AGENT.md`.
- `IMPLEMENTATION_PROMPT_TEMPLATE.md` (web) and `AI_AGENT_PROMPT_TEMPLATE.md` (mobile) — prompts
  used to build modules.
- Root `.kimchi/ferments/` — empty folder of unknown purpose (**Needs Verification**).

Related: [[AI Agent Guide]] · [[API Documentation Pipeline]]
