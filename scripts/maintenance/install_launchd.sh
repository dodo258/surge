#!/usr/bin/env bash
set -euo pipefail

LABEL="com.dodo258.surge-auto-maintain"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
WORKDIR="$(cd "$(dirname "$0")/../.." && pwd)"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>${WORKDIR}/scripts/maintenance/run_auto_maintain.sh</string>
  </array>
  <key>StartInterval</key><integer>3600</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>${WORKDIR}/observations/auto-maintain.log</string>
  <key>StandardErrorPath</key><string>${WORKDIR}/observations/auto-maintain.err.log</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
launchctl kickstart -k "gui/$(id -u)/${LABEL}" || true

echo "Installed: $PLIST"
echo "Runs every 60 minutes"
