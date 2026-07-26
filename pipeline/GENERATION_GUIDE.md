# CertiQ Question Generation Guide (contract for generation agents)

You are generating exam-prep questions for **CertiQ**, targeting IBM exam **C1000-179**
(Qiskit SDK v2.x + Runtime primitives V2). This document is a **contract**: every rule here
is enforced either by `pipeline/verify_bank.py` (machine gate) or by the adversarial review
wave that follows generation (agent gate). Questions that violate it get killed.

## 0. Inputs you must read first

1. `data/syllabus.json` — your section's official objectives, `scope_notes` (your topic
   checklist), and `resources` (your citation pool).
2. The three gold examples: `data/questions/s1/s1-q001.json` (predict-output, executed),
   `data/questions/s5/s5-q001.json` (mcq with empirical attempt-proof), and
   `data/questions/s4/s4-q001.json` (conceptual with citations).
3. `pipeline/harness/schema.py` — the schema your files must satisfy.
4. `pipeline/REVIEW_LEDGER.md` — verified library facts, dead-URL replacements,
   proof hazards, and meta-pattern calibration recipes from previous waves.
   Do not contradict a ledger entry without re-verifying it; APPEND what you
   verify. This file is how review knowledge survives between sessions.

## 1. Files, IDs, quotas

- One JSON file per question: `data/questions/<section>/<section>-q<NNN>.json`.
- **Start numbering at q010** (q001–q009 are reserved for seeds). Number sequentially.
- Section quotas (v1, ≈ weight-proportional):
  s1: 38 · s2: 26 · s3: 44 · s4: 36 · s5: 30 · s6: 30 · s7: 24 · s8: 16.
- Difficulty mix per section: ~30% level 1, ~50% level 2, ~20% level 3.
- Type mix: overall ≥50% of your section must carry an **executed proof**
  (`verification.mode: "script"`). Exceptions: s2 and s4 may go as low as 40% executed.
  Types: `mcq`, `multi` (use for genuine select-N cases, ~10-15% of quota — the real exam
  has them), `predict-output`, `spot-bug`.

## 2. Question craft (what the adversarial wave will try to kill)

1. **Exactly one defensible answer set.** The most common kill: a distractor that is
   "also kind of true". If you can argue for it, the reviewer will too.
2. **Exam-style stems**: concrete, scenario-based where possible, no trick wording,
   no negations like "which is NOT" unless clearly capitalized, self-contained
   (all needed context in stem+code).
3. **Distractors = real misconceptions**, not noise. Each wrong option encodes a specific
   confusion (V1→V2 migration habits, endianness/bit-ordering, S vs S†, shots vs precision,
   session vs batch, transpile-before-run forgotten, qasm2 vs qasm3 features...). The
   `explanation.distractors[key]` text must NAME the misconception.
4. **Options**: 4 options (A–D) standard; 5–6 allowed for `multi`. Alphabetical key order.
   Similar length/register (no "longest answer is correct" tells). No "All of the above".
   **Distractor pools**: a question MAY carry 5–6 options with `display_count: 4` (or 5) —
   the site then shows all correct answers + a seeded sample of distractors, so repeat
   encounters differ. Pool distractors are full citizens: named misconception,
   `explanation.distractors` entry, and (for executed questions) attempted/refuted in the
   proof with their own evidence key. The audit holds EVERY displayed variant to the
   anti-tell bar. `display_count` must leave >= 2 displayed distractors.
5. **No test-wise tells** (enforced by `pipeline/audit_meta_patterns.py --gate` in CI; a
   pilot user passed questions blind via "longest option wins"). A knowledge-free guesser
   must stay at chance. Concretely:
   - **Length**: the correct option must not be strictly longer than every distractor
     (audit flags high severity at ≥1.4× the longest distractor). Tighten the correct
     option; give distractors substantive plausible-but-wrong content — never filler.
   - **Position**: distribute answer keys ≈ uniformly across your section (s4, s5, and
     s8 each shipped 100% answer-"A" before review caught it — the generator's default
     habit is to write the correct option first; consciously vary it).
   - **Wording style**: hedged wording ("typically", "by default") must not appear only
     in correct options, nor absolutes ("always", "never", "only") only in distractors.
   - **Stem echo**: the correct option must not be the only one reusing the stem's
     vocabulary or exact docs terminology; distractors need equally authentic API names.
   - **Formatting**: don't code-format only the correct option (or only the distractors).
   - **Multi-select**: vary the number of correct options between questions.
   - **Calibrate to chance, not zero** — over-correcting any tell creates its
     inverse, and the audit measures both directions. Exact recipes (the N/4
     length split, the 3:1 absolutes rule, tie effects, tokenizer quirks) live
     in `pipeline/REVIEW_LEDGER.md`.
6. **Explanations teach**: `explanation.correct` explains the mechanism, not just the fact.
   Cite 1–3 URLs from your section's `resources` in syllabus.json (other
   `quantum.cloud.ibm.com/docs/...` URLs allowed if genuinely better).
7. **Coverage**: spread questions across ALL objectives and scope_notes of your section;
   tag `objectives` honestly (the mock exam samples by these tags).
8. **Version honesty**: target Qiskit 2.5 behavior as proven by execution. Don't test
   trivia that changed within the 2.x line unless the question is explicitly about it
   AND the proof pins it.

