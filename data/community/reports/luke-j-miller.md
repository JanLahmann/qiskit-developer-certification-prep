# Validation report — Luke-J-Miller / `Qiskit-v2.X-developer-certification-practice-test`

- Source: https://github.com/Luke-J-Miller/Qiskit-v2.X-developer-certification-practice-test
- Author: **Luke J. Miller** — thank you for the largest open bank in the cohort and
  for shipping the source CSVs alongside it.
- Format: a notebook driver (adaptive practice, timed tests, progress saving) over
  question banks stored as `necessary_files/*.pkl`, with the 15 source `*.csv` files
  kept in `non-necessary_files/`.
- License: none stated (minimal quoting below).
- Reviewed against: qiskit 2.5.0 / qiskit-ibm-runtime 0.48.0 / qiskit-aer 0.17.2.

## Overview & credit

This is the most-starred v2.x practice resource and by far the biggest: **1,035
rows** in `question_df.pkl`, tagged by exam section *and* by task
(`TASK 2.3: Visualize quantum states`, …), which is a level of curriculum
mapping nobody else in the cohort attempted. The notebook around it is a real
study tool — adaptive selection weighted by per-task performance, timed full
tests, and a saved student history. The section/task tagging alone makes this
bank the best raw material for gap analysis of the eight exam objectives.

## Method

**Parsing.** The bank is a pandas pickle. Unpickling arbitrary bytes executes
code, so the file was first disassembled with `pickletools.genops` (which never
executes) to enumerate its `STACK_GLOBAL` targets — only pandas/numpy container
constructors appear — and then loaded through a **restricted unpickler** whose
`find_class` whitelists exactly those ten names. No community code was imported
or run at any point. The notebook driver was read, not executed (it prompts for
file paths and writes `.pkl` files).

**Execution.** The bank is far too large to execute exhaustively, so this pass
took a **seeded, stratified random sample**: from the 890 rows that carry a usable
key, 523 were classed as code/API-bearing (stem or options reference a Qiskit
identifier), and a sample of **60** was drawn proportionally across the eight
sections with `random.Random(20260725)`. Sampled items were verified by executing
reviewed snippets offline in the pinned stack (fake backends, no credentials, no
network, 60 s per snippet): seven grouped snippets covering quantum_info/circuit
APIs, visualization signatures, runtime job/session APIs, primitives and PUBs, and
the OpenQASM 3 exporter. The sampled question numbers are reproducible from the
seed; they index `data/community/parsed/luke-j-miller.json`.

## Parse coverage

- Rows parsed from `question_df.pkl`: **1,035 / 1,035** (100%).
- Rows with an answer resolvable to an option letter: **890**.
- Rows whose `Correct_Answer` is the literal string `1`: **120** (all in section 2).
- Rows that are leftover CSV header lines: **25**.
- Distinct question stems: **465** — i.e. **564 rows are exact duplicates** of
  another row (same stem, options and answer).
- Code/API-bearing (by the sampling heuristic): **523**.
- Normalized data: `data/community/parsed/luke-j-miller.json` (keeps `section`,
  `task`, and the raw `answer_text`).

## Execution results (60-question stratified sample)

**60 sampled; 54 confirmed, 0 mismatches, 6 unverified.**

Per section: S1 3/3 confirmed · S2 8/9 (1 unverified) · S3 5/5 · S4 7/10 (3
unverified) · S5 5/5 · S6 4/5 (1 unverified) · S7 13/14 (1 unverified) · S8 9/9.

Representative confirmations:

| # | Claim tested | Observed | Stated | Verdict |
|---|---|---|---|---|
| 9 | `Pauli.evolve(frame=…)` for Heisenberg | signature default `frame='h'`; docstring "Heisenberg (default) … `frame='s'` for Schrödinger" | B | confirmed |
| 45 | CX from an `XGate` | `XGate().control(1).name == 'cx'` | B | confirmed |
| 111 | Bloch spheres drawn for a 2-qubit state | figure has 2 axes | A | confirmed |
| 115 | qsphere label/phase kwargs | `show_state_labels`, `show_state_phases` present | A | confirmed |
| 170/242 | qubit marker size in `plot_gate_map` | `qubit_size` present | A | confirmed |
| 253 | title size in `plot_bloch_multivector` | `title_font_size` present | A | confirmed |
| 315 | safe-to-mutate copy of a singleton | `XGate() is XGate()` → True; `.to_mutable()` breaks identity | C | confirmed |
| 455/515 | equivalence libraries | `StandardEquivalenceLibrary` and `SessionEquivalenceLibrary` both exported | A / A | confirmed |
| 471 | `Session.session_id` on simulators | source: "None if the backend is a simulator" | B | confirmed |
| 499/807 | constraining option values | `Options.set_validator('shots',(1,4096))`; out-of-range raises `ValueError` | C | confirmed |
| 527/698 | Estimator V2 PUB tuple | `EstimatorPub` fields: circuit, observables, parameter_values, precision | A | confirmed |
| 536 | Estimator V2 resilience levels | source documents levels 0, 1, 2 | A (0–2) | confirmed |
| 542/620 | named classical registers in a Sampler PubResult | `data.alpha.get_counts()`, `data.beta…` | A | confirmed |
| 561 | multi-qubit gates in a `Target` | `target['cx']` keyed by `(0, 1)` | B | confirmed |
| 590 | `TwirlingOptions.strategy` default | docstring: `Default: "active-accum"` | B | confirmed |
| 607/700 | Sampler V2 measurement output | `BitArray` per classical register; no `quasi_dists` | A | confirmed |
| 722/833 | `RuntimeJobV2.status()` return | `JobStatus = Literal["INITIALIZING","QUEUED","RUNNING","CANCELLED","DONE","ERROR"]` — a string | A | confirmed |
| 751/768 | where shots / precision go | `run(pubs,*,shots=None)`, `run(pubs,*,precision=None)`, plus per-PUB shots | B / B | confirmed |
| 776/796 | `max_time` constraint and format | source: "must be less than the system imposed maximum"; "a string like `2h 30m 40s`" | B / A | confirmed |
| 857 | method true only while executing | `running()` — "whether the job is actively running" | A | confirmed |
| 881 | `Session.from_id` error for unknown backend | docstring Raises: "IBMRuntimeError: If the backend of the session is unknown" | A | confirmed |
| 900 | legacy switch-case export flag | `ExperimentalFeatures.SWITCH_CASE_V1` is the only member | A | confirmed |
| 910 | `CustomGate` callable attribute | fields: `name, constructor, num_params, num_qubits` | B | confirmed |
| 949 | destination parameter of `qasm3.dump` | signature `(circuit, stream, **kwargs)` | B | confirmed |
| 1016/1019/1035 | `logs()` / `usage()` / `error_message()` | docstrings: logs only after finish; usage in seconds; error_message returns the failure reason | A / A / A | confirmed |

