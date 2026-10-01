---
type: table
tags: [database, table, addresses, reference-data]
domain: Locations
soft_deletes: false
---
# ph_locations

The PSA Philippine Standard Geographic Code: every region, province, city/municipality and
barangay, for the address pickers. Reference data, loaded by `php artisan locations:import` from
`backend/database/data/ph_locations.json.gz` and replaced wholesale for a new PSA release.

- **Model:** `backend/app/Modules/Locations/Models/PhLocation.php`
- **Soft deletes:** no
- **Migrations:** `2026_10_01_000001_create_ph_locations_table`
- **Rows:** 43,778 (17 regions, 81 provinces, 1,634 cities/municipalities, 42,046 barangays)

## Columns

| Column | Type | Notes |
|---|---|---|
| `code` | char(9) PK | PSGC code |
| `name` | string(120) | e.g. `Quezon City`, `Region IV-A (CALABARZON)` |
| `level` | string(16), indexed | `region`, `province`, `city`, `municipality`, `barangay` |
| `parent_code` | char(9) null | The next level up: a city's province, or its region when it has none (NCR); a barangay's city or municipality; null for regions |
| `region_code` | char(9), indexed | The region every place belongs to |

Index `(parent_code, name)` serves the picker's "children by name" query.

`parent_code` is deliberately **not** a foreign key: the import inserts in chunks without ordering,
and the table is replaced as a whole, never edited row by row. `ImportPhLocationsTest` checks the
shipped snapshot instead: no duplicate codes, no orphaned place, every barangay under a city or
municipality.

Related: [[Philippine Addresses]] · [[Database Index]]
