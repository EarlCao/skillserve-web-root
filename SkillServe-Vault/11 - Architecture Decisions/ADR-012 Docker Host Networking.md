---
type: adr
adr: 12
status: accepted
tags: [adr, architecture]
---
# ADR-012 Docker Host Networking

| | |
|---|---|
| Status | **Accepted** — reconstructed from code and repo docs during the 2026-09-22 audit (no ADR files existed) |
| First evidence | 2026-08-07 |

## Context

The original dev machine is a Hyper-V VM whose sandbox blocks bridge-network egress and intercepts port 5432.

## Decision

All compose services use `network_mode: host`; builds use `network: host` and `RUN --network=host`; Postgres listens on 5433 bound to 127.0.0.1.

## Consequences

- Works on that VM and Linux; Docker Desktop needs host networking enabled (4.34+).
- Removing it requires coordinated edits (compose, Dockerfiles, DB_HOST).
- Production uses a separate `Dockerfile.render` without host networking.

## Evidence

- `docker-compose.yml comments`
- `README.md → Networking note`

## Related

[[Docker Compose Local Stack]] · [[ADR Index]]
