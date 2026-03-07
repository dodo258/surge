# surge

一套可长期维护的 Surge / Clash 配置仓库。

## 配置文件说明

| 文件 | 说明 | 推荐度 |
|------|------|--------|
| `Surge-Full-Overseas-FullCoverage.conf` | ⭐ 全量版（重度 VPN 用户） | ⭐⭐⭐ |
| `Clash-Stash-FullCoverage.yaml` | Clash/Stash 全量版 | ⭐⭐⭐ |

## 目录结构

```
.
├── custom-rules/           # 自维护规则（核心规则）
│   ├── TradingView.list    # TradingView 图表（高优先级）
│   ├── Crypto.list         # 加密货币（交易所 + 钱包）
│   ├── AI.list             # AI 平台（OpenAI / Claude / DeepSeek 等）
│   ├── Social.list         # 社交平台（Telegram / Discord / Twitter）
│   ├── Streaming.list      # 流媒体（Netflix / Disney / YouTube）
│   ├── Games.list          # 游戏平台（Steam / Epic / PlayStation）
│   └── My-Direct.list      # 私有直连白名单（用户自定义）
├── observations/           # 观测与分析输出
├── scripts/                # 维护脚本
│   └── maintenance/
│       └── sync_custom_rules.py  # 规则同步脚本
└── MAINTENANCE.md          # 维护手册
```

## 自维护规则说明

| 规则文件 | 用途 | 上游来源 |
|----------|------|----------|
| TradingView.list | 交易图表 | Blackmatrix7 |
| Crypto.list | 加密货币交易所+钱包 | Blackmatrix7 |
| AI.list | AI 服务平台 | Blackmatrix7 + ACL4SSR |
| Social.list | 社交平台 | Blackmatrix7 + ACL4SSR |
| Streaming.list | 流媒体 | Blackmatrix7 + ACL4SSR |
| Games.list | 游戏平台 | Blackmatrix7 + ACL4SSR |
| My-Direct.list | 私有白名单 | 用户自定义 |

> **注意**：规则文件命名采用 CamelCase（如 `AI.list`），与上游同步脚本配合使用。

## 推荐使用方式

### Surge 用户

1. 直接导入：`Surge-Full-Overseas-FullCoverage.conf`
2. 把配置中 `policy-path` 的订阅链接改成你自己的。
3. 全量版特点：
   - 基于 Blackmatrix7 全量规则
   - 覆盖：加密货币、AI、TradingView、流媒体、社交、购物支付、游戏、CDN 等
   - 流媒体优先：新加坡 → 台湾 → 香港
   - 智能分流：国内直连，海外按场景选节点
   - 香港银行直连（不走 VPN）

### Clash/Stash 用户

1. 导入：`Clash-Stash-FullCoverage.yaml`
2. 把配置中订阅链接改成你自己的。
3. 功能与 Surge 版一致

## 规则同步（维护）

```bash
# 手动同步上游规则
cd scripts/maintenance
python3 sync_custom_rules.py
```

同步策略：**本地优先**（只补充，不删除本地规则）

## 维护原则

- 非必要不改动大框架，优先做可回滚的增量改动。
- 规则问题和链路问题分开处理，便于排障。
- 规则文件标准化：CamelCase 命名，与上游脚本配套。

## 备注

- iOS 端测试 URL 使用 HTTP（兼容性考虑）。
- `My-Direct.list` 为私有白名单模板，请根据需要添加自己的域名。
- 香港银行（蚂蚁银行、汇丰等）已加入直连，绕过 VPN 检测。
