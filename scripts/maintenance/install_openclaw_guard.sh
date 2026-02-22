#!/usr/bin/env bash
set -euo pipefail

# Every 10 min self-heal
L1=com.dodo258.openclaw-selfheal
P1="$HOME/Library/LaunchAgents/${L1}.plist"
cat > "$P1" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>${L1}</string>
<key>ProgramArguments</key><array><string>/bin/bash</string><string>/Users/risk/.openclaw/workspace/surge/scripts/maintenance/openclaw-selfheal.sh</string></array>
<key>StartInterval</key><integer>600</integer>
<key>RunAtLoad</key><true/>
<key>StandardOutPath</key><string>/Users/risk/.openclaw/workspace/surge/observations/openclaw-selfheal.log</string>
<key>StandardErrorPath</key><string>/Users/risk/.openclaw/workspace/surge/observations/openclaw-selfheal.err.log</string>
</dict></plist>
EOF

# Daily auto update at load + 24h interval
L2=com.dodo258.openclaw-autoupdate
P2="$HOME/Library/LaunchAgents/${L2}.plist"
cat > "$P2" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>${L2}</string>
<key>ProgramArguments</key><array><string>/bin/bash</string><string>/Users/risk/.openclaw/workspace/surge/scripts/maintenance/openclaw-auto-update.sh</string></array>
<key>StartInterval</key><integer>86400</integer>
<key>RunAtLoad</key><true/>
<key>StandardOutPath</key><string>/Users/risk/.openclaw/workspace/surge/observations/openclaw-autoupdate.log</string>
<key>StandardErrorPath</key><string>/Users/risk/.openclaw/workspace/surge/observations/openclaw-autoupdate.err.log</string>
</dict></plist>
EOF

launchctl unload "$P1" 2>/dev/null || true
launchctl unload "$P2" 2>/dev/null || true
launchctl load "$P1"
launchctl load "$P2"
launchctl kickstart -k "gui/$(id -u)/${L1}" || true
launchctl kickstart -k "gui/$(id -u)/${L2}" || true

echo "installed $P1"
echo "installed $P2"
