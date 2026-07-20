# Validation report — clausia / `qiskit-v2.x-cert-practice-exam`

- Source: https://github.com/clausia/qiskit-v2.x-cert-practice-exam/blob/main/practice-exam-1.md
- Author: **clausia** — thank you for publishing this openly.
- Format: Markdown, 50 questions in `practice-exam-1.md`, answers in a separate `answer-key-1.md`.
- License: none stated (question text quoted minimally below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

A genuinely well-built 50-question exam spanning the full C1000-179 syllabus:
Pauli operations, single-qubit rotations, visualization, transpilation,
execution modes, Sampler/Estimator options, results handling, and OpenQASM 3.
Questions mix conceptual, API-recall, and "predict the output" code items, and
the separate answer key keeps the exam usable for self-timed practice. Nicely
done.

## Parse coverage

- Questions found / parsed: **50 / 50** (100%).
- Options parsed for all 50; every question has a stated answer in the key
  (including the multi-answer Q6 → `A, B`).
- Code-bearing questions (snippet in stem or options): **44 / 50**.
- Normalized data: `data/community/parsed/clausia.json`.

## Execution results (code-bearing questions)

Ten items were extracted and executed offline (fake-backend harness). **10 / 10
executed cleanly; 10 / 10 confirmed the stated answer; 0 mismatches.**

| Q | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 1 | `Pauli('ZX')` is Z⊗X (Z on q1, X on q0) | matrix == kron(Z,X) | a | ✅ |
| 2 | `sx;sx` on \|0⟩ | final state \|1⟩ | c | ✅ |
| 3 | `S` on \|1⟩ global phase | +π/2 rad | a | ✅ |
| 4 | `h;z`, P(measure 1) | 0.5 | b | ✅ |
| 5 | `rx(π/3)`, P(1) | 0.25 (=sin²(π/6)) | a | ✅ |
| 6 | which fragments prepare \|Φ⁺⟩ | A and B | a,b | ✅ |
| 17 | `assign_parameters(..., inplace=False)` returns new circuit | new obj, orig untouched | a | ✅ |
| 46 | `QuasiDistribution.nearest_probability_distribution()` exists | method present | a | ✅ |
| 47 | `RuntimeEncoder`/`RuntimeDecoder` import path | importable from `qiskit_ibm_runtime` | a | ✅ |
| 49 | OpenQASM 3 export in 2.x | `qiskit.qasm3.dumps` works; `QuantumCircuit.qasm()` removed | b | ✅ |

## Conceptual spot-check (5 sampled)

- **Q15 (classical control):** the correct option is `with qc.if_test((c0, 1)): qc.x(0)`;
  the `.c_if(...)` distractor is correctly marked wrong — `c_if` was removed in
  Qiskit 2.x. Good, current. (docs: https://quantum.cloud.ibm.com/docs/guides/classical-feedforward-and-control-flow)
- **Q24 (execution modes):** `batch` is the valid mode; `stream/parallel/single-shot`
  are not. Correct. (docs: https://quantum.cloud.ibm.com/docs/guides/execution-modes)
- **Q32 (Estimator mitigation):** `options.resilience_level` is the right dial for
  built-in error mitigation — and it is an **Estimator** option. Correct.
  (docs: https://quantum.cloud.ibm.com/docs/guides/v2-primitives#error-mitigation-and-suppression)
- **Q39 (precision precedence):** precision embedded directly in the PUB taking
  precedence over `options.default_precision` matches the Estimator V2 contract. Correct.
- **Q50 (REST):** `POST /v1/jobs` to start a Runtime job — correct verb/endpoint.

## Findings & opportunities

No correctness issues were found in the executed or spot-checked subset. One
small **version-context** note, offered only as a polish opportunity:

- **Q46** frames results around `result.quasi_dists[0]`. `QuasiDistribution` still
  exists in qiskit 2.5, so the stated answer (`nearest_probability_distribution()`)
  is valid — but `quasi_dists` is the **V1 Sampler** result shape; SamplerV2 returns
  per-register `BitArray`s with `get_counts()`. A future edition could re-anchor this
  item on the V2 result surface to match the rest of the (excellent) V2 framing.

## Verdict

This is a strong, syllabus-complete exam whose code questions hold up under
execution on the current stack — every physics/operator/API item we ran matched
the answer key. The author already tracks 2.x correctly (e.g. avoiding `c_if`),
which is exactly what a v2.x practice exam should do. The only opportunity is a
cosmetic V1→V2 refresh of one results question. Thank you, clausia — this is a
valuable community resource, and a PR against `answer-key-1.md`/`practice-exam-1.md`
for the Q46 note would be welcome if you'd like to make it.
