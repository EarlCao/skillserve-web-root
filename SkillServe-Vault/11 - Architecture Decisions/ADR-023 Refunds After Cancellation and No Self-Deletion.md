---
type: adr
adr: 23
status: accepted
tags: [adr, architecture, payments, refunds, accounts, anti-fraud]
sources: [backend/app/Modules/Bookings/Services/BookingRefundService.php, backend/app/Modules/Commissions/Services/TransactionEligibility.php, backend/app/Modules/ClientAuthentication/Controllers/ClientAuthController.php]
---
# ADR-023 Refunds After Cancellation and No Self-Deletion

| | |
|---|---|
| Status | **Accepted** — builds on [[ADR-021 Direct Payment with Provider-Remitted Commission]] |
| First evidence | 2026-10-14 |

## Context

Customers can now pay a provider before the work — a downpayment or all of it — through GCash proofs
the provider confirms ([[booking_payment_proofs]]). SkillServe never holds that money (ADR-021), so
when a booking is cancelled the money sits with the provider. The owner decided on 2026-10-14 that
**the provider must return it**, that **both sides verify** the return, that a provider must not be
able to escape the obligation by **deleting their account**, and asked for safeguards against scams.

## Decision

- **A refund opens on every cancellation of a paid booking** (customer, provider or admin), for what
  was confirmed as paid — less the customer's own recorded late-cancellation fee when *they*
  cancelled late (0% unless an admin sets it). Table [[booking_refunds]].
- **Two-sided verification.** The provider marks it returned with a **required screenshot** (and
  optional GCash reference); the customer then **confirms** it arrived (recorded as `refunded` on the
  booking) or reports **not received** with an explanation.
- **Deadline and automatic consequences.** System Settings → Booking → `downpayment_refund_days`
  (default 3). A provider whose refund is past due, reported not received, or found not returned by
  an admin is **blocked from accepting bookings and publishing services** (`refund_overdue`,
  reported before any commission debt). The block reads the deadline directly; the scheduler
  (`bookings:escalate-overdue-refunds`, every 15 minutes) alerts administrators and the provider once.
- **Administrators settle disputes** in the booking dialog: *returned* (recorded as refunded,
  provider unblocked) or *not returned* (provider stays blocked — the basis for suspending or banning
  with the existing tools). Bookings → payment filter *Refund owed* lists every open case; Admin Inbox
  alerts (kind `refund`) link to it.
- **No self-deletion.** `DELETE /api/client/v1/auth/me` answers **410** with a "contact support"
  message (kept so older app builds show it); the app no longer offers *Delete account*. Accounts
  are removed only by administrators.

## Consequences

- SkillServe still cannot force money back — the safeguards make not returning it costly (no new
  work, visible to admins, grounds for a ban) and leave a documented trail for disputes.
- A customer who never confirms a returned refund leaves it `sent`; that does **not** block the
  provider, and an admin can close it as *returned* on the provider's proof.
- Policies (Terms, Privacy) were updated; an administrator who already edited them in System
  Settings must republish them to pick the change up.
- Bookings cancelled before 2026-10-14 have no refund opened retroactively.

Related: [[Payments and Refunds]] · [[booking_refunds]] · [[Account Status Lifecycle]] · [[ADR Index]]
