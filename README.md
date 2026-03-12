# Surge 个人配置仓库

个人 Surge / Clash 配置，主攻**直连白名单**维护，确保香港银行、海外券商等关键服务直连不走 VPN。

## 配置文件

| 文件 | 用途 | 导入链接 |
|------|------|----------|
| `Surge-Full-Overseas-FullCoverage.conf` | Surge 配置 | [一键导入](https://raw.githubusercontent.com/dodo258/surge/main/Surge-Full-Overseas-FullCoverage.conf) |
| `Clash-Stash-FullCoverage.yaml` | Stash 配置 | [一键导入](https://raw.githubusercontent.com/dodo258/surge/main/Clash-Stash-FullCoverage.yaml) |

## 核心规则：`My-Direct.list`

唯一自维护规则：[custom-rules/My-Direct.list](custom-rules/My-Direct.list)

**已收录直连域名：**
- 🇭🇰 **香港银行**：蚂蚁银行、汇丰、中银香港、ZA Bank、天星银行、汇立银行、众安银行等
- 🏦 **海外券商**：盈透、长桥、嘉信、富途、moomoo、老虎、盈立等
- 💱 **跨境金融**：Wise、iFast Global Bank (英国奕丰)

**配置方式：**
```
Surge: RULE-SET,https://cdn.jsdelivr.net/gh/dodo258/surge@main/custom-rules/My-Direct.list,DIRECT
Stash: RULE-SET,MyDirect,DIRECT (已内置指向上述URL)
```

## 快速开始

**Surge 用户：**
1. 复制配置导入链接
2. Surge App → 配置 → 从 URL 下载
3. 把订阅链接改成你自己的

**Stash 用户：**
1. 复制配置导入链接  
2. Stash → 配置 → 从 URL 下载
3. 把订阅链接改成你自己的

## 添加自定义直连

编辑 [My-Direct.list](custom-rules/My-Direct.list)，添加：
```
DOMAIN-SUFFIX,你的域名.com
```

提交后 CDN 自动同步（约 5 分钟）。

## 目录结构

```
.
├── custom-rules/
│   └── My-Direct.list      # 私有直连白名单（核心）
├── Surge-Full-Overseas-FullCoverage.conf
├── Clash-Stash-FullCoverage.yaml
└── README.md
```

## 特点

- ✅ 香港银行直连，绕过 VPN 检测
- ✅ 海外券商直连，降低交易延迟
- ✅ 轻量维护，只专注直连白名单
- ✅ CDN 加速，全球快速同步
