#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
FILES = [ROOT / 'Stash-Full-Overseas.yaml', ROOT / 'Surge-Full-Overseas.conf']

URL_RE = re.compile(r'https?://[^\s,\"]+')


def collect_urls(text: str):
    return sorted(set(URL_RE.findall(text)))


def head_or_get(url: str, timeout=12):
    try:
        req = Request(url, method='HEAD', headers={'User-Agent': 'surge-maintainer/1.0'})
        with urlopen(req, timeout=timeout) as r:
            return r.status
    except Exception:
        try:
            req = Request(url, method='GET', headers={'User-Agent': 'surge-maintainer/1.0'})
            with urlopen(req, timeout=timeout) as r:
                return r.status
        except Exception:
            return 0


def main():
    urls = []
    for f in FILES:
        if f.exists():
            urls.extend(collect_urls(f.read_text(encoding='utf-8', errors='ignore')))
    urls = sorted(set(urls))

    bad = []
    ignore_prefixes = ('https://dns.alidns.com/dns-query', 'https://doh.pub/dns-query')
    for u in urls:
        if u.startswith(ignore_prefixes):
            print(f'[SKIP] {u} (DoH endpoint)')
            continue
        code = head_or_get(u)
        print(f'[{code or "ERR":>3}] {u}')
        if code < 200 or code >= 400:
            bad.append((u, code))

    print(f'\nChecked: {len(urls)} URL(s)')
    print(f'Failed : {len(bad)} URL(s)')
    if bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
