---
type: reference
tags: [deployment, storage, render]
sources: [DEPLOYMENT.md, backend/deploy/render/start.sh, backend/routes/api.php]
---
# Render Persistent Disk

Render web services have an **ephemeral filesystem**; without a disk every deploy loses uploads.

| Item | Value |
|---|---|
| Mount path | `/var/www/html/storage/app` |
| Size | 1 GB suggested (can grow, not shrink) |
| Requires | paid instance (Starter+) |
| Effect | single instance; a few seconds of downtime per deploy |
| Backups | Render daily snapshots (Disks → Snapshots) |

Holds `storage/app/public` (profile photos, portfolio) and `storage/app/private` (verification
documents, `dispute-evidence/`). Logs, caches and compiled views stay in the container.

`start.sh` recreates the folders on an empty disk, checks writability, and runs
`storage:link --force`; `GET /api/health` reports `services.storage`.

Files uploaded before the disk existed are gone; users must re-upload.

Decision: [[ADR-008 Uploads on Render Persistent Disk]] (owner: never an S3-compatible or other
external bucket). Related: [[File Storage Architecture]]
