# Validation report — gnietof / `QuantumTests`

- Source: https://github.com/gnietof/QuantumTests (`exam1/exam1.md`, `exam2/exam2.md`, `exam3/exam3.md`)
- Author: **gnietof** — thank you for three full exams with image-based items.
- Format: Markdown, 3 × 20 questions, each with a collapsible "Show answer key".
- License: `LICENSE.md` present (GitHub reports NOASSERTION) — minimal quoting below.
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

Three complete 20-question exams that come closest of any surveyed resource to
the *feel* of the real thing: heavy use of "which **two**" items, rendered
circuit/qsphere/histogram images as answer choices, and a strong bias toward
"read this snippet and predict the object" over recall. The Session/Batch,
broadcasting, and PUB-shape items are exactly where the real exam lives. The
image assets (58 PNGs) are what make this set expensive to author and are its
main differentiator.

## Parse coverage

- Questions found / parsed: **60 / 60** (100%) — 20 per exam.
- All 60 have parsed options and a stated answer; 11 are multi-answer.
- Option counts: 51 × four, 8 × five, 1 × three (exam 1 Q6, see findings).
- Code-bearing questions: **46 / 60**.
- Normalized data: `data/community/parsed/gnietof.json`.

## Method

Snippets were extracted by hand, reviewed, and executed offline in the pinned
project stack (fake backends, no credentials, no network, 60 s per snippet).
18 snippets covered 27 questions. Runtime-service items were checked by reading
the installed `QiskitRuntimeService.jobs` / `Session` sources with `ast` (no
network, no credentials). Image-comparison items (Q4/Q5/Q8/Q9 families) and REST
endpoint items were not executable and are left unverified.

## Execution results

**27 questions executed; 26 confirmed, 1 mismatch.**

| Exam/Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 1 / 1 | which fragments give `Pauli('X')` | A → `X`, C → `X`, D → `YZ`, B → not valid Python | A,C | confirmed |
| 1 / 2 | `from_sparse_list([("XY",(0,2),1)], num_qubits=4)` | `IYIX` | D | confirmed |
| 1 / 3 | `rx(π/2)`, P(1) | 0.5 | C | confirmed |
| 1 / 6 | `measure_all` / `measure()` / `measure_active` | A and C build measurements; B raises `TypeError` | A,C | confirmed |
| 1 / 7 | pass-manager usage | `PassManager.run` exists, `.transpile` does not | C | confirmed |
| 1 / 10 | improper ways to run jobs in a batch | `Session.__init__` has no `mode=`; `SamplerV2(mode=backend)` bypasses the batch | A,D | confirmed (see note) |
| 1 / 11 | stop accepting new jobs, finish pending | `close()` docstring: "existing queued or running jobs will run to completion" | A | confirmed |
| 1 / 14 | Sampler parameter binding | dict-of-lists keyed by `Parameter` coerces (shape (3,)) | C | confirmed |
| 1 / 15 | Estimator parameter binding | same, via `EstimatorPub.coerce` | B | confirmed |
| 1 / 18 | retrieve jobs of a batch | `jobs()` has `session_id`, no `batch_id` | C | confirmed |
| 2 / 1 | `Pauli(qc)` for x·y·z | `-iI` | B | confirmed |
| 2 / 2 | `from_sparse_list([("X",(4,),6)], num_qubits=10)` | `IIIIIXIIII`, coeff 6 | A | confirmed |
| 2 / 3 | `x` then `y`, P(0) | 1.0 | E | confirmed |
| 2 / 10 | proper ways to run jobs in a session | context manager and `mode=session` both valid | A,D | confirmed |
| 2 / 11 | stop and drop pending | `cancel()` docstring: "Cancel all pending jobs in a session" | B | confirmed |
| 2 / 14 | where `shots=2048` goes | `run(pubs, *, shots=None)`; constructor has no `shots` | B | confirmed |
| 2 / 15 | two valid Estimator parameter forms | single-param dict and flat list both coerce | A,C | confirmed |
| 2 / 18 | retrieve jobs of a session | `session_id` kwarg | C | confirmed |
| 3 / 1 | which fragments give `Pauli('Y')` | C → `Y`; A → `-iY`; B → not valid Python; D → `XZ` | B,C | **mismatch** |
| 3 / 2 | three equivalent Pauli lists | A, C, E → `XXYYZZ`; B → `-II`; D → `ZZYYXX` | A,C,E | confirmed |
| 3 / 3 | `h` + `rz(π/4)`, P(1) | 0.5 | C | confirmed |
| 3 / 7 | which fragments build the pictured circuit | C and D build h/cx/barrier/measure; A and B raise `TypeError` | C,D | confirmed |
| 3 / 13 | read Sampler counts for register `c` | `data.c.get_counts()` works; `result[0].get_counts` does not exist | D | confirmed |
| 3 / 14 | two valid Sampler parameter forms | dict keyed by the free `Parameter`, and flat list | A,C | confirmed |
| 3 / 16 | where `precision` goes | `EstimatorV2.run(pubs, *, precision=None)` | A | confirmed |
| 3 / 17 | `h(1); cx(0,1); h(1)` from \|00⟩ | P(00) = 1.0 | A | confirmed |
| 3 / 18 | jobs for a named backend | `jobs(backend_name=...)` | B | confirmed |

