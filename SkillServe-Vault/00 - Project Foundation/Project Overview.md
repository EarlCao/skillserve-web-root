---
type: overview
tags: [foundation, overview]
sources: [README.md, SkillServe_Admin_Web_Functionalities.pdf, skill-serve-mobile-application/README.md, skill-serve-mobile-application/SkillServe_User_Mobile_Functionalities_Flutter.pdf]
---
# Project Overview

**SkillServe** is a services marketplace. Customers find and book local service providers; providers
publish services, manage jobs and get verified; administrators approve, moderate and run the
platform. The mobile app's README gives the project title as *"Bridging Service Accessibility and
Talent Visibility Through an Integrated Skills Marketplace and Service Management Platform."*

The root repo describes itself as **"Group 6 — Web Project"** (folder `web-project-bsit3blk3group6`).
The mobile Flutter package is still named `skilllink_mobile` in `pubspec.yaml` (an earlier
"SkillLink" name — see [[Known Issues and Gaps]]).

## The three applications

| App | Code | Users | Talks to |
|---|---|---|---|
| **Backend API** | `backend/` — Laravel 13, PHP 8.3 | — | PostgreSQL, storage disk, Reverb, Brevo, Google |
| **Admin Web** | `frontend/` — React 19 + Vite | super-admin, admin, custom staff roles | `/api/*` + Reverb |
| **Mobile App** | `skill-serve-mobile-application/` — Flutter | guests, customers, providers | `/api/client/v1/*` + Reverb |

See [[Architecture Overview]] for how they connect.

## What the platform does (as implemented)

- **Accounts:** email + OTP registration, Google sign-in, customer and provider accounts, admin staff
  with roles and permissions ([[User Types and Roles]]).
- **Catalog:** categories/subcategories, provider services that need admin approval, featured
  services and providers, badges ([[Service Approval Lifecycle]]).
- **Bookings:** customer books a service at a time inside the provider's weekly hours; provider
  confirms → starts → completes; cancellations with late fees; reschedule ([[Booking Lifecycle]]).
- **Payments are recorded, not processed:** paid off-platform, marked paid by the provider or an
  admin; admins record refunds ([[Payments and Refunds]]).
- **Trust & safety:** provider verification with document upload, reviews, reports, moderation
  actions, disputes with photo evidence ([[Provider Verification Lifecycle]], [[Disputes Lifecycle]],
  [[Reports and Moderation Lifecycle]]).
- **Communication:** booking-scoped chat with presence and typing, notifications (in-app, realtime,
  closed-app polling), admin announcements, support tickets.
- **Administration:** dashboard, analytics and CSV exports, audit logs, system settings that the API
  enforces, data management (archives, deleted records, 30-day purge).

## Status at audit time

Both `PENDING_FIXES.md` files (root and mobile, last audited 2026-09-21) list **no open Critical,
High, Medium or Low items**; what remains are owner go-live actions. This vault's own audit found a
few additional gaps — see [[Known Issues and Gaps]] and [[Project Status]].

## Related

[[Requirements Sources]] · [[Tech Stack]] · [[Module Completion Matrix]]
