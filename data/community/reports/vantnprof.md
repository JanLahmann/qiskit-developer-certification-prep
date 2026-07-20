# Validation report — vantnprof / `Qiskit_v2X_Certificate_Practice`

- Source: https://github.com/vantnprof/Qiskit_v2X_Certificate_Practice/blob/main/Practice.md
- Author: **vantnprof** — thank you for this thorough, exam-shaped resource.
- Format: Markdown, **68 questions** with per-question collapsible answers +
  explanations AND a full answer-key table.
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

This is the closest of the reviewed exams to the real thing: it advertises the
authentic format (68 questions / 90 minutes / suggested 47 pass), mixes single-
answer and select-all-that-apply items, and gives each question an explanation
plus a consolidated key. Coverage is deep on the Runtime V2 surface —
Sampler/Estimator PUBs, sessions/batch, resilience (ZNE/PEC/PEA/twirling/DD),
result access, and OpenQASM 3. A lot of careful work went into this. Excellent.

## Parse coverage

- Questions found / parsed: **68 / 68** (100%).
- All 68 have parsed options and a stated answer (single and multi-answer, e.g.
  Q5 → `A, C`; Q59 → `C, D`).
- Code-bearing questions: **68 / 68**.
- Normalized data: `data/community/parsed/vantnprof.json`.

## Execution results (code-bearing questions)

Eleven representative items executed offline. **11 / 11 executed cleanly;
11 / 11 confirmed; 0 mismatches.**

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 3 | `count_ops().get("cx")` after 2 CX | 2 | B | ✅ |
| 5 | `Operator(qc)` / `.data` valid; `from qiskit import Operator` invalid | top-level import fails (ImportError) | A,C | ✅ |
| 7 | `x;h` on \|0⟩ | (\|0⟩−\|1⟩)/√2 | C | ✅ |
| 11 | `x;measure`, dominant key | `'1'` | C | ✅ |
| 15 | `h`, `probabilities_dict()` | {'0':0.5,'1':0.5} | C | ✅ |
| 17 | `x(0)` on 2 qubits (little-endian) | {'01':1.0} | B | ✅ |
| 21 | `assign_parameters(inplace=False)` | returns copy, orig unchanged | C | ✅ |
| 43 | default `measure_all()` register name | `meas` | A,B | ✅ |
| 55 | ⟨Z⟩ after `x(0)` | −1.0 | A | ✅ |
| 65 | `qasm3.dumps/dump` export; `qc.qasm()` | `qc.qasm()` removed in 2.x | A,B | ✅ |
| 66 | `qasm3.loads` import | callable | A | ✅ |

Notably, Q5, Q17, Q43, Q55 and Q65 all encode subtle 2.x facts (top-level
`Operator` import removed, little-endian bit order, the `meas` register name, and
the removal of `QuantumCircuit.qasm()`) — and execution confirms each.

## Conceptual spot-check (5 sampled)

- **Q33:** `from qiskit_ibm_runtime import SamplerV2` — correct home for V2 primitives.
- **Q38:** prefer primitives / `backend.run` over the removed global `execute()` —
  correct for 2.x.
- **Q52:** align observables with `obs.apply_layout(isa_circuit.layout)` after
  layout-changing transpilation — correct. (docs: https://quantum.cloud.ibm.com/docs/guides/primitives)
- **Q60:** `estimator.options.resilience_level = 0` to disable built-in mitigation —
  correct. (docs: https://quantum.cloud.ibm.com/docs/guides/v2-primitives#error-mitigation-and-suppression)
- **Q68:** `with qc.while_loop((c, 0)):` for a circuit-level while loop — correct,
  and the Python-`while` distractor is properly excluded.

## Findings & opportunities

No correctness issues were found in the executed or spot-checked subset. The
select-all questions are consistent (all-correct-and-no-extra scoring is stated
explicitly). If anything, this exam could be a reference template for the others.

## Verdict

An exemplary community mock exam: authentic format, deep V2 coverage, clean
explanations, and — importantly — code answers that survive execution on qiskit
2.5 / runtime 0.48, including several questions that specifically test 2.x
removals and conventions. Nothing to fix in what we checked. Thank you,
vantnprof; this is a standout resource, and we'd be glad to send a PR if any
future issue surfaces.
