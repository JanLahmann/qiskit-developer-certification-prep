# Validation report — lkaucic / `QiskitV2xExamGen`

- Source: https://github.com/lkaucic/QiskitV2xExamGen (`questions/section1-8_*.yaml`)
- Author: **lkaucic** — thank you for publishing the bank as structured YAML.
- Format: YAML question banks (8 files) behind a LaTeX/PDF generator (`generate_quiz.py`).
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

This is the only surveyed resource that ships its questions as a *machine-readable
bank* rather than prose: every item is `id / section / question / [code] / choices
A-D / answer`, and `generate_quiz.py` samples per section and renders a printable
exam. That design choice makes the content trivially reusable, diffable, and
reviewable — a genuinely good idea that the rest of the cohort would benefit from
copying. Coverage spans all eight exam sections with a sensible per-section split,
and several items (PUB broadcasting shapes, register naming in Sampler output,
job retention) are pitched at real exam difficulty.

## Parse coverage

- Questions found / parsed: **51 / 51** (100%), across 8 section files.
- All 51 have four options and a stated answer; 6 are multi-answer (YAML lists).
- Code-bearing questions: **10** (plus several image-based items whose choices
  reference `assets/` PNGs).
- Normalized data: `data/community/parsed/lkaucic.json`.

## Method

Snippets were extracted by hand, reviewed, and executed offline in the pinned
project stack (fake backends, no credentials, no network, 60 s per snippet).
14 snippets covered 16 questions. Image-comparison items (qsphere/circuit
pictures) and REST/policy items were not executable and are left unverified.

## Execution results

**16 questions executed; 14 confirmed, 2 mismatches.**

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 3 | `Z` on \|1⟩ | `[0, -1]` | C | confirmed |
| 5 | ⟨Z⟩ on \|+⟩ | 0.0 | D | confirmed |
| 6 | Rx(π/2)·Rz(π/2)·Ry(−π/2) ≡ R(2π,0)? | same *state* from \|0⟩; **not** the same gate | A | confirmed (see note) |
| 7 | `sx` + `rx(π/2)`, P(1) | 1.0 | D | confirmed |
| 8 | `Pauli('XIZZ')`, which qubit gets X | q3 | A | confirmed |
| 24 | `evs` shape, obs (2,1) × params (1,3,2) | `(2, 3)` | C | confirmed |
| 27 | option unique to Sampler | none of the three (`default_shots` in both; `shots_per_randomization` is a twirling field) | D | confirmed |
| 28 | Sampler on a circuit with no measurements | runs; `DataBin` has no fields | C | confirmed |
| 36 | precision 0.02 → 0.01 effect | `default_precision` exists only on `EstimatorOptions` | B | **mismatch** |
| 37 | ⟨I⟩ for normalized states | 1.0 for all tested | D | confirmed |
| 40 | default creg name in Sampler output | `meas` | B | confirmed |
| 41 | named `ClassicalRegister('clbits')` | `data.clbits` | B | confirmed |
| 42 | `measure_all()` | `data.meas` | A | confirmed |
| 45 | valid `JobStatus` values | INITIALIZING, QUEUED, VALIDATING, RUNNING, CANCELLED, DONE, ERROR | A,C | confirmed |
| 48 | export OpenQASM 3 **to a file** | `dumps(circuit) -> str`; `dump(circuit, stream) -> None` | B | **mismatch** |
| 50 | statevector of the QASM 3 program | `[0.7071, 0.7071, 0, 0]` | A | confirmed |

## Findings

**1. Q48 (S8-002) — `dumps()` vs `dump()`.** The stem asks which method must be
used "when exporting Qiskit code to OpenQASM 3 **as a file**"; the key is `B:
dumps()`. Executed signatures: `qiskit.qasm3.dumps(circuit) -> str` (raises
`TypeError` if given a stream) and `qiskit.qasm3.dump(circuit, stream) -> None`
(writes to the file object). For the file case the answer is option **D**
(`dump()`). Both options are present, so this looks like a key slip rather than
a knowledge gap.

**2. Q36 (S6-008) — precision item has no correct option.** The stem describes
lowering Estimator `precision` from 0.02 to 0.01; the key is `B: "Precision only
affects Sampler, not Estimator"`, which execution contradicts —
`default_precision` is a field of `EstimatorOptions` and absent from
`SamplerOptions` (whose knob is `default_shots`). The intended answer ("more
shots are used") is not among the choices; option A says *fewer*, and option C
("target precision") appears to be a leftover from the neighbouring PUB question.
Worth rewriting the option set.

**3. Q33 and Q35 (S6-005 / S6-007) are the same question verbatim** — same stem,
same options, same key. One can be dropped or re-pointed.

**4. Q6 (S1-006) is right for the right reason but reads as a gate identity.**
The sequence evaluates to `diag(e^{−iπ/4}, e^{+iπ/4})` = Rz(π/2), which is *not*
equal to `R(2π,0)` as an operator (no `R(θ,φ)` gate can be a Z-rotation other
than ±I). Read as the question is worded — "*starting from* \|0⟩ … equivalent
to" — option A is correct: both leave \|0⟩ unchanged up to global phase, and no
other option does. Adding "acting on \|0⟩" to the stem would remove the
ambiguity.

**5. Housekeeping.** Q11's choices in `section2_visualization.yaml` carry LaTeX
escaping inside code strings (`plot\_state\_qsphere`), which is right for the
LaTeX renderer but makes the YAML awkward to reuse elsewhere; a raw-string field
plus renderer-side escaping would be cleaner. `generate_quiz.py` shuffles
*question order* only, so the A-D letters in the YAML are authoritative — which
is what this review checked against.

## Conceptual spot-check (5 sampled)

- **Q17** heuristic layout stage → `DenseLayout` / `SabreLayout` (both exist in
  `qiskit.transpiler.passes`; `VF2Layout` is the exact/subgraph-isomorphism pass) — correct.
- **Q34** techniques configured through dedicated Estimator option groups rather
  than `resilience_level` — matches the `ResilienceOptionsV2` / `DynamicalDecouplingOptions`
  split observed in the stack. (docs: https://quantum.cloud.ibm.com/docs/guides/v2-primitives)
- **Q43** three-year retention of undeleted job data — matches current IBM guidance.
- **Q46** `Session.details()` exposes `backend_name` / `mode` / `max_time` → "none of
  the above" is correct.
- **Q51** OpenQASM 3 features (while loops, `angle`, `barrier`; no try/catch) — correct.

## Verdict

A well-engineered little project: the YAML-bank + generator split is the most
reusable format in the cohort, and 14 of 16 executed items confirmed. Two
answer-key items (Q48, Q36) and one duplicated pair (Q33/Q35) are worth a quick
pass. Thank you, lkaucic.
