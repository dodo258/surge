#!/usr/bin/env python3
"""
Sync custom-rules/* from upstream ACL4SSR + blackmatrix7 sources.
Keeps local categories full-coverage and deduplicated.
"""

from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'custom-rules'

SOURCES = {
    'crypto-wallet.list': [
        # blackmatrix7
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Binance/Binance.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OKX/OKX.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Bybit/Bybit.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Bitget/Bitget.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/CoinMarketCap/CoinMarketCap.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/TradingView/TradingView.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/CoinGlass/CoinGlass.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Kraken/Kraken.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Ledger/Ledger.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/TRONLink/TRONLink.list',
    ],
    'ai.list': [
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Claude/Claude.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Gemini/Gemini.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Perplexity/Perplexity.list',
        'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/AI.list',
    ],
    'streaming.list': [
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Netflix/Netflix.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Disney/Disney.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/TikTok/TikTok.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/YouTube/YouTube.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/YouTubeMusic/YouTubeMusic.list',
        'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyMedia.list',
    ],
    'social.list': [
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Telegram/Telegram.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Discord/Discord.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Facebook/Facebook.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Twitter/Twitter.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/WhatsApp/WhatsApp.list',
        'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Telegram.list',
    ],
    'games.list': [
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Steam/Steam.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Epic/Epic.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/EA/EA.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/PlayStation/PlayStation.list',
        'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Xbox/Xbox.list',
        'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Steam.list',
        'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Epic.list',
        'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Origin.list',
        'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Sony.list',
        'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Nintendo.list',
    ],
}

ALLOW = ('DOMAIN,', 'DOMAIN-SUFFIX,', 'DOMAIN-KEYWORD,', 'IP-CIDR,', 'IP-CIDR6,')
ORDER = {'DOMAIN-SUFFIX,': 0, 'DOMAIN,': 1, 'DOMAIN-KEYWORD,': 2, 'IP-CIDR,': 3, 'IP-CIDR6,': 4}


def fetch(url: str) -> str:
    req = Request(url, headers={'User-Agent': 'surge-maintainer/1.0'})
    with urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', errors='ignore')


def normalize(line: str) -> str:
    t = line.strip()
    if not t or t.startswith('#'):
        return ''
    if not t.startswith(ALLOW):
        return ''
    t = t.split(' //')[0].split(' #')[0].strip()
    return t


def sort_key(x: str):
    p = next((k for k in ORDER if x.startswith(k)), '')
    return (ORDER.get(p, 9), x.lower())


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    for fn, urls in SOURCES.items():
        upstream_rows = []
        for u in urls:
            try:
                txt = fetch(u)
            except Exception:
                continue
            for ln in txt.splitlines():
                n = normalize(ln)
                if n:
                    upstream_rows.append(n)

        local_rows = []
        p = OUT / fn
        if p.exists():
            for ln in p.read_text(encoding='utf-8', errors='ignore').splitlines():
                n = normalize(ln)
                if n:
                    local_rows.append(n)

        # IMPORTANT: supplement model (never delete local coverage)
        merged = sorted(set(local_rows).union(set(upstream_rows)), key=sort_key)

        body = [
            f'# {fn}',
            '# Local-first + upstream supplement (ACL4SSR + blackmatrix7)',
            '# Strategy: only add/merge, never shrink existing local coverage',
            '# Run: python3 scripts/maintenance/sync_custom_rules.py',
            ''
        ] + merged + ['']
        p.write_text('\n'.join(body), encoding='utf-8')
        print(f'{fn}: local={len(set(local_rows))} upstream={len(set(upstream_rows))} merged={len(merged)}')


if __name__ == '__main__':
    main()
