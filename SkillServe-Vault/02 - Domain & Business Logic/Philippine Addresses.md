---
type: domain
tags: [domain, addresses, locations, identity]
sources: [backend/app/Modules/Locations, backend/app/Console/Commands/ImportPhLocations.php, backend/database/data/ph_locations.json.gz, backend/database/migrations/2026_10_01_000001_create_ph_locations_table.php]
---
# Philippine Addresses

Addresses are entered the way a government form or an online-shopping checkout asks for them:
**Region → Province → City/Municipality → Barangay**, then street/house number and ZIP. The owner
decided this on 2026-10-01 for all three places an address is entered — the user's sign-up/profile
address, the booking service address and the provider's service location — and that sign-up
starts by scanning the National ID, whose printed address fills the picker.

## The list

The official **PSA Philippine Standard Geographic Code (PSGC)**: 17 regions, 81 provinces,
1,634 cities/municipalities and 42,046 barangays (43,778 places), each with a 9-digit code.

| Where | What |
|---|---|
| `backend/database/data/ph_locations.json.gz` | Snapshot (318 KB), downloaded 2026-10-01 from the `psgc.gitlab.io` mirror of the PSA list; the file names its source |
| [[ph_locations]] | The table it is loaded into |
| `php artisan locations:import` | Loads the snapshot; a no-op once loaded, `--fresh` replaces it (how a newer PSA release is applied). Run on every start by `deploy/render/start.sh` and the local `Dockerfile` |

The rows are not loaded by the migration: the test database is migrated for every test, and
~44k inserts each time would multiply the suite's run time.

### Hierarchy quirks the picker must handle

- **No province:** the 17 NCR cities, plus Isabela City and Cotabato City, sit directly under
  their region. A region's children are therefore its provinces **and** any province-less city —
  the app reads each item's `level` to decide what to ask next.
- **City of Manila** has sub-municipalities (Tondo, Sampaloc…) in the PSGC; the picker skips that
  level — every barangay hangs off its city or municipality.
- Many municipality names repeat across provinces ("San Jose" is in nine), so a place is always
  identified by its **code**, never its name.

## Endpoints

Public (sign-up needs them before an account exists); see [[API - Locations]].

| Endpoint | Returns |
|---|---|
| `GET /api/client/v1/locations/regions` | Regions, PSGC order |
| `GET /api/client/v1/locations/{code}/children` | The next level down, by name |
| `GET /api/client/v1/locations/match?address=` | Best region/province/city/barangay for a free-text address, plus the `street` part |

## Matching an ID's address

`PhLocationService::match` turns "123 RIZAL ST, BRGY BAGONG PAG-ASA, QUEZON CITY, METRO MANILA"
into codes:

| Rule | Why |
|---|---|
| A city answers to "X City" and "City of X" exactly, and to bare "X" only as a weaker match | "Quezon" is also a province and several municipalities |
| A part already matched as the province is not reused as the city | "SAN JOSE, BATANGAS" is San Jose in Batangas, not Batangas City |
| A named province or NCR decides between same-named municipalities; otherwise the city is left **null** | Guessing would pick the wrong San Jose |
| `STA.`→Santa, `STO.`→Santo, `POB.`→Poblacion; `BRGY`/`BARANGAY` ignored | ID spellings |
| Inside a word, 0/1/5/8 read as O/I/S/B; one wrong letter tolerated in names of 5+ letters (two in 12+) | Camera misreads |
| The parts before the barangay are returned as `street`; an address without commas gets no street | Only commas say where the street ends |

Whatever is matched, the user confirms it in the picker.

## Stored addresses

The client sends only the most specific place and the server derives the rest
(`PhAddressService`), so a barangay can never be saved under the wrong city. Every structured
address is also written as formatted text into the existing column, which older app versions and
the admin web read: *"123 Rizal St, Bagong Pag-asa, Quezon City, Metro Manila 1105"*.

| Where | Request field | Kind | Columns | Text column | Response field |
|---|---|---|---|---|---|
| Sign-up (`/auth/register`, `/auth/register-provider`, `/auth/google/register`) | `address_details` (+ `birthday`) | door | `pending_registrations.address_*` → `users.address_*` | `users.address` | `user.address_details` |
| Edit profile (`PATCH /auth/me`) | `address_details` | door | `users.address_*` | `users.address` | `address_details` |
| Booking (`POST /bookings`) | `service_address_details` | door | `bookings.service_*` | `service_address` | `service_address_details` (customer and provider) |
| Service (`POST/PUT /provider/services`) | `location_details` | area | `services.location_*` | `location` | `location_details` |

- **Door:** `{barangay_code, street?, postal_code?}`, barangay required, ZIP four digits.
- **Area:** `{city_code, barangay_code?}`; a barangay outside that city is a 422.
- Sending the plain text field instead (older app versions) clears the codes, which would no longer
  describe it. Sending `null` clears both.
- The fields are optional in the API so installed app versions keep working; the new app always
  sends them, and identity enforcement (**H8**) is the server-side gate.

## Status

Phase 1 (2026-10-01): the list, the import and the endpoints. Phase 2 (2026-10-02): structured
addresses on sign-up, profile, bookings and services. Phase 3 (2026-10-02): the app's ID-scanning
sign-up and the picker widget ([[Mobile Sign-up with National ID Scan]]). Next: the picker in Edit
Profile, the booking form and Add/Edit Service (Phase 4) — tracked in `PENDING_FIXES.md` → **F1**.

Related: [[ph_locations]] · [[API - Locations]] · [[Identity Verification Lifecycle]] ·
[[Registration and OTP Flow]] · [[Domain Index]]
