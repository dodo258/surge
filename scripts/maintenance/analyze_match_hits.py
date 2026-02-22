#!/usr/bin/env python3
"""
Analyze current Stash connection table and summarize MATCH hits.
Use this to discover漏网域名/IP and feed custom-rules.
"""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

API = "http://127.0.0.1:9090/connections"
OUTDIR = Path(__file__).resolve().parents[2] / "observations"


def fetch_connections():
    req = Request(API, headers={"User-Agent": "surge-maintainer/1.0"})
    with urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode("utf-8", errors="ignore"))
    return data.get("connections", [])


def main():
    conns = fetch_connections()
    match_hosts = Counter()
    match_ips = Counter()

    for c in conns:
        if c.get("rule") != "MATCH":
            continue
        md = c.get("metadata", {})
        host = (md.get("host") or "").strip().lower()
        ip = (md.get("destinationIP") or "").strip()
        if host:
            match_hosts[host] += 1
        if ip:
            match_ips[ip] += 1

    OUTDIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_json = OUTDIR / f"match-hit-analyze-{ts}.json"
    out_md = OUTDIR / f"match-hit-analyze-{ts}.md"

    payload = {
        "ts": datetime.now().isoformat(),
        "totalConnections": len(conns),
        "matchHostTop": match_hosts.most_common(100),
        "matchIpTop": match_ips.most_common(100),
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# MATCH 命中分析",
        "",
        f"- 时间: {payload['ts']}",
        f"- 总连接数: {payload['totalConnections']}",
        f"- MATCH Host 数: {len(match_hosts)}",
        f"- MATCH IP 数: {len(match_ips)}",
        "",
        "## Top MATCH Hosts",
        "",
        "| host | hits |",
        "|---|---:|",
    ]
    for h, n in match_hosts.most_common(50):
        lines.append(f"| {h} | {n} |")

    lines += ["", "## Top MATCH IPs", "", "| ip | hits |", "|---|---:|"]
    for ip, n in match_ips.most_common(50):
        lines.append(f"| {ip} | {n} |")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_json)
    print(out_md)


if __name__ == "__main__":
    main()
