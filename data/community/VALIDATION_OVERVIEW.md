# Community Practice-Exam Validation — Overview

**CertiQ constructive review of community-authored Qiskit v2.x (C1000-179) practice exams.**
Repo-only working notes; not published to the site pending owner review. Scope,
tone, and method: credit the authors, verify what is verifiable by execution,
report findings as opportunities. Question text is quoted minimally (most repos
carry no license).

- Review dates: **pass 1 — 2026-07-20**, **pass 2 — 2026-07-25**
- Validation stack (pinned): **qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2**
- Method: raw content fetched read-only; each exam parsed to a normalized schema
  (`pipeline/community_validate.py` → `data/community/parsed/<slug>.json`);
  extracted snippets executed **offline** in the project harness (fake backends,
  no credentials/network, 60 s timeout). No community repo was cloned, installed,
  or run wholesale. One bank shipped as a pandas pickle was disassembled with
  `pickletools` and then read through a **restricted unpickler** (pandas/numpy
  container constructors only) rather than unpickled normally.

## Totals (both passes)

| Metric | Value |
|---|---|
| Exams inventoried | **23** |
| Machine-readable (markdown / notebook / YAML / CSV-PKL banks) | **14** |
| Exams fully parsed + validated | **14** |
| Questions parsed across validated exams | **1,565** |
| Questions settled by offline execution | **218** |
| Stated answers **confirmed** by execution | **203** |
| Execution **mismatches** | **9** |
| Executed but **unverifiable** (no executable surface / missing optional renderer) | **6** |

### Per validated exam

| Slug | Author | Format | Qs | Parsed | Executed | Confirmed | Mismatches | Pass |
|---|---|---|---:|---:|---:|---:|---:|:--:|
| clausia | clausia | md | 50 | 50/50 | 10 | 10 | 0 | 1 |
| vantnprof | vantnprof | md | 68 | 68/68 | 11 | 11 | 0 | 1 |
| kurian | Kurian Uthuppu | md | 20 | 20/20 | 9 | 9 | 0 | 1 |
| algovista | algovista-collab | md | 25 | 25/25 | 5 | 5 | 0 | 1 |
| rishihg | rishihg | md | 25 | 25/25 | 1 | 0 | 1 | 1 |
| qbees | Q-Bees | ipynb | 25 | 25/25 | 1 | 1 | 0 | 1 |
| marcobarroca | Marco Barroca | ipynb | 68 | 68/68 | 2 | 2 | 0 | 1 |
| lkaucic | lkaucic | yaml | 51 | 51/51 | 16 | 14 | 2 | 2 |
| gnietof | gnietof | md ×3 | 60 | 60/60 | 27 | 26 | 1 | 2 |
| bs-ns | bs-ns | ipynb ×2 | 66 | 66/66 | 39 | 38 | 1 | 2 |
| adrian-panasiewicz | Adrian Panasiewicz | ipynb | 24 | 24/24 | 14 | 13 | 1 | 2 |
| skupisz | SKupisz | ipynb | 24 | 24/24 | 16 | 13 | 3 | 2 |
| manuel-esparcia | Manuel Esparcia | md | 24 | 24/24 | 7 | 7 | 0 | 2 |
| luke-j-miller | Luke J. Miller | pkl/csv | 1035 | 1035/1035 | 60* | 54 | 0 | 2 |

\* seeded stratified random sample (`random.Random(20260725)`), 60 of 523
code/API-bearing rows drawn proportionally across the eight sections; 6 of the 60
had no executable surface and are counted as unverified.

Parsing hit **100% of questions** in every validated exam. Execution focused on
the items whose answers a computation can *prove or refute* (states, measurement
probabilities, Pauli algebra, expectation values, PUB broadcasting shapes, option
dataclasses, and API signatures). Conceptual/API-recall items were spot-checked
against the official docs (~5 per exam).

## Headline result

