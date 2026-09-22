---
type: requirements
tags: [foundation, requirements]
sources: [SkillServe_Admin_Web_Functionalities.pdf, skill-serve-mobile-application/SkillServe_User_Mobile_Functionalities_Flutter.pdf]
---
# Requirements Sources

Two PDFs are the product requirements. Requirement IDs used across the project docs are
**A x.y** (admin web) and **M x.y** (mobile), e.g. `A 7.7 Cancel Booking`, `M 5.6 Cancel Booking`.

| Document | Location | Pages | Scope |
|---|---|---|---|
| `SkillServe_Admin_Web_Functionalities.pdf` | web root | 8 | 19 admin modules |
| `SkillServe_User_Mobile_Functionalities_Flutter.pdf` | mobile repo root | 5 | 17 mobile modules |

The PDF text was extracted during the audit; module names below are verbatim.

## Admin Web — 19 modules

| # | Module | Functionalities | Feature note |
|---|---|---|---|
| 1 | Admin Authentication | 1.1 Login · 1.2 Logout · 1.3 RBAC · 1.4 Password Management · 1.5 Session Management | [[Admin Authentication]] |
| 2 | Admin Dashboard | 2.1 User · 2.2 Service · 2.3 Booking · 2.4 Verification · 2.5 Reports summaries · 2.6 Recent Activities · 2.7 Platform Analytics | [[Admin Dashboard]] |
| 3 | User Management | 3.1 View · 3.2 Search · 3.3 Filter · 3.4 Profile · 3.5 Edit · 3.6 Suspend · 3.7 Activate · 3.8 Ban · 3.9 Delete | [[User Management]] |
| 4 | Service Provider Management | 4.1 View · 4.2 Profile · 4.3 Review Verification · 4.4 Approve · 4.5 Reject · 4.6 Request Info · 4.7 Suspend · 4.8 Remove Verification | [[Service Provider Management]] |
| 5 | Service Management | 5.1 View · 5.2 Search · 5.3 Filter · 5.4 Review · 5.5 Approve · 5.6 Reject · 5.7 Edit · 5.8 Hide · 5.9 Feature · 5.10 Delete | [[Service Management]] |
| 6 | Service Category Management | 6.1 View · 6.2 Add · 6.3 Edit · 6.4 Delete · 6.5 Subcategories · 6.6 Enable/Disable | [[Service Category Management]] |
| 7 | Booking Management | 7.1 View · 7.2 Details · 7.3 Search · 7.4 Filter · 7.5 Monitor Status · 7.6 History · 7.7 Cancel · 7.8 Disputes | [[Booking Management]] |
| 8 | Reviews and Ratings Management | 8.1 View · 8.2 Search · 8.3 Filter · 8.4 Reported · 8.5 Hide · 8.6 Remove · 8.7 Restore | [[Reviews and Ratings Management]] |
| 9 | Reports and Moderation | 9.1 User · 9.2 Service · 9.3 Review · 9.4 Message reports · 9.5 Investigate · 9.6 Notes · 9.7 Resolve · 9.8 Reject · 9.9 Moderation Action | [[Reports and Moderation]] |
| 10 | Dispute Management | 10.1 View · 10.2 Details · 10.3 Evidence · 10.4 History · 10.5 Notes · 10.6 Resolve · 10.7 Close | [[Dispute Management]] |
| 11 | Notifications and Announcements | 11.1 View · 11.2 Send · 11.3 Target · 11.4 Schedule · 11.5 History | [[Notifications and Announcements]] |
| 12 | Provider Recognition | 12.1 Badges · 12.2 Assign · 12.3 Remove · 12.4 Featured · 12.5 Top-Rated | [[Provider Recognition]] |
| 13 | Reports and Analytics | 13.1 User · 13.2 Provider · 13.3 Service · 13.4 Booking · 13.5 Review · 13.6 System Activity reports · 13.7 Export | [[Reports and Analytics]] |
| 14 | Support Management | 14.1 View · 14.2 Search · 14.3 Filter · 14.4 Details · 14.5 Respond · 14.6 Assign · 14.7 Resolve | [[Support Management]] |
| 15 | Admin Management | 15.1 View · 15.2 Add · 15.3 Edit · 15.4 Activate/Deactivate · 15.5 Roles · 15.6 Permissions | [[Admin Management]] |
| 16 | Security and Audit Log | 16.1 View · 16.2 Search · 16.3 Filter · 16.4 Login Activity · 16.5 Security Events | [[Security and Audit Logs]] |
| 17 | System Settings | 17.1 General · 17.2 Marketplace · 17.3 Booking · 17.4 Notification · 17.5 Policies · 17.6 System | [[System Settings]] |
| 18 | Data Management | 18.1 Export · 18.2 Archive · 18.3 Restore Archived · 18.4 Deleted Records | [[Data Management]] |
| 19 | Logout | 19.1 Admin Logout | [[Logout (Admin)]] |

