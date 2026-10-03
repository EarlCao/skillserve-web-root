---
type: reference
tags: [ui, navigation, mobile]
sources: [skill-serve-mobile-application/lib/routes/app_router.dart]
---
# Mobile Navigation Map

Initial location `/splash`. Role access is decided by the first path segment (`redirectFor`).

| Route | Screen | Access |
|---|---|---|
| `/`, `/splash` | SplashScreen | anyone |
| `/onboarding`, `/welcome`, `/login`, `/register` | onboarding, welcome, login, register | signed-out only |
| `/google-register` | GoogleRegistrationScreen | during Google sign-up |
| `/forgot-password` | ForgotPasswordScreen | anyone |
| `/verify-email` | OTP verification | a sign-up is held here until the code is confirmed |
| `/create-password` | CreatePasswordScreen | a sign-up is held here after the code until the password is set |
| `/browse`, `/categories`, `/search`, `/service-details/:id`, `/provider-profile/:id`, `/portfolio-gallery/:id` | marketplace | guests + customers (providers redirected) |
| `/provider-preview/:id`, `/reviews/:providerId` | public profile preview, reviews | anyone (incl. providers) |
| `/about`, `/contact`, `/terms`, `/privacy`, `/community-guidelines` | static/policy screens | anyone |
| `/client` | ClientShell — bottom tabs Home · Explore · Bookings · Messages · Profile | customer |
| `/booking-form/:providerId`, `/booking-confirmation`, `/booking-history`, `/reschedule-booking/:id` | booking flow | customer |
| `/favorites`, `/payments`, `/payment-details/:bookingId`, `/write-review/:bookingId`, `/my-reviews` | customer screens | customer |
| `/provider` | ProviderShell — bottom tabs Home (dashboard) · Bookings · Services · Messages · Profile (settings) | provider |
| `/provider-onboarding`, `/verification-status`, `/provider-badges` | onboarding & verification | provider |
| `/booking-requests`, `/active-jobs`, `/completed-jobs`, `/calendar`, `/earnings`, `/statistics` | jobs & stats | provider |
| `/my-services`, `/add-service`, `/edit-service/:id`, `/availability`, `/portfolio`, `/upload-portfolio` | business management | provider |
| `/commissions`, `/gcash-details` | outstanding commission, where customers send GCash | provider |
| `/identity-verification` | National ID capture and status (optional `?next=`) | signed in (either role) |
| `/notifications`, `/chat-conversation/:bookingId`, `/booking-details/:id`, `/file-report`, `/my-reports` | shared | signed in (either role) |
| `/support/tickets`, `/support/new`, `/support/tickets/:ticketId`, `/help-center` | support | signed in (`support` segment shared); help center public |
| `/edit-profile`, `/change-password`, `/activity-history`, `/notification-preferences`, `/privacy-settings`, `/application-preferences`, `/security-activity`, `/account-data`, `/account-deletion` | account & settings | signed in |

Redirect rules: signed out + protected → `/login`; signed in + other role's route or signed-out-only
route → own home (`/client` or `/provider`). Notification taps deep-link to the booking,
conversation, ticket or service.

## After registration

Both ways of signing up **start by scanning the National ID** (front, then back) and fill the form
from it — see [[Mobile Sign-up with National ID Scan]]:

| Sign-up | Steps | Lands on |
|---|---|---|
| Email | `/register` (ID scan → pre-filled form, no password) → **no account yet** → `/verify-email` (code) → `/create-password` (password + confirmation creates it) | the scanned ID is submitted automatically, then `/client` — or `/provider-onboarding` for a provider; `/identity-verification` (pre-filled) only if it could not be sent |
| Google | `/register` or `/login` → `/google-register` (ID scan → pre-filled form, role) → `/verify-email` (code to the Google address) → `/create-password` | the same |

Signing **in** with an existing Google account asks for the account password (a sheet over the
login screen) before going to the role home; "Forgot password?" there opens `/forgot-password`
with the address filled in. `/forgot-password` runs email → 6-digit code → new password.

> [!warning] Needs Verification
> `/help-center` is not listed in any role set in `app_router.dart` (so it is reachable signed out);
> confirm this is intended.

Related: [[Mobile App Architecture]] · [[Client Mobile Features Index]] · [[Provider Mobile Features Index]]
