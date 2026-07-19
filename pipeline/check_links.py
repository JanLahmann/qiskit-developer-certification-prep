#!/usr/bin/env python
"""Link liveness checker (CI drift watchdog component).

Collects every external URL the platform points learners to — syllabus
resources, global resources, and question citations — and checks them.
Official-domain failures (quantum.cloud.ibm.com, ibm.com, openqasm.com)
are hard failures; anything else is a warning.

Usage: python pipeline/check_links.py [--report out.json] [--timeout 15]
Requires network (run in CI; local sandboxes may block some domains).
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HARD_DOMAINS = ("quantum.cloud.ibm.com", "www.ibm.com", "ibm.com", "openqasm.com")
UA = "Mozilla/5.0 (compatible; CertiQ-linkcheck/1.0; +https://github.com/JanLahmann/qiskit-developer-certification-prep)"


def collect_urls() -> dict[str, list[str]]:
    """url -> list of places it appears."""
    urls: dict[str, list[str]] = {}

    def add(url: str | None, where: str) -> None:
        if url and url.startswith("http"):
            urls.setdefault(url, []).append(where)

    syllabus = json.loads((REPO / "data" / "syllabus.json").read_text())
    for sec in syllabus["sections"]:
        for r in sec.get("resources", []):
            add(r.get("url"), f"syllabus:{sec['id']}")
    for r in syllabus.get("global_resources", []):
        add(r.get("url"), "syllabus:global")
    add(syllabus["exam"].get("official_page"), "syllabus:exam")

    for qpath in sorted((REPO / "data" / "questions").glob("s*/*.json")):
        try:
            q = json.loads(qpath.read_text())
        except json.JSONDecodeError:
            continue
        for c in q.get("explanation", {}).get("citations", []):
            add(c, f"question:{qpath.stem}")
    return urls


def check(url: str, timeout: int) -> tuple[str, int | str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return url, resp.status
    except Exception as e:  # noqa: BLE001
        return url, type(e).__name__ + (f":{getattr(e, 'code', '')}" or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()

    urls = collect_urls()
    print(f"checking {len(urls)} unique URLs…")
    results: dict[str, int | str] = {}
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for url, status in ex.map(lambda u: check(u, args.timeout), urls):
            results[url] = status

    hard_fail: list[str] = []
    warn: list[str] = []
    for url, status in sorted(results.items()):
        ok = isinstance(status, int) and status < 400
        if not ok:
            (hard_fail if any(d in url for d in HARD_DOMAINS) else warn).append(url)
            print(f"  [{status}] {url}  (used by: {', '.join(urls[url][:4])})")

    summary = {
        "total": len(urls),
        "ok": sum(1 for s in results.values() if isinstance(s, int) and s < 400),
        "hard_failures": hard_fail,
        "warnings": warn,
    }
    if args.report:
        args.report.write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"result: {summary['ok']}/{summary['total']} ok, "
        f"{len(hard_fail)} official-domain failures, {len(warn)} warnings"
    )
    return 1 if hard_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
