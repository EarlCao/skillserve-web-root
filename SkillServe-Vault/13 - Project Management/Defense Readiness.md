---
type: plan
tags: [project-management, defense]
sources: [PENDING_FIXES.md → Defense readiness, TEST_PLAN.md → Design decisions]
---
# Defense Readiness

The project is evaluated by a panel ("the panel may ask" — DEPLOYMENT.md). `PENDING_FIXES.md`
defines three deliverables:

| ID | Deliverable | State |
|---|---|---|
| D1 | Requirements traceability matrix | ✅ both `TEST_PLAN.md` files exist; Result columns empty |
| D2 | Demo script and data: customer books → provider accepts → reschedule → job done → provider records payment → review → report → admin moderates → dispute → admin resolves → notifications on both phones | script defined; not yet recorded as rehearsed; use `scripts/fresh-demo.sh` only on a local/demo DB |
| D3 | Architecture and security talking points | see below |

## Talking points (from repo docs, each backed by a vault note)

- Monolith (Laravel API + React admin) plus Flutter client → [[ADR-001 Monolith with Separate Mobile Client]]
- Sanctum tokens with rotating refresh tokens → [[Token and Session Management]]
- Role/permission model (Spatie) → [[Authorization and RBAC]]
- Realtime via Reverb, no Firebase — and why → [[ADR-005 Realtime with Reverb instead of Firebase]]
- Closed-app notifications via WorkManager polling with a read-only token → [[ADR-006 Closed-App Notifications via WorkManager]]
- Uploads on a Render persistent disk → [[ADR-008 Uploads on Render Persistent Disk]]
- Audit logging of admin actions → [[Audit Logging]]
- Payments recorded, not processed → [[ADR-007 Payments Recorded Not Processed]]
- No account deactivation (M 15.2) → [[ADR-009 No Account Deactivation]]

## Risks to address before presenting

KI-01 (closed-app notifications) and KI-02 (password recovery) would surface in a live demo of M 8.2
/ M 1.4. See [[Known Issues and Gaps]].

> [!warning] Needs Verification
> Defense date, panel composition and grading rubric are not in the repos.
