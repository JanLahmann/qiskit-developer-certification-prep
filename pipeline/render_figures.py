#!/usr/bin/env python3
"""Render (and verify) the execution-generated figures for figure questions.

Contract: a question with a `figures` block names a generator script at
data/figures/<qid>/generate.py. The generator runs in the pinned venv with a
deterministic matplotlib setup (Agg backend, fixed svg.hashsalt, no embedded
date metadata) and must write exactly the SVG files the question declares
(stem and/or one per option). Figures are committed content — like proof
artifacts — so the CI build job needs no Qiskit; this tool runs locally
whenever figure questions are added or changed.

Determinism: generators must not use unseeded randomness. We enforce
reproducibility by rendering TWICE per generator and failing on any byte
difference.

Usage:
  .venv/bin/python pipeline/render_figures.py            # all figure questions
  .venv/bin/python pipeline/render_figures.py --only s2-q040
  .venv/bin/python pipeline/render_figures.py --check    # verify committed SVGs
                                                         # match a fresh render
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
VENV_PY = ROOT / ".venv" / "bin" / "python"

# Injected before every generator: pins the backend and strips every source
# of nondeterminism matplotlib would otherwise embed in SVG output.
PRELUDE = """\
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["svg.hashsalt"] = "certiq"

_real_savefig = plt.Figure.savefig
def _savefig(self, fname, **kw):
    kw.setdefault("metadata", {"Date": None})
    kw.setdefault("bbox_inches", "tight")
    return _real_savefig(self, fname, **kw)
plt.Figure.savefig = _savefig
"""


def figure_questions(only: set[str] | None) -> list[dict]:
    out = []
    for p in sorted((DATA / "questions").glob("s*/*.json")):
        q = json.loads(p.read_text())
        if q.get("figures") and (only is None or q["id"] in only):
            out.append(q)
    return out


def declared_files(q: dict) -> list[str]:
    figs = q["figures"]
    files = []
    if figs.get("stem"):
        files.append(figs["stem"]["file"])
    for spec in (figs.get("options") or {}).values():
        files.append(spec["file"])
    return files


def render_once(q: dict, outdir: Path) -> dict[str, bytes]:
    """Run the generator with cwd=outdir; return {relative file: bytes}."""
    gen = DATA / q["figures"]["generator"]
    if not gen.exists():
        raise SystemExit(f"{q['id']}: generator missing: {gen}")
    script = PRELUDE + gen.read_text()
    env = {**os.environ, "MPLBACKEND": "Agg", "PYTHONHASHSEED": "0",
           "SOURCE_DATE_EPOCH": "0"}
    proc = subprocess.run(
        [str(VENV_PY), "-c", script], cwd=outdir, env=env,
        capture_output=True, text=True, timeout=300,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"{q['id']}: generator failed:\n{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}"
        )
    rendered = {}
    qdir = f"figures/{q['id']}/"
    for rel in declared_files(q):
        name = rel[len(qdir):]  # generator writes bare filenames into cwd
        f = outdir / name
        if not f.exists():
            raise SystemExit(f"{q['id']}: generator did not write declared file {name}")
        rendered[rel] = f.read_bytes()
    return rendered


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="question ids to render")
    ap.add_argument("--check", action="store_true",
                    help="verify committed SVGs match a fresh render (CI-able)")
    args = ap.parse_args()

    qs = figure_questions(set(args.only) if args.only else None)
    if not qs:
        print("render_figures: no figure questions matched — nothing to do")
        return 0

    failures = 0
    for q in qs:
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            r1 = render_once(q, Path(d1))
            r2 = render_once(q, Path(d2))
            if r1 != r2:
                bad = [f for f in r1 if r1[f] != r2.get(f)]
                print(f"[FAIL] {q['id']}: nondeterministic render: {bad}")
                failures += 1
                continue
            if args.check:
                # 3D matplotlib renders (Bloch spheres) are deterministic on
                # any one platform but differ in low-order path decimals
                # across OSes — byte-compare would fail on CI for figures
                # committed from a Mac. platform_sensitive figures get
                # existence + determinism checks only.
                sensitive = bool(q["figures"].get("platform_sensitive"))
                for rel, blob in r1.items():
                    committed = DATA / rel
                    if not committed.exists():
                        print(f"[FAIL] {q['id']}: committed figure missing: {rel}")
                        failures += 1
                    elif sensitive:
                        print(f"[ok] {q['id']}: {rel} exists "
                              "(platform-sensitive: byte-compare skipped)")
                    elif committed.read_bytes() != blob:
                        print(f"[FAIL] {q['id']}: committed figure stale: {rel} "
                              f"(committed {hashlib.sha256(committed.read_bytes()).hexdigest()[:12]} "
                              f"!= fresh {hashlib.sha256(blob).hexdigest()[:12]})")
                        failures += 1
                    else:
                        print(f"[ok] {q['id']}: {rel} fresh")
            else:
                for rel, blob in r1.items():
                    dest = DATA / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(blob)
                    print(f"[wrote] {rel} ({len(blob) // 1024} KB)")
    n = len(qs)
    print(f"render_figures: {n} question(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
