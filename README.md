# surge

主配置文件：
- `Surge-Full-Overseas.conf`
- `Stash-Full-Overseas.yaml`

自维护规则：
- `custom-rules/crypto-wallet.list`
- `custom-rules/ai.list`
- `custom-rules/streaming.list`
- `custom-rules/social.list`
- `custom-rules/games.list`
- `custom-rules/auto-backfill.list`（由 MATCH 命中自动回灌）

说明：
- 重点保障：交易钱包 / AI / 流媒体 / 社交 / 游戏（全量规则）
- 国内直连、Apple、Google、Microsoft 使用 ACL4SSR + blackmatrix7 双源补强
- 地区节点保留自动测速与分策略（Auto/Fallback/LoadBalance）
- 其他未命中流量默认兜底走 Proxy

## 自动维护（全自动）

维护脚本目录：`scripts/maintenance/`

- `sync_custom_rules.py`：同步 ACL4SSR + blackmatrix7 到自定义规则
- `auto_backfill_rules.py`：从 Stash `/connections` 的 MATCH 命中自动回灌规则
- `check_rule_urls.py`：检查规则 URL 是否可用
- `run_auto_maintain.sh`：一键执行同步 + 回灌 + 检查 + 自动提交推送
- `install_launchd.sh`：安装 macOS LaunchAgent，默认每 60 分钟自动维护一次

### 一次性开启全自动

```bash
chmod +x scripts/maintenance/*.sh scripts/maintenance/*.py
./scripts/maintenance/install_launchd.sh
```

### 手动触发一次

```bash
./scripts/maintenance/run_auto_maintain.sh
```

