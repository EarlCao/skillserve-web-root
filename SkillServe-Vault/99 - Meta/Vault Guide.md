---
type: meta
tags: [meta, vault, conventions]
---
# Vault Guide

How this vault is organised and how to keep it true to the code.

## Principles

1. **Code is the source of truth.** A note describes what exists, never what should exist. Plans go
   in [[Roadmap and Open Work]]; opinions go in ADRs as "Consequences".
2. **Cite sources.** Name the file (`backend/app/Modules/Bookings/Services/DisputeService.php`) so a
   reader or agent can re-check it.
3. **Never invent.** If the code does not answer a question, write
   `> [!warning] Needs Verification` with what is unknown, and add a row to
   [[Needs Verification Register]].
4. **One topic per note**, linked with wikilinks (`[[Note Name]]`). Each folder has an `… Index` note.
5. **Generated notes are not edited by hand.** Files marked `generated: true` (the endpoint notes)
   are rebuilt by scripts in `99 - Meta/Scripts`.

## Folder conventions

| Folder | Note types |
|---|---|
| `00 - Project Foundation` | overview, requirements, repos, stack, glossary |
| `01 - System Architecture` | architecture notes with mermaid diagrams |
| `02 - Domain & Business Logic` | entity and lifecycle notes (state machines) |
| `03 - Database/Tables` | one note per table (template: [[Template - Table]]) |
| `04 - API Integrations/Endpoints` | **generated** endpoint groups |
| `05 - Features & Modules/*` | one note per requirement module (template: [[Template - Feature]]) |
| `11 - Architecture Decisions` | ADRs (template: [[Template - ADR]]) |
| `12 - Troubleshooting` | symptom → cause → fix (template: [[Template - Troubleshooting]]) |
| `14 - Change Management` | changelog entries (template: [[Template - Change Entry]]) |
| `99 - Meta` | this guide, templates, scripts, registers, audit reports |

New notes created from the Obsidian UI land in `99 - Meta/Inbox` — move them into the right folder.

## Frontmatter

Every note starts with YAML properties:

```yaml
---
type: feature | table | adr | api-endpoints | architecture | domain | guide | index | moc | meta | troubleshooting
tags: [..]
status: implemented | partial | missing | needs-verification   # features only
platform: admin-web | client-mobile | provider-mobile | backend  # where it applies
sources: [relative/paths]                                        # optional
---
```

## Tags in use

`#backend` `#frontend` `#mobile` `#database` `#api` `#security` `#domain` `#adr` `#deployment`
`#testing` `#needs-verification` `#known-issue` `#generated`.

## Callouts

- `> [!warning] Needs Verification` — unconfirmed fact. Always add to the register.
- `> [!bug] Known issue` — a defect found in code. Always add to [[Known Issues and Gaps]].
- `> [!info]` — context. `> [!tip]` — how-to shortcut.

## Keeping the vault synchronized

Follow [[Documentation Sync Procedure]]. In short: after a change, regenerate endpoint notes with
`python3 "SkillServe-Vault/99 - Meta/Scripts/generate_endpoint_notes.py"`, update the feature, table
and domain notes you touched, and add an entry to [[Changelog]].

## Templates and scripts

| Item | Purpose |
|---|---|
| [[Template - Feature]], [[Template - Table]], [[Template - ADR]], [[Template - Troubleshooting]], [[Template - Change Entry]] | starting points for new notes (Obsidian core *Templates* plugin points at `99 - Meta/Templates`) |
| `99 - Meta/Scripts/generate_endpoint_notes.py` | rebuild `04 - API Integrations/Endpoints` from `php artisan route:list` (read-only; needs local PHP + `backend/vendor`) |
| `99 - Meta/Scripts/check_vault_links.py` | report broken wikilinks (exit 1 if any) |

Registers: [[Needs Verification Register]] · [[Known Issues and Gaps]] · [[Audit Report 2026-09-22]].

## Related

[[Home]] · [[AI Agent Guide]] · [[Audit Report 2026-09-22]]
