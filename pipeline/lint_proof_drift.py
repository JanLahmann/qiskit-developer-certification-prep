#!/usr/bin/env python3
"""Proof/option drift lint.

verify_bank.py proves that a proof's VERDICT matches the question's answer,
but nothing checks that the human-readable evidence strings still describe the
question's CURRENT text. When a review pass rewrites an option, the proof can
keep passing while its evidence describes the old wording (observed twice in
the 2026-07 review wave: evidence said "shots=256" while the stem said 1024;
a proof exercised a different call than the rewritten option showed).

Heuristic: extract *anchor tokens* from each evidence string —
  - kwarg-like tokens (identifier=value, e.g. `shots=256`, `backend=session`)
  - standalone numbers with >= 3 digits (e.g. 1024, 4096)
— and flag any that appear nowhere in the question's stem, code, options,
explanations, or observed-values block. Anchors are exactly the fragments that
rot silently when questions are edited; prose ("raises TypeError") is left
alone to keep the false-positive rate near zero.

Advisory by default (exit 0, prints warnings); --strict exits 1 on findings.

Usage:
    python3 pipeline/lint_proof_drift.py [--section sX] [--strict]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

KWARG_RE = re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*=[a-zA-Z0-9_.'\"-]+")
NUM_RE = re.compile(r"(?<![\w.])\d{3,}(?![\w.])")

# Evidence-formatting idioms, not question content: `match=False`, `ok=True`,
# and any flag whose value is a bare boolean/None.
VERDICT_LHS = {
    "match", "matches", "ok", "correct", "refuted", "confirmed", "observed",
    "claim", "verdict", "equal", "equals", "same", "is_correct", "result",
}
BOOL_RHS = {"True", "False", "None", "true", "false", "none"}


def question_corpus(q: dict, artifact: dict) -> str:
    parts = [q.get("stem") or "", q.get("code") or ""]
    for o in q["options"]:
        parts.append(o["text"])
    expl = q.get("explanation", {})
    parts.append(expl.get("correct") or "")
    parts.extend((expl.get("distractors") or {}).values())
    # observed{} holds values the proof measured; numbers there are legitimate
    # even when not quoted in the question text (e.g. derived shot totals).
    parts.append(json.dumps(artifact.get("verdict", {}).get("observed", {})))
    return "\n".join(parts)


def stale_anchors(evidence: str, corpus: str) -> list[str]:
    """Anchors in the evidence that contradict the current question text.

    A kwarg `lhs=rhs` is drift only when the question TALKS about `lhs`
    (word-boundary match in corpus) yet contains neither this exact pair nor
    the value — i.e. the proof describes an input the question no longer
    shows (the shots=256-vs-1024 class). Values the corpus never mentions at
    all are execution-observed reporting (nnz=1, sum=1024.0) and are fine.
    A standalone number is drift only in numeric-flavored questions (corpus
    carries some other >=3-digit number) that never mention it.
    """
    stale = []
    for kw in set(KWARG_RE.findall(evidence)):
        lhs, rhs = kw.split("=", 1)
        rhs_bare = rhs.strip("'\"")
        if len(lhs) < 2 or lhs.lower() in VERDICT_LHS or rhs in BOOL_RHS:
            continue
        if kw in corpus or rhs_bare in corpus:
            continue
        if re.search(rf"\b{re.escape(lhs)}\b", corpus):
            stale.append(kw)
    corpus_nums = set(NUM_RE.findall(corpus))
    if corpus_nums:
        for n in set(NUM_RE.findall(evidence)):
            if n not in corpus:
                stale.append(n)
    return sorted(stale)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", help="restrict to one section (s1..s8)")
    ap.add_argument("--strict", action="store_true", help="exit 1 on findings")
    args = ap.parse_args()

    findings: list[str] = []
    checked = 0
    for qpath in sorted((REPO / "data" / "questions").glob("s*/*.json")):
        q = json.loads(qpath.read_text())
        if args.section and q["section"] != args.section:
            continue
        proof_path = REPO / "data" / "proofs" / f"{q['id']}.json"
        if not proof_path.exists():
            continue
        artifact = json.loads(proof_path.read_text())
        evidence = artifact.get("verdict", {}).get("evidence", {}) or {}
        if not evidence:
            continue
        checked += 1
        corpus = question_corpus(q, artifact)
        for key, ev in evidence.items():
            if not isinstance(ev, str):
                continue
            stale = stale_anchors(ev, corpus)
            if stale:
                findings.append(
                    f"{q['id']} option {key}: evidence anchors not found in "
                    f"current question text: {sorted(stale)}\n"
                    f"    evidence: {ev[:140]}"
                )

    print(f"drift lint: {checked} proof artifacts checked, {len(findings)} finding(s)")
    for f in findings:
        print(f"  [drift?] {f}")
    if findings:
        print(
            "note: findings are heuristic — an anchor may be legitimately "
            "execution-derived. Re-run the proof and re-read the option before "
            '"fixing".'
        )
    return 1 if (findings and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
