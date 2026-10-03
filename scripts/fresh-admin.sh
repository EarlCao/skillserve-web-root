#!/usr/bin/env bash
# Reset the database to the super-admin plus the default setup: service
# categories, the Standard commission tiers and the provider badges. No sample
# customers, providers or bookings (use fresh-demo.sh for those).
# Usage: ./scripts/fresh-admin.sh

set -euo pipefail
cd "$(dirname "$0")/.."

backend_running() {
    [ -n "$(docker compose ps --status running -q backend 2>/dev/null)" ]
}

# Ensure the Docker stack is running.
if ! backend_running; then
    echo "Starting Docker stack..."
    docker compose up -d
    sleep 3
fi

if ! backend_running; then
    echo "ERROR: Docker is not running. Start Docker Desktop or Docker Engine first."
    echo "       Or run manually: cd backend && SEED_MODE=starter php artisan migrate:fresh --force --seed && php artisan locations:import"
    exit 1
fi

echo "Resetting the database and seeding the super-admin and the default setup..."
docker compose exec -T -e SEED_MODE=starter backend php artisan migrate:fresh --force --seed
# The address pickers' region/province/city/barangay list (migrate:fresh empties it).
docker compose exec -T backend php artisan locations:import

echo ""
echo "Done. Super admin: ${ADMIN_EMAIL:-admin@skillserve.test} / ${ADMIN_PASSWORD:-SkillServe#2026}"
echo "Default setup: service categories, Standard commission tiers, provider badges."
