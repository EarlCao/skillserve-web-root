---
type: feature
platform: admin-web
status: implemented
module_number: null
tags: [feature, admin-web, identity, security]
---
# Identity Verification

> [!note] Beyond the original requirements
> This module is **not** in `SkillServe_Admin_Web_Functionalities.pdf`. It was added later on the
> project owner's instruction. See [[Requirements Sources]].

| | |
|---|---|
| Backend module | `backend/app/Modules/IdentityVerification` |
| Frontend module | `frontend/src/modules/identityVerifications` |
| Admin route(s) | `/admin/identity-verifications` |
| Permissions | `view identity verifications` to read · `verify identities` to approve · `reject identities` to reject |

## What it does

The review queue for Philippine National ID submissions from **customers and providers alike**.
Distinct from [[Provider Verification Lifecycle]], which proves a provider is a legitimate
tradesperson. See [[Identity Verification Lifecycle]] for the rules.

Filter by status (defaults to *Pending review*), account type and the account's name or email.
Opening a row loads the submission's documents and decision history; the list itself stays a summary.

Approving takes an optional internal note, never shown to the holder. Rejecting requires a reason,
which **is** shown to them so they can correct the problem and resubmit.

## What the reviewer deliberately cannot see or do

- **The card number is never sent to the browser** — only its last four digits. The reviewer
  confirms the number by opening the ID image.
- **ID images are not linked.** They are fetched with the admin's token and opened as a blob URL,
  because the file is not reachable without authorization. Every open is written to the audit log.
- **Card numbers are not searchable.** Searching by one would make this queue a way to test whether
  a given National ID is registered.
- Approving and rejecting are **separate permissions**, so a reviewer can hold one without the other.
- A decision is one-way: a second decision on the same submission returns 409.

Once the retention period passes, the images are deleted and the modal says so; the decision and its
history remain.

## Automated tests

`IdentityVerificationTest`, `IdentityVerificationReviewTest`, `IdentityEnforcementTest` — see
[[Backend Test Suite]]. There is no frontend test framework; the UI is verified by `npm run lint`
and `npm run build`.

## Related

[[Identity Verification Lifecycle]] · [[ADR-018 Blind Index for National ID Uniqueness]] ·
[[identity_verifications]] · [[Service Provider Management]] · [[Admin Web Features Index]]
