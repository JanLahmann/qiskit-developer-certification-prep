# Community Practice-Exam Validation — Overview

**CertiQ constructive review of community-authored Qiskit v2.x (C1000-179) practice exams.**
Repo-only working notes; not published to the site pending owner review. Scope,
tone, and method: credit the authors, verify what is verifiable by execution,
report findings as opportunities. Question text is quoted minimally (most repos
carry no license).

- Review date: 2026-07-20
- Validation stack (pinned): **qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2**
- Method: raw content fetched read-only; each exam parsed to a normalized schema
  (`pipeline/community_validate.py` → `data/community/parsed/<slug>.json`);
  extracted snippets executed **offline** in the project harness (fake backends,
  no credentials/network, 60 s timeout). No community repo was cloned, installed,
  or run wholesale.

## Totals

| Metric | Value |
|---|---|
| Exams inventoried | **23** |
| Machine-readable (markdown / notebook / YAML banks) | **14** |
| Exams fully parsed + validated | **7** |
| Questions across validated exams | **281** |
| Snippets executed offline | **39** |
| Stated answers **confirmed** by execution | **38** |
| Execution **mismatches** | **1** (version drift) |

### Per validated exam

| Slug | Author | Format | Qs | Parsed | Executed | Confirmed | Mismatches |
|---|---|---|---:|---:|---:|---:|---:|
| clausia | clausia | md | 50 | 50/50 | 10 | 10 | 0 |
| vantnprof | vantnprof | md | 68 | 68/68 | 11 | 11 | 0 |
| kurian | Kurian Uthuppu | md | 20 | 20/20 | 9 | 9 | 0 |
| algovista | algovista-collab | md | 25 | 25/25 | 5 | 5 | 0 |
| rishihg | rishihg | md | 25 | 25/25 | 1 | 0 | 1 |
| qbees | Q-Bees | ipynb | 25 | 25/25 | 1 | 1 | 0 |
| marcobarroca | Marco Barroca | ipynb | 68 | 68/68 | 2 | 2 | 0 |

Parsing hit **100% of questions** in every validated exam. Execution focused on
the items whose answers a computation can *prove or refute* (state prep,
measurement probabilities, Pauli matrices, expectation values, broadcasting
shapes, and API existence). Conceptual/API-recall items were spot-checked against
the official docs (~5 per exam).

## Headline result

**The code that could be executed almost universally holds up.** 38 of 39
executed answers matched the authors' keys — including many deliberately tricky
items: little-endian bit order, `Pauli('ZX') = Z⊗X`, RZ leaving measurement
probabilities unchanged, `SparsePauliOp.from_sparse_list` indexing, `−iY`
composition, `measure_all(add_bits=False)` register reuse, and Estimator `evs`
broadcasting shape `(5,)`. Two exams I expected an auto-generated feel to trip up
(algovista) or a "quasi-probability" description to muddy (several) were vindicated
by execution on the specific numeric items.

## Common misconceptions / themes

1. **V1→V2 primitive drift is the one recurring pattern.** The single execution
   mismatch and the handful of docs-based wording notes all trace to the same
   root: options that moved or changed between the V1 and V2 Runtime primitives.
   - `resilience_level` is **Estimator-only** in V2 — `SamplerV2`/`SamplerOptions`
     has no such field (setting it raises a pydantic `ValidationError`). **rishihg
     Q24** keys `sampler.options.resilience_level = 1`, which was valid under the
     older model → **version drift, not author error**. (Q-Bees answers this family
     *correctly* by naming `twirling`/`dynamical_decoupling` as the Sampler groups;
     MarcoBarroca Q5 is explicitly correct here too.)
   - **Sampler output = "quasi-probability distributions."** That is V1 language;
     **SamplerV2** returns per-register bitstring samples (`BitArray` /
     `get_counts()`). Appears as a wording issue in **Q-Bees Q14**, **rishihg Q5**,
     and in the surrounding framing of **clausia Q46** (`result.quasi_dists`).
     MarcoBarroca Q1 states the V2 behavior precisely — a good model.

2. **2.x removals are generally handled well.** Across exams, `c_if` → `if_test`,
   the removed global `execute()` → primitives, and removed `QuantumCircuit.qasm()`
   → `qiskit.qasm3.dumps` are represented correctly (and often used as distractors).
   Authors clearly track the 2.x surface.

3. **Physics/linear-algebra items are a strength, not a weakness.** Every
   state-preparation, probability, expectation-value, and operator-matrix question
   executed correctly. Where mistakes might hide in a hand-written exam (endianness,
   global vs relative phase, rotation-angle → probability), these authors got it right.

## Version-drift patterns (for anyone updating these exams)

- `resilience_level`: Estimator V2 only (levels 0-2). Not a Sampler option.
  Ref: https://quantum.cloud.ibm.com/docs/guides/v2-primitives#error-mitigation-and-suppression
- Sampler results: V1 `quasi_dists` / `QuasiDistribution` → V2 `pub.data.<reg>.get_counts()`.
- Construction kwargs: prefer `mode=` (backend/session/batch) over the older
  `backend=` / `session=` primitive kwargs.

## Which exams shine

- **vantnprof** and **MarcoBarroca** — the two 68-question mocks — are the
  standouts: authentic format, deep V2 coverage, explanations, and (MarcoBarroca)
  inline IBM-docs citations. Every executed item confirmed; both correctly encode
  the V2-primitive distinctions that trip up others. MarcoBarroca is MIT-licensed.
- **clausia** (50 Q) and **kurian** (20 Q) are excellent for their size — clausia
  for breadth and clean code items, kurian for the best answer key in the cohort
  (full worked solutions and hand-calculations).
- **algovista** deserves credit for aiming at the hardest corners of the syllabus
  and getting the substance right, despite a verbose auto-generated prose style.

## Licensing note

Reuse rights are the main practical caveat: most repos (including several of the
strongest — clausia, kurian, vantnprof, algovista) carry **no license**, so their
question text should be treated as all-rights-reserved. Clear licenses exist for
**rishihg (MIT)**, **MarcoBarroca (MIT)**, and **quantum-tokyo (Apache-2.0)** —
worth prioritizing when building on community content.

## Artifacts

- Inventory (all 23): `data/community/inventory.json`
- Neutral directory (all 23): `data/community/summary.json`
- Normalized questions (7): `data/community/parsed/<slug>.json`
- Per-exam reports (7): `data/community/reports/<slug>.md`
- Reusable parser: `pipeline/community_validate.py`
- Raw fetched sources: `data/community/raw/`
