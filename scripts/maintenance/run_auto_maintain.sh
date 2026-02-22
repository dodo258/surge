#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."

python3 scripts/maintenance/sync_custom_rules.py
python3 scripts/maintenance/auto_backfill_rules.py
python3 scripts/maintenance/check_rule_urls.py

if ! git diff --quiet; then
  git add custom-rules/*.list Stash-Full-Overseas.yaml Surge-Full-Overseas.conf scripts/maintenance/*.py README.md || true
  git commit -m "chore: auto-sync rules and auto-backfill MATCH hits"
  git push
fi
