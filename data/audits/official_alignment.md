# Official-alignment audit — C1000-179 study guide + sample test (task #25)

**Date:** 2026-07-26 · **Bank state:** 243 questions, 28 primers, 216 cram facts (pre-fix-wave)
**Machine-readable version:** `official_alignment.json` (full coverage matrix, per-task question ids, style stats)

## Sources

Both official PDFs are **publicly downloadable** from the IBM exam page (verified 2026-07-26 via the
unauthenticated `getExam/C1000-179` API; bytes hash-identical to the community mirror copies):

- Study guide `C1000-179_STU` — sha256 `e9ac9881989dbaba…` (8 sections, **21 TASKs**, reference URLs)
- Sample test `C1000-179_SAM` — sha256 `8d191ff0be9dcdf4…` (**21 questions** + answer key)

NDA hygiene: the PDFs are analyzed locally and **never committed**; this report carries topic labels
and statistics only, no official question text. Per user authorization (2026-07-26) the sample test
may be *used and mentioned* on the site, citing the stable exam-page URL.

## 1 · Syllabus fidelity — VERIFIED, five wording fixes applied

- **Weights exact:** 16/11/18/15/12/12/10/6 (sum 100). Exam facts 68 Q / 90 min / pass 47 confirmed.
- **Section titles verbatim**, all 8.
- **Objective wording updated to the study guide's** (ids stable): `s4o1`, `s4o2` (now explicitly
  names *broadcasting rules*), `s5o1` (*"such as dynamical decoupling"* — official, and technically
  the correct wording since SamplerV2 has no `resilience_level`), `s7o1`, `s8o2`.
- **Known deltas kept:** s3 objective order differs from the official task order (cosmetic, ids
  stable); `s5o2` *"Bypass runtime error mitigations"* is an Advocate-Guide extra with no official
  TASK (annotated in `syllabus.json`; folds under official 5.1).
- `resource_gaps` correction: `guides/execute-on-hardware` exists (referenced verbatim by tasks
  4.1/4.2) but redirects to `guides/intro-to-patterns`; resource added under the target slug.

## 2 · Coverage matrix — 16/21 TASKs covered, 5 thin, 0 uncovered

All 21 study-guide TASKs and all 21 sample-test topics map to at least one CertiQ question; no outright
gap. Thin spots (all confirmed by independent grep):

| Where | Finding |
|---|---|
| Task 1.2 | **Circuit library absent**: 0 hits for QFT / RealAmplitudes / EfficientSU2 / TwoLocal / QuantumVolume / random_circuit — one of only two official references for a 16 % section |
| Task 2.2 | **`plot_gate_map` absent** (also plot_error_map / plot_circuit_layout) — explicitly referenced API |
| Task 7.2 | Only **4 questions** for job monitoring; `JobStatus` and `session.details()` each covered exactly once (sample topic 19 has a single covering item) |
| Task 4.2 / sample 12 | Broadcasting **mechanics** covered (7 items) but the docs' **named patterns** ("all-to-all", "standard multidimensional array generalization") never appear |
| Task 8.1 / sample 20 | OpenQASM 3 **type system** effectively 1 question, via the Qiskit feature table, not the openqasm.com types page; no casting-rules item |
| Task 8.4 | REST API: 3 questions (auth + job POST only; no results/backends/sessions endpoints) |

Minor: `SamplerPubResult` (2×, distractor-only) and `BasePrimitiveJob` (0×) never named as answers;
`ParameterExpression` named once; only 2 transpiler pass classes ever named; `Statevector.sample_counts` 0×.

**Fix wave:** the 6 material findings above become generation targets (see fix-wave commit following
this audit). Sample 18 note: IBM places the "purpose of a session" concept in exam Section 7 while all
our covering items sit in s4 — accepted, flagged for mock-exam realism.

## 3 · Anti-duplication vs the sample test — PASS

Token-Jaccard scan of all 21 sample questions against all 243 bank questions (stem+code+options):
**max similarity 0.214**, far under the 0.5 review line; the two nearest pairs were manually reviewed
and are topical neighbors with entirely different questions. **No kills, no rework.** Full per-sample
top-3 table in the JSON.

## 4 · Style/difficulty profile vs the sample test

Well matched: output-prediction share **32.1 % vs 33.3 %**, multi-select **11.9 % vs 9.5 %**, code-block
length median 6 vs 5 lines, displayed option counts (178×4, 61×5) sit on the official 4-option norm,
answer-key balance A–D 74/74/72/61.

Deviations (accepted, documented):

- **Zero image-bearing items vs 19 % of the sample** (figure-recognition format). Largest format
  divergence; static-pipeline limitation, candidate future work.
- Our bank is more code-heavy (code anywhere 92.6 % vs 57.1 %) and stems run longer (median 23 vs 14
  words) — deliberate for a *prep* bank.
- Difficulty skews one notch harder (d1/d2/d3 = 28/52/20 % vs sample ≈ 40/45/15 %) — noted; mock-exam
  sampler could over-weight d1–2 for timing realism.
- Sample has zero spot-the-bug items; we have 25 (10.3 %) — deliberate pedagogy, kept.

## 5 · Cram-layer coverage

Every one of the 21 TASKs has ≥1 primer and ≥3 facts except the thin areas above (task 8.1: 3 facts,
task 8.4: 3 facts). Fix wave adds facts alongside questions for each gap area.

## Verdict

**Aligned.** Blueprint fidelity is now verified verbatim; no NDA proximity to the sample test; no
uncovered official task. Six thin areas queued for a generation fix wave; syllabus provenance blocks
upgraded to "verified 2026-07-26".
