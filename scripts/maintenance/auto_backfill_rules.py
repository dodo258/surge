#!/usr/bin/env python3
import ipaddress
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

API = "http://127.0.0.1:9090/connections"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "custom-rules" / "auto-backfill.list"

MIN_HITS = 2
MAX_NEW_PER_RUN = 200


def fetch_connections():
    req = Request(API, headers={"User-Agent": "surge-maintainer/1.0"})
    with urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore")).get("connections", [])


def valid_host(h: str) -> bool:
    h = (h or "").strip().lower()
    if not h or h == "localhost" or h.endswith(".local"):
        return False
    if " " in h:
        return False
    if h.startswith("[") and h.endswith("]"):
        return False
    return "." in h


def is_public_ipv4(ip: str) -> bool:
    try:
        v = ipaddress.ip_address(ip)
        return v.version == 4 and not (v.is_private or v.is_loopback or v.is_link_local or v.is_multicast)
    except Exception:
        return False


def load_existing(path: Path):
    if not path.exists():
        return set()
    out = set()
    for ln in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        t = ln.strip()
        if t and not t.startswith("#"):
            out.add(t)
    return out


def main():
    conns = fetch_connections()
    host_hits = Counter()
    ip_hits = Counter()

    for c in conns:
        if c.get("rule") != "MATCH":
            continue
        md = c.get("metadata", {})
        h = (md.get("host") or "").strip().lower()
        ip = (md.get("destinationIP") or "").strip()
        if valid_host(h):
            host_hits[h] += 1
        if is_public_ipv4(ip):
            ip_hits[ip] += 1

    existing = load_existing(OUT)
    new_rules = []

    for h, n in host_hits.most_common():
        if n < MIN_HITS:
            continue
        rule = f"DOMAIN,{h}"
        if rule not in existing:
            new_rules.append(rule)
        if len(new_rules) >= MAX_NEW_PER_RUN:
            break

    if len(new_rules) < MAX_NEW_PER_RUN:
        for ip, n in ip_hits.most_common():
            if n < MIN_HITS:
                continue
            rule = f"IP-CIDR,{ip}/32,no-resolve"
            if rule not in existing:
                new_rules.append(rule)
            if len(new_rules) >= MAX_NEW_PER_RUN:
                break

    merged = sorted(existing.union(new_rules))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    head = [
        "# Auto backfill rules (generated)",
        f"# Last-Update: {datetime.now().isoformat()}",
        f"# Added this run: {len(new_rules)}",
        "# Source: Stash /connections MATCH hits",
        "",
    ]
    OUT.write_text("\n".join(head + merged) + "\n", encoding="utf-8")

    print(f"connections={len(conns)}")
    print(f"new_rules={len(new_rules)}")
    print(str(OUT))


if __name__ == "__main__":
    main()