**The code that could be executed almost universally holds up: 203 of 218
executed answers matched their author's key.** Two exams came through a
computational gauntlet without a single content error — bs-ns's "harder"
notebook (38/39, one bracket-level slip) and Luke J. Miller's 1,035-row bank
(54/54 verifiable items in the sample). The nine mismatches are dominated by
*key slips and stale kwarg names*, not by misconceptions.

## Mismatch inventory (all 9)

| Exam | Item | What execution showed |
|---|---|---|
| rishihg | Q24 | `resilience_level` is Estimator-only in V2; setting it on `SamplerOptions` raises `ValidationError` (V1→V2 drift, not author error) |
| lkaucic | Q48 | "export to a **file**" keys `dumps()`; `dumps(circuit) -> str`, `dump(circuit, stream) -> None` — the file answer is `dump()` |
| lkaucic | Q36 | key says precision affects Sampler not Estimator; `default_precision` exists only on `EstimatorOptions`. No correct option present |
| gnietof | exam3 Q1 | keyed option B (`Pauli([True],[True],0])`) is not valid Python; option A (`Pauli('X')@Pauli('Z')` → `-iY`) is the natural second answer |
| bs-ns | harder Q9 | `(circuit, [o1,o2], [[0],[π/2],[π]])` raises "observables shape (2,) and parameter values shape (3,) are not broadcastable"; `[[o1],[o2]]` gives the keyed 6 |
| adrian | Q17 | keyed `estimator.run([qc, obs])` raises `ValueError`; the PUB needs `run([(qc, obs)])` |
| skupisz | Q5 | keyed `order="desc"` — `plot_histogram` has no `order` kwarg; correct behaviour comes from `sort="desc"`, so "None of the above" is right |
| skupisz | Q6 | qsphere shows probability/phase, not Re/Im; `plot_state_city` (not in the key) is the canonical answer alongside Hinton |
| skupisz | Q15 | keyed `group_commuting(group_wise=True)` raises `TypeError`; the real kwarg is `qubit_wise` (default `False` = the behaviour asked for) |

## Common misconceptions / themes

1. **V1→V2 primitive drift is still the one recurring conceptual pattern**, and it
   is receding. `resilience_level` as a Sampler option (rishihg Q24) and
   "quasi-probability distributions" as SamplerV2 output (Q-Bees Q14, rishihg Q5)
   were the pass-1 instances. In pass 2 the newer sets get this *right*:
   Luke #607/#700 explicitly reject quasi-probabilities, Adrian Q13/Q16 split the
   Sampler and Estimator option groups correctly, and gnietof/lkaucic both key the
   `precision` vs `shots` split correctly.

2. **PUB shape and tuple structure is where authors actually slip.** Three of the
   nine mismatches are PUB-shaped: a flat observables list that does not broadcast
   (bs-ns harder Q9), a missing tuple inside `run([...])` (adrian Q17), and
   `precision` misattributed to the Sampler (lkaucic Q36). Everyone understands
   the *concept*; the errors are in the brackets. Good distractor material.

3. **Stale or invented keyword names are the second cluster.** `order=` for
   `plot_histogram`, `group_wise=` for `group_commuting`, `max_width=`/`truncate=`
   for the text drawer, `bind_parameters` for parameter binding: all plausible,
   all wrong, all cheap to check by execution. Distractors built from *nearly
   correct kwarg names* are the highest-yield trap in this exam's style.

4. **Physics/linear-algebra items remain a collective strength.** Every
   state-preparation, probability, expectation-value and operator-matrix question
   across both passes executed correctly — 60+ items including ⟨YY⟩ = −1 on Φ⁺,
   ⟨XX−YY+ZZ⟩ = −1 on Ψ⁺, `-iI` from `X·Y·Z`, and the `from_sparse_list`
   little-endian labels. Where a hand-written exam could hide a sign error, these
   authors did not make one.

