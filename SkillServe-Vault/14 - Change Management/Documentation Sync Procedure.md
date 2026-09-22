---
type: guide
tags: [change-management, documentation, meta]
---
# Documentation Sync Procedure

Goal: the vault always describes the code as it is. Run this with every change (or at least before
each release).

## 1. Regenerate what is generated

```bash
# from the web project root
python3 "SkillServe-Vault/99 - Meta/Scripts/generate_endpoint_notes.py"   # endpoint notes from route:list
python3 "SkillServe-Vault/99 - Meta/Scripts/check_vault_links.py"          # no broken wikilinks
```

(Also regenerate `api-docs/` and copy it to the mobile repo when endpoints changed —
[[API Documentation Pipeline]].)

## 2. Update hand-written notes touched by the change

| If you changed… | Update |
|---|---|
| a migration | the table note in `03 - Database/Tables`, [[Migrations Timeline]], [[Entity Relationship Diagram]] if relationships changed |
| a business rule / status | the lifecycle note in `02 - Domain & Business Logic` |
| a permission | [[Permission Catalog]], the feature note |
| a setting | [[System Settings Catalog]] |
| an admin page / mobile screen | the feature note in `05`, [[Admin Web Navigation Map]] / [[Mobile Navigation Map]] |
| API calls in a client | [[Frontend-to-API Map]] / [[Mobile-to-API Map]] |
| env vars / deployment | [[Environment Variables]], `10 - Deployment & Infrastructure` notes |
| tests | [[Backend Test Suite]] / [[Mobile Test Suite]] counts |
| a known issue fixed | remove from [[Known Issues and Gaps]], add to [[Changelog]] |
| an open question answered | resolve the row in [[Needs Verification Register]] and edit the note's callout |

## 3. Record

Add a [[Changelog]] entry (date, repos, summary, notes touched).

## 4. Periodic drift check (suggested commands)

```bash
# routes vs endpoint notes (re-run the generator and diff)
git -C . diff --stat SkillServe-Vault/"04 - API Integrations"/Endpoints
# migrations count vs Migrations Timeline
ls backend/database/migrations | wc -l
# frontend modules vs Admin Web Features Index
ls frontend/src/modules
```

## Principles

Code wins over notes; never invent; mark unknowns **Needs Verification**; cite files. See
[[Vault Guide]].
