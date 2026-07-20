# Validation report — KurianUthuppu / `ibm_qiskit_2_x`

- Source: https://github.com/KurianUthuppu/ibm_qiskit_2_x (`Practice_Exams/practice_exam_1.md`)
- Author: **Kurian Uthuppu** — thank you for the exam *and* the detailed solutions.
- Format: Markdown, 20 questions, with a full worked-solution answer key in
  `Practice_Exams/solutions/answer_key_practice_exam_1.md`. (Default branch: `root`.)
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

A compact, professional 20-question exam (exactly the advocate minimum) with an
unusually rich answer key — each question gets a full worked explanation,
including hand-calculations for the probability items. Coverage is well balanced
across the eight syllabus sections, and several questions (EstimatorV2 resilience
levels, PUB broadcasting shapes, OpenQASM 3 types) are pitched at real exam
difficulty. The solutions file alone is a great study asset.

## Parse coverage

- Questions found / parsed: **20 / 20** (100%).
- All 20 have parsed options and a stated answer, including multi-answer items
  (Q6 → `C, D`; Q19 → `B, D`).
- Code-bearing questions: **19 / 20**.
- Normalized data: `data/community/parsed/kurian.json`.

## Execution results (code-bearing questions)

Nine items executed offline. **9 / 9 executed cleanly; 9 / 9 confirmed; 0 mismatches.**

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 3 | `Sdg` on \|1⟩ global phase | −π/2 rad | D | ✅ |
| 5 | `rx(3π/4)`, P(measure 0) | 0.1464 (=cos²(3π/8)) | A | ✅ |
| 6 | which build 3 qubits + 2 clbits | `QuantumCircuit(3,2)` and `QReg(3)+CReg(2)` | C,D | ✅ |
| 11 | `reset;h` on a qubit | \|+⟩ | B | ✅ |
| 13 | retrieve failed-job error | `RuntimeJobV2.error_message` exists | D | ✅ |
| 16 | `ParameterVector.index(x)` | returns 1 | B | ✅ |
| 17 | Pauli matching printed 4×4 matrix | `Pauli('ZX')` reproduces it | A | ✅ |
| 4 | OpenQASM 3 file output | `qiskit.qasm3.dump(circuit, file)` valid | B | ✅ |
| 20 | `PubResult` `data.evs.shape` for 5 observables, param shape (5,) | `(5,)` | D | ✅ |

Q17 is a nice "read the matrix" item — the printed array is exactly
`Pauli('ZX').to_matrix()`, confirming the key. Q20's broadcasting result `(5,)`
also matched exactly.

## Conceptual spot-check (5 sampled)

- **Q1:** `resilience_level = 2` enabling ZNE + gate twirling on **EstimatorV2** —
  correct (level 2 = ZNE). (docs: https://quantum.cloud.ibm.com/docs/guides/v2-primitives#error-mitigation-and-suppression)
- **Q8:** `QiskitRuntimeService.jobs` "retrieves all runtime jobs, subject to
  optional filtering" — correct.
- **Q12:** `RemoveFinalReset` / `SabreLayout` / `BasisTranslator` live in
  `qiskit.transpiler.passes` — correct. (docs: https://quantum.cloud.ibm.com/docs/api/qiskit/transpiler_passes)
- **Q15:** `service.backend("ibm_foo")` to connect to a named backend — correct.
- **Q18:** `SamplerOptions.default_shots` = "the number of times we run the
  circuit" — correct.

## Findings & opportunities

No correctness issues were found in the executed or spot-checked subset. Two of
the questions (Q2, Q7) reference figure assets (`../Images/broadcasting.png`,
`../Images/qsphere.png`) that a reader needs to view alongside the text — worth
keeping the image paths intact in any future re-hosting. That is the only
housekeeping note.

## Verdict

A tight, exam-accurate 20-question set backed by one of the best answer keys in
the surveyed cohort — the worked solutions and hand-calculations are exactly what
learners need, and every code item we executed matched. This resource punches
well above its size. Thank you, Kurian; a PR is welcome should any future drift
appear, but nothing needs fixing today.
