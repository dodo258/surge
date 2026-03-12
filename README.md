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
- ✅ 国内常用 App 直连（微信、支付宝、抖音等）
- ✅ 轻量维护，只专注直连白名单
- ✅ CDN 加速，全球快速同步

---

## ❓ 常见问题 (FAQ)

### Q1: 配置导入后没有节点？
**A:** 需要替换订阅链接！
- **Surge**: 找到所有 `policy-path=` 后面的 URL，替换成你的订阅链接
- **Stash**: 找到 `proxy-providers` 下的 `url:`，替换成你的订阅链接
- 订阅链接在你的机场/代理服务商处获取

### Q2: 如何找订阅链接？
**A:** 
1. 登录你的机场官网
2. 找到「订阅」或「一键导入」按钮
3. 复制「Clash/Surge 订阅链接」
4. 粘贴到配置文件中

### Q3: 香港银行/券商还是打不开？
**A:** 检查以下几点：
1. 确保配置已更新（CDN 同步约 5 分钟）
2. 检查规则是否命中（Surge/Stash 有日志显示）
3. 银行 App 可能需要清除缓存或重新登录
4. 部分银行会检测 SIM 卡归属地，不完全是 IP 问题

### Q4: 可以分享给朋友用吗？
**A:** 可以！本配置适合：
- 有香港银行账户的用户
- 使用海外券商的投资者
- 希望国内 App 走直连的用户

---

## 🔧 故障排查

### 问题：配置导入后网络很慢

**可能原因 & 解决：**

| 现象 | 原因 | 解决 |
|------|------|------|
| 所有网站都慢 | 节点质量差 | 换个节点，或换机场 |
| 国内网站慢 | DNS 问题 | 检查 DNS 设置，建议用阿里 DNS 223.5.5.5 |
| 特定 App 慢 | 规则未命中 | 检查日志，确认域名是否已添加直连 |
| 偶尔卡顿 | 节点不稳定 | 开启自动测速，选延迟低的节点 |

### 问题：Surge 显示「超时」或「连接失败」

**排查步骤：**
1. 检查订阅链接是否有效（浏览器打开看看）
2. 检查节点是否过期
3. 检查 Surge 的系统代理是否开启
4. 查看 Surge 日志（Dashboard → 日志）

### 问题：Stash 提示「配置文件错误」

**排查步骤：**
1. 检查 YAML 格式（缩进是否正确）
2. 检查订阅链接是否能正常访问
3. 检查策略组名是否一致
4. 使用 Stash 内置的「配置验证」功能

### 如何查看日志

**Surge:**
```
Dashboard → 日志 → 实时日志
```

**Stash:**
```
设置 → 日志 → 查看日志
```

---

## 📝 反馈 & 贡献

遇到问题？欢迎反馈：
- 提交 Issue
- 修改 [My-Direct.list](custom-rules/My-Direct.list) 并 Pull Request
- 建议添加新的直连域名
