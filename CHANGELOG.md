# Changelog

All notable changes to this repository are documented in this file.

## [Unreleased]

## [2026-02-25]

### Added
- Added `Surge-Full-Overseas-Hardened.conf` as a non-destructive enhanced Surge profile.
- Added commented templates for AI clean-IP access in `Surge-Full-Overseas-Hardened.conf`:
  - Single-hop clean IP template (`AI-Pure-IP`)
  - Two-hop relay template (`🤖 AI链式 = relay, "🇺🇲 美国节点", AI-Pure-IP`)
- Added clear in-file placement near `🤖 AI平台` in `[Proxy Group]` for quick enable/disable.
- Added repository-level usage and maintenance guidance in `README.md`.

### Changed
- Hardened profile switched test URLs to iOS-compatible HTTP endpoints:
  - `internet-test-url = http://www.gstatic.com/generate_204`
  - `proxy-test-url = http://www.gstatic.com/generate_204`
- Hardened profile tuning for Apple dual-device usage:
  - `test-timeout` adjusted to `6`
  - `🚀 节点选择` default priority includes `♻️ 自动选择`
- Upgraded automatic routing strategy in hardened profile:
  - `url-test` groups migrated to `smart` groups for main auto-selection and regional groups.
- Upgraded subscription links in hardened profile to HTTPS (`policy-path=https://...`).
- Consolidated overlapping service rule sources in hardened profile to reduce duplicate policy overlap (kept Blackmatrix7 for Telegram/Google/Microsoft/Apple).
- Refreshed `README.md` structure:
  - file roles
  - directory roles
  - recommended workflow
  - AI two-hop quick guide
  - maintenance and rollback notes

### Fixed
- Removed temporary `Surge-Full-Overseas-Hardened-iOS.conf` after consolidating compatibility fixes back into the main hardened profile.

---

## Notes
- `Surge-Full-Overseas.conf` remains untouched as the original baseline.
- `Surge-Full-Overseas-Hardened.conf` is the actively maintained enhanced profile.
