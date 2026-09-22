---
type: troubleshooting
tags: [troubleshooting, local, docker]
sources: [README.md → Troubleshooting, docker-compose.yml]
---
# Local Environment Issues

| Symptom | Cause | Fix |
|---|---|---|
| `network.host is not allowed`, or the SPA can't reach `localhost:8000` on Docker Desktop | host networking disabled | enable it (Docker Desktop ≥4.34 → Settings → Resources → Network), or remove host networking everywhere ([[ADR-012 Docker Host Networking]]) |
| `port is already allocated` / address in use | something else on 5433/8000/5173/8080 (e.g. a local Postgres) | stop it |
| Login fails right after setup | database never seeded | `./scripts/fresh-demo.sh` (wipes DB) |
| `Permission denied` writing `storage/` or `vendor/` | host UID ≠ 1000 | `HOST_UID=$(id -u) docker compose up -d --build` |
| `./scripts/...: Permission denied` | not executable | `chmod +x scripts/*.sh` |
| Pages load but nothing updates live | Reverb down or key mismatch | `docker compose logs reverb`; check `VITE_REVERB_*` vs `REVERB_APP_KEY` ([[Realtime Issues]]) |
| Changed `.env`, nothing happened | config cached in running processes | `docker compose restart backend reverb` (frontend: `restart frontend`) |
| Backend container keeps restarting | failing migration or composer error | `docker compose logs backend` |
| Tests wiped my data?! | a test not extending `Tests\TestCase` | always extend it — it forces in-memory SQLite |
| HMR websocket fails on Windows+WSL | `localhost` resolves to `::1` | Vite config already pins HMR host to `127.0.0.1`; use `127.0.0.1` |
| `php api-docs/generate.php` skips method checks | host `php artisan route:list` failed (e.g. unparsable `backend/.env`) | fix `.env` parsing or ignore the warning |

Related: [[Local Setup]] · [[Docker Compose Local Stack]]
