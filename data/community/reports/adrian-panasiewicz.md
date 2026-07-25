# Validation report — AdrianPanasiewicz / `Qiskit_v2.X_Developer_practice_exam`

- Source: https://github.com/AdrianPanasiewicz/Qiskit_v2.X_Developer_practice_exam (`practice_exam.ipynb`)
- Author: **Adrian Panasiewicz** — thank you for the notebook and the rendered figures.
- Format: Jupyter notebook, 24 questions across ~90 markdown cells; each answer in a
  collapsible `<Details>` block with a one-line justification.
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

A compact 24-question exam with an unusual amount of care in the *distractors*:
several items differ from the keyed answer by a single attribute path
(`sampler.options.twirling.enable_gates` vs `sampler.twirling`), which is exactly
the discrimination the real exam asks for. It is also one of the few sets that
covers the REST-API and bearer-token corner of section 8, and it renders its own
circuit images (`q_photos/`) for the "which diagram" items.

## Parse coverage

- Questions found / parsed: **24 / 24** (100%).
- All 24 have options and a stated answer; 3 are multi-answer (Q9 → A,C,E via an
  "Both A and C" option; Q13 → B,C; Q16 → A,B,C,D).
- Code-bearing questions: **18 / 24**.
- Normalized data: `data/community/parsed/adrian-panasiewicz.json` (each item keeps
  the author's `answer_note`).

## Method

Snippets were extracted by hand, reviewed, and executed offline in the pinned
project stack (fake backends, no credentials, no network, 60 s per snippet).
Five snippets covered 14 questions. Image-comparison items (Q1) and REST/policy
items (Q23, Q24) were not executed.

## Execution results

**14 questions executed; 13 confirmed, 1 mismatch.**

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 2 | which `initialize` list prepares (4\|00⟩+8\|01⟩+5\|10⟩)/√105 | `[4,8,5,0]/√105` matches; `qc.prepare` does not exist (options C/D) | A | confirmed |
| 7 | parameterized `rx(x²+2x+1)` | builds; angle `2*x + x**2 + 1` | D | confirmed (see note) |
| 8 | `sin` on a `Parameter` | `phi.sin()` → `sin(phi)` | B | confirmed (see note) |
| 9 | which transpile forms work | `transpile(qc, backend=)` ✔, `pm.run(qc)` ✔, `pm.transpile` does not exist | E (A+C) | confirmed |
| 11 | submit a sampler job | `run([qc])` ✔; `run(qc)` raises `ValueError` | A | confirmed |
| 12 | initialize batch mode | `Batch(backend=…)` + `Sampler(mode=batch)` matches signatures | D | confirmed |
| 13 | Sampler error-handling options | `SamplerOptions` groups: `dynamical_decoupling`, `twirling` (no resilience) | B,C | confirmed |
| 14 | submit for sampling | `run([qc])` ✔; `run(qc)` raises | A | confirmed |
| 15 | enable twirling + DD | `options.twirling.enable_gates` ✔; `options.twirling = True` raises `ValidationError` | C | confirmed |
| 16 | Estimator error-handling options | `EstimatorOptions` adds `resilience` (`zne_mitigation`, `measure_mitigation`) + twirling + DD | A,B,C,D | confirmed |
| 17 | submit for estimation | `run([qc, obs])` raises `ValueError`; `run([(qc, obs)])` works | A | **mismatch** |
| 18 | enable ZNE + T-REx | `options.resilience.zne_mitigation` ✔; `options.zne_mitigation` raises | A | confirmed |
| 19 | read expectation values | `results[0].data.evs` ✔; `results.data` does not exist | B | confirmed |
| 22 | why `dumps(qc, f)` fails | `dumps() takes 1 positional argument but 2 were given`; `dump(qc, f)` writes | D | confirmed |

## Findings

**1. Q17 — the keyed snippet is not a valid PUB.** The key is option A, whose
body is `job = estimator.run([qc, obs])`. Executed against a local V2 estimator
that raises

> `ValueError: An invalid Estimator pub-like was given (<class 'QuantumCircuit'>)…`

because `[qc, obs]` is read as *two* PUBs rather than one `(circuit, observable)`
PUB. The working form is `estimator.run([(qc, obs)])`. The other three options
are worse (they invent `backend.run(..., mode="estimator")`), so A is still the
best of the four — but the tuple parentheses are missing. Note that the same
notebook gets the analogous Sampler item right (Q11/Q14, `run([qc])`), so this is
a typo-level slip.

**2. Q7 has two functionally identical options.** Option A and option D produce
exactly the same circuit; A merely creates a `Parameter("theta")` that is then
rebound and discarded (executed: both give `rx(2*x + x**2 + 1)` with free
parameters `{x}`). Keying D alone is defensible if the intent is "which is the
*clean* way", but a strict reader can justify A. Making A genuinely wrong (for
example, keeping `theta` as the bound symbol) would sharpen the item.

**3. Q8 — option A is closer to correct than it looks.** The key is
`phi.sin()`, which is right. But `numpy.sin(phi)` also returns `sin(phi)`
(`ParameterExpression` supports the ufunc), so a reader who reads option A's bare
`sin(phi)` as NumPy's `sin` is not wrong. Qualifying the option (e.g.
`math.sin(phi)`) would remove the ambiguity.

**4. Q13 / Q16 are a well-designed pair.** Same options, different primitive, and
both keys match the installed option dataclasses exactly: Sampler exposes only
twirling and dynamical decoupling; Estimator adds the `resilience` group with
`zne_mitigation` (ZNE) and `measure_mitigation` (T-REx). This is precisely the
V1→V2 distinction that trips up other sets in the cohort.

## Conceptual spot-check (5 sampled)

- **Q3** amplitude encoding for ⌈log₂N⌉ qubits — correct.
- **Q4** barrier as a transpiler-reordering boundary (not merely cosmetic) — correct.
- **Q6** gate-map visualization for virtual→physical mapping — correct.
- **Q10** session mode for iterative/dependent executions — correct. (docs: https://quantum.cloud.ibm.com/docs/guides/execution-modes)
- **Q21** `job.result()` blocks until completion — correct.

## Verdict

A tight, well-targeted 24-question set whose distractors are better than average,
with 13 of 14 executed items confirmed. One PUB-parenthesis slip (Q17) and two
items with a defensible second answer (Q7, Q8) are the only issues. Thank you,
Adrian.
