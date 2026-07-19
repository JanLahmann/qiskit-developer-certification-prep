#!/usr/bin/env python
"""Verify the question bank: schema + execute-and-prove.

Usage (from repo root, with .venv):
    .venv/bin/python pipeline/verify_bank.py                 # verify all
    .venv/bin/python pipeline/verify_bank.py --only s5-q001  # one question
    .venv/bin/python pipeline/verify_bank.py --check         # no file updates
    .venv/bin/python pipeline/verify_bank.py --summary-json out.json

Exit code 0 iff every question passes schema validation AND (for executed
proofs) its proof run succeeds. Writes proof artifacts to data/proofs/ and
stamps freshness back into each question file unless --check is given.
This script is the CI gate and the freshness (drift-watchdog) engine.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness.runner import run_proof  # noqa: E402
from harness.schema import QuestionError, load_question  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = REPO / "data" / "questions"
PROOFS_DIR = REPO / "data" / "proofs"
PYTHON_BIN = REPO / ".venv" / "bin" / "python"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="verify a single question id")
    ap.add_argument("--section", help="verify only one section (e.g. s5) — used by parallel generation agents to avoid cross-section writes")
    ap.add_argument("--check", action="store_true", help="don't write artifacts/freshness")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--summary-json", type=Path, help="write summary JSON here")
    ap.add_argument("--python", default=str(PYTHON_BIN), help="python binary for proofs")
    args = ap.parse_args()

    paths = sorted(QUESTIONS_DIR.glob("s*/*.json"))
    if args.section:
        paths = [p for p in paths if p.parent.name == args.section]
    if args.only:
        paths = [p for p in paths if p.stem == args.only]
        if not paths:
            print(f"no question named {args.only}", file=sys.stderr)
            return 2

    failures: list[tuple[str, str]] = []
    questions: list[tuple[Path, dict]] = []
    for p in paths:
        try:
            questions.append((p, load_question(p)))
        except QuestionError as e:
            failures.append((p.stem, f"schema: {e}"))

    to_run = [(p, q) for p, q in questions if q["verification"]["mode"] == "script"]
    conceptual = [q["id"] for _, q in questions if q["verification"]["mode"] == "none"]

    print(f"bank: {len(paths)} files · {len(questions)} schema-valid · "
          f"{len(to_run)} executable proofs · {len(conceptual)} conceptual")

    results = {}
    if to_run:
        with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futs = {
                ex.submit(run_proof, q, args.python, args.timeout): (p, q)
                for p, q in to_run
            }
            for fut in cf.as_completed(futs):
                p, q = futs[fut]
                res = fut.result()
                results[q["id"]] = res
                status = "PROVEN" if res.ok else "FAILED"
                print(f"  [{status}] {q['id']} ({res.artifact.get('wall_seconds')}s) — {res.reason}")
                if not res.ok:
                    failures.append((q["id"], res.reason))

    now = dt.date.today().isoformat()
    if not args.check:
        PROOFS_DIR.mkdir(parents=True, exist_ok=True)
        for p, q in questions:
            qid = q["id"]
            if qid in results:
                artifact_rel = f"proofs/{qid}.json"
                (PROOFS_DIR / f"{qid}.json").write_text(
                    json.dumps(results[qid].artifact, indent=2) + "\n"
                )
                q["proof"]["artifact"] = artifact_rel
                q["freshness"] = {
                    "verified_against": results[qid].artifact.get("versions", {}),
                    "verified_on": now,
                    "stale": not results[qid].ok,
                }
                p.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n")

    summary = {
        "date": now,
        "total_files": len(paths),
        "schema_valid": len(questions),
        "executable": len(to_run),
        "proven": sum(1 for r in results.values() if r.ok),
        "conceptual": len(conceptual),
        "failures": [{"id": qid, "reason": r} for qid, r in failures],
    }
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2) + "\n")

    print(
        f"result: {summary['proven']}/{summary['executable']} proven, "
        f"{len(conceptual)} conceptual, {len(failures)} failure(s)"
    )
    for qid, reason in failures:
        print(f"  FAIL {qid}: {reason}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
