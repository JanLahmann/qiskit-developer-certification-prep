# Validation report — rishihg / `Qiskit-v2.x-Certification-practice-exam`

- Source: https://github.com/rishihg/Qiskit-v2.x-Certification-practice-exam (`mock_exam.md`)
- Author: **rishihg** — thank you; the MIT license here is especially appreciated.
- Format: Markdown, 25 questions, inline collapsible answer grid; labeled "(Verified)".
- License: **MIT** (clear reuse terms — a nice example for the cohort).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

A clean, fast-moving 25-question set focused on conceptual and API recall across
all eight sections — packages, gates, primitives, transpilation, execution modes,
OpenQASM 3, and dynamic circuits. It is compact, readable, and (rare among these
repos) permissively licensed, which makes it easy to build on. Thanks for making
it MIT.

## Parse coverage

- Questions found / parsed: **25 / 25** (100%).
- All 25 have parsed options and a single stated answer (from the answer grid).
- Code-bearing questions: mostly prose/API recall — few executable snippets
  (~3 flagged as containing code).
- Normalized data: `data/community/parsed/rishihg.json`.

## Execution results

This exam is conceptual, so most items are checked against docs rather than
executed. The one directly executable API claim was run offline:

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 24 | set resilience level on the **Sampler** primitive via `sampler.options.resilience_level = 1` | **raises** `pydantic ValidationError: SamplerOptions has no attribute 'resilience_level'` | B | ⚠️ version drift |

**1 executed; 0 confirmed; 1 mismatch (classified as version drift — see below).**

## Conceptual spot-check (5 sampled)

- **Q13:** `qiskit.primitives` offers simplified interfaces for running
  computations — correct.
- **Q16:** `AerSimulator` as the default Aer simulator backend — correct.
- **Q23:** `bit[5] myregister;` for a 5-bit OpenQASM 3 classical register — correct.
  (docs: https://quantum.cloud.ibm.com/docs/guides/interoperate-qiskit-qasm3)
- **Q25:** `circuit.if_test((clbit, 1), true_body)` for classical feedforward —
  correct, and consistent with the 2.x removal of `c_if`.
- **Q22:** Batch mode for "multiple related jobs with reduced queue times" — an
  acceptable answer (both Batch and Session reduce queueing; Session is the more
  natural fit for tightly *iterative* related jobs). (docs: https://quantum.cloud.ibm.com/docs/guides/execution-modes)

## Findings & opportunities

The exam is largely accurate. Three items are worth a look, one substantive and
two cosmetic:

1. **Q24 — version drift (substantive).** The question asks how to "set the
   resilience level to 1 … in the **Sampler** primitive" and keys answer B:
   `sampler.options.resilience_level = 1`. On the pinned v2.x stack this **fails** —
   `SamplerV2`/`SamplerOptions` has no `resilience_level`; it is an **Estimator**
   option. This was valid under the older/V1 runtime model where resilience applied
   to both primitives, so we classify it as **version drift, not an author error**.
   Because the exam explicitly targets v2.x, the constructive fix is to re-point the
   question at `EstimatorV2` (or ask which Sampler options *do* exist —
   `dynamical_decoupling`, `twirling`). Reference:
   https://quantum.cloud.ibm.com/docs/guides/v2-primitives#error-mitigation-and-suppression
   ("resilience_level (if using Estimator)").

2. **Q5 — V1 terminology (cosmetic).** "Which V2 primitive … gets *quasi-probability
   distributions*?" keys `SamplerV2`. SamplerV2 returns per-register bitstring
   samples/counts (`BitArray`); *quasi-probability distributions* were the **V1**
   Sampler output. The intended answer is still SamplerV2 — only the phrasing is a
   V1 holdover.

3. **Q20 — imprecise "all of the above" (cosmetic).** For "intermediate statevectors",
   option C (`StatevectorSampler`) returns sampled counts, not statevectors, so the
   keyed "All of the above" is a slight stretch. `save_statevector` (Aer) and
   `Statevector.from_instruction` are the clean answers.

## Verdict

A tidy, permissively licensed exam that is correct on the concepts we checked —
its main issue is a single question (Q24) that drifted with the V1→V2 move of the
`resilience_level` option, plus two spots where V1-era wording lingers. None of
these reflect a misunderstanding of the underlying physics; they are exactly the
kind of upkeep every v2.x exam needs as the runtime evolves. Thank you, rishihg —
and given the MIT license, we'd be happy to open a small PR re-anchoring Q24 on
EstimatorV2 if that would help.
