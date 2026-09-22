#!/usr/bin/env python3
"""
Report broken [[wikilinks]] in the vault (targets with no matching note name).

Usage, from the web project root:
    python3 "SkillServe-Vault/99 - Meta/Scripts/check_vault_links.py"

Exit code 1 when broken links are found. Code spans, fenced blocks and template placeholders
({{...}}, <...>) are ignored.
"""
import os
import re
import sys

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
names = set()
files = []
for root, dirs, fs in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d != ".obsidian"]
    for f in fs:
        if f.endswith(".md"):
            names.add(f[:-3])
            files.append(os.path.join(root, f))

broken = []
for path in files:
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # ignore fenced code
    text = re.sub(r"`[^`\n]*`", "", text)             # ignore inline code
    for m in re.finditer(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]", text):
        target = m.group(1).strip()
        if "{{" in target or "<" in target or target == "...":
            continue
        if target not in names:
            broken.append((os.path.relpath(path, VAULT), target))

for rel, target in sorted(set(broken)):
    print(f"{rel}: [[{target}]]")
print(f"{len(files)} notes, {len(set(broken))} broken links")
sys.exit(1 if broken else 0)
