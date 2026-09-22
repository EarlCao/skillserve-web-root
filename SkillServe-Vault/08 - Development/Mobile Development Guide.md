---
type: guide
tags: [development, mobile, how-to]
sources: [skill-serve-mobile-application/README.md, AGENT.md, lib/]
---
# Mobile Development Guide

## Adding a feature

1. Read `api-docs/README.md`, `api-docs/MODULES.md` and the module file in the mobile repo's
   `api-docs/` (a copy of the web root's generated docs).
2. `lib/features/<feature>/models/` — `fromJson` models for the API resources.
3. `lib/features/<feature>/services/` — call `ApiClient.instance.dio` with `/client/v1/...` paths;
   no mock data; unknown endpoint → `UnsupportedError`.
4. `lib/features/<feature>/controllers/` — `ChangeNotifier`, catch errors, expose
   loading/empty/error states; register in `main.dart` (`MultiProvider`).
5. `lib/features/<feature>/views/` — reuse `core/widgets` (StatusBadge, EmptyState, ErrorState…) and
   theme tokens.
6. `lib/routes/app_router.dart` — add the `GoRoute` **and** put its first segment in exactly one of
   `_customerOnly`, `_providerOnly`, `_sharedSignedIn`, `_marketplace`, `_signedOutOnly`.
7. Tests in `test/` (model parsing, controller behaviour, route guards, phone-size layout).
8. `tool/wsl-flutter.sh analyze` and `tool/wsl-flutter.sh test`.

## Useful facts

- Send datetimes as UTC ISO-8601 (`BookingModel.apiDateTime`).
- Use `Idempotency-Key` for create operations that users may retry.
- 403 with `meta.account` = restricted account → the ApiClient ends the session.
- 503 with `meta.maintenance` → `MaintenanceState` shows the gate.
- Realtime: subscribe through `RealtimeClient.listen('App.Models.User.$id', event, …)`; presence via
  `joinPresence`.

## Release

See [[Mobile Release Build]].

Related: [[Mobile App Architecture]] · [[Mobile UI System]] · [[Mobile Test Suite]]
