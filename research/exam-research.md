# IBM Qiskit Developer Certification — Research Report (as of 2026-07-19)

## Verification note on sources
`ibm.com` (IBM Training page C9008400, IBM Quantum blog) and `web.archive.org` are **blocked** from
direct fetch in this environment; Scribd required login. Primary IBM facts were therefore triangulated
from: (a) IBM search-result snippets of the official pages, (b) a first-hand exam-taker blog
(schrodinteq.github.io), (c) an in-depth competency review (ppalme.wordpress.com), and (d) EDUSUM.
Where three+ independent sources agree and section weights sum to 100%, confidence is high. Granular
official per-objective task wording could NOT be pulled from the primary IBM exam guide (blocked) — the
objective bullets below are synthesized from section titles + the official sample test + secondary reviews
and should be treated as *indicative*, not verbatim IBM blueprint text.

## 1. Exam identity & status
- **Exam code:** C1000-179
- **Exam title:** "Fundamentals of Quantum Computing Using Qiskit v2.X Developer"
- **Certification (badge) title:** "IBM Certified Quantum Computation using Qiskit v2.X Developer - Associate"
- **Status:** ACTIVE and CURRENT as of mid-2026. Released 2025. No evidence of a v3 exam or any
  replacement/retirement. It is the successor to C1000-112.
- **Predecessor:** C1000-112 "IBM Certified Associate Developer - Quantum Computation using Qiskit v0.2X"
  — **RETIRED 30 September 2025** (per search snippet; itcareerroadmap/edusum). C1000-179 is its replacement.
- **Target Qiskit version:** Qiskit SDK v2.x + Qiskit Runtime (Sampler V2 / Estimator V2 primitives).
- **Cost:** USD $200 (EDUSUM). [Confidence: medium — single explicit source]
- **Delivery:** Pearson VUE; online option via OnVUE (IBM certification exams are delivered through Pearson
  VUE; OnVUE proctoring available in English & Japanese). [Standard IBM cert delivery; not confirmed on the
  specific exam page due to block]
- **Badge:** Digital badge issued via **Credly** on passing.
- Source: https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400
- Source: https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification
- Source: https://www.edusum.com/blog/ibm-c1000-179-why-quantum-isnt-just-geniuses
- Source (predecessor retirement): https://itcareerroadmap.com/cert/ibm/c1000-112 ; https://www.ibm.com/certify/exam?id=C1000-112

## 2. Format
- **Questions:** 68
- **Duration:** 90 minutes
- **Passing score:** 47 / 68 correct = **69%**
- **Question types:** Multiple choice, including multi-select ("select two"/"select three") — confirmed by
  sample-test items (Q10 select 3; Q19 select 2).
- **Language:** English (OnVUE English/Japanese). [Language not explicitly confirmed on exam page]
- Source: https://schrodinteq.github.io/ibm-cert-quantum-exam-v2x/ ; https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification

## 3. Section / objective list + weights (THE KEY DELIVERABLE)

Eight sections; weights sum to 100%. Confirmed consistently by EDUSUM + the first WebSearch snippet of the
official page + ppalme review.

| # | Section (exact title) | Weight |
|---|---|---|
| 1 | Perform quantum operations | 16% |
| 2 | Visualize quantum circuits, measurements, and states | 11% |
| 3 | Create quantum circuits | 18% |
| 4 | Run quantum circuits | 15% |
| 5 | Use the sampler primitive | 12% |
| 6 | Use the estimator primitive | 12% |
| 7 | Retrieve and analyze results | 10% |
| 8 | Operate with OpenQASM | 6% |

**Indicative objectives per section** (synthesized — see verification note):
1. Perform quantum operations — define Pauli operators; tensor products of Pauli matrices; apply gates;
   global phase (e.g. T gate on |1⟩); statevector/operator manipulation.
2. Visualize — draw circuits; plot measurement histograms; Bloch sphere; QSphere; interpret statevector plots.
3. Create quantum circuits — build circuits/registers; parameterized circuits; dynamic circuits (classical
   control flow / conditionals); transpile & optimize for hardware (`generate_preset_pass_manager`, pass
   managers, ISA circuits, optimization levels).
4. Run quantum circuits — execution modes: job, session (dedicated / priority), batch; `QiskitRuntimeService`;
   open a Session; run on real hardware via primitives.
5. Use the sampler primitive — `SamplerV2`, `run([isa_circuit])`, PUBs, `default_shots`/SamplerOptions, bitstring output.
6. Use the estimator primitive — `EstimatorV2`, observables, PUB `(circuit, observable, params, precision)`,
   precision↔shots relationship, resilience options / error mitigation (Zero Noise Extrapolation), suppression.