Unverified (6): **#94** (`plot_gate_map` `ax` behaviour — the renderer needs the
Graphviz binaries, unavailable in the offline harness; the `ax` parameter does
exist), and **#462, #493, #501/#809, #716** — prose statements about session
purpose, the provider interface, sync vs async provider jobs, and Open Plan
execution modes, which have no executable surface. None of them looked wrong;
they are simply not provable by running code.

**#263 is confirmed with a note:** the key says `QiskitError` is raised for an
invalid statevector in `plot_state_qsphere`; the class actually raised is
`VisualizationError`, which *subclasses* `QiskitError`, so the key is true but the
more specific option B is arguably the better answer.

## Findings

**1. Roughly half the bank is duplicated.** 1,035 rows reduce to **465 distinct
stems**; 564 rows repeat an earlier row exactly (same options, same answer). The
seeded 60-question sample happened to draw seven duplicate pairs
(#170/#242, #499/#807, #501/#809, #527/#698, #542/#620, #607/#700, #722/#833),
which is what a ~55% duplication rate predicts. In practice this means a "50
random questions" session will repeat itself, and the adaptive weighting will
double-count the same concept. Deduplicating on the stem would take the bank to
465 high-quality items — still the largest in the cohort.

**2. 120 rows have an unusable answer key.** Every row in
`TASK 2.1/2.2/2.3` (three blocks of 42, minus header rows) has `Correct_Answer`
set to the literal string `"1"` rather than the text of the correct choice. The
driver matches the answer by text, so these items cannot be scored. If `1` was
meant as "choice 1", the affected items are all keyed A — which is also worth a
look (see next point).

**3. 25 rows are leftover CSV header lines** that were concatenated into the
DataFrame (`Question / Answer A / … / Correct Answer Choice`). They will surface
to the learner as a question whose text is the word "Question".

**4. Answer-position bias.** Of the 890 keyed rows: **A × 476, B × 303, C × 95,
D × 16**. More than half the answers are the first choice and fewer than 2% are
the last. Since the notebook presents choices in column order, a candidate who
always picked A would score ~53%. A one-line shuffle at load time (permuting the
four choice columns per row and re-pointing the key) would fix this without
touching the content — and it is the single highest-leverage change available to
this bank.

**5. Content quality within the sample was high.** Zero mismatches in 54
executed items is the best result in either validation pass, and the sample
included genuinely fine-grained API questions (singleton gates and `to_mutable()`,
`SessionEquivalenceLibrary` for custom basis gates, `TwirlingOptions.strategy`
defaults, `Session.max_time` string format, `ExperimentalFeatures.SWITCH_CASE_V1`).
Where other sets in the cohort drift toward V1 language, this bank is consistently
V2-correct: #607/#700 explicitly reject "quasi-probability distributions" as the
SamplerV2 output.

**6. Provenance note (flagged, not adjudicated).** `non-necessary_files/` also
contains `C1000-179_SAM_SampleTestQiskitv2.pdf` and
`C1000-179_STU_StudyGuideQiskitv2.pdf` — IBM's official sample test and study
guide — redistributed in the repo, and the notebook's default paths point at a
Kaggle dataset mirror of the same files. Those PDFs are IBM's own material with
their own terms; the question *bank* itself reads as independently written (its
phrasing and task tagging do not track the sample test). Noting this only so that
anyone reusing this repo checks the redistribution terms first. This review did
not open or parse those PDFs.

## Verdict

The largest and, per executed item, the most accurate bank surveyed: 54 of 54
verifiable sampled answers confirmed, with section/task tagging that no one else
provides. Its three issues are all mechanical rather than conceptual —
deduplication (564 repeated rows), the 120 rows keyed `"1"`, and the A-heavy
answer distribution. Fixing those three would turn an already-strong 465-question
bank into the reference resource for this exam. Thank you, Luke.
