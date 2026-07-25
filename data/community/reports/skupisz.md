# Validation report — SKupisz / `qiskit-certificate-mock-test`

- Source: https://github.com/SKupisz/qiskit-certificate-mock-test (`questions.ipynb`)
- Author: **SKupisz** — thank you for the scenario-style phrasing.
- Format: Jupyter notebook, one markdown cell per question, single answer-key cell at the end.
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

24 questions written as short *scenarios* ("you take a look at the transpiled ISA
circuit and see…", "you are asked to estimate heat transfer between two parts of
a factory…") rather than API lookups. That style is closer to how the real exam
frames its harder items, and it produces some genuinely good questions — the
PUB-ordering item (Q11), the ISA-qubit-count item (Q13), and the complex-coefficient
observable item (Q17) are all excellent. Option counts vary (2–5 per question),
and several items include an explicit "None of the above", which is a good habit.

## Parse coverage

- Questions found / parsed: **24 / 24** (100%); answers from the final key cell.
- All 24 have a stated answer; 3 are multi-answer.
- Option counts: 9 × three, 8 × four, 5 × five, 2 × two.
- Code-bearing questions: **16 / 24**.
- Normalized data: `data/community/parsed/skupisz.json`.

## Method

Snippets were extracted by hand, reviewed, and executed offline in the pinned
project stack (fake backends, no credentials, no network, 60 s per snippet).
Seven snippets covered 16 questions; visualization semantics were checked against
the installed docstrings and renderer source.

## Execution results

**16 questions executed; 13 confirmed, 3 mismatches.**

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 1 | tensor of B by A | `B.tensor(A) == A.expand(B)` → True | A,B | confirmed |
| 2 | channel fidelity | `process_fidelity` exists; `channel_fidelity` / `fidelity` do not | B | confirmed |
| 4 | limit text-drawer line length | `draw(output="text", fold=50)` ✔; `max_width` / `truncate` raise `TypeError` | C | confirmed |
| 5 | order a histogram 11 → 00 | `plot_histogram` has no `order` kwarg (`TypeError`); valid kwarg is `sort` | C | **mismatch** |
| 6 | show Re and Im of a density matrix separately | city: "two 3d bar graphs … real and imaginary part"; hinton: renders `Re[ρ]`/`Im[ρ]`; qsphere: size ∝ probability, colour = phase | A,D | **mismatch** |
| 8 | create k parameters | `ParameterVector("hi", k)` → `hi[0..k-1]` | C | confirmed |
| 11 | PUB element order | `(params, circuit, obs)` raises `TypeError`; `(circuit, obs, params)` accepted | C | confirmed |
| 12 | estimator over an external `Backend` | `BackendEstimatorV2` exists; `EstimatorBackendV2` does not | D | confirmed |
| 13 | qubit count of the ISA circuit | 3-qubit GHZ on a 156-qubit backend → 156 | C | confirmed |
| 14 | run exactly 512 shots | `run([qc], shots=512)` → 512 counts | A | confirmed |
| 15 | commute on the whole operator | signature is `group_commuting(qubit_wise=False)`; `group_wise` / `per_qubit` raise `TypeError` | A | **mismatch** |
| 16 | evs shape, obs (10,1) × params (1,4) | (10, 4) | C | confirmed |
| 17 | why the observable is invalid | complex coefficient → `ValueError: Non-Hermitian input observable…` | C | confirmed |
| 18 | standard error of the mean | `PubResult.data` exposes `evs`, `stds`; no `stde` | B | confirmed |
| 20 | filter jobs by date | `jobs()` accepts `created_after` | A | confirmed |
| 23 | QASM 3 → circuit | `qiskit.qasm3.loads` exists | C | confirmed |

## Findings

**1. Q5 — the keyed option uses a kwarg that does not exist.** The key is
`order="desc"`, but `plot_histogram`'s parameters are
`(data, figsize, color, number_to_keep, sort, target_string, legend, bar_labels,
title, ax, filename)` — passing `order=` raises `TypeError`. The behaviour the
stem describes (leftmost `11`, rightmost `00`) is produced by `sort="desc"`,
which is not offered. Since options A/B name `sort` with invalid *values*
(`"increasing"` raises `VisualizationError`; `"asc"` gives the opposite order)
and C/D name a non-existent kwarg, the correct answer under the printed options
is **E, "None of the above"**.

**2. Q6 — "City" is the canonical answer and is not in the key.** The key is
A (QSphere) and D (Hinton). Checked against the installed renderers:
`plot_state_city` — "Plot two 3d bar graphs of the real and imaginary part of the
density matrix rho"; `plot_state_hinton` — draws labelled `Re[ρ]` and `Im[ρ]`
panels; `plot_state_qsphere` — "the size of the points is proportional to the
probability … and the colour represents the phase", i.e. it does not separate
real and imaginary components at all. So D is right, **C should be in the key**,
and A should not.

**3. Q15 — none of the four options is a valid call.** The real signature is
`SparsePauliOp.group_commuting(qubit_wise: bool = False)`; the keyed
`group_wise=True` raises `TypeError`, as do `per_qubit=False` and
`op_as_whole=True`. The behaviour the stem wants (commute on the whole operator,
not per qubit) is the *default*, `qubit_wise=False`. Renaming the options to
`qubit_wise=…` would make this a good item — the underlying distinction is real
and exam-relevant.

**4. Q3 wording.** "Which of the classes below stores linear operators as density
matrix?" keys `Operator`. `Operator` stores a dense matrix, so the key is the
best of the three offered; but "density matrix" has a specific meaning in Qiskit
(`DensityMatrix`), and that class is not among the options. Rewording to "as a
dense matrix" would avoid the collision.

**5. Strengths worth keeping.** Q11 (PUB element order), Q13 (ISA circuits keep
the backend's full qubit count), Q16 (broadcasting (10,1) × (1,4) → 10×4) and
Q17 (Hermitian-observable requirement) all executed exactly as keyed, and all
four are the kind of question that separates candidates who have actually run a
V2 primitive from those who have only read about one.

## Conceptual spot-check (5 sampled)

- **Q7** optimization level 1 → 2 to gain commutative cancellation of rotations — correct.
- **Q9** `PauliEvolutionGate` for a time-evolution problem (`TimeEvolutionGate` does not exist) — correct.
- **Q19** results serialize to JSON via the Qiskit runtime encoders — correct.
- **Q22** physical qubits cannot be used inside `gate` bodies in OpenQASM 3 — correct.
- **Q24** `include "stdgates.inc";` — correct.

## Verdict

Strong scenario-style writing with four genuinely excellent primitive/ISA items,
13 of 16 executed answers confirmed, and three keys that need a fix (Q5 kwarg,
Q6 missing "City", Q15 kwarg name). The underlying concepts in all three are
right — it is the option text that drifted from the API. Thank you, SKupisz.
