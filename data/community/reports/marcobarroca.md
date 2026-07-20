# Validation report — MarcoBarroca / `qiskit-v2-mock-exam`

- Source: https://github.com/MarcoBarroca/qiskit-v2-mock-exam/blob/main/notebooks/qiskit_v2_mock_exam.ipynb
- Author: **Marco Barroca** — thank you; the MIT license and doc citations stand out.
- Format: Jupyter notebook, **68 questions**, collapsible answers with per-choice
  explanations, IBM docs reference links, and optional scratch code cells.
- License: **MIT**.
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

This is a meticulously produced 68-question mock. Every question carries a
"Choice review" that explains each option, plus **references to the official IBM
Quantum docs** — which is exactly the behavior you want a study resource to model.
It mirrors the real exam's length and passing target, includes multi-select
("Select 2/3") items with up to six options, and keeps optional scratch cells so
learners can experiment. Genuinely high-craft work.

## Parse coverage

- Questions found / parsed: **68 / 68** (100%).
- All 68 have parsed options and stated answers, including 5- and 6-option
  multi-select items (answers span A-F; e.g. Q3 → `D, E, F`).
- Options use both plain (`- **A.**`) and checkbox (`- [ ] **A.**`) markers; both
  are handled. Code appears in ~56 stems.
- Normalized data: `data/community/parsed/marcobarroca.json`.

## Execution results (code-bearing questions)

Representative code items executed offline. **2 / 2 executed cleanly; 2 / 2
confirmed; 0 mismatches** (the exam is mostly reason-locally by design, so few
items have a single runnable output):

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 4 | multi-gate circuit final state (q2=1, q0→1, q1=1, then CX(1,2)) | dominant `'011'` | A (\|011⟩) | ✅ |
| 6 | Bloch vector of (√3/2)\|0⟩ + (1/2)\|1⟩ | (0.866, 0, 0.5) | C (panel C) | ✅ |

## Conceptual spot-check (5 sampled)

- **Q1:** `SamplerV2` returns "classical-register bitstring samples / count-access
  data" — **correct, and precisely V2-accurate** (no V1 "quasi-probability"
  language). (docs: https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/sampler-v2)
- **Q2:** `ParameterVector.resize(6)` to change vector length — correct.
- **Q5:** the Sampler option groups are `twirling` and `dynamical_decoupling` —
  **correct, and notably it does NOT claim Sampler has `resilience_level`** (the
  V1→V2 distinction that trips up several other exams). Nicely current.
- **Q7:** a `CircuitInstruction` combines an operation with its qubit/clbit
  operands — correct.
- **Q8:** transpiler passes are executed through a `PassManager` — correct.
  (docs: https://quantum.cloud.ibm.com/docs/guides/transpile)

## Findings & opportunities

No correctness issues were found in the executed or spot-checked subset. A few of
the "reason locally" numeric questions (e.g. Q4, Q6) reference figure assets under
`../assets/visuals/` that a reader must view alongside the notebook — worth keeping
those asset paths intact if the notebook is ever re-hosted. That is the only note.

## Verdict

Among the reviewed exams, this one is a model of good practice: exam-accurate
length and format, per-choice explanations, **inline doc citations**, and — where
we could test it — code answers that match Qiskit 2.5 behavior. It is also
conspicuously correct on the exact V2-primitive distinctions (Sampler has no
`resilience_level`; results are bitstring samples) that are the most common
drift traps in this cohort. Thank you, Marco; there is nothing to fix in what we
checked, and a PR would be welcome should any future issue arise.
