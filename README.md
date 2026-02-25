# surge

一套可长期维护的 Surge / Clash 配置仓库。

## 配置文件说明

- `Surge-Full-Overseas.conf`：Surge 原版（保留历史使用习惯）
- `Surge-Full-Overseas-Hardened.conf`：Surge 增强版（建议日常使用）
- `Clash-Hybrid-OurPolicy.yaml`：Clash/Stash 通用版

## 目录结构

- `custom-rules/`：自维护规则（交易 / AI / TV / 流媒体 / 社交 / 游戏 / 自动回灌）
- `legacy/`：历史配置备份（如 Stash 旧版）
- `observations/`：观测与分析输出
- `scripts/`：维护脚本

## 推荐使用方式（Surge）

1. 直接导入：`Surge-Full-Overseas-Hardened.conf`
2. 把配置中 `policy-path` 的订阅链接改成你自己的。
3. 导入后先确认以下策略组可正常加载：
   - `♻️ 自动选择`
   - `🇺🇲 美国节点`
   - `🤖 AI平台`

## AI 纯净 IP（两跳链式）快速说明

增强版配置里已内置注释模板，按注释启用即可：

- 在 `[Proxy]` 增加你的纯净 IP 节点（示例名：`AI-Pure-IP`）
- 在 `[Proxy Group]` 启用：
  - `🤖 AI链式 = relay, "🇺🇲 美国节点", AI-Pure-IP`
  - `🤖 AI平台 = select, "🤖 AI链式", ...`
- 将旧的 `🤖 AI平台` 默认行注释掉，避免同名冲突

链路目标：

`设备 -> 机场美国线路（自动） -> 纯净IP出口 -> AI平台`

## 维护原则

- 不覆盖原版配置，增强版独立维护。
- 非必要不改动大框架，优先做可回滚的增量改动。
- 规则问题和链路问题分开处理，便于排障。

## 备注

- iOS 端测试 URL 使用 HTTP（兼容性考虑）。
- 如需回滚，可直接切回 `Surge-Full-Overseas.conf`。
