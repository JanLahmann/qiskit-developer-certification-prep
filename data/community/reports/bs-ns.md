# Validation report — bs-ns / `qiskit-v2-exam-quiz`

- Source: https://github.com/bs-ns/qiskit-v2-exam-quiz (`01-easy test.ipynb`, `02-harder test.ipynb`)
- Author: **bs-ns** — thank you for splitting the set by difficulty.
- Format: Two Jupyter notebooks, one markdown cell per question, answer in a
  `<details>` block with a short rationale.
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

Two clean, well-formed notebooks: 39 "easy" questions covering the whole syllabus
at recall level, and 27 "difficult" questions that are almost entirely
*computational* — Bell-state identification, expectation values of Pauli sums,
and PUB broadcasting shapes. That second notebook is unusual and valuable: it is
the only set in the cohort where nearly every item can be settled by running
three lines of Qiskit, which makes it excellent self-check material and made it
the most thoroughly verifiable set in this pass.

## Parse coverage

- Questions found / parsed: **66 / 66** (39 easy + 27 harder).
- All 66 have four options and a stated answer.
- Code-bearing questions: **41 / 66**.
- Normalized data: `data/community/parsed/bs-ns.json` (each item carries a `tier`
  field: `easy` / `harder`).

## Method

Snippets were extracted by hand, reviewed, and executed offline in the pinned
project stack (fake backends, no credentials, no network, 60 s per snippet).
Six grouped snippets — single-qubit states, Bell-state identification,
expectation values, PUB broadcasting, Pauli conventions, and API existence —
covered **39 of the 66 questions**. The remainder are conceptual recall items
(execution modes, twirling, transpilation purpose) and were spot-checked against
the docs.

## Execution results

**39 questions executed; 38 confirmed, 1 mismatch.**

| Tier/Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| easy 1 | `Pauli("YZ")` reading | q0 = Z, q1 = Y | A | confirmed |
| easy 2 | `ry(π/2)`, P(1) | 0.5 | C | confirmed |
| easy 6 | `x` then `h` | (\|0⟩ − \|1⟩)/√2 | B | confirmed |
| easy 23 | `Pauli("ZZ")` matrix | 4 × 4 | C | confirmed |
| easy 24 | `h` then `z` | (\|0⟩ − \|1⟩)/√2 | B | confirmed |
| easy 27 | `ry(0)` | \|0⟩ | A | confirmed |
| easy 29 | export to OpenQASM 3 | `qiskit.qasm3.dump`; no `QuantumCircuit.to_openqasm3` | D | confirmed |
| easy 30 | `x(1); cx(1,0)` | \|11⟩ | C | confirmed |
| easy 33 | `h` + `measure_all` | {0: 0.5, 1: 0.5} | C | confirmed |
| easy 35 | success status | `DONE` in `JobStatus` | C | confirmed |
| easy 36 | `h; h` | \|0⟩ | A | confirmed |
| easy 37 | `Statevector.from_label("+")` | [0.7071, 0.7071] | C | confirmed |
| harder 1 | ⟨ZZ⟩ on Bell | 1.0 | C | confirmed |
| harder 2 | `h; cx; z(0)` | Φ⁻ | B | confirmed |
| harder 3 | ⟨XX⟩ on Φ⁺ | 1.0 | C | confirmed |
| harder 4 | ⟨ZI⟩ on Φ⁺ | 0.0 | B | confirmed |
| harder 5 | evs count for `[[0],[1],[2]]` | shape (3,) | C | confirmed |
| harder 6 | ⟨X⟩ after `ry(π/2)` | 1.0 | D | confirmed |
| harder 7 | ⟨X⟩ on \|−⟩ | −1.0 | A | confirmed |
| harder 8 | `Pauli("XYZ")`, which qubit gets Z | q0 | A | confirmed |
| harder 9 | evs count, obs (2,) × params (3,) | `ValueError: … not broadcastable` | D (6) | **mismatch** |
| harder 10 | ⟨XX+YY+ZZ⟩ on Ψ⁻ | −3.0 | A | confirmed |
| harder 11 | ⟨XX+YY⟩ on Φ⁺ | 0.0 | C | confirmed |
| harder 12 | evs shape, obs (3,1) × params (4,) | (3, 4) | A | confirmed |
| harder 13 | `x(0); h(0); cx; z(1)` | Φ⁺ | A | confirmed |
| harder 14 | ⟨XX−YY+ZZ⟩ on Ψ⁺ | −1.0 | A | confirmed |
| harder 15 | ⟨X+Z⟩ after `ry(π/4)` | 1.414214 (=√2) | B | confirmed |
| harder 16 | `h; cx; h(1)` | (\|00⟩+\|01⟩+\|10⟩−\|11⟩)/2 | A | confirmed |
| harder 17 | Z⊗Z on Φ⁺ | Φ⁺ | A | confirmed |
| harder 18 | ⟨XX+ZZ⟩ on Φ⁺ | 2.0 | D | confirmed |
| harder 19 | ⟨XX+YY−ZZ⟩ on Φ⁻ | −1.0 | B | confirmed |
| harder 20 | `h; cx; h(0); h(1)` | (\|00⟩+\|11⟩)/√2 | C | confirmed |
| harder 21 | `h; cx; x(0)` | Ψ⁺ | C | confirmed |
| harder 22 | ⟨Z⟩ after `ry(π/3)` | 0.5 | A | confirmed |
| harder 24 | `x(0); h(0); cx` | Φ⁻ | B | confirmed |
| harder 25 | ⟨YY⟩ on Φ⁺ | −1.0 | A | confirmed |
| harder 26 | ⟨Z⟩ after `rx(π/2)` | 0.0 | B | confirmed |
| harder 27 | `h; cx; x(1)` | Ψ⁺ | C | confirmed |
| harder 28 | `h; cx; z(0); x(1)` | Ψ⁻ | B | confirmed |

