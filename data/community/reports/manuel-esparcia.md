# Validation report — ManuelEsparcia / `v2.x-Certification-practice-exam`

- Source: https://github.com/ManuelEsparcia/v2.x-Certification-practice-exam (`README.md`)
- Author: **Manuel Esparcia** — thank you for keeping it to a single self-contained file.
- Format: Markdown; the README *is* the exam — 24 `# N.` questions with A–D options
  and an `# Anwers` key at the end.
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

A 24-question conceptual exam with no code blocks and no images: every item is a
prose statement about how Qiskit v2.x behaves. That makes it a good *warm-up*
resource — it tests whether a candidate has the right mental model (what a Target
is for, what a preset pass manager is, what a Sampler returns) before they start
practising snippets. The framing is careful and hedged in the right places
("bitstring order depends on classical bit/register ordering; always verify the
mapping"), which is more accurate than the flat "Qiskit is little-endian" claim
that several other sets make.

**Inventory correction:** pass 1 recorded this exam as having no answer key. It
does — a `# Anwers` section at the end of the README lists all 24 answers. The
inventory has been updated.

## Parse coverage

- Questions found / parsed: **24 / 24** (100%).
- All 24 have four options and a stated answer.
- Code-bearing questions: **4 / 24** (inline API names only; no fenced blocks).
- Normalized data: `data/community/parsed/manuel-esparcia.json`.

## Method

Snippets were extracted by hand, reviewed, and executed offline in the pinned
project stack (fake backends, no credentials, no network, 60 s per snippet).
One grouped snippet covered the 7 items with a mechanically checkable claim; the
remaining 17 are conceptual and were spot-checked against the docs.

## Execution results

**7 questions executed; 7 confirmed, 0 mismatches.**

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 1 | `measure_all()` creates classical bits | 0 clbits → 2 clbits | B | confirmed |
| 2 | how to evaluate at θ = 0.3 | `bind_parameters` no longer exists; `assign_parameters` does | C | confirmed |
| 3 | `qc.cx(0,1)` | `x(0)` then `cx(0,1)` → \|11⟩ (X on qubit 1 controlled by qubit 0) | C | confirmed |
| 17 | `StatevectorEstimator.run()` returns | `PrimitiveJob` with `.result()` | B | confirmed |
| 20 | export to an OpenQASM 3 **string** | `dumps()` returns `str`; no `QuantumCircuit.to_qasm3` | B | confirmed |
| 21 | parsing OpenQASM 3 | `loads()` raised `MissingOptionalLibraryError: 'qiskit_qasm3_import' … is required` | B | confirmed |
| 24 | measuring q1→c0 and q0→c1 | X on q0 → counts `{'10': 16}`, i.e. bit position follows the *classical* bit | A | confirmed |

Q21 is a nice catch and confirmed in the most direct way possible: on a stock
install, `qiskit.qasm3.loads` raises `MissingOptionalLibraryError` telling you to
`pip install qiskit_qasm3_import`. Option A ("works out-of-the-box for all
OpenQASM 3 programs") is exactly the misconception the item targets. Q2 is
similarly well-aimed — `QuantumCircuit.bind_parameters` was removed in the 1.x→2.x
cleanup, so the hedged option C is the only survivor.

## Findings

**1. Answer-position distribution is skewed.** Across the 24 keyed answers:
A × 8, B × 13, C × 3, D × 0. A test-wise candidate who always guessed B would
score 54%. Shuffling the option order (and letting some correct answers land on
D) would remove the tell. This is a pure presentation issue — no item's *content*
is affected.

**2. Several correct options are noticeably longer and more hedged than their
distractors** (Q4, Q9, Q13, Q18), which is the classic "longest answer wins"
pattern. Q18 is the clearest example: the keyed option is the only one with a
qualifying clause. Trimming the key or padding the distractors would help.

**3. The key section header reads `# Anwers`** (typo) — worth fixing since a
reader scanning the README may not spot it.

**4. One item is drifting slightly toward V1 language.** Q18 keys "Samples from
classical output registers (bitstrings), **possibly as quasi-probabilities
depending on implementation**". SamplerV2 returns per-register `BitArray` samples;
quasi-probabilities were the V1 `SamplerResult.quasi_dists` concept. The hedge
makes the option defensible, but dropping the clause would make it strictly V2.

## Conceptual spot-check (5 sampled)

- **Q5** `StatevectorSampler` / `StatevectorEstimator` for exact prototyping — correct.
- **Q10** `Target` describes backend constraints to guide compilation — correct.
- **Q11** an explicit `coupling_map` can override backend-derived constraints — correct.
- **Q15** V2 primitives are the current interfaces — correct. (docs: https://quantum.cloud.ibm.com/docs/guides/v2-primitives)
- **Q16** `BackendSamplerV2` wraps a `BackendV2` behind the SamplerV2 interface — correct.

## Verdict

A clean, honest conceptual warm-up: every executable claim confirmed, no content
errors found, and two of the items (Q2 on `bind_parameters`, Q21 on the
`qiskit-qasm3-import` dependency) target misconceptions that most sets in the
cohort miss entirely. The main improvement is presentational — the B-heavy answer
distribution and the length tell. Thank you, Manuel.
