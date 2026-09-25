---
type: guide
tags: [development, frontend, how-to]
sources: [frontend/src, CLAUDE.md, AGENT.md]
---
# Frontend Development Guide

## Adding an admin page

1. `src/modules/<feature>/api/<feature>Api.js` — functions calling `api.get/post/put/patch/delete`
   from `src/services/api.js` (they resolve to the full envelope).
2. `src/constants/index.js` — add `QUERY_KEYS.<feature>` (`all`, `list(params)`, `detail(id)`…).
3. `src/modules/<feature>/hooks/use<Feature>.js` — `useQuery` / `useMutation`; on success
   `queryClient.invalidateQueries(QUERY_KEYS.<feature>.all)` and a `sonner` toast.
4. `src/modules/<feature>/schemas/*.js` — zod schemas for forms.
5. `src/modules/<feature>/pages/<Feature>Page.jsx` + `components/` — reuse `DataTable`,
   `Pagination`, `Modal`, `ConfirmDialog`, `FormField`, badges; handle loading/error/empty states.
6. `src/routes/lazyPages.jsx` — lazy import; `src/routes/index.jsx` — add under `/admin` wrapped in
   `RequirePermission permissions={[…]}`.
7. `src/layouts/AdminLayout.jsx` — add a sidebar item gated by `hasAnyCapability`.
8. If the backend broadcasts changes for this resource, map it in `services/liveUpdates.js`.
9. `npm run lint && npm run build`.

## Conventions to keep

- Relative imports; plain JS; React Compiler (avoid manual memo unless needed).
- Blob downloads currently use the raw axios instance in two modules — prefer adding a blob helper to
  `services/api.js` rather than repeating that.
- Money via `formatCurrency`; dates via `date-fns`.
- Never render raw backend errors — use `error.message` from the normalised error.

## Manual verification (no test framework)

Run the page against the local stack signed in as `admin@skillserve.test` and as
a staff account created in Administrator Management (limited admin) to check permission gating; follow the matching UAT row in
`TEST_PLAN.md`.

Related: [[Admin Web Frontend Architecture]] · [[Admin Web UI System]]
