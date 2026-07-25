#!/usr/bin/env python3
"""Meta-pattern audit: detect answer-revealing patterns across the question bank.

A test-wise candidate can sometimes score far above chance without any Qiskit
knowledge by exploiting *how* questions are written (e.g. "the longest option
is correct"). This tool simulates such a candidate: every heuristic below
answers the whole bank blind, and its score is compared against random
guessing. It also flags individual questions whose surface features give the
answer away, so reviewers can rewrite them.

Origin: pilot-user feedback (2026-07-24) that the longest option was always
the correct one in the questions they saw.

Usage:
    python3 pipeline/audit_meta_patterns.py                # full report
    python3 pipeline/audit_meta_patterns.py --gate         # CI mode: exit 1 on blockers
    python3 pipeline/audit_meta_patterns.py --section s5   # restrict to one section

Outputs (repo-only, like data/community/ — never linked from the site):
    data/audits/meta_pattern_audit.json   machine-readable, incl. per-question flags
    data/audits/meta_pattern_audit.md     human-readable report

Scoring: heuristics that select a *set* of candidate options are scored as the
expected value of a uniform pick from that set, so ties neither help nor hurt.
Thresholds: a heuristic scoring >= PASS_LINE (0.69, the real exam's pass mark)
is a shipping BLOCKER; >= WARN_LINE (0.40) is a warning. Per-question flags are
independent of the aggregate and feed the adversarial reviewers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = ROOT / "data" / "questions"
AUDIT_DIR = ROOT / "data" / "audits"

PASS_LINE = 0.69   # real exam pass mark: 47/68
WARN_LINE = 0.40

SINGLE_ANSWER_TYPES = {"mcq", "predict-output", "spot-bug"}

HEDGE_WORDS = {
    "typically", "usually", "generally", "often", "commonly", "default",
    "defaults", "approximately", "roughly", "may", "might", "most",
    "recommended", "preferred", "designed",
}
ABSOLUTE_WORDS = {
    "always", "never", "only", "all", "none", "every", "must", "cannot",
    "impossible", "guaranteed", "any", "exactly", "immediately", "entirely",
}

STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "on", "for", "and", "or", "is", "are",
    "be", "with", "as", "by", "at", "it", "its", "this", "that", "which",
    "what", "when", "you", "your", "will", "would", "does", "do", "not",
    "from", "into", "than", "then", "each", "can", "has", "have",
}


def tokens(text: str) -> set[str]:
    return {
        w for w in re.split(r"[^a-z0-9_]+", text.lower())
        if len(w) >= 3 and w not in STOPWORDS
    }


def word_set(text: str) -> set[str]:
    return set(re.split(r"[^a-z]+", text.lower())) - {""}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def load_bank(section: str | None) -> list[dict]:
    files = sorted(QUESTIONS_DIR.glob("s*/*.json"))
    bank = []
    for f in files:
        q = json.loads(f.read_text())
        if section and q["section"] != section:
            continue
        q["_file"] = str(f.relative_to(ROOT))
        bank.append(q)
    return bank


def display_variants(q: dict) -> list[dict]:
    """All option sets a learner can actually be shown.

    Without a pool this is the question itself. With display_count < pool,
    the site renders all correct answers + every possible distractor subset
    (uniformly), so the audit must hold EVERY variant to the bar — a tell
    that only appears in one subset is still a tell.
    """
    dc = q.get("display_count")
    if not dc or dc >= len(q["options"]):
        return [q]
    answers = set(q["answer"])
    correct = [o for o in q["options"] if o["key"] in answers]
    distractors = [o for o in q["options"] if o["key"] not in answers]
    k = dc - len(correct)
    variants = []
    for combo in combinations(distractors, k):
        opts = [o for o in q["options"] if o in correct or o in combo]
        v = dict(q)
        v["options"] = opts
        variants.append(v)
    return variants


# ---------------------------------------------------------------------------
# Heuristics: each returns the set of option keys a test-wise guesser would
# pick from (empty set = heuristic abstains on this question).
# ---------------------------------------------------------------------------

def h_longest(q):
    lens = {o["key"]: len(o["text"]) for o in q["options"]}
    m = max(lens.values())
    return {k for k, v in lens.items() if v == m}


def h_shortest(q):
    lens = {o["key"]: len(o["text"]) for o in q["options"]}
    m = min(lens.values())
    return {k for k, v in lens.items() if v == m}


def h_avoid_longest(q):
    """Inverse tell: if correct is NEVER the longest, picking among the
    non-longest options beats chance. Healthy banks sit at chance for both
    this and h_longest."""
    lens = {o["key"]: len(o["text"]) for o in q["options"]}
    m = max(lens.values())
    rest = {k for k, v in lens.items() if v < m}
    return rest  # empty (abstain) if all options equal length


def make_h_position(letter):
    def h(q):
        keys = {o["key"] for o in q["options"]}
        return {letter} if letter in keys else set()
    return h


def h_stem_overlap(q):
    stem_t = tokens(q["stem"] + " " + (q.get("code") or ""))
    if not stem_t:
        return set()
    scores = {o["key"]: len(tokens(o["text"]) & stem_t) for o in q["options"]}
    m = max(scores.values())
    if m == 0:
        return set()
    return {k for k, v in scores.items() if v == m}


def h_most_hedged(q):
    scores = {o["key"]: len(word_set(o["text"]) & HEDGE_WORDS) for o in q["options"]}
    m = max(scores.values())
    if m == 0:
        return set()
    return {k for k, v in scores.items() if v == m}


def h_avoid_hedged(q):
    """Inverse of h_most_hedged: hedge-based tell fixes can teach a guesser
    'never pick the hedged option'."""
    scores = {o["key"]: len(word_set(o["text"]) & HEDGE_WORDS) for o in q["options"]}
    if max(scores.values()) == 0:
        return set()
    m = min(scores.values())
    return {k for k, v in scores.items() if v == m}


def h_least_absolute(q):
    scores = {o["key"]: len(word_set(o["text"]) & ABSOLUTE_WORDS) for o in q["options"]}
    if max(scores.values()) == 0:
        return set()  # no signal to discriminate on
    m = min(scores.values())
    return {k for k, v in scores.items() if v == m}


def h_most_absolute(q):
    """Inverse of h_least_absolute: over-correcting the absolute-distractor
    tell by moving absolutes into correct options creates THIS tell."""
    scores = {o["key"]: len(word_set(o["text"]) & ABSOLUTE_WORDS) for o in q["options"]}
    m = max(scores.values())
    if m == 0:
        return set()
    return {k for k, v in scores.items() if v == m}


def h_code_formatted(q):
    with_code = {o["key"] for o in q["options"] if "`" in o["text"]}
    if not with_code or len(with_code) == len(q["options"]):
        return set()
    return with_code


def h_numeric_middle(q):
    vals = {}
    for o in q["options"]:
        nums = re.findall(r"-?\d+(?:\.\d+)?", o["text"].replace("`", ""))
        if len(nums) == 1:
            vals[o["key"]] = float(nums[0])
    if len(vals) < 3:
        return set()
    ordered = sorted(vals, key=lambda k: vals[k])
    mid = ordered[1:-1]  # drop extremes: "never the biggest or smallest number"
    return set(mid) if mid else set()


def h_odd_one_out(q):
    tk = {o["key"]: tokens(o["text"]) for o in q["options"]}
    keys = list(tk)
    if len(keys) < 3:
        return set()
    avg_sim = {
        k: sum(jaccard(tk[k], tk[j]) for j in keys if j != k) / (len(keys) - 1)
        for k in keys
    }
    m = min(avg_sim.values())
    return {k for k, v in avg_sim.items() if v == m}


def h_twin_member(q):
    tk = {o["key"]: tokens(o["text"]) for o in q["options"]}
    keys = list(tk)
    if len(keys) < 3:
        return set()
    best_pair, best = None, -1.0
    for a, b in combinations(keys, 2):
        s = jaccard(tk[a], tk[b])
        if s > best:
            best, best_pair = s, {a, b}
    if best < 0.5:  # options not similar enough to look like a deliberate pair
        return set()
    return best_pair


HEURISTICS = {
    "longest_option": h_longest,
    "shortest_option": h_shortest,
    "avoid_longest": h_avoid_longest,
    "position_A": make_h_position("A"),
    "position_B": make_h_position("B"),
    "position_C": make_h_position("C"),
    "position_D": make_h_position("D"),
    "stem_keyword_overlap": h_stem_overlap,
    "most_hedged": h_most_hedged,
    "avoid_hedged": h_avoid_hedged,
    "least_absolute": h_least_absolute,
    "most_absolute": h_most_absolute,
    "code_formatted_only": h_code_formatted,
    "numeric_middle": h_numeric_middle,
    "odd_one_out": h_odd_one_out,
    "similar_twin_member": h_twin_member,
}


# ---------------------------------------------------------------------------
# Per-question tells (independent of aggregate heuristic scores)
# ---------------------------------------------------------------------------

def question_flags(q) -> list[dict]:
    flags = []
    answer = set(q["answer"])
    opts = {o["key"]: o["text"] for o in q["options"]}
    distractors = {k: v for k, v in opts.items() if k not in answer}
    if not distractors:
        return flags

    # Length tell: every correct option longer than every distractor.
    min_ans = min(len(opts[k]) for k in answer)
    max_dis = max(len(v) for v in distractors.values())
    if min_ans > max_dis:
        ratio = min_ans / max(1, max_dis)
        flags.append({
            "flag": "length_tell",
            "severity": "high" if ratio >= 1.4 else "low",
            "detail": f"correct option(s) strictly longest (min correct {min_ans} chars"
                      f" vs longest distractor {max_dis}, ratio {ratio:.2f})",
        })

    # Hedge/absolute asymmetry.
    ans_hedge = any(word_set(opts[k]) & HEDGE_WORDS for k in answer)
    dis_hedge = any(word_set(v) & HEDGE_WORDS for v in distractors.values())
    ans_abs = any(word_set(opts[k]) & ABSOLUTE_WORDS for k in answer)
    dis_abs = any(word_set(v) & ABSOLUTE_WORDS for v in distractors.values())
    if ans_hedge and not dis_hedge and not ans_abs:
        flags.append({
            "flag": "hedge_tell", "severity": "medium",
            "detail": "only the correct option(s) use hedged wording",
        })
    if dis_abs and not ans_abs and not dis_hedge:
        flags.append({
            "flag": "absolute_distractor_tell", "severity": "medium",
            "detail": "absolute wording (always/never/only/...) appears only in distractors",
        })

    # Stem-echo tell: correct option shares far more stem vocabulary.
    stem_t = tokens(q["stem"] + " " + (q.get("code") or ""))
    if stem_t:
        ans_ov = max(len(tokens(opts[k]) & stem_t) for k in answer)
        dis_ov = max(len(tokens(v) & stem_t) for v in distractors.values())
        if ans_ov >= 2 * max(1, dis_ov) and ans_ov >= 3:
            flags.append({
                "flag": "stem_echo_tell", "severity": "medium",
                "detail": f"correct option echoes stem vocabulary (overlap {ans_ov}"
                          f" vs best distractor {dis_ov})",
            })

    # Formatting tell: code formatting present only in correct or only in wrong.
    ans_code = all("`" in opts[k] for k in answer)
    dis_code_none = all("`" not in v for v in distractors.values())
    dis_code_all = all("`" in v for v in distractors.values())
    ans_code_none = all("`" not in opts[k] for k in answer)
    if ans_code and dis_code_none:
        flags.append({"flag": "format_tell", "severity": "medium",
                      "detail": "only correct option(s) are code-formatted"})
    if ans_code_none and dis_code_all:
        flags.append({"flag": "format_tell", "severity": "medium",
                      "detail": "correct option(s) are the only non-code-formatted ones"})

    return flags


# ---------------------------------------------------------------------------
# Aggregate analyses
# ---------------------------------------------------------------------------

def score_heuristics(bank):
    """Expected score of each blind heuristic over single-answer questions.

    Pool questions contribute via their displayed variants, each weighted
    1/n_variants, matching the uniform runtime selection.
    """
    singles = [q for q in bank if q["type"] in SINGLE_ANSWER_TYPES]
    results = {}
    for name, h in HEURISTICS.items():
        total_ev, answered_w = 0.0, 0.0
        for q in singles:
            variants = display_variants(q)
            w = 1 / len(variants)
            for v in variants:
                picks = h(v)
                if not picks:
                    continue
                answered_w += w
                if q["answer"][0] in picks:
                    total_ev += w / len(picks)
        results[name] = {
            "expected_accuracy": round(total_ev / answered_w, 4) if answered_w else None,
            "questions_answered": round(answered_w, 2),
            "coverage": round(answered_w / len(singles), 3) if singles else 0,
        }
    baseline = (
        sum(
            sum(1 / len(v["options"]) for v in display_variants(q)) / len(display_variants(q))
            for q in singles
        )
        / len(singles)
        if singles
        else 0
    )
    return results, round(baseline, 4), len(singles)


def position_stats(bank):
    per_section = defaultdict(Counter)
    for q in bank:
        if q["type"] in SINGLE_ANSWER_TYPES:
            per_section[q["section"]][q["answer"][0]] += 1
    out = {}
    for sec in sorted(per_section):
        c = per_section[sec]
        n = sum(c.values())
        top_key, top = c.most_common(1)[0]
        out[sec] = {
            "counts": dict(sorted(c.items())),
            "n": n,
            "max_share": round(top / n, 3),
            "skewed": top / n > 0.45 and n >= 8,
            "top_key": top_key,
        }
    return out


def multi_select_stats(bank):
    multis = [q for q in bank if q["type"] == "multi"]
    n_correct = Counter(len(q["answer"]) for q in multis)
    adjacent = 0
    for q in multis:
        keys = sorted(q["answer"])
        idx = [ord(k) for k in keys]
        if len(idx) >= 2 and idx == list(range(idx[0], idx[0] + len(idx))):
            adjacent += 1
    return {
        "n": len(multis),
        "answer_count_distribution": dict(sorted(n_correct.items())),
        "adjacent_letter_answers": adjacent,
        "count_predictable": len(n_correct) == 1 and len(multis) >= 5,
    }


def duplicate_texts(bank):
    """Cross-question leakage: identical option texts playing both roles."""
    role = defaultdict(set)
    for q in bank:
        for o in q["options"]:
            t = o["text"].strip().lower()
            role[t].add((q["id"], o["key"] in q["answer"]))
    return {
        t: sorted(f"{qid}:{'correct' if ok else 'wrong'}" for qid, ok in v)
        for t, v in role.items()
        if len({ok for _, ok in v}) == 2 and len(t) > 20
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", help="restrict to one section (s1..s8)")
    ap.add_argument("--gate", action="store_true",
                    help="CI mode: exit 1 if any blocker exists")
    args = ap.parse_args()

    bank = load_bank(args.section)
    if not bank:
        print("no questions found", file=sys.stderr)
        return 2

    heur, baseline, n_singles = score_heuristics(bank)
    positions = position_stats(bank)
    multi = multi_select_stats(bank)
    dupes = duplicate_texts(bank)

    flagged = []
    for q in bank:
        variants = display_variants(q)
        fl_all: dict[str, dict] = {}
        for v in variants:
            for fl in question_flags(v):
                prev = fl_all.get(fl["flag"])
                sev_rank = {"low": 0, "medium": 1, "high": 2}
                if prev is None or sev_rank[fl["severity"]] > sev_rank[prev["severity"]]:
                    if len(variants) > 1:
                        fl = {**fl, "detail": fl["detail"] + " (in >=1 displayed pool variant)"}
                    fl_all[fl["flag"]] = fl
        if fl_all:
            flagged.append({"id": q["id"], "type": q["type"],
                            "file": q["_file"], "flags": list(fl_all.values())})

    blockers, warnings = [], []
    for name, r in heur.items():
        acc = r["expected_accuracy"]
        if acc is None or r["coverage"] < 0.25:
            continue  # too little coverage to matter as an exam-wide strategy
        exam_score = acc * r["coverage"] + baseline * (1 - r["coverage"])
        r["exam_score_estimate"] = round(exam_score, 4)
        if exam_score >= PASS_LINE:
            blockers.append(f"heuristic '{name}' passes the exam blind "
                            f"(estimated score {exam_score:.0%})")
        elif exam_score >= WARN_LINE:
            warnings.append(f"heuristic '{name}' scores {exam_score:.0%} "
                            f"(chance is {baseline:.0%})")
    for sec, p in positions.items():
        if p["skewed"]:
            warnings.append(f"{sec}: answer position skew — "
                            f"'{p['top_key']}' is correct in {p['max_share']:.0%} of questions")
    if multi["count_predictable"]:
        k = next(iter(multi["answer_count_distribution"]))
        warnings.append(f"multi-select: every question has exactly {k} correct options")

    report = {
        "generated_note": "repo-only audit artifact; do not link from the website",
        "scope": args.section or "all sections",
        "n_questions": len(bank),
        "n_single_answer": n_singles,
        "random_baseline": baseline,
        "pass_line": PASS_LINE,
        "heuristics": heur,
        "position_stats": positions,
        "multi_select": multi,
        "cross_question_duplicate_options": dupes,
        "flagged_questions": flagged,
        "warnings": warnings,
        "blockers": blockers,
    }

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    (AUDIT_DIR / "meta_pattern_audit.json").write_text(json.dumps(report, indent=2))

    lines = [
        "# Meta-pattern audit (test-wise guesser simulation)",
        "",
        "*Repo-only quality artifact — not linked from the website.*",
        "",
        f"Scope: **{report['scope']}** — {len(bank)} questions "
        f"({n_singles} single-answer, {multi['n']} multi-select). "
        f"Random-guess baseline: **{baseline:.1%}**. Exam pass line: **{PASS_LINE:.0%}**.",
        "",
        "## Blind-guesser scores",
        "",
        "| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |",
        "|---|---|---|---|",
    ]
    for name, r in sorted(heur.items(),
                          key=lambda kv: -(kv[1].get("exam_score_estimate") or 0)):
        acc = r["expected_accuracy"]
        est = r.get("exam_score_estimate")
        lines.append(
            f"| {name} | {acc:.1%} |" if acc is not None else f"| {name} | – |"
        )
        lines[-1] = (f"| {name} | {'–' if acc is None else f'{acc:.1%}'} "
                     f"| {r['coverage']:.0%} "
                     f"| {'–' if est is None else f'{est:.1%}'} |")
    lines += ["", "## Verdicts", ""]
    if blockers:
        lines += [f"- 🛑 **BLOCKER**: {b}" for b in blockers]
    if warnings:
        lines += [f"- ⚠️ {w}" for w in warnings]
    if not blockers and not warnings:
        lines.append("- ✅ no aggregate biases above thresholds")
    lines += ["", f"## Flagged questions ({len(flagged)})", ""]
    for f in flagged:
        for fl in f["flags"]:
            lines.append(f"- `{f['id']}` ({f['type']}) — **{fl['flag']}**"
                         f" [{fl['severity']}]: {fl['detail']}")
    if dupes:
        lines += ["", "## Cross-question duplicate option texts", ""]
        for t, where in dupes.items():
            lines.append(f"- \"{t[:80]}…\" appears as: {', '.join(where)}")
    lines.append("")
    (AUDIT_DIR / "meta_pattern_audit.md").write_text("\n".join(lines))

    print(f"audited {len(bank)} questions -> data/audits/meta_pattern_audit.{{json,md}}")
    print(f"blockers: {len(blockers)}  warnings: {len(warnings)}  "
          f"flagged questions: {len(flagged)}")
    for b in blockers:
        print(f"  BLOCKER: {b}")
    for w in warnings:
        print(f"  warn: {w}")

    if args.gate and blockers:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