## Findings

**1. Harder Q9 — the observables array as written is not broadcastable.** The PUB
is `(circuit, [obs1, obs2], [[0],[np.pi/2],[np.pi]])` and the key is 6. Executed,
that shape pairing raises

> `ValueError: The observables shape (2,) and the parameter values shape (3,) are not broadcastable.`

A flat list of two observables has shape `(2,)`, not `(2,1)`. Writing the
observables as `[[obs1], [obs2]]` gives shape `(2,1)`, which broadcasts against
`(3,)` to `(2,3)` = 6 expectation values — i.e. the key is right about the
*intended* arithmetic but the snippet as printed errors out. Adding the inner
brackets fixes it. (This is exactly the distinction the same notebook gets right
in harder Q12, where the observables *are* written `[[obs1],[obs2],[obs3]]` and
the executed shape is (3,4), matching the key.)

**2. The harder notebook skips Q23** — numbering runs …21, 22, 24, 25… so the
notebook contains 27 questions under 28 headings. Cosmetic only.

**3. Everything else in the computational set is exactly right**, including the
sign-sensitive items that are easy to get wrong by hand: ⟨YY⟩ = −1 on Φ⁺,
⟨XX+YY⟩ = 0 on Φ⁺, ⟨XX−YY+ZZ⟩ = −1 on Ψ⁺, and the Bell-state relabelling chain
(`z(0)` → Φ⁻, `x(1)` → Ψ⁺, `z(0); x(1)` → Ψ⁻). The Pauli-ordering items (easy
Q1, harder Q8) also use the correct little-endian reading.

## Conceptual spot-check (5 sampled)

- **easy Q10** valid EstimatorV2 PUB `(circuit, observable, parameter_values, precision)` — correct.
- **easy Q14/Q15** Session for iterative variational work, Batch for grouping many
  independent jobs — correct. (docs: https://quantum.cloud.ibm.com/docs/guides/execution-modes)
- **easy Q16** dynamical decoupling as the idle-gate Sampler option — correct.
- **easy Q18** larger precision → fewer shots — correct.
- **easy Q21** `complex` as an OpenQASM 3 classical type — correct.

## Verdict

The strongest *verifiable* set in this pass: 38 of 39 executed answers confirmed,
including a long run of expectation-value items that are precisely the kind of
thing a hand-written exam usually gets wrong somewhere. One PUB item (harder Q9)
needs an extra pair of brackets in the snippet. Thank you, bs-ns.