7. Retrieve and analyze results — Runtime job object, `session.details()` (session state, last-job timestamp),
   result data bins, analyze counts / expectation values.
8. Operate with OpenQASM — OpenQASM 3 classical data types (e.g. `complex`); `qiskit.qasm3.dump`/`load`; export/import; Runtime REST API context.

## 4. Official study guide
Lives on the IBM Training certification page (C9008400) under an exam-guide / objectives tab. Contains the
section list, weights, and per-objective task statements plus recommended resources. Could not be extracted
verbatim (ibm.com blocked). A mirrored copy exists on Scribd ("Qiskit v2.x Developer Exam Guide",
https://www.scribd.com/document/909459255/Qiskit-Developer-Exam) but is login-gated. **GAP: verbatim official
sub-objective bullets not captured — recommend orchestrator fetch C9008400 from an unblocked network.**

## 5. Official sample / practice test
- Official **Sample Test** linked from the exam page. **21 questions**, mirrors real-exam difficulty. There is
  also an optional paid **Assessment Exam** (IBM/Pearson).
- Full sample questions are publicly reproduced/explained (verbatim Q11–21 below; Q1–10 topics + answers):
  Source: https://schrodinteq.github.io/ibmcertsamplev2x01/ (Q1–10) and https://schrodinteq.github.io/ibmcertsamplev2x02/ (Q11–21)

Q1 Pauli tensor products → A · Q2 T-gate global phase on |1⟩ → D · Q3 measurement prob. w/ RY → D ·
Q4 conditional-circuit viz → A · Q5 statevector histogram → C · Q6 QSphere from code → D ·
Q7 parameterized rotation gates → B · Q8 register types for measurement → C · Q9 pass-manager transform → A ·
Q10 Runtime execution modes (select 3) → B,E,F.

Q11 correct way to open a Session → C · Q12 array-broadcasting pattern → A · Q13 `default_shots` meaning → C
(number of times the circuit runs) · Q14 valid SamplerV2 `run` → A (`sampler.run([isa_circuit])`) ·
Q15 precision 0.015625→0.03125 effect on shots → D (decreases) · Q16 mitigation via resilience options → C
(Zero Noise Extrapolation) · Q17 Estimator PUB format → B (`(circuit, observable, parameter_values, precision)`) ·
Q18 purpose of a Session → C (group a collection of calls) · Q19 `session.details()` keys (select two) → B,C ·
Q20 OpenQASM 3 classical type → A (`complex`) · Q21 export qc to OpenQASM3 file → B (`qiskit.qasm3.dump(qc, qasmprogram)`).

## 6. Official recommended prep
- IBM Quantum Learning platform (learning.quantum.ibm.com) courses: "Understanding Quantum Information and
  Computation" (John Watrous) and "Quantum Computing in Practice".
- Qiskit documentation (docs.quantum.ibm.com): execution modes, circuit creation, transpilation, primitives,
  error mitigation/suppression, OpenQASM 3.
- Qiskit YouTube: "Preparing for Qiskit Developer Certification 2.0".
- Hands-on on IBM Quantum Platform; IBM Quantum Challenge transpilation materials.
- Source: https://ppalme.wordpress.com/2025/11/06/qiskit-developer-certification-2-0-a-comprehensive-review-of-core-competencies-and-learning-resources/
- Source: https://schrodinteq.github.io/ibm-cert-quantum-exam-v2x/

## 7. 2025–2026 news / program ties
- **Qiskit Advocate Program 2.0** relaunched (announced ~July 2025). Passing the **Qiskit v2.x developer
  certification (C1000-179) is a HARD REQUIREMENT to progress beyond Tier 0** (into Tier 1). Tier 1 = public
  recognition, swag, QAMP mentorship eligibility.
  Source: https://www.ibm.com/quantum/blog/qiskit-advocate-program ; https://www.hpcwire.com/2025/07/29/ibm-launches-qiskit-advocate-program-2-0/
- C1000-179 registration announcement: https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification
- No public sign of a Qiskit **v3** exam as of 2026-07-19.

## Conflicts / uncertainties
- ppalme groups the blueprint as "four primary sections"; this is editorial grouping — the official weighted
  list has **eight** sections (verified, sums to 100%). Not a real conflict.
- $200 cost and Pearson VUE/OnVUE delivery: only medium confidence (secondary/standard-practice), not read off
  the exam page.
- Verbatim official per-objective task statements: NOT captured (primary page blocked) — flagged as a gap.