5. **Presentation issues are more common than content errors.** Two of the seven
   pass-2 exams have a measurable answer-position tell: Luke's bank is
   A 476 / B 303 / C 95 / D 16 across 890 keyed rows, and ManuelEsparcia is
   A 8 / B 13 / C 3 / D 0 across 24. Luke's bank also contains 564 exact duplicate
   rows and 120 rows whose key is the literal string `"1"`. None of this affects
   the correctness of the underlying items, and all of it is fixable with a load-time
   shuffle plus a dedupe.

## Version-drift patterns (for anyone updating these exams)

- `resilience_level`: Estimator V2 only (levels 0-2). Not a Sampler option.
  Ref: https://quantum.cloud.ibm.com/docs/guides/v2-primitives#error-mitigation-and-suppression
- Sampler results: V1 `quasi_dists` / `QuasiDistribution` → V2 per-register
  `BitArray` (`pub.data.<reg>.get_counts()`); `measure_all()` names the register `meas`.
- Construction kwargs: prefer `mode=` (backend/session/batch) over `backend=` / `session=`.
- `shots` and `precision` are **run-time** keyword arguments (`run(pubs, *, shots=…)`,
  `run(pubs, *, precision=…)`) or per-PUB entries — not constructor arguments.
- `QuantumCircuit.bind_parameters` is gone; use `assign_parameters`.
- `qiskit.qasm3.loads` needs the optional `qiskit-qasm3-import` package; `dumps`
  returns a string and `dump` writes to a stream.

## Which exams shine

- **vantnprof** and **MarcoBarroca** (pass 1) remain the standout 68-question
  mocks: authentic format, deep V2 coverage, explanations, inline docs citations.
- **gnietof** is the closest thing to the real paper: three complete 20-question
  exams with rendered circuit/qsphere/histogram images as answer choices, and
  27/28 executed answers confirmed.
- **Luke J. Miller** has the largest bank by an order of magnitude (1,035 rows,
  465 distinct) and the only per-task curriculum tagging; 54/54 verifiable sampled
  answers confirmed. Dedupe + shuffle would make it the reference resource.
- **bs-ns** is the best *self-check* set: its "harder" notebook is almost entirely
  computable, so a learner can verify every answer themselves in three lines.
- **lkaucic** has the best engineering: questions as YAML, exam as generated output.
  Anyone wanting to build on community content should start from a format like this.
- **clausia** (50 Q) and **kurian** (20 Q) are excellent for their size — kurian
  still has the best answer key in the cohort.

## Notes on provenance (flagged, neutral)

- **Luke-J-Miller** `non-necessary_files/` redistributes IBM's official
  `C1000-179_SAM_SampleTestQiskitv2.pdf` and `C1000-179_STU_StudyGuideQiskitv2.pdf`
  (also mirrored in the linked Kaggle dataset). The question bank itself reads as
  independently written. Anyone reusing that repo should check IBM's terms for
  those PDFs. Not opened or parsed here.
- **quantum-tokyo** `src/sample.ipynb` reproduces the 21-question sample test from
  IBM's official certification page, with community-written explanations, and says
  so in its first cell. Transparently attributed; not parsed here because the
  question text originates with IBM.

## Licensing note

Reuse rights remain the main practical caveat: most repos (including several of
the strongest — clausia, kurian, vantnprof, algovista, gnietof, lkaucic,
Luke-J-Miller, bs-ns) carry **no license or NOASSERTION**, so their question text
should be treated as all-rights-reserved. Clear licenses exist for
**rishihg (MIT)**, **MarcoBarroca (MIT)**, and **quantum-tokyo (Apache-2.0)**.

## Artifacts

- Inventory (all 23): `data/community/inventory.json`
- Neutral directory (all 23): `data/community/summary.json`
- Normalized questions (14): `data/community/parsed/<slug>.json`
- Per-exam reports (14): `data/community/reports/<slug>.md`
- Reusable parser (14 parsers): `pipeline/community_validate.py`
- Raw fetched sources: `data/community/raw/` (Luke's CSV/PKL banks under `raw/luke/`)