## Mobile — 17 modules

| # | Module | Functionalities | Feature note(s) |
|---|---|---|---|
| 1 | User Authentication and Account | 1.1 Registration · 1.2 Login · 1.3 Logout · 1.4 Password · 1.5 Session · 1.6 Account Status | [[Client Authentication and Account]] |
| 2 | User Profile | 2.1 View · 2.2 Edit · 2.3 Photo · 2.4 Account Status · 2.5 Activity History | [[Client Profile]] |
| 3 | Service Discovery | 3.1 Browse · 3.2 Search · 3.3 Filter · 3.4 Details · 3.5 Featured · 3.6 Categories | [[Service and Provider Discovery]] |
| 4 | Service Provider Discovery | 4.1 Browse · 4.2 Search · 4.3 Filter · 4.4 Profile · 4.5 Verification Status · 4.6 Recognition | [[Service and Provider Discovery]] |
| 5 | Booking | 5.1 Create · 5.2 Details · 5.3 My Bookings · 5.4 Status · 5.5 History · 5.6 Cancel · 5.7 Report/Dispute | [[Client Booking]] |
| 6 | Reviews and Ratings | 6.1 Submit Review · 6.2 Rating · 6.3 View · 6.4 Report Review · 6.5 My Reviews | [[Client Reviews]] |
| 7 | Messaging and Communication | 7.1 Conversations · 7.2 Send · 7.3 Receive · 7.4 History · 7.5 Report Message | [[Client Messaging]] |
| 8 | Notifications and Announcements | 8.1 View · 8.2 Booking · 8.3 Service notifications · 8.4 Announcements · 8.5 Targeted · 8.6 History | [[Client Notifications]] |
| 9 | Service Provider Account | 9.1 Become a Provider · 9.2 Profile · 9.3 Submit Verification · 9.4 Status · 9.5 Respond to Info Request · 9.6 Restrictions | [[Provider Onboarding and Registration]] · [[Provider Account and Verification]] |
| 10 | Service Management for Providers | 10.1 Create · 10.2 My Services · 10.3 Edit · 10.4 Submit for Review · 10.5 Approval Status · 10.6 Availability | [[Provider Service Management]] · [[Provider Availability]] |
| 11 | Dispute | 11.1 Submit · 11.2 My Disputes · 11.3 Details · 11.4 Evidence · 11.5 Updates | [[Client Disputes]] |
| 12 | Support | 12.1 Create · 12.2 My Tickets · 12.3 Details · 12.4 Reply · 12.5 Status | [[Client Support]] |
| 13 | Search and Personalized Discovery | 13.1 Global Search · 13.2 Suggestions · 13.3 Recent Searches · 13.4 Featured · 13.5 Top-Rated | [[Search and Personalized Discovery]] |
| 14 | User Settings and Preferences | 14.1 Notification · 14.2 Privacy · 14.3 App Preferences · 14.4 Policies | [[Client Settings and Preferences]] |
| 15 | Data and Account Control | 15.1 View Data · 15.2 Deactivation · 15.3 Deletion · 15.4 Restriction Info | [[Client Data and Account Control]] |
| 16 | Mobile Security | 16.1 Secure Auth · 16.2 Session Expiry · 16.3 Unauthorized Access · 16.4 Security Notifications | [[Mobile Security]] |
| 17 | Logout | 17.1 User Logout | [[Logout (Mobile)]] |

> [!info] Deliberate deviation — M 15.2 Request Account Deactivation
> Not implemented by design: accounts are active or deleted (soft delete, restorable by an admin).
> See [[ADR-009 No Account Deactivation]].

## Related documents in the repos

| File | Purpose |
|---|---|
| `TEST_PLAN.md` (root, mobile) | UAT + traceability matrix per requirement → [[UAT and Traceability]] |
| `PENDING_FIXES.md` (root, mobile) | master list of open work → [[Roadmap and Open Work]] |
| `ADMIN_WEB_MOBILE_READINESS_AUDIT.md` | historical audit dated 2026-09-08 (62% estimate) — superseded → [[Changelog]] |
| `IMPLEMENTATION_PROMPT_TEMPLATE.md`, mobile `AI_AGENT_PROMPT_TEMPLATE.md` | prompts used to build modules with AI agents |
| mobile `module-by-module` | recommended mobile module build order (text file) |
