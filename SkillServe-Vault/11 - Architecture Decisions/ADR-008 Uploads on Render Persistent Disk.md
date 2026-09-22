---
type: adr
adr: 8
status: accepted
tags: [adr, architecture]
---
# ADR-008 Uploads on Render Persistent Disk

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-09-21 |

## Context

Render's filesystem is ephemeral; uploads (photos, verification documents, dispute evidence) were lost on deploy.

## Decision

Keep Laravel local disks under `storage/app` and mount a Render persistent disk there. The owner requires uploads to stay on Render — never an S3-compatible or other external bucket.

## Consequences

- Requires a paid instance; service pinned to one instance with brief deploy downtime.
- Daily snapshots by Render; health check reports storage status.
- The configured `s3` disk stays unused.

## Evidence

- `DEPLOYMENT.md → Uploaded files`
- `deploy/render/start.sh`
- `PENDING_FIXES.md`

## Related

[[Render Persistent Disk]] · [[File Storage Architecture]] · [[ADR Index]]
