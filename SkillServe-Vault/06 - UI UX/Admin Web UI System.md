---
type: guide
tags: [ui, frontend, design-system]
platform: admin-web
sources: [frontend/src/index.css, frontend/src/components, frontend/src/layouts/AdminLayout.jsx, frontend/src/providers/ThemeProvider.jsx, frontend/src/constants/index.js]
---
# Admin Web UI System

## Foundations

- **Tailwind CSS 4** + **daisyUI 5** (`@import "tailwindcss"; @plugin "daisyui";` in `src/index.css`).
- **Themes:** daisyUI built-in `light` and `dark` (`THEMES` in `src/constants`), stored in
  `localStorage['skillserve:theme']` and applied as `data-theme` on `<html>` by `ThemeProvider`;
  toggle in the top bar.
- **Font:** system stack (`system-ui, 'Segoe UI', Roboto, sans-serif`). No custom brand palette
  or web font is defined in the admin web.
- **Icons:** `lucide-react`. **Charts:** `recharts`. **Toasts:** `sonner` (bottom-right, custom
  motion in `components/feedback/toaster.css`).
- **Money:** `formatCurrency` from `src/utils` with `DEFAULT_CURRENCY = 'PHP'` (₱).

> [!info] Mobile README vs admin web
> The Flutter README claims the app "shares the admin web's identity: Ink Navy / Brass / Warm
> Slate". The admin web uses stock daisyUI themes and the Flutter code uses a charcoal + lime
> palette — see [[Mobile UI System]] and [[Known Issues and Gaps]].

## Layouts

| Layout | Used for | Notes |
|---|---|---|
| `AdminLayout` | everything under `/admin` | daisyUI drawer: overlay on mobile (< lg), collapsible icon rail on desktop; top bar with theme toggle, user menu (change password, sign out); `OfflineBanner` |
| `AuthLayout` | login, forgot, reset | centred `AuthCard` |
| `BlankLayout` | `/` redirect | |

## Shared components (`src/components`)

| Folder | Components |
|---|---|
| `common/` | `EmptyState`, `ErrorState`, `FullScreenLoader`, `OfflineBanner` (used), `PageSkeleton`, `SearchInput` |
| `feedback/` | `ConfirmDialog`, `ErrorBoundary`, `OfflineBanner` (**appears unused** — only the `common/` one is imported), `Toaster` |
| `forms/` | `FormField` (react-hook-form + zod) |
| `tables/` | `DataTable` (@tanstack/react-table), `Pagination` |
| `ui/` | `Badge`, `Button`, `Card`, `Input`, `Modal`, `Skeleton`, `Spinner`, `Textarea` |

Module-level badges: `BookingStatusBadge`, `PaymentStatusBadge`, `DisputeStatusBadge`,
`ApprovalStatusBadge`, `ServiceStatusBadge`, `ReviewStatusBadge`, `ReportStatusBadge`,
`ReportTypeBadge`, `VerificationStatusBadge`, `ProviderStatusBadge`, `UserStatusBadge`,
`CategoryStatusBadge`, `SupportTicketStatusBadge`, `SupportTicketPriorityBadge`,
`StatusBadge` (administrators).

## Page pattern

Each module page = header + filter/search/sort bar + `DataTable` + `Pagination`, with row actions
opening modals (details, form, action-with-reason, confirm). Forms use react-hook-form + zod
schemas in `modules/*/schemas`. Mutations show toasts and invalidate React Query keys.

Other unused assets found: `src/assets/hero.png` (not referenced).

Related: [[Admin Web Navigation Map]] · [[UX Patterns and States]] · [[Admin Web Frontend Architecture]]
