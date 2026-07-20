# Validation report — algovista-collab / `qiskit_v2_study_materials`

- Source: https://github.com/algovista-collab/qiskit_v2_study_materials/blob/main/25_Practice_Questions.md
- Author: **algovista-collab** — thank you for pairing the exam with full explanations.
- Format: Markdown, 25 questions + a "Complete Answer Key & Thorough Explanations"
  section; also ships 8 per-section study notebooks/PDFs.
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

A 25-question set that deliberately targets the trickier corners of the syllabus
— little-endian Pauli ordering, `from_sparse_list` indexing, PUB broadcasting,
ECR-vs-CX translation, execution-mode billing — and backs every question with a
per-option explanation of why it is right or wrong. The companion notebooks cover
all eight sections. This is a lot of material, generously shared.

## Parse coverage

- Questions found / parsed: **25 / 25** (100%).
- All 25 have parsed options and a stated answer (multi-answer items too, e.g.
  Q1 → `A, B`; Q10 → `A, D`).
- Code-bearing questions: **21 / 25**.
- Normalized data: `data/community/parsed/algovista.json`.

## Execution results (code-bearing questions)

Five items executed offline. **5 / 5 executed cleanly; 5 / 5 confirmed; 0 mismatches.**
Several of these were the exam's hardest "gotcha" items, and they held up:

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 1 | which give `−iY` | `X@Z == −iY` ✅, `from_list([("Y",−1j)])` ✅, `Z@X == +iY` ✗ | A,B | ✅ |
| 2 | `from_sparse_list([("XYZ",(1,3,4),2.0)], num_qubits=6)` | label `'IZYIXI'` | B | ✅ |
| 3 | `ry(π/3); rz(π/2)`, P(1) | 0.25 (RZ leaves probabilities unchanged) | A | ✅ |
| 5 | `Statevector.from_label('r-')` Bloch dirs | q0(from '-') = −X, q1(from 'r') = +Y | B | ✅ |
| 6 | `measure_all(add_bits=False)` | reuses existing register; no new `meas`, clbits 2→2 | B | ✅ |

Q5 and Q6 are worth calling out: both encode a subtle claim (the little-endian
mapping of the `'r-'` label, and the exact behavior of `add_bits=False`), and
**execution vindicates the author on both** — the −X/+Y assignment and the
"reuse the pre-allocated register" behavior are exactly what Qiskit does.

## Conceptual spot-check (5 sampled)

- **Q7:** `optimization_level` governs transpiler effort/depth — correct.
  (docs: https://quantum.cloud.ibm.com/docs/guides/set-optimization)
- **Q11:** `.close()` stops new submissions but lets queued jobs finish — correct.
- **Q13:** the V2 workflow order (backend → circuit → transpile → map observables
  → configure → run) — correct. (docs: https://quantum.cloud.ibm.com/docs/guides/primitives)
- **Q19:** `array[uint[4], 8] my_array;` for an OpenQASM 3 array of 4-bit registers
  — correct syntax. (docs: https://quantum.cloud.ibm.com/docs/guides/interoperate-qiskit-qasm3)
- **Q23:** submitting an untranspiled circuit to a V2 primitive fails (ISA circuits
  required) — correct.

## Findings & opportunities

No answer errors were found in the executed or spot-checked subset — including
the questions I most expected to catch out an auto-generated exam. Two gentle,
polish-only opportunities:

- **Explanation style:** several rationales use ornate phrasing ("continuous phase
  multiplier", "un-optimized opaque black-box structures") that reads as
  machine-generated and occasionally over-explains. Tightening to plain language
  would make the (correct) answers land harder.
- **Q22 wording:** `job.wait_for_final_state()` is the right choice, but its
  explanation says it "prints progress updates" — it primarily *blocks* until a
  final state and doesn't print by default. The answer is fine; the justification
  could be trimmed.

## Verdict

Despite a verbose, auto-generated feel to the prose, the substance is sound: the
hardest code items — `−iY` composition, sparse-Pauli indexing, RZ-invariance of
probabilities, `'r-'` Bloch directions, `add_bits=False` semantics — all match
Qiskit's actual behavior. That is a real credit to the author's care. The only
opportunities are cosmetic (explanation tightening). Thank you, algovista-collab;
PRs welcome if you'd like help trimming the rationales.
