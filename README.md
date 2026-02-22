# surge

主配置文件（推荐）：
- `Surge-Full-Overseas.conf`
- `Clash-Hybrid-OurPolicy.yaml`  ← 通用 Clash/Stash 融合版（当前主页推荐）

其他配置：
- `Stash-Full-Overseas.yaml`

自维护规则：
- `custom-rules/crypto-wallet.list`
- `custom-rules/ai.list`
- `custom-rules/tradingview.list`
- `custom-rules/streaming.list`
- `custom-rules/social.list`
- `custom-rules/games.list`
- `custom-rules/auto-backfill.list`

说明：
- 场景分流：交易/AI/流媒体/社交/游戏
- 地区锁定：按策略组限定地区，不跨区乱跳
- 地区内自动测速：在已锁定地区内自动选优
- 规则策略：本地维护优先，ACL4SSR + blackmatrix7 补充
- 订阅地址可替换：请按文件内注释改成你自己的订阅链接
