#!/usr/bin/env python3
"""
Regenerate the endpoint notes in "04 - API Integrations/Endpoints" from the
live Laravel route table, so the vault never drifts from the code.

What it reads (read-only — it never touches the database):
  * `php artisan route:list --json -v` in ../backend (needs local PHP + vendor/)
  * every backend controller, to find the ability each action authorizes
  * every backend policy, to translate policy abilities into Spatie permissions

Usage, from the web project root:
    python3 "SkillServe-Vault/99 - Meta/Scripts/generate_endpoint_notes.py"

Only files named "API - *.md" in the Endpoints folder are rewritten. Anything
written by hand elsewhere is left alone. Re-run after any route change.
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(VAULT, ".."))
BACKEND = os.path.join(ROOT, "backend")
MODULES = os.path.join(BACKEND, "app", "Modules")
OUT = os.path.join(VAULT, "04 - API Integrations", "Endpoints")

# (note title, predicate on uri, description, feature note link)
GROUPS = [
    ("API - Admin Authentication", lambda u: u.startswith("api/auth/"), "Admin web sign-in, sign-out, profile and password endpoints (`/api/auth/*`).", "Admin Authentication"),
    ("API - Dashboard", lambda u: u.startswith("api/dashboard"), "Admin dashboard read model.", "Admin Dashboard"),
    ("API - Administrators, Roles and Permissions", lambda u: u.startswith(("api/administrators", "api/roles", "api/permissions")), "Staff accounts, roles and the permission catalogue.", "Admin Management"),
    ("API - Users", lambda u: u.startswith("api/users"), "Admin User Management (customer and provider accounts).", "User Management"),
    ("API - Service Categories", lambda u: u.startswith("api/service-categories"), "Categories and nested subcategories.", "Service Category Management"),
    ("API - Providers", lambda u: u.startswith("api/providers"), "Admin provider management and verification workflow.", "Service Provider Management"),
    ("API - Services", lambda u: u.startswith("api/services"), "Admin service moderation.", "Service Management"),
    ("API - Bookings", lambda u: u.startswith("api/bookings"), "Admin booking management, payments and refunds.", "Booking Management"),
    ("API - Disputes", lambda u: u.startswith("api/disputes"), "Admin dispute queue (disputes live on the bookings table).", "Dispute Management"),
    ("API - Reviews", lambda u: u.startswith("api/reviews"), "Admin review moderation.", "Reviews and Ratings Management"),
    ("API - Reports and Moderation", lambda u: u.startswith("api/reports"), "Admin report queue and moderation actions.", "Reports and Moderation"),
    ("API - Notifications and Announcements", lambda u: u.startswith("api/notifications"), "Admin announcements and notification history.", "Notifications and Announcements"),
    ("API - Analytics", lambda u: u.startswith("api/analytics"), "Admin reports and CSV export.", "Reports and Analytics"),
    ("API - Provider Recognition", lambda u: u.startswith("api/provider-recognition"), "Badges, featured and top-rated providers.", "Provider Recognition"),
    ("API - Audit Logs", lambda u: u.startswith("api/audit-logs"), "Security and audit log viewer.", "Security and Audit Logs"),
    ("API - System Settings", lambda u: u.startswith("api/settings"), "Admin system settings.", "System Settings"),
    ("API - Data Management", lambda u: u.startswith("api/data-management"), "Exports, archives and deleted-record management.", "Data Management"),
    ("API - Support Tickets (Admin)", lambda u: u.startswith("api/support"), "Admin support ticket desk.", "Support Management"),
    ("API - Client Authentication", lambda u: u.startswith("api/client/v1/auth"), "Mobile registration, OTP, login, Google sign-in, refresh, profile and account deletion.", "Client Authentication and Account"),
    ("API - Client Catalog", lambda u: u.startswith(("api/client/v1/categories", "api/client/v1/services", "api/client/v1/providers")), "Public marketplace discovery (no token required).", "Service and Provider Discovery"),
    ("API - Client Bookings", lambda u: re.match(r"api/client/v1/bookings(/\{booking\})?(/cancel|/reschedule)?$", u) is not None, "Customer booking lifecycle.", "Client Booking"),
    ("API - Client Disputes", lambda u: "dispute" in u and u.startswith("api/client/v1/"), "Either party raises a dispute and uploads evidence.", "Client Disputes"),
    ("API - Client Messaging", lambda u: u.startswith("api/client/v1/conversations") or "/messages" in u and u.startswith("api/client/v1/"), "Booking-scoped chat and the conversation inbox.", "Client Messaging"),
    ("API - Client Notifications", lambda u: u.startswith("api/client/v1/notifications"), "Notification feed, read state and the background (closed-app) token.", "Client Notifications"),
    ("API - Client Favorites", lambda u: u.startswith("api/client/v1/favorites"), "Customer's saved providers.", "Client Favorites"),
    ("API - Client Reviews", lambda u: u.startswith("api/client/v1/reviews"), "Customer reviews of completed bookings.", "Client Reviews"),
    ("API - Client Reports", lambda u: u.startswith("api/client/v1/reports"), "Reports filed from the app against a user, review or message.", "Client Reports"),
    ("API - Client Support", lambda u: u.startswith("api/client/v1/support"), "Support tickets from customers and providers.", "Client Support"),
    ("API - Client Preferences and Platform", lambda u: u.startswith(("api/client/v1/preferences", "api/client/v1/platform")), "Per-user app preferences and public platform info/policies.", "Client Settings and Preferences"),
    ("API - Provider Bookings (Mobile)", lambda u: u.startswith("api/client/v1/provider/bookings"), "The provider's jobs and their lifecycle.", "Provider Jobs"),
    ("API - Provider Services (Mobile)", lambda u: u.startswith("api/client/v1/provider/services"), "Provider-managed services (subject to admin approval).", "Provider Service Management"),
    ("API - Provider Account (Mobile)", lambda u: u.startswith("api/client/v1/provider/"), "Provider profile, portfolio, availability, badges and verification upload.", "Provider Account and Verification"),
    ("API - Platform and Infrastructure", lambda u: True, "Health checks, broadcasting auth, Swagger docs, storage and framework routes.", None),
]


def run_route_list() -> list[dict]:
    try:
        raw = subprocess.check_output(
            ["php", "artisan", "route:list", "--json", "-v"], cwd=BACKEND, stderr=subprocess.DEVNULL
        )
    except (OSError, subprocess.CalledProcessError) as exc:  # pragma: no cover
        sys.exit(f"route:list failed ({exc}). Run from a machine with PHP and backend/vendor installed.")
    return json.loads(raw)


def controller_abilities() -> dict[str, list[str]]:
    """Map 'Module::Controller@method' → abilities it checks."""
    found: dict[str, list[str]] = {}
    for path in glob.glob(os.path.join(MODULES, "*", "Controllers", "*.php")):
        src = open(path, encoding="utf-8").read()
        module = path.split(os.sep)[-3]
        ctl = os.path.basename(path)[:-4]
        parts = re.split(r"\n    public function (\w+)\(", src)
        for i in range(1, len(parts), 2):
            body = parts[i + 1]
            abilities = re.findall(r"(?:->authorize|Gate::authorize|Gate::allows|Gate::denies)\(\s*'([^']+)'", body)
            abilities += re.findall(r"->can\(\s*'([^']+)'", body)
            found[f"{module}::{ctl}@{parts[i]}"] = list(dict.fromkeys(abilities))
    return found


def policy_permissions() -> dict[str, dict[str, list[str]]]:
    """Map module → {policy ability → permission strings}."""
    result: dict[str, dict[str, list[str]]] = {}
    for path in glob.glob(os.path.join(MODULES, "*", "Policies", "*.php")):
        module = path.split(os.sep)[-3]
        src = open(path, encoding="utf-8").read()
        parts = re.split(r"\n    public function (\w+)\(", src)
        for i in range(1, len(parts), 2):
            body = parts[i + 1].split("\n    public function")[0]
            perms = [p for p in re.findall(r"'([a-z][a-z ]+[a-z])'", body) if " " in p]
            if perms:
                result.setdefault(module, {})[parts[i]] = list(dict.fromkeys(perms))
    return result


def short_middleware(mw: list[str]) -> str:
    names = []
    for m in mw:
        if m in ("api", "web"):
            continue
        name = m.split("\\")[-1]
        name = name.replace("Authenticate:sanctum", "auth:sanctum").replace("ThrottleRequests:", "throttle:")
        name = name.replace("CheckAbilities:", "abilities:").replace("ValidateSignature", "signed")
        names.append(name)
    return ", ".join(f"`{n}`" for n in names) or "—"


def action_key(action: str) -> str | None:
    m = re.match(r"App\\Modules\\(\w+)\\Controllers\\(\w+)@(\w+)", action)
    return f"{m.group(1)}::{m.group(2)}@{m.group(3)}" if m else None


def describe_authz(key: str | None, abilities: dict, policies: dict) -> str:
    if not key:
        return "—"
    found = abilities.get(key, [])
    module = key.split("::")[0]
    if not found:
        if module.startswith("Client"):
            return "Role gate in middleware; ownership/participant check in the client policy or service"
        return "No controller check found (see middleware / service)"
    out = []
    for ability in found:
        perms = policies.get(module, {}).get(ability)
        if perms:
            out.append(f"policy `{ability}` → " + " / ".join(f"`{p}`" for p in perms))
        else:
            out.append(f"`{ability}`")
    return "; ".join(out)


def main() -> None:
    routes = run_route_list()
    abilities = controller_abilities()
    policies = policy_permissions()
    buckets: dict[str, list[dict]] = {title: [] for title, *_ in GROUPS}
    for route in routes:
        uri = route["uri"]
        for title, predicate, *_ in GROUPS:
            if predicate(uri):
                buckets[title].append(route)
                break

    os.makedirs(OUT, exist_ok=True)
    for old in glob.glob(os.path.join(OUT, "API - *.md")):
        os.remove(old)

    today = dt.date.today().isoformat()
    index_rows = []
    for title, _pred, description, feature in GROUPS:
        items = sorted(buckets[title], key=lambda r: (r["uri"], r["method"]))
        if not items:
            continue
        lines = [
            "---",
            "type: api-endpoints",
            "generated: true",
            f"generated_on: {today}",
            "source: php artisan route:list --json -v",
            "tags: [api, endpoints, generated]",
            "---",
            f"# {title}",
            "",
            f"> [!info] Generated file — do not edit by hand",
            f"> Rebuilt by `99 - Meta/Scripts/generate_endpoint_notes.py` from the live route table on {today}.",
            "> Authorization is extracted from controller/policy source; request/response shapes live in the",
            "> generated OpenAPI reference (`api-docs/modules/*.md`, Swagger UI at `/api/documentation`).",
            "",
            description,
            "",
        ]
        if feature:
            lines += [f"Feature note: [[{feature}]] · Conventions: [[API Conventions]] · Index: [[API Index]]", ""]
        else:
            lines += ["Conventions: [[API Conventions]] · Index: [[API Index]]", ""]
        lines += [
            "| Method | Path | Controller action | Middleware | Authorization |",
            "|---|---|---|---|---|",
        ]
        for r in items:
            key = action_key(r["action"])
            action = r["action"].replace("App\\Modules\\", "").replace("\\Controllers\\", "::")
            action = action.replace("\\", "\\\\")
            method = r["method"].replace("|HEAD", "").replace("GET|POST", "GET, POST")
            lines.append(
                f"| {method} | `/{r['uri']}` | `{action}` | {short_middleware(r['middleware'])} | "
                f"{describe_authz(key, abilities, policies)} |"
            )
        lines += [
            "",
            "Every `api/*` route also runs the `api` group: `throttle:api` (60/min per user or IP), "
            "`SubstituteBindings`, `ForceJsonResponse`, `CacheApiResponse`, `AddRateLimitHeaders`.",
            "",
        ]
        with open(os.path.join(OUT, f"{title}.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        index_rows.append((title, len(items), description))

    total = sum(n for _, n, _ in index_rows)
    idx = [
        "---",
        "type: index",
        "generated: true",
        f"generated_on: {today}",
        "tags: [api, index, generated]",
        "---",
        "# Endpoints Index",
        "",
        f"> [!info] Generated on {today} from `php artisan route:list` — {total} route entries in {len(index_rows)} groups.",
        "",
        "| Group | Routes | Scope |",
        "|---|---|---|",
    ]
    idx += [f"| [[{t}]] | {n} | {d} |" for t, n, d in index_rows]
    idx += ["", "Back to [[API Index]]", ""]
    with open(os.path.join(OUT, "Endpoints Index.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(idx))
    print(f"Wrote {len(index_rows)} endpoint notes ({total} routes) to {OUT}")


if __name__ == "__main__":
    main()
