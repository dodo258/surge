#!/usr/bin/env python3
import ipaddress
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

API = "http://127.0.0.1:9090/connections"
ROOT = Path(__file__).resolve().parents[2]
RULES_DIR = ROOT / "custom-rules"
OUT_STABLE = RULES_DIR / "auto-backfill.list"
OUT_STAGING = RULES_DIR / "auto-backfill-staging.list"
STATE = ROOT / "observations" / "auto-backfill-state.json"

MIN_HITS_PER_RUN = 2
PROMOTE_TOTAL_HITS = 4
MAX_NEW_PER_RUN = 200
MAX_STABLE_RULES = 800
TTL_DAYS = 14


def fetch_connections():
    req = Request(API, headers={"User-Agent": "surge-maintainer/1.0"})
    with urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore")).get("connections", [])


def valid_host(h: str) -> bool:
    h = (h or "").strip().lower()
    if not h or h == "localhost" or h.endswith(".local"):
        return False
    if " " in h or h.startswith("["):
        return False
    return "." in h


def is_public_ipv4(ip: str) -> bool:
    try:
        v = ipaddress.ip_address(ip)
        return v.version == 4 and not (v.is_private or v.is_loopback or v.is_link_local or v.is_multicast)
    except Exception:
        return False


def load_state(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(path: Path, state: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def write_list(path: Path, title: str, added: int, rules: list[str], note: str):
    head = [
        f"# {title}",
        f"# Last-Update: {datetime.now().isoformat()}",
        f"# Added this run: {added}",
        note,
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(head + rules) + "\n", encoding="utf-8")


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

    run_candidates = []
    for h, n in host_hits.most_common():
        if n >= MIN_HITS_PER_RUN:
            run_candidates.append((f"DOMAIN,{h}", n))
    for ip, n in ip_hits.most_common():
        if n >= MIN_HITS_PER_RUN:
            run_candidates.append((f"IP-CIDR,{ip}/32,no-resolve", n))
    run_candidates = run_candidates[:MAX_NEW_PER_RUN]

    state = load_state(STATE)
    now = datetime.now()
    now_s = now.isoformat()

    # update state
    for rule, n in run_candidates:
        rec = state.get(rule, {"first_seen": now_s, "last_seen": now_s, "total_hits": 0})
        rec["last_seen"] = now_s
        rec["total_hits"] = int(rec.get("total_hits", 0)) + int(n)
        state[rule] = rec

    # prune by TTL
    cutoff = now - timedelta(days=TTL_DAYS)
    pruned = {}
    for rule, rec in state.items():
        try:
            last_seen = datetime.fromisoformat(rec.get("last_seen", now_s))
        except Exception:
            last_seen = now
        if last_seen >= cutoff:
            pruned[rule] = rec
    state = pruned

    stable = sorted([r for r, rec in state.items() if int(rec.get("total_hits", 0)) >= PROMOTE_TOTAL_HITS])
    staging = sorted([r for r, rec in state.items() if int(rec.get("total_hits", 0)) < PROMOTE_TOTAL_HITS])

    if len(stable) > MAX_STABLE_RULES:
        stable = stable[-MAX_STABLE_RULES:]

    save_state(STATE, state)
    write_list(
        OUT_STABLE,
        "Auto backfill rules (stable)",
        len(run_candidates),
        stable,
        "# Source: Stash /connections MATCH hits | policy=TTL+promote"
    )
    write_list(
        OUT_STAGING,
        "Auto backfill rules (staging)",
        len(run_candidates),
        staging,
        "# Staging pool before promotion; for review"
    )

    print(f"connections={len(conns)}")
    print(f"run_candidates={len(run_candidates)}")
    print(f"stable={len(stable)} staging={len(staging)}")
    print(str(OUT_STABLE))
    print(str(OUT_STAGING))
    print(str(STATE))


if __name__ == "__main__":
    main()
