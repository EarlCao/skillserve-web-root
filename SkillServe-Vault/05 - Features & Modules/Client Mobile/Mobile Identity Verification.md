---
type: feature
platform: client-mobile
status: implemented
tags: [feature, mobile, identity]
---
# Mobile Identity Verification

Mobile requirement(s): **(extra)** ([[Requirements Sources]]). Shared: customers and providers
submit the same National ID through the same screen, because identity is identity. This is separate
from [[Provider Account and Verification]], which proves a provider is a legitimate tradesperson.

| | |
|---|---|
| Screens / routes | `/identity-verification` (optionally `?next=`) |
| Code (Flutter `lib/`) | `features/identity/ (models/identity_verification_model.dart, services/identity_service.dart, controllers/identity_controller.dart, views/identity_verification_screen.dart, views/eligibility_banner.dart)` |
| Endpoints | `GET`/`POST /api/client/v1/identity-verification`, `GET /api/client/v1/transaction-eligibility` |

## Requirement coverage

| ID | Functionality | Implementation | Status |
|---|---|---|---|
| — | Submit the National ID | the 16-digit PhilSys number, the name and birthdate on the card, and photos of both sides (camera only, through the no-filter document scanner; checked on the phone for size, darkness, glare and blur; JPG/PNG, ≤10 MB each), sent as one multipart request with upload progress | implemented |
| — | See where a submission stands | a review state or approval screen, the card's last four digits, and the reviewer's reason when it was turned down — resubmitting is allowed while unverified or rejected | implemented |
| — | Know why an account cannot transact | `EligibilityBanner` on the customer home and the provider dashboard, rendering the API's `reason` as a prompt that opens the screen which fixes it | implemented |
| — | Skip it when it is not required | "I'll do this later" appears only while `identity_required` is false for that account | implemented |

## Where it appears

- **Sign-up scans the card first** (since 2026-10-02, [[Mobile Sign-up with National ID Scan]]):
  the photos and the confirmed details are submitted automatically once the account exists, so this
  screen is no longer a step of sign-up. It opens straight after sign-up only as the fallback — when
  the scan was incomplete or the API refused it — and then **pre-filled** from the scan (card number,
  full name, birthday, both photos). A provider carries on to `/provider-onboarding` afterwards,
  which is what `?next=` carries.
- **Profile tab**, for both roles, so it can be revisited or resubmitted at any time.
- A back arrow appears only when there is somewhere to go back to, so the screen is dismissable when
  opened from Settings and is a deliberate dead end straight after sign-up.

## Tests

`identity_test` — the payload shapes, the eligibility reasons, the capture rules, a submission, a
failed submission, and what signing out clears. `id_photo_quality_test` — the photo checks;
`national_id_scan_flow_test` — refusing a dark or unreadable blurry photo, keeping a soft one that
still reads. Backend: `IdentityVerificationTest` (minimum size).

## Notes

- **Photo quality (2026-10-13).** The card must be clearly verifiable, so:
  - **No filters or edits.** Both sides are taken with ML Kit's Document Scanner in *base* mode
    (crop and rotate only) — the *full* mode offered colour filters and erased "stains" and
    fingers. The National ID screen no longer offers the gallery, where an edited picture cannot be
    told from a real one.
  - **Checked on the phone** before a side is kept (`identity/services/id_photo_quality.dart`):
    at least 800 × 500 px; not too dark (mean brightness < 55/255); not washed out by light or glare
    (mean > 235, or > 35 % of pixels blown out — high because the card is mostly white); and in
    focus (variance of the Laplacian at 800 px wide ≥ 35). Each refusal says how to fix it. A photo
    that measures blurry is still kept when its text or QR code reads — then it is sharp enough.
  - **Checked again by the API:** a front/back photo under 800 × 500 px is refused (422).
  - The thresholds are forgiving by design and still need a check on real phones (PENDING_FIXES);
    the reviewer remains the final judge and can reject with a reason.

- **The card number never touches storage.** It lives in the form's controller, is sent once, and is
  cleared as soon as the API has it. The API only ever returns its last four digits, so the model
  has no field for the full number.
- The controller follows the session: signing out drops the verification state, the eligibility and
  any captured photos, so one account's answer is never left on screen for the next person.
- Eligibility is **advisory**. Every protected endpoint re-checks server-side
  ([[Identity Verification Lifecycle]]), so the banner explains a refusal rather than enforcing one.
- A brand-new install assumes it is eligible until the API says otherwise — assuming a block would
  lock people out of a platform that does not require verification at all.

## Related

[[Identity Verification Lifecycle]] · [[Provider Commissions (Mobile)]] ·
[[Client Mobile Features Index]] · [[ADR-018 Blind Index for National ID Uniqueness]]