## Findings

**1. Exam 3 Q1 — the keyed pair includes an option that cannot run.** The key is
`B,C`. Option C (`Pauli(qc)` from a circuit with `qc.y(0)`) returns `Y` exactly —
correct. Option B is the text `Pauli([True],[True],0])`, which is not valid Python
(unbalanced bracket); in its closest valid form `Pauli([True],[True],0)` it raises
`TypeError: Pauli.__init__() takes from 1 to 2 positional arguments but 4 were
given`. Meanwhile option A (`Pauli('X') @ Pauli('Z')`) evaluates to `-iY`, i.e.
Y up to a phase — the natural second answer if the intent was "generates a Pauli
Y operator". Note exam 1 Q1 uses the same option-B pattern
(`Pauli([False],[True],3])`) and correctly *excludes* it from the key (A,C), so
this looks like a key slip in exam 3 rather than a belief about the API.

**2. Exam 1 Q6 has only three options** (A, B, C) while asking for "**two**"
correct fragments; no option D is present in the source. Both keyed options are
correct as far as execution goes.

**3. Exam 1 Q10 asks for "two" improper batch usages but three options are
improper.** Executed: A fails (`Session()` has no `mode=` kwarg), D runs but
attaches the samplers to the raw backend rather than the batch, and C references
a non-existent `Backend(backend=...)` context manager. Only B is a proper batch
usage. The keyed pair (A,D) is defensible; the item would be tighter if C were
made a valid alternative.

**4. Consistent strengths.** Every numeric/state item executed cleanly, including
the deliberately tricky `from_sparse_list` indexing (both exams), `-iI` from
`X·Y·Z`, the little-endian `IYIX` label, and the `measure_all(add_bits=False)` /
negative-qubit-index fragment in exam 3 Q7. The Session/Batch lifecycle items
(`close()` vs `cancel()`) match the installed docstrings word for word.

## Conceptual spot-check (5 sampled)

- **E1 Q12** "session closed → no new jobs, existing jobs run to completion" — matches
  `Session.close()` semantics. (docs: https://quantum.cloud.ibm.com/docs/guides/execution-modes)
- **E1 Q16** PUB broadcasting rule "equal in size or size one" — correct.
- **E2 Q12** batch usage counts QPU time only; session usage is wall-clock including
  compilation — matches current execution-mode guidance.
- **E2 Q13** Sampler PUB = circuit, parameters, optional shots — correct (Estimator adds observables/precision).
- **E2 Q16** "missing dimensions are assumed to have size two" is indeed the false
  statement — correct.

## Verdict

The most exam-like set surveyed: three complete papers, image-based items, and
26 of 27 executed answers confirmed. One key slip (exam 3 Q1) and two
option-completeness nits (exam 1 Q6, exam 1 Q10) are the only issues found.
Thank you, gnietof — this is a lot of work and it holds up.