9. **Figure questions** (exam-realistic image items; gold example: `s2-q040`):
   - The `figures` block names a generator at `data/figures/<qid>/generate.py` that
     renders every declared SVG (basenames `<qid>-*.svg`, bare filenames into cwd).
     Run `.venv/bin/python pipeline/render_figures.py --only <qid>` — it renders twice
     and fails on nondeterminism (no unseeded randomness, no timestamps).
   - **Figures are execution artifacts**: option images are renders of the
     misconception's circuit/plot. The proof script MUST construct the *same* variants
     as the generator (copy-paste the variant definitions; note the sync duty in both
     files) and prove structural identity/difference vs the stem code.
   - Image options: all-or-none per question; option `text` may be `""` (uniformly);
     `alt` text is mandatory and must describe each figure faithfully AND with equal
     specificity across options (accessibility without extra answer leakage).
   - Anti-tell: the correct option's SVG must not be the visual-complexity outlier —
     the audit measures SVG byte size both directions (`largest_image_option` /
     `smallest_image_option` + `image_size_tell` flag). Craft distractor variants of
     comparable visual complexity.
   - `color_essential: true` for figures whose MEANING needs color (q-sphere phase);
     those are excluded from the e-ink EPUB (alt text stands in).
   - Figure questions may use 4-5 authored options (rendering cost); `display_count`
     rotation still applies when >4.

## 3. Legal / NDA rules (non-negotiable)

- Generate **original** questions from the public objectives + official docs + your own
  expertise. Do NOT copy or lightly paraphrase questions from the IBM sample test, any
  community practice exam, Udemy course, or the docs' own examples. If a scenario
  coincides in topic (inevitable), the numbers, code, framing, and distractors must be yours.
- Never reproduce more than a short code idiom from official docs (prose: never).

## 4. Proof-script contract (`verification.proof_script`)

The harness prepends a prelude giving you `emit_verdict(dict)` and (optionally) patching
`QiskitRuntimeService` to fake backends. Your script must:

1. **Prove empirically.** Execute the actual claim of every option:
   - predict-output: compute the real result; compare against each option's claimed value.
   - "which call is correct": attempt each option's call; correct must succeed with
     observed output; wrong ones must raise (capture exception type+message).
   - spot-bug: run the buggy code (show the failure/wrong result), run the fix (show it works).
2. Call `emit_verdict({...})` **exactly once**, with:
   - `"answer"`: list of option keys your execution PROVED correct — computed from the
     execution, not hardcoded. (If your execution disagrees with your intended answer,
     your question is wrong: fix the question, don't fake the proof.)
   - `"evidence"`: an entry for EVERY option key, containing observed values
     (numbers, exception names, counts...) — these strings appear on the site as the proof.
   - `"observed"`: key raw results (JSON-serializable).
3. **Determinism**: seed everything that samples
   (`AerSimulator(seed_simulator=42)`, `GenericBackendV2(..., seed=42)`,
   `sampler.run(..., shots=...)` on fake backends is seeded by the backend's simulator —
   prefer assertions with tolerances for sampled counts, exact checks for statevectors).
4. **Stay small and local**:
   - No network, no credentials, no `QiskitRuntimeService` (the patch makes it fake, but
     prefer fake backends directly: `from qiskit_ibm_runtime.fake_provider import FakeManilaV2`).
   - **The 127-qubit trap**: transpiling to FakeBrisbane pads circuits to 127 qubits; a
     non-Clifford circuit then kills the statevector simulator. Use small backends
     (`FakeManilaV2` 5q, or `GenericBackendV2(num_qubits=..., seed=...)` from
     `qiskit.providers.fake_provider`) unless your circuit is pure Clifford.
   - Budget: < 60s wall time per proof (hard kill at 180s). `MPLBACKEND=Agg` is set —
     never call `plt.show()`.
5. Visualization questions (s2): prove programmatically — check return types
   (`matplotlib.figure.Figure`), the statevector/counts behind the plot, or attempt-based
   proofs of call signatures. If a claim is genuinely not machine-checkable, make the
   question conceptual (mode `"none"`) with strong citations instead of a weak proof.

## 5. Conceptual questions (`verification.mode: "none"`)

Allowed where execution genuinely can't decide (policy/when-to-use-what, workflow,
plan/queueing semantics). Requirements: `proof.status: "conceptual"`, ≥1 citation that
actually supports the answer (the adversarial wave opens your citations), and the
distractor rationales must be checkable against those pages.

## 6. Provenance block

```json
"provenance": {
  "generated": "2026-07-20",
  "model": "claude-opus (generation agent, section sX)",
  "adversarial_rounds": 0,
  "reviewed": false
}
```
(`adversarial_rounds` is incremented by the review wave, not by you.)
Do NOT include a `freshness` block — the verifier stamps it.

## 7. Your workflow

1. Read inputs (§0). Plan coverage across objectives/scope_notes.
2. Write questions in batches of ~5. After each batch run BOTH gates:
   `.venv/bin/python pipeline/verify_bank.py --section <sX> --jobs 2`
   `python3 pipeline/audit_meta_patterns.py --section <sX>`
   Fix every verify failure before continuing. A failure of the form
   "verdict.answer != question.answer" means your question (or your understanding) is
   wrong — investigate the observed evidence, then fix the QUESTION to match reality.
   Fix every high/medium audit flag as you go — form defects (position skew, length
   tells) are generator habits; they compound silently if left to the review wave.
   Calibration target is CHANCE, never zero: the audit measures each tell in both
   directions (longest/avoid_longest, most/avoid_hedged, least/most_absolute) — the
   exact recipes are in `pipeline/REVIEW_LEDGER.md`.
3. Finish only when: full quota written AND `verify_bank.py --section <sX>` exits 0
   with zero failures AND the section audit shows 0 blockers/warnings and no
   high/medium flags.
4. Do NOT run git commands. Do NOT touch files outside `data/questions/<your section>/`
   and `data/proofs/` (written by the verifier for your section).
5. Final message = data for the orchestrator (not prose): counts by type/difficulty,
   objective coverage map, list of question ids with one-line topic each, anything you
   are uncertain about (flag candidates for extra review), verify summary line.
