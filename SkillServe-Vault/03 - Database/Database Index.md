---
type: index
tags: [index, database]
---
# Database Index

- [[Database Overview]] — engine, environments, conventions, testing caveats
- [[Entity Relationship Diagram]] — the core schema as a mermaid ERD
- [[Migrations Timeline]] — all 69 migrations in order with their data impact

## Tables (one note each, in `Tables/`)

| Domain | Tables |
|---|---|
| Accounts & auth | [[users]] · [[personal_access_tokens]] · [[client_refresh_tokens]] · [[pending_registrations]] · [[password_reset_tokens]] |
| RBAC | [[roles]] · [[permissions]] · [[Permission Pivot Tables]] |
| Providers | [[provider_profiles]] · [[verification_requests]] · [[verification_documents]] · [[provider_availabilities]] · [[provider_portfolio_items]] |
| Recognition | [[provider_badges]] · [[provider_badge_assignments]] |
| Catalog | [[service_categories]] · [[service_subcategories]] · [[services]] |
| Bookings | [[bookings]] · [[reviews]] · [[messages]] |
| Commissions | [[commission_tiers]] · [[commission_settlements]] |
| Identity | [[identity_verifications]] · [[identity_documents]] · [[identity_verification_events]] |
| Moderation | [[reports]] |
| Support | [[support_tickets]] · [[support_ticket_messages]] |
| Notifications | [[notifications]] · [[announcements]] |
| Mobile | [[client_preferences]] · [[favorite_providers]] |
| Platform | [[settings]] · [[data_archives]] · [[activity_log]] · [[media]] |
| Framework | [[sessions]] · [[cache and cache_locks]] · [[Queue Tables]] |

Back to [[Home]]
