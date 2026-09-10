#!/usr/bin/env bash
# Reset the database and seed the full demo dataset.
# Usage: ./scripts/fresh-demo.sh

set -euo pipefail
cd "$(dirname "$0")/.."

# Ensure Docker stack is running.
if ! docker compose ps --status running --filter name=group6-backend -q 2>/dev/null | grep -q .; then
    echo "Starting Docker stack..."
    docker compose up -d --build 2>/dev/null || true
    sleep 3
fi

if docker compose ps --status running --filter name=group6-backend -q 2>/dev/null | grep -q .; then
    echo "Resetting database and seeding full demo data via Docker..."
    docker compose exec -T backend php artisan migrate:fresh --force --seed
else
    echo "ERROR: Docker is not running. Start Docker Desktop or Docker Engine first."
    echo "       Or run manually: cd backend && php artisan migrate:fresh --force --seed"
    exit 1
fi

echo ""
echo "Done. Accounts:"
echo "  Super admin: ${ADMIN_EMAIL:-admin@skillserve.test} / ${ADMIN_PASSWORD:-SkillServe#2026}"
echo "  System admin: ${SYSTEM_ADMIN_EMAIL:-system@skillserve.test} / ${SYSTEM_ADMIN_PASSWORD:-SkillServe#2026}"
echo "  Customers: 150 demo accounts (password: password)"
