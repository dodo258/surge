#!/usr/bin/env bash
set -euo pipefail

# User-approved auto update task
openclaw update status >/tmp/openclaw-update-status.txt 2>&1 || true
openclaw update >/tmp/openclaw-update-run.txt 2>&1 || true
