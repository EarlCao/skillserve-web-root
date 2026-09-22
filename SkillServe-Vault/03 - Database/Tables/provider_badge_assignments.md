---
type: table
tags: [database, table, recognition]
domain: Recognition
soft_deletes: false
---
# provider_badge_assignments

Pivot: which provider holds which badge.

- **Model:** `— (pivot)`
- **Soft deletes:** no
- **Migrations:** `2026_09_05_000011_create_provider_badges_tables`

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | bigint PK |  |
| `provider_profile_id` | FK |  |
| `provider_badge_id` | FK |  |
| `assigned_by` | FK users null, indexed |  |
| `assigned_at` | timestamp default now |  |
| `created_at, updated_at` |  |  |

## Indexes & constraints

- unique(provider_profile_id, provider_badge_id)

## Foreign keys

- provider_profile_id, provider_badge_id → cascade on delete

## Related

[[provider_badges]] · [[Database Index]]
