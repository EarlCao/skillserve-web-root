---
type: guide
tags: [ui, ux]
sources: [AGENT.md, frontend/src/components, mobile lib/core/widgets/feedback]
---
# UX Patterns and States

Project rule (AGENT.md): every data-driven screen handles **loading, error, empty and success**
states and never shows raw backend errors.

| Pattern | Admin Web | Mobile |
|---|---|---|
| Loading | `PageSkeleton`, `Skeleton`, `Spinner`, `FullScreenLoader` (auth hydration) | `LoadingState`, `ShimmerPlaceholder` |
| Empty | `EmptyState` | `EmptyState` |
| Error | `ErrorState`, `ErrorBoundary`; normalised messages from axios interceptor | `ErrorState`; `apiErrorMessage()` in `core/utils/api_error.dart` |
| Offline | `OfflineBanner` (`useNetworkStatus`) | `ConnectivityGate` |
| Rate limited (429) | "Too many attempts. Please wait a minute and try again." | same message (`api_error_test`) |
| Maintenance | admin keeps working | full-screen `MaintenanceGate`, rechecks `/platform` |
| Confirmation | `ConfirmDialog` (incl. unsaved-changes guard) | `AppDialog`, bottom sheets |
| Action with reason | modals (suspend, ban, reject, cancel, refund…) | cancel/decline dialogs show late-fee policy |
| Feedback | `sonner` toasts | `AppSnackbar` |
| Live data | realtime refresh + 15 s polling fallback | realtime + 30 s polling; optimistic chat send with retry |
| Restricted account | — | login screen `AccountRestrictionCard` with reason and end date |
| Accessibility | `aria-label`s on drawer/theme/sign-out controls; semantic daisyUI components | reduce-motion preference |

Related: [[Admin Web UI System]] · [[Mobile UI System]]
