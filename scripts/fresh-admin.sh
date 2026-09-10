#!/usr/bin/env bash
# Reset the database and seed only the super-admin account.
# Usage: ./scripts/fresh-admin.sh

set -euo pipefail
cd "$(dirname "$0")/.."

# Ensure Docker stack is running.
if ! docker compose ps --status running --filter name=group6-backend -q 2>/dev/null | grep -q .; then
    echo "Starting Docker stack..."
    docker compose up -d --build 2>/dev/null || true
    sleep 3
fi

if docker compose ps --status running --filter name=group6-backend -q 2>/dev/null | grep -q .; then
    echo "Resetting database and seeding super-admin via Docker..."
    SEED_MODE=admin-only docker compose exec -T backend php artisan migrate:fresh --force --seed
else
    echo "ERROR: Docker is not running. Start Docker Desktop or Docker Engine first."
    echo "       Or run manually: cd backend && SEED_MODE=admin-only php artisan migrate:fresh --force --seed"
    exit 1
fi

echo ""
echo "Done. Super-admin account:"
echo "  Email:    ${ADMIN_EMAIL:-admin@skillserve.test}"
echo "  Password: ${ADMIN_PASSWORD:-SkillServe#2026}"
