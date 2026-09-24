---
type: adr
adr: 18
status: accepted
tags: [adr, architecture, identity, security]
---
# ADR-018 Blind Index for National ID Uniqueness

| | |
|---|---|
| Status | **Accepted** |
| First evidence | 2026-09-24 |

## Context

SkillServe must enforce "one Philippine National ID = one active account", server-side and at the
database level. That requires comparing card numbers across accounts.

Three properties are in tension:

1. The PhilSys Card Number is sensitive personal data and should not be held in the clear.
2. Laravel's encryption is randomised, so two rows holding the same number produce different
   ciphertext — an encrypted column cannot be uniquely indexed or compared.
3. A plain hash is not safe here: the number space is only 10¹⁶, so anyone who obtained the database
   could enumerate every hash offline and recover the numbers.

## Decision

Store a **blind index**: `HMAC-SHA256(normalised_digits, pepper)` in `id_number_hash`, where the
pepper lives in configuration (`IDENTITY_HASH_KEY`, defaulting to `APP_KEY`) and therefore outside
the database. Enforce uniqueness with a **partial unique index** over that column, excluding released
records.

Keep the number itself in a separate `encrypted` column so a disputed match can be settled, and the
last four digits in the clear for display. Normalise to digits before hashing, so formatting cannot
create a second identity.

## Consequences

- Uniqueness is enforced by the database on both PostgreSQL and SQLite, so the test suite exercises
  the real constraint rather than an application-only approximation.
- A leaked database alone does not yield card numbers: the pepper is required, and it is not stored
  there.
- **The pepper must never change.** Rotating it makes every stored hash unmatchable and silently
  stops duplicate detection. It defaults to `APP_KEY` so that it fails together with the encrypted
  copy rather than diverging invisibly. Changing it requires re-hashing existing rows.
- Card numbers cannot be searched by an administrator — deliberately, since a hashed search term
  would make the endpoint an oracle for testing whether a stolen ID is registered.
- Releasing an ID (permanent account deletion) keeps the hash and drops the ciphertext, so a
  previously-removed ID stays recognisable without retaining the number.

## Alternatives considered

- **Plain SHA-256:** simplest, but offline-enumerable over a 10¹⁶ space. Rejected.
- **Storing the number in the clear with a unique index:** trivially correct, unacceptable exposure
  for sensitive government identifiers. Rejected.
- **Application-only duplicate checks:** loses the race between two concurrent submissions and can be
  bypassed by any direct database write. Rejected as the *sole* mechanism; it is kept as the
  user-friendly first check, with the index as the real guarantee.

## Related

[[Identity Verification Lifecycle]] · [[identity_verifications]] · [[ADR-016 Soft Delete with 30-Day Purge]] · [[ADR Index]]
