#!/usr/bin/env bash
set -euo pipefail

# Basic self-heal for OpenClaw on flaky network/daemon hiccups
openclaw status >/tmp/openclaw-status.txt 2>&1 || true
if ! rg -q "Gateway.*reachable|Gateway service.*running" /tmp/openclaw-status.txt; then
  openclaw gateway restart || true
fi

# lightweight health probe
openclaw security audit >/tmp/openclaw-audit.txt 2>&1 || true
