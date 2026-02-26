# Surge 仓库维护指南

## 仓库概述

这是一个 Surge / Clash 配置仓库，提供完整的代理规则和配置文件。

**主要用途：** iOS/macOS Surge 客户端、Clash/Stash 客户端的网络代理规则配置

---

## 目录结构

```
surge/
├── 配置文件
│   ├── Surge-Full-Overseas.conf              # 原版配置（保留历史习惯）
│   ├── Surge-Full-Overseas-Hardened.conf     # 增强版（推荐日常使用）
│   ├── Clash-Hybrid-OurPolicy.yaml           # Clash/Stash 通用版
│   └── legacy/Stash-Full-Overseas.yaml       # 历史备份
│
├── custom-rules/                              # 自维护规则（3116 行）
│   ├── ai.list                              # AI 平台规则（142行）
│   ├── crypto-wallet.list                    # 加密货币钱包（141行）
│   ├── streaming.list                        # 流媒体（1820行）
│   ├── social.list                           # 社交媒体（673行）
│   ├── games.list                            # 游戏（312行）
│   ├── tradingview.list                      # 交易工具（16行）
│   └── auto-backfill.list                    # 自动回灌规则（12行）
│
├── scripts/maintenance/                       # 维护脚本
│   ├── sync_custom_rules.py                  # 同步上游规则
│   ├── auto_backfill_rules.py                # 自动回灌规则
│   ├── check_rule_urls.py                    # 检查规则 URL 有效性
│   ├── analyze_match_hits.py                 # 分析规则匹配
│   └── *.sh                                  # 安装/更新脚本
│
├── observations/                             # 观测与分析
│   └── targeted-backfill-latest.json         # 回灌分析数据
│
├── CHANGELOG.md                              # 版本变更记录
└── README.md                                 # 使用说明
```

---

## 配置文件说明

### 1. Surge-Full-Overseas.conf
- **类型：** 原版配置
- **用途：** 保留历史使用习惯
- **维护方式：** 不主动更新，作为基线

### 2. Surge-Full-Overseas-Hardened.conf ⭐ 推荐
- **类型：** 增强版
- **用途：** 日常使用
- **特性：**
  - AI 纯净 IP 支持（两跳链式）
  - 优化的策略组（smart 替代 url-test）
  - HTTPS 订阅链接
  - 降低规则重复

### 3. Clash-Hybrid-OurPolicy.yaml
- **类型：** 通用配置
- **用途：** Clash/Stash 客户端

---

## 规则分类统计

| 规则文件 | 行数 | 用途 |
|---------|------|------|
| streaming.list | 1820 | Netflix/Disney/TikTok/YouTube |
| social.list | 673 | Telegram/Discord/Facebook/Twitter |
| games.list | 312 | 游戏平台 |
| ai.list | 142 | OpenAI/Claude/Gemini/Perplexity |
| crypto-wallet.list | 141 | Binance/OKX/Bybit/TradingView |
| tradingview.list | 16 | TradingView |
| auto-backfill.list | 12 | 自动回灌 |

**总计：** 3116 行规则

---

## 维护任务

### 1. 同步上游规则

```bash
cd scripts/maintenance
python3 sync_custom_rules.py
```

**上游来源：**
- blackmatrix7/ios_rule_script
- ACL4SSR/ACL4SSR

**同步策略：**
- 只增不减（合并，不删除现有本地覆盖）
- 自动去重

### 2. 检查规则 URL 有效性

```bash
python3 check_rule_urls.py
```

### 3. 自动回灌规则

```bash
python3 auto_backfill_rules.py
```

### 4. 分析规则匹配

```bash
python3 analyze_match_hits.py
```

---

## 自动维护

### 定时任务（macOS launchd）

```bash
# 安装定时任务
./scripts/maintenance/install_launchd.sh
```

### 自动更新脚本

```bash
# 自动更新规则
./scripts/maintenance/openclaw-auto-update.sh

# 自愈检查
./scripts/maintenance/openclaw-selfheal.sh
```

---

## 使用指南

### 快速开始（Surge）

1. **下载配置**
   - 推荐：`Surge-Full-Overseas-Hardened.conf`

2. **修改订阅**
   - 找到 `policy-path` 改为你自己的订阅链接

3. **验证策略组**
   - `♻️ 自动选择`
   - `🇺🇲 美国节点`
   - `🤖 AI平台`

### AI 纯净 IP 配置

增强版已内置模板：

1. 在 `[Proxy]` 添加纯净 IP 节点（名：`AI-Pure-IP`）

2. 在 `[Proxy Group]` 启用：
   ```
   🤖 AI链式 = relay, "🇺🇲 美国节点", AI-Pure-IP
   🤖 AI平台 = select, "🤖 AI链式", ...
   ```

3. 链路：`设备 -> 机场美国 -> 纯净IP -> AI平台`

---

## 维护原则

1. **不破坏原版** - 增强版独立维护
2. **可回滚** - 优先增量改动
3. **分离关注点** - 规则问题与链路问题分开处理

---

## 版本历史

详见 [CHANGELOG.md](./CHANGELOG.md)

---

## 相关链接

- blackmatrix7/ios_rule_script: https://github.com/blackmatrix7/ios_rule_script
- ACL4SSR/ACL4SSR: https://github.com/ACL4SSR/ACL4SSR
