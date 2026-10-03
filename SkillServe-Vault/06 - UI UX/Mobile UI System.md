---
type: guide
tags: [ui, mobile, design-system]
platform: client-mobile, provider-mobile
sources: [skill-serve-mobile-application/lib/core/constants/app_colors.dart, app_text_styles.dart, lib/core/theme/app_theme.dart, lib/core/theme/app_palette.dart, lib/core/widgets, test/contrast_sweep_test.dart, README.md]
---
# Mobile UI System

## Tokens actually in code (`lib/core/constants/app_colors.dart`)

| Token | Value | Comment in code |
|---|---|---|
| `primary` | `#1C2128` | Soft Charcoal Black |
| `secondary` / `accent` | `#C7F33C` | Soft Pastel Lime Accent |
| `background` | `#F8F9F3` | soft creamy off-white |
| `surface` | `#FFFFFF` | |
| `surfaceAlt` | `#EEF3E4` | |
| `line` | `#E2E7D7` | |
| dark: `backgroundDark` / `surfaceDark` / `surfaceAltDark` / `lineDark` | `#0F1318` / `#1A2027` / `#242C36` / `#2E3742` | |
| `secondaryInk` | `#4A6B00` | the lime's hue dark enough to read on light surfaces |
| text: `textPrimary` / `textSecondary` / `textMuted` | `#1C2128` / `#575E6A` / `#626975` | |
| dark text: `textOnDark` / `textSecondaryDark` / `textMutedDark` | `#F5F7FA` / `#C2C8D0` / `#9DA3AF` | |
| status: success / warning / error / info | `#12896A` / `#9E6D0F` / `#D1453B` / `#1F5F8B` (+ light backgrounds) | |
| status on dark: `successOnDark` / `warningOnDark` / `errorOnDark` / `infoOnDark` | `#4FD1A5` / `#E8B84A` / `#F08A82` / `#7DB8E8` | |
| `star` / `starOnLight` | `#F2B705` / `#B07800` | rating star on dark / light |

## Readability in light and dark mode

**Rule: lime is a fill, never a foreground on a light surface.** `#C7F33C` on white is 1.3:1, so
lime text, icons, links and focus rings were close to invisible in light mode; in the same way
charcoal, slate and the status colours were near-invisible on the dark surfaces. Fixed 2026-10-03:

- Foregrounds come from the theme-aware getters in `lib/core/theme/app_palette.dart`
  (`context.accentInk`, `textPrimaryColor`, `textSecondaryColor`, `textMutedColor`,
  `surfaceAltColor`, `starColor`, `successColor`/`warningColor`/`errorColor`/`infoColor`). They
  return the light or dark value for the current theme. `accentInk` is olive `#4A6B00` in light mode
  and lime in dark mode.
- Lime stays as a **fill** behind charcoal text (primary buttons, selected chips, send buttons, my
  chat bubbles, step circles) and as text on the charcoal hero cards, in both modes.
- The theme uses `accentInk` for text buttons, focus borders, the cursor, spinners, the selected
  tab and nav item, switches, radios and checkboxes; `ColorScheme.primary` is the readable accent.
- `test/contrast_sweep_test.dart` renders 49 screens in light **and** dark mode and fails if any
  text or icon sits on its real background below **3:1**. At the time of the fix, all text was at
  4.5:1 or better; three icons sit at 3.3–3.6:1.

**Typography:** Google Fonts **Outfit** (`AppTextStyles._outfit`, the theme's font family).
`assets/fonts/` is empty; the pubspec font block is commented out.

**Themes:** light and dark `ThemeData` in `lib/core/theme/app_theme.dart`; the user's
`client_preferences.theme` (light/dark/system) and `reduce_motion` apply.

> [!bug] README describes a different design system
> The mobile README says: Ink Navy `#101828`, Brass `#C9852E`, Warm Slate `#F5F4F1`; Space Grotesk /
> Inter / IBM Plex Mono. None of those values or fonts are used by the code (only a stale doc comment
> in `primary_button.dart` mentions the brass gradient; the button actually uses the lime
> `secondary`). Git history shows a 2026-08-07 "soft pastel visual redesign and Outfit typography".
> Treat the code as authoritative. See [[Known Issues and Gaps]].

## Shared widgets (`lib/core/widgets`)

| Folder | Widgets |
|---|---|
| `buttons/` | PrimaryButton, SecondaryButton, OutlinedAppButton, DangerButton |
| `cards/` | BookingCard, CategoryCard, ProfileCard, ProviderCard, ReviewCard, ServiceCard |
| `feedback/` | AppBottomSheet, AppDialog, AppSnackbar, ConnectivityGate, EmptyState, ErrorState, LoadingState, ShimmerPlaceholder |
| `inputs/` | AppSearchBar, AppTextField |
| `misc/` | AppAvatar, AppIcon (HugeIcons), ImageCarousel, InfoRow, RatingWidget, SectionHeader, StatCard, **StatusBadge**, **VerificationSeal** |
| `navigation/` | AppBottomNav, AppDrawer |

Statuses render through `StatusBadge`; trust signals (verified provider, approved document) through
`VerificationSeal`. Layout helpers: `flutter_screenutil`, `responsive_framework`; animation:
`flutter_animate`, `lottie`, `shimmer`.

Layout overflow is guarded by widget tests (`app_sweep_test`, `overflow_*_test`).

Related: [[Mobile Navigation Map]] · [[UX Patterns and States]] · [[Mobile App Architecture]]
