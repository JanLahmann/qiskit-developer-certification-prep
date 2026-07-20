# Validation report — Q-Bees / `Qiskit-v2.X-Certification-Practice-Questions`

- Source: https://github.com/Q-Bees/Qiskit-v2.X-Certification-Practice-Questions/blob/main/Qiskit-Practice-Exam.ipynb
- Author: **Q-Bees** — thank you for a polished, scenario-driven notebook.
- Format: Jupyter notebook, 25 MCQs (one markdown cell each, inline `**Answer**`),
  plus a full set of per-section theory/coding practice + tutorial notebooks.
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

Rather than terse recall items, Q-Bees writes *scenario* questions ("You are
building a variational algorithm…", "You submitted a long-running experiment…"),
which is a genuinely good way to test whether a learner can apply the concept.
The 25-question exam is complemented by section-by-section practice notebooks, so
the repo doubles as a study path. Thoughtfully assembled.

## Parse coverage

- Questions found / parsed: **25 / 25** (100%).
- All 25 have parsed options (A-D) and a stated answer.
- Code-bearing questions: mostly prose scenarios; ~3 embed code (e.g. the Q13
  OpenQASM 3 fragment).
- Normalized data: `data/community/parsed/qbees.json`.

## Execution results

This is a concept/application exam; almost no item is a "run it and read the
output" question, so validation is primarily docs-based. The one embedded-code
item (Q13) was reasoned/executed offline: an OpenQASM 3 `reset; rx(π/2); measure;
if(c==1) z` block behaves as the keyed answer A describes (reset → rotate →
measure → conditional Z). **Confirmed.** No mismatches surfaced from execution.

## Conceptual spot-check (5 sampled)

- **Q5:** compare two circuits' unitaries by converting to `Operator` and comparing
  matrices — correct. (docs: https://quantum.cloud.ibm.com/docs/api/qiskit/qiskit.quantum_info.Operator)
- **Q7:** represent `0.5·Z₀Z₁ + X₁` with `SparsePauliOp` — correct and idiomatic.
- **Q13:** OpenQASM 3 conditional block semantics — correct (answer A).
  (docs: https://quantum.cloud.ibm.com/docs/guides/interoperate-qiskit-qasm3)
- **Q16:** a single long-lived `Session` groups related jobs / reduces overhead —
  correct. (docs: https://quantum.cloud.ibm.com/docs/guides/execution-modes)
- **Q17:** transpiler inserts SWAPs to satisfy the coupling map — correct.

## Findings & opportunities

The concepts are on target. One item is worth revisiting for v2.x accuracy:

- **Q14 — Sampler output wording (version drift).** The keyed answer C says the
  Sampler "returns *quasi-probabilities* per bitstring that may not be exactly
  non-negative or normalized." That description fits the **V1** Sampler (quasi-
  probability distributions, possibly negative under mitigation). **SamplerV2**
  returns per-register bitstring samples exposed as integer counts (`BitArray` /
  `get_counts()`) — so option A ("raw counts", modulo the "no normalization"
  nuance) is actually closer to V2 behavior than the keyed C. Since the exam
  targets v2.x, re-wording this toward "sampled bitstring counts" would remove the
  ambiguity. Reference:
  https://quantum.cloud.ibm.com/docs/guides/v2-primitives (Sampler V2 result shape).

A tiny cosmetic note: Q10 cites `StochasticSwap` as the routing pass example; it
still exists but `SabreSwap` is the modern default, so a refreshed example would
read as more current.

## Verdict

A well-designed, application-focused exam with strong companion material; the
scenario style is a real strength. The concepts check out, with a single
v2.x-accuracy opportunity around how SamplerV2 reports results (Q14), which
carries V1 "quasi-probability" language. That is normal runtime-evolution upkeep,
not a conceptual error. Thank you, Q-Bees — happy to send a PR tweaking the Q14
wording if useful.
