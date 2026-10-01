# Exam-Realism Contract (wave R, 2026-10-01)

Binding contract for the realism **audit** agents (R1, one per section) and the
**expansion** agents (R2). Authority: the official C1000-179 study guide and sample
test, analyzed locally; every official-derived number below is a committed statistic
from `data/audits/official_alignment.*`. **NDA rule (non-negotiable): no official
question text, figures, or option sets may appear in any repo file or any agent
output — topic labels and statistics only.**

## Official exam profile (the target)

- 68 questions / 90 min / pass 47. Section weights 16/11/18/15/12/12/10/6.
- Formats: ~33 % output-prediction, ~10 % multi-select, ~19 % figure-based, 0 spot-bug
  (ours stay — deliberate pedagogy — but they don't grow).
- 4 displayed options is the norm. Stems are short and concrete: official median
  ~14 words, minimal scenario dressing.
- Difficulty mix ≈ **40 % easy / 45 % medium / 15 % hard**. Our bank pre-wave:
  27/56/17 with stem median 23 — one notch too hard, one sentence too long.

## Difficulty rubric (rate honestly; never force the mix per question)

- **1** — one recalled fact, or a one-step read of a short snippet; a prepared
  candidate answers in <30 s.
- **2** — apply one concept with a twist, or two mental steps (e.g. transpile then
  reason about layout; compute a parameter count).
- **3** — ≥2 interacting concepts, subtle semantics, or multi-step code tracing
  (e.g. broadcasting edge cases, endianness through composition).

## R1 audit tasks (per question, edited in place)

1. **Correctness**: re-verify the claim against the pinned Qiskit stack. Executed
   questions: rerun proofs via `verify_bank.py`. Conceptual: open the citations
   (qiskit-docs MCP or the live docs). If execution/docs contradict the stored
   answer → fix the QUESTION (and proof), never hand-edit the verdict; append a
   `REVIEW_LEDGER.md` entry.
2. **Difficulty**: re-rate per the rubric above. The bank historically over-rates:
   expect a real share of 2s to become 1s. Record every change.
3. **Stem concision**: rewrite stems toward exam register — target ≤18 words
   typical, hard cap 30 unless the scenario genuinely needs more. Keep stems
   self-contained; do not change what is asked; do not touch code blocks except to
   fix a verified error.
4. **Anti-tell re-check** after edits: `audit_meta_patterns.py --section` must stay
   at 0 blockers / 0 warnings, no high/medium flags (recipes: `REVIEW_LEDGER.md`).
5. **Provenance**: `adversarial_rounds += 1`; append to `notes`:
   `"realism audit 2026-10-01: <one line of what changed>"`.

## R1 agents may NOT

- Change answer keys, options, or proofs except to fix a verified correctness error
  (ledger entry required).
- Delete questions — flag kill-candidates to the orchestrator instead.
- Run any git command.
- Touch files outside `data/questions/<their section>/` (+ `data/proofs/` via the
  verifier, + appending to `pipeline/REVIEW_LEDGER.md`).
- Copy official sample-test or study-guide text anywhere.

## R2 expansion targets (after R1; to ~350 questions)

Adds per section (weight-proportional): s1 +12 · s2 +2 · s3 +14 · s4 +11 · s5 +8 ·
s6 +9 · s7 +6 · s8 +1 → 350. Rules: `GENERATION_GUIDE.md` applies in full, plus:

- New questions are predominantly difficulty 1 (bank-wide landing target 40/45/15).
- Figure questions prioritized wherever the topic renders naturally (circuits,
  histograms, gate maps, Bloch/q-sphere): aim ≥⅓ of each section's adds, pushing
  bank figure share from 9 % toward the official 19 %.
- Session-concept items added under **s7** (official exam places "purpose of a
  session" in Section 7; see alignment audit, sample 18 note).
- The orchestrator runs the anti-duplication token-Jaccard scan of every new
  question against the official sample test (threshold 0.5 review line) — agents
  never see or need the official PDFs.

## Validation commands (the only commands agents run)

- `.venv/bin/python pipeline/verify_bank.py --section sX --jobs 2` → must exit 0
- `python3 pipeline/audit_meta_patterns.py --section sX` → 0 blockers / 0 warnings
- `.venv/bin/python pipeline/render_figures.py --only <qid>` after editing any
  figure question
- `python3 -c` one-liners for local inspection

Orchestrator gates per wave: full verify_bank, meta-audit `--gate`, both builders
(`build_study.py`, `build_epub.py`), `npm run build`, diff review, ledger review.
