# Review Ledger — verified facts, hazards, and recipes

Carry-forward knowledge for generation and review agents. **Read this before
touching the question bank; append (never delete) when you verify something
new.** Every entry here was empirically verified or observed during a review
wave — do not contradict an entry without re-verifying and updating it.

Format: keep entries terse, dated, and falsifiable. This file exists because
review knowledge previously lived only in the orchestrator's session context
and died with it.

## Verified library facts (pinned stack: qiskit 2.5.0 / runtime 0.48.0 / aer 0.17.2)

- **SamplerV2 has NO `resilience_level`** (pydantic ValidationError on assignment);
  EstimatorV2 has it (0/1/2, default 1). SamplerV2 noise management = dynamical
  decoupling + Pauli twirling only. The official objective wording "set sampler
  primitive options such as resilience levels" contradicts the library — questions
  state library reality and reconcile in the explanation. (2026-07-25, s5 wave)
- **Fake-backend shots trap:** Runtime primitives on fake backends silently use
  `qiskit.primitives.BackendSamplerV2` defaults (`default_shots=1024`); the real
  Runtime service default is **4096** (twirling auto = 32×128; fallback chain in
  guides/sampler-options). Any answer depending on an unspecified shot count is
  provably-wrong-but-passing. Killed s5-q012 over this. (2026-07-25)
- **`RuntimeJobV2.done()/.errored()/.running()/.in_final_state()/.wait_for_final_state()/.metrics()/.usage()` all EXIST** in runtime 0.48. `.metrics()`/`.usage()` are not observable on local primitives — proofs must not assert them locally. (2026-07-25, s7)
- **`RuntimeJobV2.status()` returns a plain string** (`"DONE"` etc.), not a
  `JobStatus` enum; the enum is still importable and compares False vs strings —
  a good distractor, a wrong claim if keyed. (2026-07-25, s7)
- **`DataBin` supports attribute AND item access** (`db["meas"]` works); has
  `keys/values/items/shape/ndim/size`; has NO `get_counts()` and NO `registers`.
  Never use `db["name"]` as a wrong option. (2026-07-25, s7)
- **`StatevectorEstimator` rejects measured circuits** (QiskitError) but Runtime
  `EstimatorV2` on a fake backend ACCEPTS them — implementation-fragile territory;
  version-scope or avoid. `StatevectorEstimator` also reports `stds=0.0` even with
  `default_precision` set; only Runtime EstimatorV2 (fake backend suffices) yields
  a real standard error. (2026-07-25, s6/s7)
- **`QuantumCircuit.from_qasm_str/from_qasm_file` still exist in Qiskit 2.5** and
  work — never key "removed in 2.x", never offer as distractor where it would be
  a second correct answer. `c_if` IS removed in 2.x; `qiskit.tools` is gone
  (ModuleNotFoundError). (2026-07-25, s8/s2)
- **qasm3 asymmetry:** `qiskit.qasm3.dumps/dump` are native; `loads/load` require
  the `qiskit-qasm3-import` package (MissingOptionalLibraryError without it — and
  that package is NOT in our .venv; proofs must block/handle it). `qiskit.qasm2`
  does both natively. (2026-07-25, s8)
- **`Operator.compose` applies self FIRST (B·A); `.dot` is A·B.** (2026-07-25, s1)
- **`json.dump(x, cls=RuntimeDecoder)`** fails with TypeError (Decoder passed
  where Encoder belongs) — verified distractor. (2026-07-25, s7)
- **`session.details()` returns None in local testing mode** (guard at
  session.py:296); live keys incl. state/accepting_jobs/max_time/last_job_completed.
  `backend=`/`session=` kwargs removed in favor of `mode=`. (2026-07-20/25)

## Documentation link facts

- **404 (dead):** `guides/get-started-with-primitives` (→ use get-started-with-sampler /
  get-started-with-estimator), `guides/specify-runtime-options` (→ sampler-options /
  estimator-options).
- **Content-free redirects (treat as dead; check_links now fails on slug mismatch):**
  `guides/primitives-rest-api` → guides/primitives (no REST content; → use
  sampler-rest-api / estimator-rest-api / cloud-setup-rest-api),
  `guides/map-problem-to-circuits` → intro-to-patterns.
- **301 (normalize):** `guides/configure-error-suppression` →
  `guides/error-mitigation-and-suppression-techniques`.
- Locale redirect `/docs/X` → `/docs/en/X` is normal, not drift.
- Good primitive-specific pages: sampler-input-output, sampler-noise-management,
  sampler-options, estimator-options, estimator-noise-management,
  get-started-with-sampler, get-started-with-estimator. (2026-07-25)

## Meta-pattern calibration recipes (audit: pipeline/audit_meta_patterns.py)

- **Target CHANCE (25%), never zero.** Every naive fix inverts the tell; the audit
  measures both directions (longest/avoid_longest, most_hedged/avoid_hedged,
  least_absolute/most_absolute). Instrument the inverse BEFORE fixing the forward tell.
- **Length recipe:** ~N/4 questions correct-strictly-longest (ratio ≤1.3), every
  other question exactly ONE distractor strictly longest. Ties are the trap
  (2-way tie with correct: 0.5 to longest, 0 to avoid_longest — strictly worse
  than correct-longest). All-four-equal questions are free ballast (avoid_longest
  abstains). Correct-is-shortest should also happen ~N/4 (s3 hit 6% and taught
  "avoid the shortest").
- **Absolutes 3:1 recipe:** per ~4 affected questions, 3× "one distractor carries
  the absolute + another distractor hedges", 1× factually-true absolute in the
  correct option.
- **Hedges:** let 1–2 correct options truthfully carry "typically"/"by default";
  ≥3 hedged distractors in one question drives avoid_hedged to 1.0 for it.
- **Tokenizer quirks:** `word_set` splits on non-alpha → `measure_all()` counts as
  absolute "all", `default_shots` as hedge "default", `most_available` as hedge
  "most". `tokens()` keeps underscores → `num_qubits` is one stem-echo token.
  Never remove real API idioms to silence a flag; compensate elsewhere.
- **Fix length + absolutes TOGETHER:** trimming a correct option can create an
  absolute tell that wasn't there (s4).
- **Known accepted residuals (2026-07-25 bank-wide):** shortest_option 16.7%,
  odd_one_out 13.4% (below chance; weak inverse exploits ~27%), similar_twin_member
  27.8%, 48 deliberate low length flags, 2 benign cross-question duplicate option
  texts in s6 (same real API path, different stems, no contradiction).

## Proof-quality hazards

- **Circular proofs:** a proof that recomputes the question's own formula proves
  nothing (s6-q017). Proofs must OBSERVE independently (measure spread, catch the
  exception, diff the output).
- **Proof/option drift:** verify_bank checks the verdict, not whether evidence
  strings still describe current option texts (s4-q023 said shots=256 while the
  stem said 1024; s4-q038 proof exercised a different call than the option showed).
  `pipeline/lint_proof_drift.py` now flags kwarg-like tokens and ≥3-digit numbers
  in evidence that appear nowhere in the question — run it after rewriting options.
- Evidence must reference option KEYS, and per-option evidence must cover every key.
- Never reference display letters in explanations/evidence ("option A") — the site
  shuffles positions at render time (2026-07-25); stored keys ≠ shown letters.

## Community-bank intelligence (validation passes 1–2, 14/23 exams)

- Highest-yield distractor classes observed in real banks: PUB bracketing
  (`[o1,o2]` shape (2,) vs `[[o1],[o2]]` shape (2,1)); near-miss kwargs
  (`order=`→none, `group_wise=`→`qubit_wise=`, `dumps`→`dump`,
  `bind_parameters`→`assign_parameters`); V1 signatures (`run(circuits=,
  observables=)`).
- Similarity kills so far: s1-q011, s1-q046, s6-q020 (vantnprof), s7-q010/q013/q028
  reworked (vantnprof/marcobarroca/adrian). Always check data/community/parsed/*.json.
- Provenance flags (neutral, unadjudicated): Luke-J-Miller repo redistributes
  official IBM sample-test/study-guide PDFs; quantum-tokyo reproduces the official
  sample test with attribution. Luke's parsed bank is stored as fingerprints only
  (unlicensed, 1035 Qs); raw pickle gitignored.

## Distractor pools (2026-07-25)

- Schema: optional `display_count` (4–5); must be < len(options) and leave >= 2
  displayed distractors. Runtime: `shuffledOptions()` seededly samples distractors
  (correct always shown), then position-shuffles; same seed = same subset+layout.
- Pool distractors need: named misconception + explanation entry + proof
  attempt/refutation with evidence (executed questions). Keys append alphabetically
  (E, F). Anki decks show the full pool (stored order).
- The audit enumerates displayed variants: a tell in ANY variant flags the question;
  aggregate heuristics weight variants uniformly. Gold pilots: s5-q019 (executed,
  enabled-vs-enable near-miss E), s4-q001 (conceptual, session-max_time misuse E).
- Multis with 4+ correct answers cannot pool (display_count constraint) — skip them.
- Highest-yield pool distractor classes: near-miss attribute/kwarg names
  (enable/enabled, dump/dumps, qubit_wise/group_wise), PUB bracketing, V1
  signatures, wrong-options-group paths (resilience on Sampler, twirling fields
  on dynamical_decoupling).
- **Options cap is 6** (schema `maxItems`): a 5-option question can take exactly
  ONE pool distractor, a 4-option question two. 3-correct multis need
  `display_count: 5`. (2026-07-25, s1 pool wave)
- **Pool length rules (derived on the s1 wave — a variant can create a tell the
  base question does not have):** (a) if the correct option is currently strictly
  longest, keep new distractors ≤ correct AND ≥ the longest existing distractor —
  the variant that drops that distractor otherwise raises the ratio (s1-q040 would
  have gone 1.21 → 1.52 = HIGH); (b) if the correct option is NOT longest, new
  distractors must be ≥ len(correct), because one variant always drops the current
  longest distractor.
- **Pool hedge/absolute rule:** the absolute/hedge balance is re-evaluated per
  variant. If a question's only hedged distractor can be dropped while an
  absolute-carrying distractor survives, the new pool distractor MUST carry the
  hedge, or `absolute_distractor_tell` (medium) fires (hit s1-q015/018/041/042/047
  in design; all pre-empted).
- **Pool stem-echo rule:** dropping the high-overlap distractor can expose a
  `stem_echo_tell` (medium). Caught live on s1-q037 (correct overlap 4 vs 2 after
  the twin distractor was dropped); fixed by giving the pool distractor ≥3
  stem-vocabulary tokens (`qubit`, `operator`, `tensor`).
- Do NOT offer `Pauli(...).reverse_qargs()` as a distractor on label-order
  questions — it genuinely reverses qubit order and would be a second correct
  answer. `.adjoint()` is the safe near-miss (Hermitian labels return unchanged).
- Predict-output pools: a wrong-VALUE option must not duplicate another option's
  value (two options claiming the same output is itself a tell). For 2-qubit index
  questions the value space (0–3) is exhausted after 4 options — use a type/shape
  error ("raises", "length-2 vector", "dict keys") instead.

## Verified library facts (s1 pool wave, 2026-07-25, qiskit 2.5.0)

- `Statevector.from_int(2, dims=4)` **accepts an int `dims`** (total dimension) and
  returns dims `(2, 2)` — "dims must be a tuple" is a safe, refuted distractor.
- `Statevector.probabilities_dict()` keys are **`np.str_` bitstrings** (str
  subclass), never ints; `probabilities([q])` returns an **ndarray**, not a dict.
- `Statevector(qc)` (constructor) raises the **same** QiskitError as
  `from_instruction` on a measured circuit (`Cannot apply instruction with
  classical bits: measure`) — there is no constructor bypass.
- `Statevector.evolve` is functional: returns a NEW Statevector, source unchanged
  (never in-place / never None).
- `Statevector.from_label` accepts **multi-character** labels and '+','-','r','l'.
- `Pauli` labels accept a **phase prefix** (`Pauli('-iXZ').phase == 1`); a plain
  multi-letter label has phase 0, so `Pauli('XZ').to_matrix()` is exactly X⊗Z.
- `Pauli('ZI').adjoint()` returns `'ZI'` (Hermitian) — adjoint never reverses
  qubit order.
- `SparsePauliOp.simplify()` **sums** duplicate terms (1+2 → 3), never averages,
  and only drops coefficients that are zero within `atol` (a coeff-1 term survives).
- Pauli products: X·Y = iZ, Y·Z = iX, Z·X = iY; reversing the operands conjugates
  the phase (Z·Y = −iX). `Pauli('ZI').commutes(Pauli('XX'))` is False — an identity
  factor does not buy commutation.
- `Operator.equiv` (up to global phase): T ≢ RZ(π/2) (that is S), H ≢ RY(π/2)
  (determinants differ in sign); H = RY(π/2)·Z.

## Process rules

- Reviewers/generators run BOTH gates per batch: `verify_bank.py --section sX`
  AND `audit_meta_patterns.py --section sX` (0 blockers/warnings, no high/medium
  flags). The audit artifact data/audits/meta_pattern_audit.* is section-scoped
  to the last run — always re-run bank-wide (`--gate`) before assembly.
- The orchestrator independently re-runs both gates after every agent — and after
  its own edits (an orchestrator touch-up once created a new medium flag).
- Reality wins: fix the question, never the proof.
- Append what you verify to this ledger.

## Verified library facts (s2 pool wave — visualization, 2026-07-25, qiskit 2.5.0)

- **`QuantumCircuit.draw()` has a fixed signature (no `**kwargs`)**: any near-miss
  keyword raises `TypeError` (`initial_states=` for `initial_state=`). Same for the
  standalone drawer: `circuit_drawer(qc, format="text")` → TypeError (the kwarg is
  `output=`). Both are clean, cheap pool distractors.
- **`style={...}` is silently ignored by the text renderer** — no error, and no
  `|0>` labels appear. A non-raising refutation (good for "which call adds X?" stems).
- **`draw("mpl", ax=ax)` returns `None`** (the caller owns the Axes) — verified
  distractor for any "which call returns a `Figure`?" question.
- **`idle_wires="auto"` keeps idle wires unless the circuit carries a transpiler
  layout**; on an untranspiled circuit q_1 is still drawn. Safe distractor there,
  a SECOND CORRECT ANSWER on a transpiled circuit — version/context-scope it.
- **`circuit_drawer(qc, output="matplotlib")` raises the same `VisualizationError`
  as the method** ("valid choices are text, latex, latex_source, and mpl") — the
  method and the function share one renderer registry.
- **`with qc.if_test(qc.clbits[0] == 1):` → `TypeError: 'bool' object is not
  subscriptable`** (`Clbit.__eq__` returns a plain bool). `if_test` wants a
  `(clbit, value)` tuple or an `expr` condition.
- **`plot_histogram` / `plot_distribution` have NO `shots=` parameter** (TypeError) —
  normalization is derived from the counts themselves. The V1 habit
  `plot_histogram(counts, shots=...)` is a verified-wrong pool distractor.
- **`legend=` must be a list**, matched element-wise against the executions: a plain
  string raises `VisualizationError: Length of legend (13) doesn't match number of
  input executions (2)`. `labels=` does not exist (TypeError).
- **`number_to_keep=k` builds a `rest` bar equal to the SUM of the folded counts**
  (heights 500/500/24 for the 20+4 remainder), never their average.
- **`BitArray` has `get_counts()`, `get_int_counts()`, `get_bitstrings()` and NO
  bare `counts()`** (AttributeError). CAUTION:
  `plot_histogram(bitarray.get_int_counts())` **SUCCEEDS** (returns a Figure) — never
  use it as a distractor. `plot_histogram(bitarray.get_bitstrings())` raises
  `AttributeError: 'str' object has no attribute 'values'` (safe).
- **`Statevector.draw(output="qsphere")` works** (`output` is the first positional
  parameter) — never offer it as a wrong option. `sv.plot(...)` does not exist
  (AttributeError), and `sv.draw("q_sphere")` is the safe spelling near-miss.
- **`plot_bloch_multivector([[0,0,1],[0,0,1]])` → `QiskitError: Invalid DensityMatrix
  input: not a square matrix`** — a list of Bloch vectors is parsed as a state.
- **`plot_bloch_multivector(partial_trace(state, [1]))` succeeds but draws ONE
  sphere** — a "runs fine, wrong result" distractor (needs a count-the-axes proof).
- **`Statevector.from_label('r')` = +Y (0,1,0), `'l'` = −Y (0,−1,0)** — the safe
  ±Y foils for ±X Bloch-arrow questions.
- **`rz` on |0> leaves ⟨Z⟩ = 1** (global phase only) — safe "not on the equator"
  distractor. `ry(π/2)` would be a SECOND CORRECT answer on equator questions.

## Pool-craft rules (s2 pool wave, 2026-07-25)

- **Pool variants re-expose `format_tell`**: when exactly one distractor carries the
  backticks that cleared an earlier format tell, the variant dropping it flags. The
  new pool distractor must be code-formatted too (hit s2-q012 live).
- **Stem-echo (medium) fires when the only high-overlap distractor is droppable** —
  give the pool distractor at least as much stem vocabulary as the correct option
  (s2-q018: correct overlap 3 vs best distractor 1 after the drop; fixed by echoing
  `output`/`high`/`resolution`/`figure`/`savefig`).
- **Absolute/hedge rule re-confirmed** (s2-q032): distractor D carried the absolutes
  and A was the only hedge, so the variant dropping A flagged — the pool distractor
  had to hedge.
- **Length rule (b) refined:** a pool distractor SHORTER than the correct option is
  safe whenever every displayed subset still contains a long distractor (choose-3-of-4
  can never be all-short). The real bar is: no variant may drop max-distractor length
  below `len(correct)/1.4` (that is the low→high boundary). Extra low `length_tell`
  entries are an accepted residual; medium/high are not.
- **All-equal-length option sets tolerate one short pool distractor** (s2-q019, int
  key `{5: 1.0}`): it drags `shortest_option` and `avoid_longest` below chance.
- **Pooling raises the position heuristics**: variants that drop key A abstain from
  `position_A` on the questions where A is wrong, so the surviving sample is
  A-heavy (s2 went 0.315 → 0.359 against a 0.40 warn line). Watch it in sections
  whose answer keys already skew, and prefer `display_count: 5` there.
- **Whole-basis questions cannot be pooled**: s2-q031 lists all four 2-qubit basis
  states as options; a fifth option would not be a basis state (a tell). Skipped.

## Verified library facts (s3 pool wave — circuit construction, 2026-07-25, qiskit 2.5.0)

- **`transpile()` no longer defaults to optimization level 1.** Qiskit 2.5 resolves
  `optimization_level=None` via `config.get("transpile_optimization_level", 2)` — the
  SAME default as `generate_preset_pass_manager`. The widespread "transpile defaults
  to 1" lore is Qiskit 1.x. Reality-check fix applied to the explanations of
  s3-q031 and s3-q036 (keyed answers unaffected: both are "level 2").
  `generate_preset_pass_manager`'s default is a signature constant — a 5-qubit and a
  9-qubit backend both reproduce level 2.
- **`measure_all()` ALWAYS appends a fresh `meas` register** (`add_bits=True` default):
  `QuantumCircuit(2, 2).measure_all()` ends with `cregs=['c','meas']`, 4 clbits, and
  space-separated counts keys. `measure_active()` behaves the same way (also names its
  register `meas`). Instruction order is `... barrier, measure, measure` — the barrier
  goes BEFORE the measurements.
- **`QuantumCircuit.bind_parameters` is GONE** in 2.5 (`AttributeError`) — a clean pool
  distractor for every positional-binding question.
- **`assign_parameters` matches dict keys by Parameter IDENTITY**: a *different*
  `Parameter('th')` object raises `CircuitError: Cannot bind parameters (th) not
  present in the circuit`. **Name strings ARE valid keys** (`{'q': 1.0}` works) — never
  offer "string keys raise" as a distractor.
- **`ParameterVector` does not auto-grow**: `x[3]` on a length-3 vector raises
  `IndexError`; a 1-element list for a 2-element vector raises the same length
  `ValueError` as plain `Parameter`s (a vector never broadcasts one value).
- **`x()` returns an `InstructionSet` with NO `.condition`** (`AttributeError`) — the
  whole condition mechanism left with `c_if` in 2.0. A plain Python `if cr[0] == 1:`
  is silently False at build time (no gate added, no error) — a "runs fine, does
  nothing" refutation.
- **`if_test((ClassicalRegister, 1))` is valid** (register-valued conditions); never
  key or offer "conditions must be a single `Clbit`". `if_test(cr[0] == 1)` →
  `TypeError: 'bool' object is not subscriptable` (confirms the s2 finding for
  register bits). `while_loop((clbit, 1))` builds a `while_loop` op, not `if_else` —
  the safe near-miss on "which snippet produces an `if_else`?" stems.
- **`expr.equal(creg, 3)` lifts the bare int automatically** (no `expr.lift` needed).
  `switch`: `case(case.DEFAULT)` may be declared LAST; `for_loop(range(3))` needs no
  `as i` when the body ignores the index.
- **`add_register` refuses a duplicate register name** (`CircuitError: register name
  "q" already exists`) — and `QuantumCircuit(2, 2)` already owns `q` and `c`.
- **Pass-manager call shapes:** `pm.run([qc])` returns a LIST (not a circuit);
  `pm.transpile`, `pm(qc)` and `QuantumCircuit.transpile` do not exist;
  `generate_preset_pass_manager(target=<list of gate names>)` →
  `AttributeError: 'list' object has no attribute 'build_coupling_map'`;
  `basis_gates=` without `coupling_map=` translates but does NOT route (result is
  not ISA).
- **Preset `pm.stages` is always the same 6-tuple** `(init, layout, routing,
  translation, optimization, scheduling)` — the scheduling slot exists even with no
  scheduling method (it just runs empty).
- **Routing costs, measured:** `cx(0, 4)` on a 5-qubit line → level 0 keeps the
  trivial layout `[0,1,2,3,4]` and emits **10 cx**; level 1 picks layout `[0,4,2,3,1]`
  and emits **1 cx** (the win is LAYOUT, not gate cancellation). A `ccx` on a 3-qubit
  line at level 1 → **9 cx** (textbook 6 + routing).
- **`initial_layout` is an ordered virtual→physical map**: `[2,3,4]` gives
  `initial_index_layout() == [2,3,4]`, and `[4,3,2]` gives `[4,3,2]` — it is not a set
  of "allowed" qubits. Pinning a 4-entry layout on a 3-qubit backend still raises.
- **`h.decompose()` → `u`**, which is outside the IBM basis: `decompose()` never
  produces an ISA circuit (a high-yield "decompose ≠ transpile" distractor).
- **`QuantumCircuit.measure`'s keyword is `cbit`, not `clbit`** — and naming the
  arguments does not rescue a circuit with zero classical bits.

## Pool-craft rules (s3 pool wave, 2026-07-25 — 43/44 pooled, 76 new distractors)

- **The `display_count: 4` feasibility test** (4-option question → 6 options, 3 of 5
  distractors displayed): the audit enumerates every 3-subset, so **at most ONE
  existing distractor may be shorter than `len(correct)/1.4`**. With two short ones,
  the subset containing both fires a HIGH `length_tell` no matter what you add
  (s3-q013/q014/q016/q018/q019/q030/q033/q034 hit this). Fix: use `display_count: 5`
  (drop-one variants) and make at least one new distractor ≥ `len(correct)`.
  12 of 43 s3 questions needed dc=5 for this reason; the rest stayed at dc=4.
- **One hedged distractor is NOT enough at dc=4.** With 3 of 5 distractors displayed,
  the variant dropping the lone hedge exposes any absolute-carrying distractor. Rule:
  if a distractor carries an absolute and the correct option carries none, **both**
  new pool distractors must hedge (hit q012, q020, q021, q025, q027, q032, q037,
  q039, q041, q043, q046, q047 — all pre-empted or fixed in one pass).
- **Corollary that saves work:** when the CORRECT option itself carries an absolute
  (very common in "select the true statement" stems), `absolute_distractor_tell` can
  never fire in any variant — skip the hedge engineering entirely.
- **Stem-echo at dc=4:** give EVERY new pool distractor ≥3 stem tokens when the
  correct option has ≥4; the flag fires as soon as the one high-overlap distractor is
  droppable (q013, q015, q017, q027, q049). A pool distractor with MORE stem overlap
  than the correct option is free insurance (q049 E: 6 vs 4).
- **Code-snippet options tokenize:** `measure_all` → {`measure`, `all`}, so an
  innocuous snippet silently becomes the absolute-carrier (q014). `measure_active`
  was the drop-in replacement with the same misconception and no absolute.
- **Exhausted-value predict-output questions** (all bitstrings/levels already used)
  still pool via: a wrong-SHAPE key (`1`, or `2` for the `get_int_counts` confusion),
  a right-outcomes/wrong-weights option ("`11` in roughly a quarter of the shots"),
  or a control-flow error claim. Never a second option with an existing value.
- **Aggregate side-effect of the length rules:** because most pool distractors have to
  be ≥ `len(correct)`, `longest_option` collapsed (s3: 0.257 → 0.070) and
  `avoid_longest` rose (0.252 → 0.283). `avoid_longest`'s ceiling with 4 displayed
  options is 1/3, so it stays under the 0.40 warn line, but a heavily pooled section
  should deliberately keep a few questions correct-longest in ALL variants (only
  s3-q016 here). Position heuristics behaved as s2 predicted: 0.263 → ~0.35 EV
  (0.32 exam-weighted), still under warn.
- **4-of-6 multis cannot pool** (`display_count` must leave ≥2 displayed distractors
  and be < len(options)): s3-q042 skipped — the only s3 question without a pool.
- **Post-pool length calibration is mandatory (s3 lesson):** pooling silently
  drove longest_option from 25.7% to 7.0% because new E/F options out-lengthed
  the keeper questions' correct answers. Rule: on ~N/4 keeper questions the
  correct option must stay strictly longest in EVERY variant — i.e. every pool
  distractor on a keeper must be shorter than the correct option. Check the
  section aggregate AFTER pooling, not just per-question flags. (2026-07-26)

## Verified library facts (s4 pool wave — execution modes, 2026-07-25, runtime 0.48.0)

- **`SamplerV2()` / `EstimatorV2()` with no mode raise `ValueError: A backend or
  session must be specified.` IN THE CONSTRUCTOR**, not at `run()`. The widespread
  "mode defaults to None so construction succeeds, run() fails" lore is wrong for
  0.48 — s4-q021's explanation said exactly that and was corrected (keyed answer
  unaffected: the exception and message are what the option names).
- **`Session.session_id` is `None` in local testing mode.** So
  `EstimatorV2(mode=session.session_id)` degrades to `mode=None`, which inside a
  `with Session(...)` block INHERITS the session and runs fine. Never use
  `mode=session_id` as a wrong option — it is environment-dependent. (Killed one
  s4-q038 draft; replaced by `EstimatorV2(options={"mode": session})`, which raises
  a pydantic `ValidationError` — `mode` is a constructor arg, never an options field.)
- **`Session.backend()` / `Batch.backend()` return the backend NAME string**
  (`'fake_manila'`), so `SamplerV2(mode=batch.backend())` raises `ValueError` — a
  clean, robust pool distractor. `backend.name` and `backend.target` fail the same way.
- **`Session` has no public `run`** (only `_run`): the public surface is
  `backend, cancel, close, details, from_id, service, session_id, status, usage`.
  `session.run(SamplerV2(), [isa])` → `AttributeError`.
- **`QiskitRuntimeService.least_busy` DOES accept `filters=`** (signature:
  `min_num_qubits, instance, filters, use_fractional_gates, **kwargs`) —
  `least_busy(filters=lambda b: not b.simulator)` is a SECOND CORRECT ANSWER on
  "pick the least busy real QPU" stems. `service.backends(...)` is not queue-sorted
  (safe distractor); `service.backend()` needs a positional `name` (TypeError).
- **`save_account` has no `api_key` parameter** (it is `token=`), and
  `QiskitRuntimeService` has no `.save()` method — both verified near-misses.
- **PUB bracketing on `SamplerV2.run`, measured:** `run([[isa1],[isa2]])` and
  `run([(isa1,),(isa2,)])` BOTH SUCCEED (2 pub results) — never offer nested-list or
  tuple-wrapped PUBs as wrong options. `run({isa1, isa2})` → `TypeError: unhashable`;
  `run(pubs, shots=[1024, 1024])` → `TypeError: shots must be an integer`;
  `run([...]).run([...])` → `AttributeError` (a job has no `run`).
- **Fake backends enforce the ISA exactly like hardware** — local testing mode does
  NOT skip the target check, for either primitive. Transpiling a measured circuit
  PRESERVES its `measure` instructions (refutes "pm.run strips measurements").
- **`SparsePauliOp("ZZ", target=...)` → `TypeError`**: the operator has no device
  binding; alignment is `obs.apply_layout(isa.layout)` after transpilation, and
  nothing pads a narrow observable automatically.

## Pool-craft rules (s4 pool wave, 2026-07-25 — 35/36 pooled, 66 new distractors)

- **Keepers-first length calibration (the fix for the s3 collapse).** BEFORE adding
  anything, run the audit and list the questions that already carry a low
  `length_tell` — those are your keepers. s4 had exactly 8 of 32 single-answer
  questions = N/4, so no new keeper had to be manufactured. Then: every pool
  distractor on a keeper must be SHORTER than the correct option and long enough
  that no variant drives the ratio past 1.3; every pool distractor elsewhere must
  leave at least one displayed distractor LONGER than the correct option in EVERY
  variant. Result: `longest_option` finished at exactly 25.0% and `avoid_longest`
  at 23.6% (s3 finished at 7.0%).
- **Put keepers on `display_count: 5`, not 4.** Fewer dropped distractors means the
  max displayed distractor cannot fall as far, so the ratio stays under the 1.4 HIGH
  boundary; it also keeps key A displayed more often (position heuristics) and costs
  nothing on `avoid_longest`, since a keeper contributes 0 to it at any dc.
- **`avoid_longest` arithmetic to plan a wave:** a non-keeper contributes 1/3 at
  dc=4 and 1/4 at dc=5; keepers contribute 0. With N/4 keepers and every non-keeper
  at dc=4 the section lands at ~0.25, and each non-keeper moved to dc=5 costs
  ~0.0026. s4 spent 7 of them and landed at 0.236 — budget ~10 before the 0.20 floor
  gets close.
- **The absolute/hedge fix is far cheaper at dc=5.** At dc=4 (3 of 5 distractors
  shown) BOTH new distractors must hedge whenever a distractor carries an absolute
  and the correct option does not — which pushes that question's `avoid_hedged`
  contribution from 1/3 to 0.5. At dc=5 (drop-one) exactly ONE new distractor needs
  the hedge and the contribution stays ~0.30. Rule: correct option has no absolute
  AND only one existing distractor hedges → use dc=5 and hedge one pool distractor.
  (s3's corollary re-confirmed: a correct option that itself carries an absolute is
  immune — 12 of 36 s4 questions were, and needed no hedge engineering at all.)
- **Never open a pool distractor with the same verdict word as the keyed answer.**
  On "which execution mode?" stems, "Session mode with a short `max_time` …" is a
  fine distractor when the answer is *batch* (the s4-q001 pilot) but an ambiguous
  half-right option when the answer *is* session. Two s4 drafts were rewritten for
  this; check it whenever the correct option is a short label.
- **`attempt(key, fn)` proof harnesses score "it ran" as proven.** A pool distractor
  that runs but produces the wrong *mode* or the wrong *result* will come back as a
  second correct answer and fail verify. Either pick distractors that raise, or add
  an explicit post-condition to the harness. (Caught live on the s4-q038 draft.)
- **`similar_twin_member` climbs when you pool code-construction questions** (s4:
  25% → 38.5%): every near-miss call is a token twin of the correct call. It is not
  gated below 25% coverage and its exam-score estimate stayed at ~26%, so it is an
  accepted residual — check its coverage before spending effort on it.
- **Pooling lowers the section's random-guess baseline** (s4: 25.0% → 22.7%) because
  dc=5 variants display five options. Read every heuristic against the printed
  baseline, not against a hard-coded 25%.
- **A 3-correct multi that already has 6 options (schema cap) can still be pooled by
  rotation alone:** set `display_count: 5` and add nothing (s4-q039). It rotates 2 of
  3 distractors and costs nothing, since multis do not feed the heuristics.
- **More reusable predict-output pool shapes** (value space exhausted): a value on
  the WRONG SIDE of the ideal ("slightly above `+1`" for a noisy ⟨ZZ⟩), and an
  over-specific mechanism ("exactly `+0.5`, because noise halves every two-qubit
  correlation"). Both refute against a single measured number.

## Verified library facts (s5 pool wave — sampler primitive, 2026-07-25, runtime 0.48.0)

- **The full `SamplerOptions` tree** (dataclass fields, so anything else is a
  pydantic `ValidationError`): top level `max_execution_time, environment,
  simulator, default_shots, dynamical_decoupling, execution, twirling,
  experimental`; `execution` = `SamplerExecutionOptionsV2(init_qubits,
  rep_delay, meas_type)` — **no `shots`, no `seed_simulator`**; `simulator` =
  `noise_model, seed_simulator, coupling_map, basis_gates`; `dynamical_decoupling`
  = `enable, sequence_type, extra_slack_distribution, scheduling_method,
  skip_reset_qubits`; `twirling` = `enable_gates, enable_measure,
  num_randomizations, shots_per_randomization, strategy`.
- **`dynamical_decoupling.sequence_type = "XX"` is ACCEPTED and leaves `enable`
  Unset** — a "runs fine, does nothing" refutation (needs a post-condition, not
  an exception). `twirling.shots_per_twirl` and `simulator.seed` are rejected.
- **`sampler.options.update(**kwargs)` exists and works** (`update(default_shots=512)`
  → 512), and plain attribute assignment works too — "SamplerV2.options is
  read-only" is false. The constructor is no escape hatch either:
  `SamplerV2(mode=backend, options={"resilience_level": 1})` →
  `ValidationError: Unexpected keyword argument`. Same for `{"shots": 4096}` and
  a top-level `{"seed_simulator": 42}`.
- **`options.experimental` does not absorb unknown option names** — it is an
  opt-in dict you fill yourself; a misspelled field is rejected outright.
- **`SamplerV2.set_options(...)` does NOT exist** (AttributeError) — clean V1 habit.
  So is `run(circuits=[...])` (TypeError). `run([isa], vals, shots=256)` →
  `TypeError: run() takes 2 positional arguments`; `run([isa], options={...})` →
  TypeError (no `options` kwarg on run); `run([isa], shots=[1024])` →
  `TypeError: shots must be an integer` (confirms the s4 finding at list length 1).
- **`DataBin[0]` → `KeyError: 'Key (0) does not exist in this data bin.'`**;
  `DataBin.get_counts(name)` and `DataBin.registers` → AttributeError. (Item
  access by NAME still works — never a wrong option.)
- **`BitArray.get_bitstrings(0)` on a shape-() BitArray returns a LIST OF ONE
  bitstring** — it does not raise and does not select a qubit column. Never key
  or offer "raises without an index". `BitArray.counts()` (bare) is AttributeError.
- **Broadcast `get_counts()` with NO index pools every parameter set**
  (4 sets x 500 shots → 2000); `get_counts(i)` gives 500. It never raises for a
  missing index — "an index is required once broadcast" is a safe, refuted distractor.
- **Parameter-array shapes, measured:** (6,2)→result (6,); (3,4,2)→(3,4);
  a (5,3) array for 2 parameters → `ValueError: Length of ('p0','p1') inconsistent
  with last dimension`. Transposing, flattening, and splitting into one PUB per
  row all raise the SAME error; `isa.assign_parameters(np.zeros((5,3)))` raises a
  DIFFERENT one (`Mismatching number of values and parameters`) — useful to prove
  "bind first" is not a fix.
- **`decompose()` emits `u` and still fails the target check**;
  `transpile(qc, basis_gates=...)` without a coupling map fails on `cx` between
  NON-ADJACENT qubits — the two error messages differ, which is what proves
  "translation is not routing" independently.
- **A PUB's own shot count beats `options.default_shots`** (50 wins over 1000);
  `len(PrimitiveResult)` is defined and equals the number of PUBs submitted.

## Pool-craft rules (s5 pool wave, 2026-07-25 — 30/30 pooled, 56 new distractors)

- **`shortest_option` is the inverse that s3/s4 missed.** The rule that protects
  `avoid_longest` (new distractors >= len(correct) on non-keepers) drives the
  correct option to be the SHORTEST displayed option. s5 went 27.8% → 38.3%,
  two points under the 0.40 warn line, before it was caught. Fix: on the
  questions where the correct option is already shortest, make exactly ONE pool
  distractor SHORTER than it and keep the other longer — at dc=4 that drops the
  question's shortest EV from 1.00 to 0.40 (the short distractor is displayed in
  6 of 10 subsets). Six such edits took s5 back to exactly 25.0%. Budget: each
  edit buys ~0.022 of section-level `shortest_option`. Audit ALL THREE length
  heuristics after a pool wave, not just longest/avoid_longest.
- **Trimming a pool distractor can strip the hedge that was pre-empting
  `absolute_distractor_tell`** — s5-q021's shortened E lost "typically" and the
  flag came back. Re-run the flag check after every length edit, not just after
  the first draft.
- **Pre-flight the flags in memory.** Import `audit_meta_patterns`, build the
  modified question dicts, and run `question_flags` over `display_variants`
  before writing any file. This caught 5 medium flags (2 stem-echo, 1 format,
  2 hedge/absolute) with zero disk churn or proof re-runs.
- **Stem-echo at dc=4 is a COUNTING rule, not a per-option rule:** the flag fires
  on the 3-subset built from the low-overlap distractors, so raising one new
  distractor's overlap is not enough — keep the number of distractors with
  overlap < 3 at TWO or fewer (hit s5-q021 and s5-q035).
- **`format_tell` has the same shape:** pooling made an all-backticked 3-subset
  reachable on a question whose base set had only one code-formatted distractor
  (s5-q021). When the correct option is prose, keep >= 3 non-code-formatted
  distractors in the pool.
- **Endianness / "which fix" spot-bug questions are the most dangerous to pool.**
  On s5-q032 (`b[0]` reads the wrong end), `b[::-1][0]`, `b[1]` for 2 qubits,
  `qc.reverse_bits()`, swapping the measure mapping, and `BitArray.slice_bits(0)`
  are ALL second correct answers. The safe wrong "fixes" are the ones that change
  nothing observable (a barrier before `measure_all()`, `execution.init_qubits =
  True`) or that read the wrong bit (`(k >> 1) & 1` instead of `k & 1`).
- **New pool evidence must avoid >=3-digit numbers.** `lint_proof_drift` turns on
  its number check as soon as ANY >=3-digit number exists in the corpus — and the
  artifact's own `observed` block counts. Report percentages or small counts
  (`len(kept)` rather than `sum(kept.values())`); 3 would-be findings were removed
  this way on s5-q028/q031. An evidence string like `run(options=...)` also trips
  the kwarg-anchor rule — spell the value out or drop the `=`.
- **A pool distractor can FIX a pre-existing lint finding:** s5-q001's
  known-accepted `'1024'` disappeared because the new option F quotes
  `shots=[1024]`, putting the number into the question corpus.
- **Conceptual questions pool at zero proof cost** (explanation entry only,
  `proof.status` stays `conceptual`): 5 of the 30 s5 questions (q021, q030, q034,
  q037, q038) were pooled this way.
- s5 final: `longest_option` 22.2%, `avoid_longest` 25.2%, `shortest_option` 25.0%,
  positions 28–32% (baseline 23.3%), 0 blockers/warnings, 6 low `length_tell`
  residuals = the 6 deliberate keepers. `similar_twin_member` 40.7% at 22%
  coverage — below the 25% gating floor, accepted residual as in s4.

## Verified library facts (s6 pool wave — estimator primitive, 2026-07-25, qiskit 2.5.0 / runtime 0.48.0)

- **`EstimatorV2.run` accepts a LIST-shaped PUB**: `run([[isa, iobs]])` succeeds
  (coerced exactly like the tuple), and `run(pubs=[...])` is the real keyword —
  never offer either as a wrong option. What DOES fail: `run([(iobs, isa)])`
  (`TypeError: Invalid observable type: QuantumCircuit`), `run({isa: iobs})`
  (`TypeError: unhashable type: QuantumCircuit`), and a dict-shaped PUB
  `run([{"circuit": isa, "observable": iobs}])` (`KeyError: 0` during coercion).
- **`EstimatorV2.run` keyword surface is `precision=` only**: `shots=`,
  `default_precision=`, `resilience_level=` and `backend=` all raise
  `TypeError: unexpected keyword argument`. `options.precision` does not exist
  either (pydantic `no_such_attribute`) — the options field is `default_precision`.
- **`resilience_level` coerces silently**: `2.0`, `"2"` and `True` are ACCEPTED
  (so a string level is a SECOND CORRECT ANSWER — never a distractor); `1.5` and
  `None` raise. `3`, `4`, `5`, `-1` raise the range error (`must be <=2` / `>=0`).
- **`default_precision = 0` raises whatever route you take**: attribute assignment,
  `EstimatorV2(options={"default_precision": 0})` and `EstimatorOptions(default_precision=0)`
  all hit the same `must be >0` validator — "set it in the constructor instead"
  is a clean, refuted distractor. `options.execution` holds only `init_qubits`
  and `rep_delay` (an `ExecutionOptionsV2` `default_precision` is a ValidationError).
- **`ZneOptions` fields are exactly `amplifier, noise_factors, extrapolator,
  extrapolated_noise_factors`** — `zne.factors`, `zne.scale_factors` (the Mitiq
  spelling) and `zne.enable` are all `no_such_attribute`; so is
  `resilience.noise_factors` (right name, wrong nesting level) and a top-level
  `options.zne_mitigation`. `resilience.zne.noise_factors = [1, 3]` is ACCEPTED
  and leaves `zne_mitigation` **Unset** — configuring is not enabling (the s5
  `sequence_type` pattern, now confirmed for the Estimator).
- **`options.resilience.zne_mitigation.enable = True` does NOT raise** — the flag
  is `Unset` (a plain singleton), so the attribute write lands on it and ZNE stays
  off. A "runs fine, does nothing" distractor; it needs a post-condition, never an
  exception. Same shape for `dynamical_decoupling.sequence_type = "XY4"`
  (accepted, `enable` still Unset), while `dynamical_decoupling.enabled` and
  `dynamical_decoupling = True` both raise.
- **PUB precision beats `default_precision`**: a PUB written `(isa, iobs, None, 0.005)`
  under `options.default_precision = 0.05` reports `target_precision` 0.005 — the
  resolution order is PUB > `run()` > options (mirrors the s5 shots finding).
- **Observable broadcasting, measured:** a flat list of 3 observables → `evs.shape
  (3,)`; `[[o1],[o2],[o3]]` → `(3, 1)`; `[[o1, o2, o3]]` → `(1, 3)`. A
  `SparsePauliOp` built from several terms stays ONE observable and returns a
  0-d array — there is no per-term breakdown. `evs` dtype is real `float64`
  even though `SparsePauliOp.coeffs` is complex.
- **`SparsePauliOp` construction near-misses:** `SparsePauliOp("ZZ", num_qubits=5)`
  → `TypeError: unexpected keyword argument` (only `from_sparse_list` takes
  `num_qubits`, and there it is a REQUIRED positional — omitting it is a
  TypeError). `SparsePauliOp(["ZZ","XX"], coeffs=[1.0,0.5,0.25])` → `ValueError:
  operands could not be broadcast`. `from_sparse_list([("Z",[0],1.0)], num_qubits=3)`
  pads to `IIZ` — it never raises and never leaves a bare `Z`.
- **`initial_layout` does not narrow the transpiled circuit**: a preset pass manager
  with `initial_layout=[0, 1]` still emits a 5-qubit ISA circuit on a 5-qubit
  backend, so the observable/circuit width mismatch survives — a good refuted
  "fix" on `apply_layout` spot-bug stems.
- **`PubResult.metadata` carries `target_precision` and `circuit_metadata` only**
  (KeyError for `evs`); `PubResult.values` and `DataBin.expectation_values` are
  AttributeErrors. CAUTION: `DataBin.values` is a bound METHOD and
  `DataBin.values()` returns the arrays — never use it as a wrong option.
- **`StatevectorEstimator` `stds` stays exactly `0.0`** even with
  `run(..., precision=0.01)` (re-confirms the s6/s7 entry): `isnan` is False, so
  both "nan-filled" and "shrinks as precision tightens" are safe refuted options.

## Pool-craft rules (s6 pool wave, 2026-07-25 — 29/30 pooled, 56 new distractors)

- **Manufacture keepers when the section starts short.** s6 had only 5 low
  `length_tell` keepers for 27 single-answer questions (18.5%), and the preflight
  landed `longest_option` at 20.7% — inside the 20–30% band but with no margin.
  Fix: pick TWO non-keepers whose correct option is second-longest (s6-q013,
  s6-q031) and make BOTH pool distractors shorter than the correct option. At
  dc=4 that flips the 4 of 10 variants which drop the one longer distractor into
  correct-strictly-longest, worth ~+0.4 each on `longest_option` (23.3% final).
  The cost is one extra low `length_tell` residual per question, and ~-0.13 each
  on `avoid_longest`. Cheaper and more honest than rewriting a correct option.
- **`shortest_option` can start BELOW chance** (s6 baseline 13.6%) — the s5 rule
  is symmetric: when the aggregate is low, the ordinary "pool distractors >=
  len(correct)" discipline is exactly what fixes it (13.6% → 21.7%), and the
  shortest-correct questions should be LEFT alone rather than compensated.
  Always read the pre-pool aggregate before deciding which direction to push.
- **All-equal-length option sets are longest_option ballast worth 0.25 each.**
  Predict-output label questions (s6-q033 `IZIZ`-style, s6-q035) keep it for free
  if the new options are the same width; prose or shape-flavoured pool distractors
  break it and cost 0.225 apiece. Budget the trade explicitly — s6 spent it on
  q011/q027/q035 for better misconceptions and bought the loss back with the two
  manufactured keepers.
- **Predict-output value spaces exhaust fast; the reliable refills are SHAPE and
  TYPE claims** — `(3, 1)` vs `(1, 3)` vs `(3,)` broadcasting, "a length-1 array",
  "a complex value", "one value per Pauli term", "one row per observable". Each is
  refuted by a single `.shape`/`.dtype` read and none duplicates an existing value.
- **Verify every bracketing before using it.** On the Estimator, `[[circuit, obs]]`
  SUCCEEDS while `[(obs, circuit)]`, `{circuit: obs}` and `[{...}]` fail — the
  s4 Sampler finding generalises: nested-list PUBs are coerced, not rejected.
- **Watch the lint corpus when adding option text, not just evidence.** s6-q020's
  proof evidence contains pydantic `type=no_such_attribute` fragments; they are
  invisible to `lint_proof_drift` only because the word "type" appears nowhere in
  that question's stem/options/explanations. Adding a distractor explanation that
  says "type" would have created five new findings at once.
- **Sign/exponent inversions are the cheapest conceptual pool pair** on any
  scaling question: "it DEcreases by 4x" (direction inverted) and "it increases by
  1.4x" (sqrt instead of square) both refute against the measurement the proof
  already took — no extra execution, no new >=3-digit numbers in the evidence.
- **4-of-6 multis still cannot pool** (s6-q028, the section's only skip) — the
  third instance of this constraint after s3-q042 and the s4 note.
- s6 final: `longest_option` 23.3%, `avoid_longest` 26.0%, `shortest_option` 21.7%,
  positions 30.0–33.3% (baseline 25.0%, answer keys 7/7/7/6), 0 blockers/warnings,
  7 low `length_tell` residuals (5 inherited keepers + 2 manufactured), lint
  findings unchanged from the pre-pool baseline (4, all pre-existing).
  `similar_twin_member` 40.0% at 59% coverage → 33.9% exam estimate, accepted
  residual as in s4/s5.

## Verified library facts (s7 pool wave — results retrieval/analysis, 2026-07-25, qiskit 2.5.0 / runtime 0.48.0)

- **`json.dumps` / `json.loads` are keyword-only after the first argument**:
  `json.dumps(result, f, cls=RuntimeEncoder)` raises `TypeError: dumps() takes 1
  positional argument but 2 positional arguments (and 1 keyword-only argument)
  were given`. The dump/dumps near-miss is therefore a clean, cheap distractor
  on every serialization stem. Encoding with `RuntimeEncoder` but loading with a
  plain `json.load` "succeeds" and hands back nested dicts — indexing the pub
  then fails with `KeyError: 0` (a two-stage refutation, not an exception at the
  call site).
- **`BitArray.postselect` has no `num_bits=` parameter** (`TypeError: ...
  unexpected keyword argument 'num_bits'`) — width preservation is automatic.
  `postselect(...).slice_bits([i])` is the safe "right call, ruined follow-up"
  distractor: it drops `num_bits` to 1 while keeping the correct shot set.
- **`BitArray.from_counts(a.get_counts() | b.get_counts())` SUCCEEDS** and returns
  a real BitArray — with the wrong shot total, because dict `|` overwrites
  duplicate outcome keys instead of summing them. Needs a post-condition
  (`num_shots == a+b`), never an exception. `np.concatenate([a.array, b.array])`
  also succeeds and returns a bare `ndarray` (no `num_bits`, no BitArray methods).
- **`BitArray.array` is bit-PACKED `uint8`**, `shape[1] == ceil(num_bits/8)` — a
  3-bit register gives `shape[1] == 1`, and dtype is never `bool`. The transposed
  shape and a fixed 8-column width are both safe refuted claims.
- **`bits.slice_bits([2])` on a 3-bit register does NOT raise** — indices run
  `0..num_bits-1`, so "IndexError, index out of range" is a safe refuted option
  (proved by calling it and catching nothing).
- **`DataBin` has no `get_counts()`, no `get_bitstrings()`, and its fields are not
  callable** (`TypeError: 'BitArray' object is not callable`). `PubResult` has no
  `get_counts()` either; `PrimitiveResult` has neither `.results` (the V1 list) nor
  a register attribute. Four independent AttributeError distractors, all verified.
  Re-confirmed: `db["name"]` WORKS and must never be a wrong option.
- **`DataBin.values()` returns the stored BitArrays** — so `list(db.values())` is a
  refuted "list the register names" option, but do NOT test it with
  `"ans" in list(db.values())`: `BitArray.__eq__` against a `str` raises
  `AttributeError: 'str' object has no attribute 'num_bits'`, which makes the
  evidence read like the option's own expression crashed. Use
  `any(isinstance(v, str) and v == name for v in ...)`.
- **`BitArray` does not carry its register name** (`AttributeError: 'BitArray'
  object has no attribute 'name'`) — the name exists only as the DataBin field.
- **`PubResult.metadata["evs"]` → `KeyError: 'evs'`** and `DataBin.expvals` →
  `AttributeError` (re-confirms the s6 metadata finding from the retrieval side).
  The estimator DataBin also has no `variance` field.
- **The achieved standard error is NOT `1/sqrt(shots)`**: on a noisy Bell/ZZ pub,
  `shots ** -0.5` returns 0.02 while `pub.data.stds` and the independent
  prediction `sqrt((1 - evs^2)/shots)` both give 0.0096 — a factor of 2 apart, so
  the "shot noise is 1/sqrt(N)" distractor refutes cleanly at a 10% tolerance.
- **`BitArray.expectation_values("ZZ")` returns a 0-d scalar** (ndim 0), one value
  per Pauli string — never a per-bit vector, and it exists (an "AttributeError,
  you need an Estimator" claim is safe and refuted).
- Re-confirmed for pooling: `StatevectorEstimator` evs on a Bell/ZZ pub is a 0-d
  array, so "a length-one 1-D array" is a safe shape distractor; `evs` for a
  `(4, 1)` parameter array is `(4,)`, so `(1, 4)` (observable axis first) is safe.

## Pool-craft rules (s7 pool wave, 2026-07-25 — 23/24 pooled, 44 new distractors)

- **Read the pre-pool `shortest_option` FIRST; s7 started at 10.3%**, the lowest of
  any section. That is the s6 situation amplified: the ordinary discipline (pool
  distractors LONGER than the correct option on every non-keeper) is exactly the
  fix, and it took s7 to 25.0% with no compensating edits at all. The s5
  shortest-option rule (add a SHORTER pool distractor) is only for sections that
  START above ~30% — applying it here would have been backwards.
- **`shortest_option` arithmetic for planning:** at dc=4 (3 of 5 distractors shown),
  a question with exactly `s` existing distractors shorter than the correct option
  contributes `C(5-s, 3)/10` once both new distractors are longer — 1.0 for s=0,
  0.4 for s=1, 0.1 for s=2, 0 for s>=3. Sort the section by `s` before drafting:
  the s=1 questions are where the aggregate is actually bought.
- **Keeper count came out at exactly N/4 for free.** 4 questions carried a low
  `length_tell` pre-wave; the 5th keeper was *manufactured for free* on s7-q023,
  whose correct option TIED with one distractor (72 vs 72). Making both pool
  distractors shorter than the correct option turns the 4-of-10 variants that drop
  the tying distractor into correct-strictly-longest: the question goes 0.5 -> 0.7
  on `longest_option` at zero content cost. **Look for tied-longest questions
  before manufacturing a keeper the expensive way (s6's second-longest trick).**
- **All-equal-length option sets are worth keeping when the template allows it**
  (s7-q011: every option is `` `num_shots=X`, `num_bits=Y` `` = 25 + len(X) +
  len(Y) chars, so two more 30-char options were free ballast at 0.25 longest AND
  0.25 shortest). When only ONE same-width option can be found (s7-q014), pairing
  it with a deliberately SHORTER second distractor gives 0.30/0.10 instead of the
  0.10/0.30 you get from pairing it with a longer one — pick the direction the
  section aggregate needs.
- **Stem-echo at dc=5 is a one-variant problem.** Only the single variant that drops
  the highest-overlap distractor can fire, so exactly one pool distractor needs
  overlap >= ceil(ans_ov/2) (hit s7-q015: correct overlap 4, best remaining 2).
  Reusing the correct option's own sentence frame ("Only the `111` shots survive,
  narrowed to ...") is the cheapest way to buy the tokens and it doubles as a
  strong half-right distractor.
- **A pool distractor's evidence must not report >=3-digit numbers the question
  never shows** — but note the escape hatch: numbers already in the artifact's
  `observed` block are corpus, and any number you put in the NEW OPTION TEXT
  becomes corpus too (s7-q011's `6000`/`1024` options made their own evidence
  legal). Where that is not possible, write the post-condition in prose
  ("holds a shot total below `a.num_shots + b.num_shots`") — s7-q018's E would
  otherwise have cloned the section's existing `num_shots=200` finding onto a
  second option.
- **Same trap for kwarg anchors:** `dtype=uint8` in new evidence is a finding as
  soon as the word `dtype` enters the corpus via your new option — pre-empt it by
  naming the real value (`uint8`) in the distractor's explanation (s7-q019).
- **Ledger facts pay off directly as *rejected* drafts:** `result[0].data["readout"]`
  (item access works), `next(iter(result))` (PrimitiveResult is iterable),
  `bits.get_int_counts()` key-set duplicates, `pickle` round-trips and
  `DataBin.values` were all discarded as second-correct-answers before drafting.
  On predict-output questions that compare KEY SETS, a "keys are reversed" option
  is a proven-correct trap — the set is identical.
- s7 final: `longest_option` 25.0%, `shortest_option` 25.0%, `avoid_longest` 24.0%
  (baseline 24.1%), positions 30.2–35.2% exam-weighted, 0 blockers/warnings, 5 low
  `length_tell` residuals = the 5 deliberate keepers, lint findings unchanged from
  the pre-wave baseline (3, all pre-existing). `similar_twin_member` 40.7% at 64%
  coverage -> 34.8% exam estimate, accepted residual as in s4/s5/s6.
  `numeric_middle` rose 25.0% -> 44.6% at 18% coverage (below the 25% gating floor,
  not scored): it is a tokenizer artifact — `result[0]`-style options all parse as
  the single number 0, so "never the biggest or smallest" degenerates. Do not
  distort real API paths to chase it.
- **4-correct multis at the 6-option cap still cannot pool** (s7-q030, the section's
  only skip; `display_count` would need to be >= 6 to leave 2 displayed distractors
  yet must be < len(options)). Fourth instance after s3-q042, s4's note and s6-q028.

## Verified library facts (s8 pool wave — OpenQASM, 2026-07-25, qiskit 2.5.0)

- **`qasm3.dumps` forwards its kwargs to the `Exporter` constructor**, so any
  unknown one raises `TypeError: Exporter.__init__() got an unexpected keyword
  argument '...'` (verified with `file=`). It never writes to a stream.
- **`qasm3.dump(circuit, stream)` calls `.write` on its second argument**: a
  path string raises `AttributeError: 'str' object has no attribute 'write'`.
  Signature is `(circuit, stream, **kwargs)`. The mirror-image trap is
  **`qasm2.load(filename)`**, which calls `os.fspath` — an open `StringIO`
  raises `TypeError: argument should be a str or an os.PathLike object ...`.
  So in this family exactly one call takes a path and one takes a stream; both
  near-misses are clean, cheap distractors.
- **`qasm3.loads` on OpenQASM *2* text raises `MissingOptionalLibraryError`
  before it parses anything** (the optional-dependency guard runs first). That
  makes "one loader handles both versions" refutable without the extra package
  installed and without a meta-path block — a plain `try/except` in an
  `attempt()` harness is sufficient handling. It also means
  **`QASM3ImporterError` is a safe distractor exception**: that error only
  exists once `qiskit-qasm3-import` IS installed.
- **`QuantumCircuit.qasm()` is gone in 2.5** (`AttributeError`) — removed in
  1.0 in favour of the `qasm2`/`qasm3` modules. Companion to the ledger's
  `from_qasm_str`/`from_qasm_file` entry (those two still exist).
- **`qasm2.dump` and `qasm2.dumps` share one exporter and one set of language
  limits**: `qasm2.dump(qc_with_if_test, stream)` raises the same
  `QASM2ExportError: 'OpenQASM 2 only supports register-equality conditions'`.
  "Write to a file instead" is never a fix.
- **DANGER on that same question:** because the limit is *register*-equality,
  rewriting the condition as `if_test((qc.cregs[0], 1))` genuinely EXPORTS —
  it is a SECOND CORRECT ANSWER on "make the OpenQASM 2 export succeed" stems.
  Rejected as a pool draft; never offer it.
- **`qasm2.dumps` on a circuit with a non-zero `global_phase` emits no phase at
  all** — the text is exactly `OPENQASM 2.0; include "qelib1.inc"; qreg q[1];
  h q[0];`, with no `gphase` and no `u(...)` rewrite, and **re-importing that
  text raises nothing**. Both "the phase is folded into the gate" and "the
  re-import chokes on a `gphase` line" refute against a single emitted string.
- **The qasm3 exporter preserves the custom gate's NAME and mangles only its
  parameters**: the emitted declaration is `gate mygate _gate_q_0 { rz(0.5)
  _gate_q_0; h _gate_q_0; }`. So "the declaration is emitted under a mangled
  name" is a safe refuted option. `opaque` never appears in v3 output (it is
  an OpenQASM 2 device) — a second safe option on the same stem.
- **`qasm3.dumps` output for `QuantumCircuit(2, 3)` is exactly**
  `OPENQASM 3.0;` / `include "stdgates.inc";` / `bit[3] c;` / `qubit[2] q;` /
  `h q[0];` — classical register first, width on the type, no `creg`/`qreg`.

## Pool-craft rules (s8 pool wave, 2026-07-25 — 15/16 pooled, 29 new distractors)

- **s8 started perfectly balanced (longest 26.8%, shortest 26.8%,
  avoid_longest 24.4%), which is the hardest starting point to pool**: the s7
  discipline (all new distractors longer than the correct option) would have
  driven `shortest_option` to ~39%. When a section starts INSIDE the band, the
  wave must be planned as arithmetic, not as a rule: budget every question's
  post-pool contribution before drafting. Sorting by `s` (existing distractors
  shorter than the correct option) and using the s7 table
  (`C(5-s,3)/10` = 1.0/0.4/0.1/0 for s=0/1/2/>=3) predicted the finish to
  within 0.5 points on all three heuristics.
- **The mixed pair is the tool the earlier waves lacked.** On a question whose
  correct option is currently TIED-longest, adding one distractor LONGER and
  one SHORTER lands `longest_option` at exactly 0.25 for that question (s8-q010:
  0.5 tied -> 0.25), versus 0.7 for two-shorter (s7's keeper trick) or 0 for
  two-longer. Three settings from one question — use it to trim the aggregate
  instead of rewriting content.
- **On correct-is-shortest questions (s=0), one shorter + one longer takes the
  question from 1.00 to 0.40 on `shortest_option`** (the s5 rule, re-derived).
  Three such edits (q015/q017/q019) were exactly what kept s8 from overshooting;
  each buys ~0.043 of section-level `shortest_option` at 14 single-answer
  questions.
- **A section with ZERO hedge words and near-zero absolutes is a trap in the
  other direction.** s8's `most_hedged`/`avoid_hedged` coverage was 0.0 — which
  means any single hedge or absolute word added to a pool distractor turns a
  dormant heuristic on. `absolute_distractor_tell` fires the moment a distractor
  carries an absolute while the correct option does not and nothing hedges, so
  in such sections the cheapest policy is to draft every pool distractor
  absolute-free and hedge-free. Two drafts were reworded for a stray "only".
  (The s3 corollary still applies where it can: q017 and q021 have absolutes in
  the correct option and were immune.)
- **Explanations are NOT scanned by `question_flags`** (it reads option texts
  only) — absolutes and hedges in the distractor explanations are free. Worth
  knowing before contorting explanatory prose.
- **Pooling a 5-option multi:** `display_count: 4` on a 2-correct/4-distractor
  multi exposes 2-distractor variants, which re-opened both `stem_echo_tell`
  and `format_tell` on s8-q025 (the variant that dropped the one backticked
  distractor left the correct options as the only code-formatted ones).
  `display_count: 5` (drop-one) cleared both. Rule: **prefer dc=5 on multis** —
  their variants have far fewer distractors to hide a tell behind, and multis
  contribute nothing to the length aggregates anyway.
- **Verbatim-output pool distractors are the cheapest of all**: on
  predict-output questions whose proof compares an emitted string or line to a
  candidate dict, a new option costs one dict entry and the harness writes its
  own ATTEMPTED/REFUTED evidence (q010, q014, q016, q020). Match the option's
  character count to the section's needs by choosing WHICH line to corrupt —
  swapping `bit[1] c;`/`qubit[1] q;` for `qreg`/`creg` plus an arrow measure
  runs +1 char, swapping `stdgates.inc` for `qelib1.inc` runs -2.
- **`str(exception)` is often already quoted.** A `msg.startswith("<input>:1,")`
  check on a `QASM2ParseError` returns False because `str(e)` is
  `'<input>:1,9: ...'` INCLUDING the quotes — the evidence then reads
  "reported on line one=False" and describes reality backwards. Use `in`, not
  `startswith`, on exception text, and read the rendered evidence for every new
  key before declaring the batch done (caught live on s8-q015).
- **3-correct multis at the 6-option cap pool by rotation only** (s8-q022,
  `display_count: 5`) — fifth instance of the cap constraint after s3-q042,
  s4-q039, s6-q028 and s7-q030.
- s8 final: `longest_option` 25.0%, `shortest_option` 24.3%, `avoid_longest`
  25.8% (baseline 23.9%), positions 27.9–34.7% exam-weighted (keys 4/4/3/3),
  0 blockers/warnings, 4 low `length_tell` residuals (3 inherited keepers +
  s8-q010's one-variant mixed pair), lint findings unchanged from the pre-wave
  baseline (0). `similar_twin_member` 42.0% at 49% coverage -> 32.9% exam
  estimate, accepted residual as in s4/s5/s6/s7.

## Verified library facts (s1 quick-study wave, 2026-07-26, qiskit 2.5.0)

- **`Pauli.compose` vs `Pauli.dot` is visible in the phase prefix:**
  `Pauli('X').dot(Pauli('Y')).to_label()` is `'iZ'`, but
  `Pauli('X').compose(Pauli('Y')).to_label()` is `'-iZ'` (compose = B·A). The
  compose/dot distinction is not Operator-only — it changes the *label* on
  Paulis, which makes it a sharp predict-output item.
- **`Pauli('X').expand(Pauli('Y')).to_label()` = `'YX'`** — expand is b ⊗ a,
  the exact mirror of tensor (docs: `A.expand(B)` = B ⊗ A, A on subsystem 0).
- **Exact-equality gate identities (`Operator.__eq__`, not just `equiv`):**
  `SGate == PhaseGate(pi/2)` True; `TGate.dot(TGate) == SGate` True;
  `SGate.dot(SGate) == ZGate` True; `PhaseGate(pi) == ZGate` True.
  `SGate == RZGate(pi/2)` is **False** but `.equiv` is True (RZ splits the
  phase symmetrically); same shape for `TGate` vs `RZGate(pi/4)`.
  `SdgGate == SGate.adjoint()` True.
- **Docs wording confirmed by fetch (guides/operator-class):** `A.compose(B)`
  returns the operator with matrix B·A, `A.compose(B, front=True)` gives A·B,
  `A.tensor(B)` indexes B on subsystem 0, `Operator.__eq__` is elementwise
  *approximate* equality and is False for a global-phase difference.
- **Docs wording confirmed by fetch (guides/operators-overview):** `Pauli`
  labels take an optional phase prefix from `''`/`'i'`/`'-'`/`'-i'`
  (`Pauli('iXX').phase == 3`); `SparsePauliOp.from_sparse_list([("ZX", [1, 4],
  1.0)], num_qubits=5)` prints as `XIIZI` — the label chars pair with the index
  list left-to-right and the *display* stays little-endian.
- API page `api/qiskit/qiskit.circuit.library.SGate` is live (200, slug match)
  and states S = sqrt(Z) = diag(1, i), a pi/2 Z-rotation — safe citation for
  the S/T/P/RZ relationship family.

## Verified library facts (s2/s3 quick-study wave, 2026-07-26, qiskit 2.5.0)

- **Multi-register counts keys are space-separated with the LAST-declared
  register leftmost:** registers `a` then `b`, with q0 -> a[0] = 1, gives
  `{'0 1': …}`. `QuantumCircuit(2, 2).measure_all()` gives `cregs=['c','meas']`
  and keys like `'01 00'` — the appended `meas` group prints leftmost. Anything
  keyed on a single flat bitstring after `measure_all` on a circuit that already
  has clbits is wrong.
- **`style={...}` really is inert in the text renderer** (re-confirmed):
  `draw("text", style={"initial_state": True})` produces no `|0>` labels while
  `draw("text", initial_state=True)` does.
- **`Statevector.draw`'s valid option list, verbatim from its `ValueError`:**
  `'text', 'latex', 'latex_source', 'qsphere', 'hinton', 'bloch', 'city'` or
  `'paulivec'` — the authoritative set for state-drawer questions.
- **`ParameterVector` elements sort NUMERICALLY by index inside `qc.parameters`**
  (`x[9]`, `x[10]`, `x[11]`), whereas two plain `Parameter('x10')`/`Parameter('x2')`
  sort as strings (`x10` first). "Alphabetical by name" is true for plain
  Parameters only; do not key a vector question on string ordering.
- **`transpile()`'s signature default is `optimization_level=None`** and resolves
  to level 2 (functional check: no-argument transpile output == explicit level 2
  on GenericBackendV2(5)); `generate_preset_pass_manager`'s signature default is
  the literal `2`. Confirms the earlier s3 ledger entry from the other direction.
- **`QuantumCircuit.compose(other, front=True)` prepends** (`['h','x']` vs the
  default `['x','h']`); `append` mutates in place and returns an `InstructionSet`.
  compose/append is the functional-vs-mutating pair worth teaching together.
- **`measure_active()` names its register `meas` and sizes it to the ACTIVE
  qubits only** (3-qubit circuit with one gate -> 1 clbit) — differs from
  `measure_all()`, which is always full width.
- **Docs-vs-library drift, noted not resolved:** `guides/transpiler-stages` and
  `guides/set-optimization` both describe `optimization_level` as a *required
  positional* argument of `generate_preset_pass_manager`, while the 2.5 signature
  carries the default 2. Questions must key the library; explanations may flag
  the docs wording.
- **Proof-status hygiene for study files:** facts must never cite a
  `proof.status == "conceptual"` question with a `{"type":"proof"}` source —
  `build_study.py` only checks that the qid exists, so the cram page would render
  a false ⚙️ "executed" badge. s3-q027/q036/q038/q044/q048 and s2-q018 are the
  conceptual ones in these two sections; cite the guide instead.

## Verified library facts (s4/s5 quick-study wave, 2026-07-26, runtime 0.48.0)

- **`SamplerV2.run`'s signature is `run(self, pubs, *, shots=None) -> RuntimeJobV2`**
  — `shots` is KEYWORD-ONLY, which is why `run([isa], vals, shots=256)` fails with
  "takes 2 positional arguments". Confirms the s5 pool-wave entry from the
  signature side.
- **`SamplerOptions.__dataclass_fields__` (0.48), verbatim order:** `_VERSION,
  max_execution_time, environment, simulator, default_shots,
  dynamical_decoupling, execution, twirling, experimental`. Matches the s5 pool
  wave; `_VERSION` is the only field not documented in guides/sampler-options.
- **A no-mode primitive constructed inside `with Session(...)` really does inherit
  the session** (`SamplerV2().mode is session` -> True, and the run succeeds
  locally). The `ValueError: A backend or session must be specified.` from the s4
  wave fires only when there is no enclosing context.
- **`Session` and `Batch` expose the SAME public surface** in 0.48:
  `backend, cancel, close, details, from_id, service, session_id, status, usage`.
  Neither has a public `run`.
- **Locally: `session.details()` and `session.session_id` are both `None`** while
  `session.backend()` returns `'fake_manila'` (a str). Re-confirmed.
- **`StatevectorSampler` runs an ABSTRACT (never transpiled) `measure_all` circuit
  and defaults to 1024 shots** — same number as the fake-backend local fallback,
  vs the Runtime service's 4096. Useful as the reference-vs-runtime contrast:
  guides/simulate-with-qiskit-sdk-primitives states in words that the reference
  primitives still accept abstract instructions.
- **Broadcast BitArray accounting, measured:** a (4,) BitArray from
  `run([(isa, vals)], shots=500)` reports `num_shots == 500` (per parameter set)
  while `sum(get_counts().values()) == 2000` (pooled). Both numbers are true at
  once — do not treat `num_shots` as the pooled total.
- **`QiskitRuntimeService.least_busy` signature (0.48):** `(min_num_qubits,
  instance, filters, use_fractional_gates, **kwargs)`; `save_account` has
  `token, url, instance, channel, filename, name, proxies, verify, overwrite,
  set_as_default, private_endpoint, region, plans_preference, tags` — no
  `api_key`. Re-confirmed from the s4 pool wave.

## Documentation link facts (s4/s5 quick-study wave, 2026-07-26)

- Live and slug-stable (curl -L, final 200, slug match): `guides/execution-modes`,
  `guides/choose-execution-mode`, `guides/execution-modes-faq`,
  `guides/run-jobs-session`, `guides/run-jobs-batch`, `guides/max-execution-time`,
  `guides/minimize-time`, `guides/cloud-setup`, `guides/save-credentials`,
  `guides/initialize-account`, `guides/local-testing-mode`, `guides/transpile`,
  `guides/hello-world`, `guides/instances`, `guides/qpu-information`,
  `guides/save-jobs`, `guides/sampler-noise-management`,
  `guides/simulate-with-qiskit-sdk-primitives`, `guides/qiskit-runtime-primitives`,
  `guides/v2-primitives`, `guides/estimate-job-run-time`,
  `api/qiskit-ibm-runtime/sampler-v2`,
  `api/qiskit-ibm-runtime/options-sampler-options`,
  `api/qiskit/qiskit.primitives.StatevectorSampler`,
  `api/qiskit/qiskit.primitives.BitArray`,
  `tutorials/multi-product-formula`. `guides/fair-share-queue` is a 404 — there is
  no fair-share slug; queue/TTL semantics live in execution-modes +
  max-execution-time.
- **Doc statements confirmed by fetch, safe to cite:** execution-modes (batch jobs
  not guaranteed in submission order, no exclusive access, calibration jobs may
  interleave; queuing time does not decrease for the FIRST job of a batch/session;
  session = exclusive window, no calibration jobs); choose-execution-mode (batch
  unless inputs are not ready at the outset, session for iterative/dedicated,
  ALWAYS job mode for a single primitive request, sessions generally more
  expensive); max-execution-time (max TTL starts at first job, running jobs
  continue, queued jobs fail; service job timeout capped at 3 h; Open Plan 10 min
  QPU per 28-day window); run-jobs-batch (interactive TTL 1 min, not configurable;
  default max TTL 8 h paid / 10 min Open); run-jobs-session (Open Plan cannot
  submit session jobs; close -> "In progress, not accepting new jobs");
  initialize-account (default channel `ibm_quantum_platform`; multiple saved
  accounts with no default -> LAST alphabetically; `channel="local"` needs no
  credentials); save-credentials (`token=`, `$HOME/.qiskit/qiskit-ibm.json`);
  sampler-options (four-step shots precedence: PUB > run(shots=) > twirling
  num_randomizations x shots_per_randomization > default_shots).
- **Docs-vs-docs drift, noted not resolved:** guides/sampler-options lists
  `twirling.enable_measure` **Default: False**, while the same page's shots
  precedence says "if `twirling` is enabled (True by default)" and the
  run-jobs-session/batch sample output shows `'enable_measure': True`. Do not key
  anything on the Sampler twirling default; teach the precedence chain instead.
- **guides/local-testing-mode claims "all options except shots are ignored when
  run on a local simulator"** — but `options.simulator.seed_simulator` demonstrably
  changes results on a fake backend (s5-q031). Treat that sentence as scoped to
  bare Aer simulators; never cite it for fake-backend behaviour.

## Study-wave craft rules (s4/s5, 2026-07-26)

- **A section with few objectives needs MULTIPLE primers per objective.** s4 has
  only two objectives but four scope areas, so s4o2 carries two primers (ISA/PUB
  workflow; credentials + local testing). `build_study.py` renders every primer
  under its objective heading, so this costs nothing and keeps each primer inside
  the 300-600 word band.
- **Cross-section proof citations are forbidden in practice**, even though the
  build gate would accept them: `render_fact` links `⚙️ proven in [qid]` to
  `/docs/sections/<the study file's section>`, so citing `s5-q033` from `s4.json`
  would render a link to a question that is not on that page. Keep proof refs
  inside the section.

## Verified library facts (s6/s7 quick-study wave, 2026-07-26, qiskit 2.5.0 / runtime 0.48.0)

- **`pec_mitigation` and `zne_mitigation` cannot be enabled together**: setting
  both raises `ValidationError: 'pec_mitigation' and 'zne_mitigation' options
  cannot be simultaneously enabled. Set one of them to False.` This matches the
  docs' feature-compatibility table (PEC incompatible with gate-folding ZNE and
  with PEA). NEW finding — a clean "both flags on" refutation.
- **`EstimatorOptions.__dataclass_fields__` (0.48), verbatim order:** `_VERSION,
  max_execution_time, environment, simulator, default_precision, default_shots,
  resilience_level, seed_estimator, dynamical_decoupling, resilience, execution,
  twirling, experimental`. `resilience` fields: `measure_mitigation,
  measure_noise_learning, zne_mitigation, zne, pec_mitigation, pec,
  layer_noise_learning, layer_noise_model`. `pec` fields: `max_overhead,
  noise_gain`. `twirling` fields: `enable_gates, enable_measure,
  num_randomizations, shots_per_randomization, strategy`.
- **`EstimatorV2.run` signature is `run(self, pubs, *, precision=None)`** —
  `precision` is KEYWORD-ONLY (confirms the s6 pool-wave finding from the
  signature side). `EstimatorOptions().default_precision` and
  `.resilience_level` are both `Unset` in the library; the documented values
  (0.015625 and 1) are SERVER defaults, not dataclass defaults — never key a
  question on `EstimatorOptions().resilience_level == 1`.
- **`zne.amplifier` is enum-validated:** `"pea"` is accepted, `"richardson"` is a
  `ValidationError`. Documented choices are `gate_folding`,
  `gate_folding_front`, `gate_folding_back`, `pea` (default `gate_folding`).
- **`SparsePauliOp.apply_layout(None)` is a no-op** (returns the operator
  unchanged, `'ZZ'` stays `'ZZ'`) — it does NOT raise, so "pass None" is a
  silent-failure distractor, never an exception one.
- **Estimator broadcasting re-measured (StatevectorEstimator):** flat list of 3
  observables → `(3,)`; `[[o1],[o2],[o3]]` → `(3, 1)`; `[[o1,o2,o3]]` → `(1, 3)`;
  a single op → `()`. A 2-term `SparsePauliOp` returns a 0-d `float64` holding
  the weighted sum. `PubResult.metadata` keys are `target_precision` +
  `circuit_metadata` (Estimator) and `shots` + `circuit_metadata` (Sampler);
  `PrimitiveResult.metadata` is `{'version': 2}`.
- **`BitArray` public surface (2.5), full list:** `array, bitcount, concatenate,
  concatenate_bits, concatenate_shots, expectation_values, from_bool_array,
  from_counts, from_samples, get_bitstrings, get_counts, get_int_counts, ndim,
  num_bits, num_shots, postselect, reshape, shape, size, slice_bits,
  slice_shots, to_bool_array, transpose`. Measured: `concatenate_shots` doubles
  `num_shots` at constant `num_bits`; `concatenate_bits` doubles `num_bits` at
  constant `num_shots`; `slice_shots(range(5)).num_shots == 5`.
- **`RuntimeJobV2` public surface (0.48):** `ERROR, JOB_FINAL_STATES, backend,
  cancel, cancelled, creation_date, done, error_message, errored, image,
  in_final_state, inputs, instance, job_id, logs, metrics, primitive_id,
  private, properties, result, running, session_id, status, tags, update_tags,
  usage, usage_estimation, wait_for_final_state`. `JOB_FINAL_STATES ==
  ('DONE','CANCELLED','ERROR')`; `done()` is literally `status() == "DONE"` and
  `cancel()` sets `_status = "CANCELLED"` — the string-status entry is confirmed
  from the source side.
- **`QiskitRuntimeService.jobs` signature (0.48):** `(limit=10, skip=0,
  backend_name, pending, program_id, instance, job_tags, session_id,
  created_after, created_before, descending=True)`; `job` is `(job_id) ->
  RuntimeJobV2`.
- **RuntimeEncoder/Decoder round trip re-confirmed end to end:**
  `json.loads(json.dumps(res, cls=RuntimeEncoder), cls=RuntimeDecoder)` returns a
  real `PrimitiveResult` with identical counts; loading the same string with a
  PLAIN `json.loads` returns a `dict` whose `[0]` is `KeyError: 0`; no encoder at
  all is `TypeError: Object of type PrimitiveResult is not JSON serializable`.

## Documentation link facts (s6/s7 quick-study wave, 2026-07-26)

- Live and slug-stable (curl -L, final 200, slug match):
  `guides/estimator-options`, `guides/estimator-noise-management`,
  `guides/error-mitigation-and-suppression-techniques`,
  `guides/runtime-options-overview`, `guides/get-started-with-estimator`,
  `guides/specify-observables-pauli`, `guides/primitive-input-output`,
  `guides/save-jobs`, `guides/monitor-job`,
  `api/qiskit-ibm-runtime/runtime-job-v2`, `api/qiskit-ibm-runtime/session`,
  `api/qiskit-ibm-runtime/options-estimator-options`,
  `api/qiskit-ibm-runtime/options-zne-options`,
  `api/qiskit-ibm-runtime/estimator-v2`,
  `api/qiskit/qiskit.quantum_info.SparsePauliOp`,
  `api/qiskit/qiskit.primitives.BitArray`,
  `api/qiskit/qiskit.primitives.DataBin`,
  `api/qiskit/qiskit.primitives.PrimitiveResult`, `api/qiskit/primitives`.
- **Doc statements confirmed by fetch, safe to cite:** estimator-noise-management
  (resilience table 0 = none / 1 = [Default] TREX + measurement twirling / 2 =
  "Level 1 + Zero Noise Extrapolation (ZNE) and gate twirling"; the Important
  callout that manual options apply *in addition to* the level's base set, with
  level 0 turning `zne_mitigation` off but an explicit `True` overriding it);
  error-mitigation-and-suppression-techniques (ZNE = digital gate folding +
  extrapolation, "not guaranteed to produce an unbiased result", default 3 noise
  factors ≈ 3x overhead; PEC unbiased, overhead quadratic in γ = Σ|η_i| which is
  exponential in depth, `pec.max_overhead` default 100; TREX = twirled
  measurement + inverted diagonal readout matrix, enabled by `measure_mitigation`;
  DD pulses idle qubits, default sequence "XX"; PEA needs `zne_mitigation = True`
  plus `zne.amplifier = "pea"`); estimator-options (five-step precision
  precedence PUB > run(precision=) > num_randomizations × shots_per_randomization
  > default_shots > default_precision; `default_precision` default 0.015625 =
  1/sqrt(4096); `resilience_level` choices 0/1/2 default 1;
  `resilience.measure_mitigation` default True, `zne_mitigation`/`pec_mitigation`
  default False; `zne.noise_factors` default (1,3,5) — (1,1.5,2) for PEA;
  `twirling.enable_gates` False / `enable_measure` True;
  `max_execution_time` default 10800; run() takes only `precision`; feature
  compatibility table); primitive-input-output (Estimator PUB is at most FOUR
  values, one ev per broadcast element, `SparsePauliOp` counts as ONE element
  regardless of term count, commuting observables must share a PUB to share a
  measurement, Sampler DataBin holds one BitArray per ClassicalRegister with
  `meas` the default name, BitArray stores shots as bytes with shots on the left
  axis); specify-observables-pauli (only I/Z Paulis are diagonal; X → HXH and
  Y → HS†YSH basis changes are performed automatically by the Estimator);
  save-jobs ("IBM Quantum automatically stores results from every job"; the
  literal `j.status() == "DONE"` comparison; `service.jobs(created_after=...)`
  with a datetime; RuntimeEncoder/RuntimeDecoder round trip); monitor-job
  (`job.result()` is "a blocking call until the job completes", `job.job_id()`,
  `job.status()`, `service.job(<job_id>)`, "use `job.cancel()` to cancel a job",
  `service.jobs()` default `limit` 10 and its deprecated-provider note, plus the
  Workloads / Instances / Analytics pages); api/qiskit-ibm-runtime/runtime-job-v2
  (`status()` return type `Literal['INITIALIZING','QUEUED','RUNNING','CANCELLED',
  'DONE','ERROR']`); api/qiskit-ibm-runtime/session (`details()` key list:
  `max_time, state, accepting_jobs, last_job_started, last_job_completed,
  closed_at, activated_at, usage_time`; `close()` stops accepting new jobs while
  existing ones finish, `cancel()` cancels all pending jobs).

## Study-wave craft rules (s6/s7, 2026-07-26 — final two sections)

- **An objective with ZERO executed questions must be citation-only.** s7o2
  ("Monitor jobs") is backed exclusively by conceptual questions (q026, q027,
  q028, q030, q033), so all 8 of its facts are `{"type":"citation"}`. Resist the
  temptation to borrow an s7o1 proof qid: `build_study.py` only checks that the
  qid exists in the executed set, so a borrowed ref would render a ⚙️
  "proven by execution" badge over a claim that proof never touched.
- **API reference pages are the right citation for method surfaces.**
  `guides/monitor-job` is thin (no status strings, no predicate list); the
  `api/qiskit-ibm-runtime/runtime-job-v2` page states the `Literal[...]` return
  type and `JOB_FINAL_STATES` verbatim, which is exactly what the job-lifecycle
  facts need. Same shape for `api/qiskit-ibm-runtime/session` vs
  `guides/monitor-job` on `details()` keys.
- **Two objectives, five primers.** s6 and s7 each have only two syllabus
  objectives but four-plus scope areas, so s6 carries 2+2 primers and s7 carries
  3+2 — extending the s4/s5 rule. Every primer stayed in the 340-435 word band.

## Verified library facts (s1/s2 official-alignment fix wave, 2026-07-26, qiskit 2.5.0)

Circuit library (official task 1.2 — the bank had ZERO coverage):

- **The n-local CLASSES are deprecated, the lowercase FUNCTIONS are the 2.x way.**
  `EfficientSU2`, `RealAmplitudes`, `TwoLocal`, `NLocal`, `QFT` and
  `BlueprintCircuit` all emit `DeprecationWarning: ... deprecated as of Qiskit 2.1.
  It will be removed in Qiskit 3.0. Use the function ... instead`. The functions
  (`efficient_su2`, `real_amplitudes`, `n_local`, `quantum_volume`, …) return a
  plain **`QuantumCircuit`** — still parameterized, nothing is pre-bound.
  Both forms still give the same parameter counts, so a question may key either;
  prefer the function form.
- **Parameter counts, measured:** `efficient_su2(n, reps=r).num_parameters ==
  2*n*(r+1)` (4 qubits, reps 2 -> **24**; reps 1 -> 16, reps 3 -> 32);
  `skip_final_rotation_layer=True` drops it to `2*n*r` (**16**).
  `real_amplitudes(n, reps=r) == n*(r+1)` (4 qubits, reps 2 -> **12**).
  There is one rotation layer MORE than `reps` by default.
- **Gate sets, measured (`count_ops`):** `real_amplitudes(3)` = `{ry: 12, cx: 6}`
  — the ONLY ry+cx member; `efficient_su2(3)` = `{ry: 12, rz: 12, cx: 6}`;
  `pauli_two_design(3, seed=7)` = `{rz, cz, ry, rx}`; `quantum_volume(3, seed=7)`
  = `{unitary: 3}` with **0 parameters**; `zz_feature_map(3)` and
  `pauli_feature_map(3)` are **identical** (`{p: 12, cx: 12, h: 6}`, 3 params) —
  never offer both as separate options; `excitation_preserving(3)` =
  `{rz: 12, Interaction: 9}`. `real_amplitudes` default entanglement is
  `reverse_linear` (3 qubits, reps 1 -> 2 `cx`; `'full'` -> 3).
- **`QFTGate(n)`'s constructor takes ONLY `num_qubits`**: `do_swaps=` and
  `approximation_degree=` are `TypeError` (they belonged to the deprecated `QFT`
  class). `qc.append(QFTGate(n), …).decompose().count_ops()` = n `h`,
  n(n−1)/2 `cp`, ⌊n/2⌋ `swap` — measured `{h: 4, cp: 6, swap: 2}` for n=4 and
  `{h: 3, cp: 3, swap: 1}` for n=3. One decompose step never reaches `cx`
  (that is translation, i.e. the transpiler). `QFTGate(4).inverse().name ==
  'qft_dg'`; the gate's own name is `'qft'`, so pre-decompose `count_ops` is
  `{'qft': 1}`.
- `random_circuit(n, depth)` defaults to `measure=False` (0 clbits);
  `measure=True` adds one `measure` per qubit.

Device visualization (official task 2.2 — also ZERO coverage before this wave):

- **Graphviz is NOT installed in the pinned env.** `plot_gate_map`,
  `plot_error_map`, `plot_circuit_layout` and `plot_coupling_map` all end in
  `MissingOptionalLibraryError: The 'Graphviz' library is required to use
  'plot_coupling_map'` — the pip `graphviz` package would not help, the BINARY is
  needed. **Workaround used by s2-q036/q037/q038:** stub
  `qiskit.visualization.gate_map.plot_coupling_map` (bind its real signature with
  `inspect.signature`, capture the arguments, return a bare
  `matplotlib.figure.Figure`). Everything above the leaf renderer — input
  validation, coupling-map extraction, colour and label computation — runs
  unmodified, so the proof asserts on what Qiskit actually computes. The rendered
  image is the only thing not exercised; say so in the provenance notes.
- **What each device plot forwards to `plot_coupling_map` (FakeManilaV2, 5q):**
  `plot_gate_map(backend)` -> `num_qubits=5`, the 8 directed coupling pairs,
  `qubit_color=None`, `line_color=None` (uniform drawing; `plot_directed=True`
  changes only the arrowheads). `plot_error_map(backend)` -> **5 distinct** per-qubit
  colours and **4 distinct** per-link colours, computed from calibration.
  `plot_circuit_layout(isa, backend)` -> a **2-tone** highlight
  (`['#648fff',…,'black','black']`) plus `qubit_labels=['', '', '', '0', '1']`
  (the VIRTUAL indices on the occupied physical qubits). "Distinct colour count > 2
  on both qubits and links" is a clean, executable discriminator for
  error-map-vs-the-others.
- **Input-type refutations, all verified (no Graphviz needed — they raise first):**
  `plot_gate_map(counts_dict)` / `plot_gate_map(CouplingMap)` -> `AttributeError:
  ... has no attribute 'num_qubits'`; `plot_gate_map(QuantumCircuit)` /
  `plot_gate_map(Target)` -> `AttributeError: ... has no attribute 'coupling_map'`;
  `plot_error_map(counts_dict)` -> `AttributeError: 'dict' object has no attribute
  'name'`; `plot_histogram(backend)` -> `AttributeError: ... has no attribute
  'values'`; `plot_circuit_layout(backend, qc)` -> `AttributeError: ... has no
  attribute '_layout'`; `plot_circuit_layout(isa, backend, view='bogus')` ->
  `VisualizationError: Layout view must be 'virtual' or 'physical'.`
- **`plot_circuit_layout(untranspiled, backend)` -> `QiskitError: 'Circuit has no
  layout. Perhaps it has not been transpiled.'` at EVERY optimization level** —
  `transpile` is functional, so `qc.layout` stays `None` after a level-3 run while
  the returned circuit carries a `TranspileLayout`. A clean spot-bug stem, and
  `view="physical"` is a safe refuted "fix" (the check runs before the view).
- **`plot_histogram(counts)` returns a Figure whose axis x-tick labels are the
  outcome bitstrings** (`['00', '11']`) — the observable post-condition that
  refutes "the histogram shows the device", since a mere `attempt()` scores it as
  "it ran" (the s4 harness trap). Equivalent post-condition for the device plots:
  did the call reach the coupling-map renderer at all?
- **`Statevector.sample_counts(shots, qargs=None)` returns a
  `qiskit.result.Counts`** whose keys are `np.str_` bitstrings and whose values are
  `int64` summing EXACTLY to `shots`; only nonzero-amplitude outcomes appear
  (Bell -> `00`/`11` only). It takes **no `seed` argument** — determinism comes from
  `sv.seed(1234)` on the Statevector, which reproduces the same counts across fresh
  objects. `sample_memory(shots)` is the per-shot `ndarray`. No measurement
  instruction is needed (and adding one would break `from_instruction`).
  `plot_histogram(sv.sample_counts(n))` works directly.

## Craft rules (s1/s2 fix wave, 2026-07-26)

- **A whole-basis question CAN be pooled by widening the register.** The ledger's
  earlier "s2-q031 cannot pool" note was correct for 2 qubits (all four basis
  states were already options, so any fifth option would not be a basis state = a
  tell). Rewriting the same q-sphere item on **3 qubits** (`h(1)`, `x(2)`) offers
  6 of the 8 basis states, keeps every option a legal basis state, and supports
  `display_count: 5` (2 correct + 3 of 4 distractors). Endianness misreads supply
  two distractors for free (`|001>` and `|011>` are `|100>`/`|110>` read
  backwards), a "forgot the X" state supplies a third and a "H on the wrong qubit"
  state the fourth. Generalizes: widen the register before declaring a
  value-space exhausted.
- **`lint_proof_drift` punishes MENTIONING a kwarg you do not pin.** A kwarg
  `lhs=rhs` in evidence is only a finding when the corpus talks about `lhs` yet
  shows neither the pair nor the value — so adding `qubit_labels`/`num_qubits` to
  an explanation to "cover" the evidence would CREATE findings. Leave such names
  out of the question text, or quote the exact pair. Corollary: any
  `something=True/False/None` is exempt (BOOL_RHS), which is why
  `skip_final_rotation_layer=True`, `do_swaps=False` and `plot_directed=True` are
  free to report.
- **Position skew is cheapest to fix by rotating the keys, not the content.**
  s2 `position_A` sat at 37.5% (warn line 0.40) after this wave's first draft;
  re-lettering one spot-bug's options so the answer moved A -> D took it to 33.1%
  at zero content cost. Do this before touching option text.
- **On a 6-option / `display_count: 5` question the length arithmetic is trivial:**
  make ALL five distractors shorter than the correct option for a keeper, or keep
  TWO distractors longer than it so no drop-one variant can flip it. Three of the
  seven new questions were made keepers deliberately (s1-q048, s2-q036, s2-q037);
  the bank aggregate moved 23.2% -> 23.9% `longest_option`, 22.2% -> 22.4%
  `shortest_option`, 24.8% -> 24.4% `avoid_longest`, 0 blockers/warnings.
- **`zz_feature_map` vs `pauli_feature_map` are the same circuit** — a reminder
  that "two plausible library calls" must be diffed by `count_ops` before both
  are used as options in one question.

## Verified library facts (s3/s4/s7/s8 official-alignment fix wave, 2026-07-26)

Broadcasting pattern NAMES (official task 4.2 / sample topic 12 — the bank had
the mechanics but never the names):

- **guides/primitive-input-output names exactly four patterns**, verbatim:
  *Broadcast single observable* (parameters `(5,)` x observables `()` -> `(5,)`),
  *Zip* (`(5,)` x `(5,)` -> `(5,)`), *Outer/Product* (`(1, 6)` x `(4, 1)` ->
  `(4, 6)`) and *Standard nd generalization* (`(3, 6)` x `(2, 3, 1)` ->
  `(2, 3, 6)`). There is no "all-to-all" wording on the live page — the audit's
  guess at the name was wrong; use these four. The page also states the three
  NumPy rules and that each `SparsePauliOp` counts as ONE element whatever its
  term count.
- **Measured on `StatevectorEstimator` (2026-07-26):** with a ONE-parameter
  circuit the parameter array's shape IS the parameter-value-set shape, so
  `(1, 4)` x `(3, 1)` -> `evs.shape (3, 4)`; `(3,)` x `(3,)` -> `(3,)`;
  `(3,)` x `()` -> `(3,)`; `(3, 1)` x `(3,)` -> `(3, 3)`; `(2, 3)` x `(4, 2, 1)`
  -> `(4, 2, 3)`; `(3,)` x `(4,)` raises `ValueError: The observables shape (4,)
  and the parameter values shape (3,) are not broadcastable.` With a TWO-parameter
  circuit the trailing axis is consumed instead (`(5, 2)` -> `(5,)`), confirming
  the s5/s7 entries. `ObservablesArray.coerce(obs).shape` is the cheap way to
  report an observables-array shape in evidence.
- **Zip and broadcast-single-observable produce the SAME result shape** — the
  only executable discriminator is the observables-array shape (`()` vs equal to
  the parameter shape). Any zip question must score on that, not on `evs.shape`.

Job state / primitive containers (official task 7.2):

- **`RuntimeJobV2` predicates can be executed with NO service and NO network:**
  `_set_status_and_error_message` short-circuits when `_status` is already in
  `JOB_FINAL_STATES`, so a subclass whose `__init__` just sets `self._status`
  runs the real inherited `status()/done()/errored()/cancelled()/in_final_state()`.
  Measured: `DONE` -> done True / in_final_state True; `CANCELLED` -> done False,
  cancelled True, in_final_state True; `ERROR` -> errored True. This unblocks
  executed s7o2 questions, which the s6/s7 study wave had declared impossible.
- **`JobStatus.DONE.value` is the sentence `'job has successfully run'`**, so
  `status() == JobStatus.DONE` is False against the string and `status().name`
  raises `AttributeError: 'str' object has no attribute 'name'`. `qiskit.providers.JobStatus`
  has SEVEN members (INITIALIZING, QUEUED, VALIDATING, RUNNING, CANCELLED, DONE,
  ERROR) — one more (`VALIDATING`) than the runtime `Literal`. There is no
  `FAILED` state anywhere.
- **The local reference primitives return `JobStatus` ENUM members**, not strings:
  `StatevectorSampler().run(...).status()` is `JobStatus.DONE`. So the
  string-vs-enum contrast is a *Runtime vs reference primitive* fact, not a
  universal one — scope every status question to `RuntimeJobV2`.
- **`BasePrimitiveJob` lives in `qiskit.primitives`** (not importable from
  `qiskit.primitives.base`); its abstract methods are exactly `cancel, cancelled,
  done, in_final_state, result, running, status` (+ concrete `job_id`) — note
  **no `errored`**, which is a `RuntimeJobV2` extra. `PrimitiveJob` and
  `RuntimeJobV2` are both instances of it.
- **A Sampler pub result's exact type is `SamplerPubResult`** (MRO
  `SamplerPubResult -> PubResult -> object`), so "it is a `PubResult`" is TRUE by
  isinstance and FALSE as a type name — word such options as `type(x).__name__`.
- **`Session.status()` and `details()["state"]` use different vocabularies**
  (api/qiskit-ibm-runtime/session, fetched 2026-07-26): `status()` returns
  `Pending` / `In progress, accepting new jobs` / `In progress, not accepting new
  jobs` / `Closed` / `None`, while `state` is `open|active|inactive|closed`.
  `interactive_timeout` = max IDLE time between jobs before deactivation,
  `active_timeout` = max time active, `max_time` = total allowed length,
  `usage_time` = time a QPU is committed to a job (not wall clock).

OpenQASM 3 types (official task 8.1) and REST (task 8.4):

- **`qiskit-qasm3-import` is NOT installed** in the pinned env (re-checked
  2026-07-26: `ModuleNotFoundError`) — the s8 pool-wave entry stands, and the
  brief for this wave was wrong on that point. OpenQASM type questions are
  therefore conceptual; and even with the package, Qiskit's importer is narrower
  than the language, so a `loads()` proof would refute perfectly legal OpenQASM.
- **openqasm.com answers this environment's fetch tool with HTTP 403** (the whole
  site, including `/versions/3.0/index.html`) — a user-agent block, not a dead
  page. Spec content was read from `raw.githubusercontent.com/openqasm/openqasm/
  main/source/language/types.rst`. `syllabus.json` already cites the UNVERSIONED
  `https://openqasm.com/language/types.html`; the new s8 questions cite the
  versioned `.../versions/3.0/language/types.html` as briefed. **Not machine-verified
  from here — check_links is the arbiter.**
- **Spec facts, quoted:** the special types (no C equivalent) are `bit`, `angle`,
  `duration`, `stretch`; the standard ones `bool`, `int`, `uint`, `float`,
  `complex`. `complex` takes a FLOAT type in its designator
  (`complex[float[64]] c;`) and bare `complex` means `complex[float]` — never
  offer bare `complex` as a wrong option, but `complex[64]` IS invalid. There is
  no `string`, `char`, `real` or `unsigned` type. Casting: the lesser operand is
  promoted (`complex` > `float` > `int`/`uint`, wider beats narrower); `bool` and
  scalar `bit` are interchangeable; `bit[n]` <-> `int[m]`/`uint[m]`/`angle[m]`
  only when `m == n`; nothing casts to or from `duration` (divide by a duration);
  `float` -> `angle[m]` takes the nearest value modulo 2pi (ties toward a zero
  LSB), not truncation; width designators must be `const`.
- **Runtime REST jobs endpoints, read off the live reference** (both
  `api/qiskit-runtime-rest` and `api/qiskit-runtime-rest/tags/jobs` fetched 200):
  `POST /api/v1/jobs`, `GET /api/v1/jobs`, `GET|DELETE /api/v1/jobs/{id}`,
  `POST /api/v1/jobs/{id}/cancel`, `GET /api/v1/jobs/{id}/logs`,
  `GET /api/v1/jobs/{id}/metrics`, **`GET /api/v1/jobs/{id}/results`**,
  `PUT /api/v1/jobs/{id}/tags`; sessions are `POST /api/v1/sessions`, backends
  `GET /api/v1/backends`. Headers: `Authorization: Bearer <IAM token>`,
  `Service-CRN`, `IBM-API-Version: <YYYY-MM-DD>`, `Accept: application/json`,
  plus `Content-Type` on bodies. The `eu-de` region swaps the host only.

Circuit/transpiler (official minor gaps):

- **`2 * Parameter('th')` is a `ParameterExpression`**, `isinstance(expr, Parameter)`
  is False (`Parameter.__mro__` is `Parameter -> ParameterExpression -> object`),
  the circuit still reports ONE free parameter, and `expr.bind({th: 0.5})` returns
  a (bound) `ParameterExpression`, never a float. `ParameterVectorElement`
  subclasses `Parameter`.
- **Stage membership of a level-2 preset, measured by walking
  `stage.to_flow_controller().tasks` recursively** (`PassManager.passes()` no
  longer exists in 2.5): layout = SetLayout, VF2Layout, BarrierBeforeFinalMeasurements,
  SabreLayout, FullAncillaAllocation, EnlargeWithAncilla, ApplyLayout;
  routing = CheckMap, BarrierBeforeFinalMeasurements, SabreSwap, VF2PostLayout,
  ApplyLayout, FilterOpNodes; translation = UnitarySynthesis, HighLevelSynthesis,
  BasisTranslator; optimization = TwoQubitPeepholeOptimization, ... ,
  Optimize1qGatesDecomposition, CommutativeCancellation, ... ; init (levels 2/3)
  contains ConsolidateBlocks and Split2QUnitaries. **Traps:** `BasisTranslator`
  appears in THREE stages (init, translation, optimization) and `ApplyLayout` in
  two (layout, routing) — never use either as a "which stage" distractor without
  saying which stage is being asked about; `ConsolidateBlocks` is an INIT pass at
  level 2, not an optimization pass (Qiskit 2.5 replaced that role with
  `TwoQubitPeepholeOptimization`); at level 1 the layout stage additionally holds
  TrivialLayout and CheckMap.

Craft notes from this wave:

- **`None` in an option text is an ABSOLUTE word** to the audit's tokenizer
  (`word_set` lowercases, so `None` -> `none`). A distractor saying "`details()`
  returns `None`" turned on `absolute_distractor_tell` on the drop-one variant
  that removed the only hedged distractor — fixed by hedging a second distractor.
  Same class of surprise as the ledger's `measure_all` -> "all" note.
- **A 6-option / dc=5 question needs TWO distractors longer than the correct
  option**, and the cheapest way to get there is to lengthen two distractors
  rather than trim the answer (s7-q035: correct 161 chars vs longest distractor
  143 fired a low `length_tell` until two distractors were extended past it).
- 10 new questions moved the bank aggregates 23.9% -> 23.2% `longest_option`
  (predict-output triples and single-class-name option sets are equal-length
  ballast, worth 0.25 each), `shortest_option` unchanged at 22.4%,
  `avoid_longest` 24.4% -> 24.3%, positions 29.6-30.7%, 0 blockers/warnings,
  one deliberate low `length_tell` residual (s7-q036).

## Figure-question craft (task #27 figure wave, 2026-07-26, qiskit 2.5.0)

Seven new figure questions (s2-q041..q045, s3-q056, s4-q047) plus the
visual-literacy page. Facts below were measured in the pinned venv.

Rendering / determinism:

- **`render_figures.py` only walks `data/questions/**`**, so a non-question
  figure directory (`data/figures/guide/`) is never rendered by it. Generate
  such figures by hand — `cd data/figures/guide && ../../../.venv/bin/python
  generate.py` — and reproduce the tool's prelude INSIDE the script
  (`matplotlib.use("Agg")`, `svg.hashsalt="certiq"`, a `savefig` wrapper that
  defaults `metadata={"Date": None}` and `bbox_inches="tight"`), otherwise the
  SVGs carry a timestamp and differ on every run. Determinism was verified by
  rendering into two scratch dirs and comparing sha256 per file.
- `build_site_data.copy_figures()` mirrors `data/figures/**` with `rglob`, so
  any subdirectory (including `guide/`) lands under `site/static/img/bank/`;
  MDX references `/img/bank/guide/guide-*.svg`.
- **Deterministic counts without sampling:** `{str(k): round(v * SHOTS) for k, v
  in Statevector(qc).probabilities_dict().items()}`. Never call
  `sample_counts` in a generator — the double render would diverge.
- `generate_preset_pass_manager(..., seed_transpiler=42)` + an explicit
  `initial_layout` reproduces byte-identical drawings across processes.

Proof technique for figures (all four shapes used this wave):

- **Read the drawing back off the axes.** `plot_histogram` puts one Rectangle
  per bar in `ax.patches` **in the same order** as `ax.get_xticklabels()`, so
  `tuple(zip(labels, heights))` IS the picture and can be compared between the
  stem call and every variant (s2-q041, s2-q045).
- **`qiskit.visualization.circuit._utils._get_layered_instructions(circuit,
  reverse_bits=..., idle_wires=...)`** is the layout engine shared by the text,
  mpl and latex drawers; `(wire order, ops addressed by wire position)` is a
  faithful signature of a circuit drawing (s2-q044). Measured: `reverse_bits=True`
  gives wires `('q_2','q_1','q_0')` with the same geometry that
  `QuantumCircuit.reverse_bits()` produces under wires `('q_0','q_1','q_2')` —
  the two pictures differ ONLY in the wire labels, which makes them a clean,
  provable option pair.
- **Bloch drawings** reduce to one Bloch vector per sphere
  (`partial_trace` + `expectation_value(Pauli('X'|'Y'|'Z'))`); the sphere COUNT
  is part of the signature (s2-q042).
- **Q-sphere drawings** reduce to `(bitstring, magnitude, relative phase)` per
  non-zero amplitude, phases taken against the first non-zero amplitude
  (s2-q043).

Drawer facts measured this wave:

- **`plot_histogram` prints the value above every bar** (`bar_labels=True` is
  the default), and an integer-counts dict gives a `Count` y axis (not
  probabilities). This is what makes value-reading distractors fair.
- **`number_to_keep=k` keeps the k LARGEST outcomes and appends a `rest` bar**:
  `{"000":400,"111":380,"001":120,"010":70,"100":30}` with `k=3` draws FOUR bars
  `000:400, 001:120, 111:380, rest:100` (sorted by label, `rest` last). Refines
  the earlier ledger entry: the kept count is k, not k-1, and `rest` is the SUM.
  A literal `"rest"` key in a plain dict renders identically — that is how the
  wrong-`rest` distractors were built.
- **`plot_bloch_multivector` titles the spheres `qubit 0`, `qubit 1`, …** and
  labels the poles `|0>`/`|1>`. **For a Bell state it draws NO arrow at all**
  (reduced vector is 0) — not a dot at the origin, not a short arrow.
- **`plot_state_qsphere` is global-phase blind:** multiplying the state by
  `exp(0.9j)` produced a **byte-identical** SVG. `show_state_labels` defaults
  True (kets are drawn), `show_state_phases` defaults **False**, so relative
  phase is carried by marker colour alone -> `color_essential: true`.
- **S/T/Z on the same entangled state render at IDENTICAL byte size** (147950 B
  each; only the marker colour differs) — a q-sphere option family is
  automatically immune to the image-size tell.
- **`h(0); cx(0,1); s(0)` and `h(0); cx(0,1); s(1)` produce the SAME state** —
  never offer both as options on a q-sphere item.
- **Transpiled circuits are visually self-identifying:** their wire labels read
  `q_0 -> 0`. If some options in a transpiler figure question are real
  pass-manager outputs and others are hand-built circuits, the layout labels are
  a free tell — make EVERY option a real transpiler output (s3-q056 does).
- **Routing without translation:** `coupling_map` alone (no `basis_gates`) keeps
  `h` as `h` and draws the inserted SWAP as a real SWAP box. Measured on a
  3-qubit line at level 0 with layout `[0,1,2]` for `h(0), cx(0,1), cx(0,2)`:
  `h[0], cx[0,1], swap[1,2], cx[0,1]`. Adding `basis_gates=["rz","sx","x","cx"]`
  expands the same result to `rz,sx,rz` + five `cx` with a `global phase: pi/4`
  note (26.8 KB vs 11.5 KB) — the busiest distractor in the wave.
- **Estimator broadcast, re-measured:** observables `(4, 1)` x parameter values
  `(1, 6)` -> `evs.shape (4, 6)`, 24 values, no exception.
  `ObservablesArray.coerce(obs).shape` is the cheap evidence value; the four
  pattern names remain the ones in guides/primitive-input-output.

Anti-tell calibration for image options:

- The audit's `image_size_tell` needs BOTH "strictly the largest/smallest SVG"
  AND a deviation `> 0.4` from the distractor median. **Ties defeat the first
  clause**, and near-identical renders defeat the second — so a family of
  same-complexity variants is safe even when the correct one is nominally
  extreme (s2-q041 A/B both 12745 B; s2-q044 A/E both 8303 B).
- Check the sizes in EVERY `display_count` variant, not just the full set: a
  variant that drops the tying distractor can expose the correct option as the
  strict extreme (s2-q041 B, s2-q044 A were both checked this way; deviation
  stayed under 6%).
- **Bank aggregates after this wave (6 questions carry option images):**
  `largest_image_option` 11.1%, `smallest_image_option` 25.0%, coverage 2%,
  0 blockers / 0 warnings, no `image_size_tell` anywhere. Smallest is at chance;
  largest sits below it because the busiest drawing was a distractor in five of
  six items (an extra swap, an extra sphere, an extra bar, an ISA expansion).
  **Recipe for the next figure wave:** deliberately author ~1 in 4 figure items
  whose KEYED drawing is the busiest — e.g. key the routed/expanded circuit and
  make the misconceptions the simpler pictures — instead of trimming distractors.
  Do not distort a misconception to chase it: the heuristic is ungated at this
  coverage (same policy as `numeric_middle` in s7).
- **Weight:** `plot_bloch_multivector` SVGs are ~210 KB for two spheres and
  ~110 KB for one (5 options ≈ 1 MB); q-spheres ~150 KB; circuit and histogram
  renders are 8–18 KB. Budget bloch-heavy questions sparingly.
- Image options make the text-length heuristics abstain in a healthy way: with
  all option texts `""`, `longest_option`/`shortest_option` return every key
  (exactly chance) and `avoid_longest` abstains — figure questions are neutral
  ballast for the length aggregates.

## Figure-question wave 2 (task #28 wave 1, 2026-07-26, qiskit 2.5.0 / runtime 0.48.0)

Eleven new figure questions in the four sections that had none: s1-q051/q052/q053,
s5-q040/q041/q042, s6-q040/q041/q042, s7-q037/q038. Six carry option images, five
are stem-figure items (figure = the question, text options). All measured in the
pinned venv.

Drawer / rendering facts measured this wave:

- **`plot_state_city` draws on TWO `Axes3D` panels** (Re(rho) left, Im(rho)
  right) -> `platform_sensitive: true`, same as Bloch. It draws all 16 bars of a
  2-qubit density matrix whatever the state, so **the whole family renders at
  68.2-68.8 KB — a 0.9% spread across five very different states**. That makes a
  city-plot option set automatically immune to `image_size_tell` while still
  letting you place the keyed figure at either extreme.
- **`plot_histogram` SKIPS zero-valued entries but keeps their tick**: the dict
  `{"00":24,"01":2,"10":0,"11":14}` yields 4 x-tick labels and only 3 patches,
  with the bars at x = -0.25, 0.75, **2.75**. So a proof that zips
  `ax.get_xticklabels()` with `ax.patches` silently mispairs (caught live on
  s5-q041). Pair by slot instead: `int(round(p.get_x() + 0.25))`. The two
  drawings ("three categories" vs "four categories, one empty") differ by ~450
  bytes and are a fair, genuinely visible option pair.
- **`plot_histogram([c1, c2], legend=[...])` creates ONE `BarContainer` PER BAR**
  (2 series x 4 outcomes = 8 containers), series-major and label-sorted, so the
  series split is `heights[i:i+len(labels)]`. Legend text reads off
  `ax.get_legend().get_texts()`. Re-confirmed: a single counts dict with a
  two-entry legend raises `VisualizationError: Length of legend (2) doesn't match
  number of input executions (1).`
- **Runtime primitives on a fake backend are reproducible ACROSS PROCESSES with
  `options.simulator.seed_simulator`** — safe inside a figure generator (the
  double render is byte-identical for both SamplerV2 and EstimatorV2 runs).
  `options.seed_estimator` warns `Options {'seed_estimator': ...} have no effect
  in local testing mode` — never set it.
- **`default_precision` -> shot budget, measured** (1-qubit RY, FakeManilaV2):
  0.2 -> 25 shots, 0.1 -> 100, 0.05 -> 400, 0.02 -> 2500, 0.01 -> 10000. The
  reported `stds` are state-dependent, largest where the expectation value is
  near zero (0.1 gave 0.039/0.088/0.095/0.039 across a 0..pi sweep) — which is
  what makes an error-bar drawing readable as evidence.
- **`estimator.options.precision = x` and `estimator.options.execution.shots = n`
  are both `ValidationError` (`Object has no attribute ...`)**, and
  `default_precision = 0` **and** `= 0.0` hit the same `must be >0` validator
  (useful: the `0.0` spelling is two characters longer, which is how s6-q041's
  length tell was cleared without touching content).
- **`<ZZ>` on `ry(theta,0); cx(0,1)` is CONSTANT** (both |00> and |11> give +1) —
  a dead sweep observable. Use a single-qubit Z on a 1-qubit circuit for any
  angle-sweep figure.
- Estimator broadcasting re-measured for the grouped-bar item: `[[Z],[X]]` (2,1)
  x parameters (1,3) -> `(2, 3)`; a single observable x a (2,3) parameter array
  -> also `(2, 3)` (right shape, wrong content — refute on values, not shape);
  `[Z, X]` (2,) x (3,) -> `ValueError ... not broadcastable`; **`[[Z, X]]` (1,2)
  x a (3,1) array -> ValueError too, because with ONE free parameter a (3,1)
  array is read as parameter shape (3,)**; `SparsePauliOp(["Z","X"])` x (3,) ->
  `(3,)` (one observable, whatever its term count).
- s7 container refutations re-confirmed from the plotting side:
  `SamplerPubResult.get_counts`, `DataBin.get_counts`, `PrimitiveResult.results`,
  `PrimitiveResult.data`, `PubResult.evs` are all `AttributeError`;
  `pub.metadata["evs"]` is `KeyError`. `result[0].data.stds` is the dangerous one
  — it exists, has the right shape and plots, but collapses onto the axis
  (0.005-0.018 vs evs spanning +-0.9), so it needs a value post-condition.
- Bloch reading: `h` then `sdg` lands the arrow on **-y** (`s` gives +y); `z` on
  |0> leaves it at the pole. `plot_bloch_multivector` of a 2-qubit product state
  is ~211 KB.
- **SVG weight table for budgeting:** bloch 2 spheres ~211 KB; city plot (2
  qubits) ~68 KB; **grouped bar chart with hatched bars ~93 KB** (hatching is by
  far the most expensive 2D primitive — a plain 9-point line plot is ~23 KB);
  histogram 2 bars ~12.6 KB, 8 bars ~21 KB; 40-point step trace ~17 KB;
  1-qubit 3-gate circuit render ~4.4-5.3 KB.

Stem-figure craft (the shape the gold example does not cover):

- When the FIGURE is the stem and the options are text, "figure variants ==
  proof variants" cannot apply. The replacement rule: **the proof hardcodes a
  literal TARGET describing what the drawing shows (Bloch vectors, marker
  heights, bar values), and the generator carries an `assert` that the artifact
  it renders matches that same literal.** Drift then fails at render time
  instead of silently invalidating the proof. Used by s1-q051, s6-q041, s6-q042,
  s7-q037, s7-q038.
- A retrieval-flavoured stem (`service.job(job_id)`) is provable offline by
  rebuilding the same result with a local seeded run: the container path is what
  the question tests, not the network round trip. Say so in the provenance note.

Image-size calibration (the bank-level fix this wave was asked for):

- **`largest_image_option` 11.1% -> 24.3%, `smallest_image_option` 25.0% ->
  28.1%**, 12 image-option questions bank-wide, 0 blockers/warnings, no
  `image_size_tell` anywhere and no other flag on any of the 11 new questions.
- The lever that works is choosing the DISTRACTOR SET after measuring, inside a
  family whose renders differ by <1%: two keepers were made strictly largest
  (s5-q040 at 21456 B vs a 20777 B distractor median = 3% deviation; s5-q042 at
  14841 B vs 14799 B = 0.3%) and one strictly smallest (s5-q041, 13710 B vs a
  17125 B median = 20%). All are far under the 0.4 deviation bar, so the
  heuristic moves while the flag stays silent. **Never trim a misconception to
  chase the number — pick which equally-valid misconception renders where.**
- **Enumerate the `display_count` variants, not just the full option set.** A
  question whose keyed figure is *second* smallest contributes 0.25 through the
  single variant that drops the one smaller distractor (s6-q040 after its fix,
  s1-q052 symmetric on the largest side). This is where the aggregate leaks.
- **A mirrored curve renders BYTE-IDENTICAL** (`cos` vs `-cos` over 0..pi: 23125 B
  each), which is a free tie — ties defeat the strictness clause, worth 0.625 EV
  at dc=4 rather than 1.0. To take a keyed curve OFF the extreme, change the
  sweep range rather than the distractor set: 0..pi put `cos`/`-cos` jointly at
  the max, 0..2*pi moved the max to the amplitude curve and left the keyed cosine
  in the middle (also the better teaching picture — one full period).
- Answer keys for the wave: A x2, B x2, C x3, D x2, E x2; difficulty 1/8/2 across
  levels 1/2/3.

## Figure-question wave 3 (task #28 wave 2, 2026-07-27, qiskit 2.5.0 / runtime 0.48.0)

Eight new figure questions, sized to saturate the mock sampler's 20% figure cap
in the three thin sections and to add variety elsewhere: s3-q057, s3-q058
(s3 1 -> 3), s4-q048, s4-q049 (s4 1 -> 3), s8-q029 (s8 0 -> 1), plus s2-q046,
s5-q043, s1-q054. Six carry option images, two are stem-figure items. All
measured in the pinned venv.

Library / drawer facts measured this wave:

- **`qiskit_qasm3_import` is NOT installed in the pinned venv**, so
  `qiskit.qasm3.loads(...)` raises
  `MissingOptionalLibraryError: The 'qiskit_qasm3_import' library is required to
  use 'loading from OpenQASM 3'`. QASM3 *export* (`qasm3.dumps`) is native and
  works. Any s8 item that must LOAD a program has to use
  `QuantumCircuit.from_qasm_str` (qasm2) until that package is added — s8-q029
  was written that way and says so in its provenance.
- **`from_qasm_str` keeps the program's own register names**: `qreg a[2]; creg
  m[2];` draws wires `a_0`, `a_1` and one bundled classical wire `m` (never the
  default `q`/`c`), and `measure a -> m;` expands index by index into two
  `measure` instructions (`a[0]`->`m[0]`, `a[1]`->`m[1]`). A five-way family of
  loader outputs (own names / default names / reversed bit targets / reversed cx
  operands / single measure) renders at 10.5-12.2 KB, with the own-names and
  reversed-target variants **byte-identical in size** (12183 B both) — a free tie.
- **`generate_preset_pass_manager` with NO backend/coupling map leaves
  `circuit.layout` as None**, so the drawing keeps plain `q_0..q_n` wire labels.
  That removes the "`q_0 -> 0` labels give the transpiled option away" tell of
  s3-q056 without having to make every option a routed circuit: an
  optimization-level family needs no `initial_layout` at all.
- **Levels 1, 2 and 3 produce IDENTICAL output** for a plain inverse-pair
  circuit (`h;cx;cx;h;z;z;cx`). Never offer two different levels as two option
  images without diffing them first — build the misconception variants by
  EDITING THE INPUT CIRCUIT and running level 0 on it instead (s3-q057 does:
  "only the Z pair cancelled", "only the CX pair cancelled", "each pair kept
  once" are all real level-0 outputs of edited circuits).
- **Level >= 1 fuses adjacent single-qubit gates even with no `basis_gates`**:
  `h(0)` followed by `sdg(0)` came back as a single `U2(-pi/2,-pi)` box. If you
  want the optimized option to read as "the pairs simply vanished", keep every
  surviving 1q gate separated by a 2q gate (s3-q057 ends with `cx(0, 2)` for
  exactly this reason).
- **`for_loop` drawing**: `op.params` is `(index_set, loop_parameter, body)`, the
  box label prints the index set verbatim (`For-0 range(0, 3)`; `range(2)` ->
  `For-0 range(0, 2)`), and the instruction's qubit tuple is ordered by first use
  in the body ((1, 0) when the body starts with an Rx on q1). Signature for a
  loop drawing: `(name, qubits, repr(index_set), body ops re-addressed through
  the outer qubit tuple)`. `switch` draws `Switch-0` plus one `Case-0 (v)` region
  per case with `Case-0 default` last, and the tested value prints as `0x3` on
  the classical wire.
- **Q-sphere marker sizes are readable**: magnitudes 0.5 vs 0.87 on the two poles
  give visibly different markers, and a 4-marker product state renders only 1.6%
  larger (149805 vs 147429-147962 B). The mirrored pair `ry(2pi/3)+cx` vs
  `ry(pi/3)+cx` renders 147962 vs 147961 B — one byte apart, i.e. the mirrored
  curve trap in its q-sphere form.
- **`plot_bloch_multivector` on a partially entangled pair** (`ry(pi/3,0); cx`)
  draws two HALF-LENGTH arrows at the |0> pole (reduced vector length 0.5) —
  the readable middle ground between two full arrows (product) and no arrow at
  all (Bell). The whole five-state family renders 216092-216510 B (0.2% spread),
  so the arrowless Bell figure is a free strict-smallest keyed option at 0.2%
  deviation.
- **`number_to_keep` re-confirmed** on real sampler counts: k largest kept, plus
  a `rest` bar equal to the SUM of everything folded away (42 of 400 shots
  here), bars alphabetical with `rest` last, values printed above each bar.
- **Seeded SamplerV2 counts, reusable**: GHZ-3 (`h;cx;cx;measure_all`) transpiled
  at level 1 for `FakeManilaV2` with `seed_transpiler=42`, `SamplerV2` with
  `options.simulator.seed_simulator = 11`, 400 shots ->
  `{'000':188,'111':150,'011':20,'100':14,'110':12,'101':6,'001':6,'010':4}`,
  reproducible across processes. Both the generator and the proof assert this
  dict so a stack bump fails loudly instead of silently redrawing the figure.
- **`EstimatorPub.coerce((qc, obs, values))` is the authoritative shape probe**
  for broadcasting items: `.observables.shape`, `.parameter_values.shape`,
  `.shape`. Measured: a flat list of 5 observables against a `(5, 1)` value array
  on a ONE-parameter circuit coerces to `(5,)` x `(5,)` -> `evs.shape (5,)` —
  with a single free parameter the trailing axis is the parameter axis, not a
  broadcast axis. (Cheaper and more honest than `ObservablesArray.coerce` alone,
  which says nothing about the parameter side.)

Process facts:

- **A conceptual stem-figure question still needs `code`** — the schema requires
  the key, so use `"code": null` (verify_bank fails with `'code' is a required
  property` otherwise). s4-q049 is the first figure item with no code at all.
- **Rasterize hand-drawn diagrams before committing them.** Running the
  generator with `savefig` patched to write `.png` (dpi 110) into the scratch dir
  and reading the image caught two collided column captions in s4-q048 and a
  "gap" label overlapping a job box in s4-q049 — neither is visible in the SVG
  bytes or in any gate.
- Queueing-semantics items stay conceptual (guide section 5 allows it): s4-q049
  draws only features stated in prose on guides/execution-modes (one queue entry
  per workload, dedicated/exclusive active window, no calibration job inside it,
  interactive-TTL gaps) and guides/choose-execution-mode (batch is scheduled
  together but never exclusive, and is cheaper). Both fetched 2026-07-27.

Image-size calibration:

- Per-item expected value of the two image heuristics (dc=4, all four displayed
  variants enumerated): s3-q057 largest **1.000** (strict max in every variant,
  worst deviation 33.5%); s8-q029 largest 0.625 (tied max with one distractor,
  strict max in the variant that drops it, deviation 2.0%); s5-q043 largest 0.250
  (deviation 3.6%); s2-q046 and s3-q058 largest 0.125 each (tie effects only);
  s1-q054 smallest **1.000** (strict min everywhere, deviation 0.2%). New-item
  totals: largest 2.125, smallest 1.000 over 6 image-option questions.
- **Bank aggregates: `largest_image_option` 24.3% -> 28.0%,
  `smallest_image_option` 28.1% -> 24.3%** across 18 image-option questions;
  0 blockers / 0 warnings, no `image_size_tell` anywhere, and no flag of any kind
  on the eight new questions. The two heuristics essentially swapped places —
  both stay within 3 points of chance.
- **The 40% deviation bar is a per-VARIANT constraint on the distractor median,
  not on the full option set.** For a keyed-largest item you need at least THREE
  distractors above `correct / 1.4`, because any dc=4 variant drops one and the
  median of the remaining three is what the flag measures. The first s3-q057 draft
  had two small distractors and flagged at 63.9% in two of four variants; the fix
  was to widen the STEM circuit (a trailing `cx(0, 2)` that survives every level)
  so the fully-optimized distractor grew from 8109 to 10806 B, lifting the worst
  variant deviation to 33.5% with the misconceptions untouched.
- Answer keys for the wave: A x1, B x2, C x3, D x1, E x1; difficulty 2 across all
  eight (figure items are read-the-picture items, so level 2 is the honest tag).

## Realism audit R1 — s1 (2026-10-01, qiskit 2.5.0)

- All 44 s1 questions are executed (`verification.mode: "script"`); every proof
  re-ran PROVEN with the stored key — no correctness fixes needed.
- **Stem trims that removed in-stem API definitions raise honest difficulty:**
  s1-q013 (`.dot` = A·B hint), s1-q017 (definition of "commute"), s1-q026 (RZ
  matrix convention), s1-q032 (control/target spelled out) no longer hand the
  candidate the tested fact. These were rated with the hint gone; a later wave
  must not re-add such glosses without re-rating down.
- **Stem trims are anti-tell neutral here:** median 17 -> 10 words, the s1
  meta-audit stayed at the same 9 low length flags, 0 blockers/warnings;
  `stem_keyword_overlap` 20.1 % (below chance). Generic stems ("What does this
  code print?") cannot create stem-echo tells.
- Honest re-rating of s1 lands far easier than the bank target (24/19/1): the
  section is dominated by one-fact items (Pauli label endianness ×6, single-gate
  statevectors ×8). Hard items have to come from R2 adds (interacting concepts:
  compose+endianness, equiv+global phase), not from inflating ratings.

## Realism audit R1 — s2 (2026-10-01, qiskit 2.5.0)

- 36/37 s2 questions are executed; all re-ran PROVEN with the stored key. The one
  conceptual item (s2-q018, publication figure -> `output="mpl"`) was re-checked
  against both citations (guides/visualize-circuits: `mpl` -> `matplotlib.Figure`,
  `latex` -> `PIL.Image`, text is the default, `style` is mpl-only;
  api/qiskit/visualization: `savefig` on the returned Figure) plus the
  `QuantumCircuit.draw` API (`latex_source` -> `str`). No correctness fixes.
- **Stem glosses removed, rated with the hint gone:** s2-q012 (q_0-on-top default),
  s2-q031 ("node at every nonzero amplitude"), s2-q034 ("`plot_bloch_vector` treats
  its argument as a raw [x, y, z]"), s2-q039 ("sampled straight from the
  statevector"). Kept deliberately: s2-q035 equator definition ⟨Z⟩ = 0 (defines the
  term, not the tested gates), s2-q032 equal-size/different-color detail (options
  depend on it), s2-q038 "`isa` is transpiled for `backend`" (option B uses `isa`).
- **Stem-echo trap on spot-bug trims:** trimming s2-q036 to "should plot the
  physical qubits the transpiled circuit occupies" raised `stem_echo_tell` to
  MEDIUM (key D overlap 4 vs 2: `plot`, `circuit` …). Fixed by a stem that names
  the symptom without the API's own vocabulary ("raises instead of drawing which
  device qubits are in use"). Short stems that paraphrase the keyed option's
  nouns are the risk; generic symptom stems are safe.
- Honest re-rating: 12/20/5 -> 22/15/0 (one 1->2: s2-q041 needs entanglement +
  endianness of `x(2)`). Like s1, s2 has no genuinely 3-level item left; hard
  items must come from R2 adds. Stem median 22 -> 12 words, max 18; meta-audit
  unchanged at 8 low length flags, 0 blockers/warnings.

## Realism audit R1 — s3 (2026-10-01, qiskit 2.5.0)

- 44/49 s3 questions are executed; all re-ran PROVEN with the stored keys. The five
  conceptual items were re-checked against their citations: s3-q027
  (classical-feedforward-and-control-flow: mid-circuit measurement + in-circuit
  classical logic = dynamic circuit), s3-q036 (set-optimization: level 0 = no
  optimization but still TrivialLayout + SabreSwap routing; higher levels "do not
  always make a difference"; D keyed to the 2.5 library default 2 per the earlier
  docs-drift entry), s3-q038 (transpiler-stages: routing inserts SWAPs, layout only
  selects qubits), s3-q044 (transpile: "circuits must adhere to the backend's ISA"),
  s3-q048 (construct-circuits: registers can be named and combined; option F
  re-executed — an ISA circuit from `data`/`anc` registers has one register `q`).
  construct-circuits supports q048 only weakly (it shows naming, not "readability");
  the claim is uncontroversial, but a future wave could add a stronger citation.
- **Correctness fix (self-containedness), s3-q033:** distractor F ("6-qubit circuit
  … on adjacent qubits") was refuted by "6 virtual qubits cannot map onto 5
  physical ones", but the stem never stated the device size (the proof uses a
  5-qubit line). Stem now says "A 5-qubit line backend". Key, options and proof
  unchanged. Rule: when a distractor's refutation depends on a target property
  (qubit count, basis, connectivity), the stem must state it — trimming must not
  drop it.
- **Glosses removed, rated with the hint gone:** s3-q015 (in-stem `width()`
  definition that decided options B/E), s3-q026 (prose spelling out the if/else
  branches of `if_test((cr[0], 0)) as else_`), s3-q027 (parenthetical definition
  of a dynamic circuit, which also echoed the key), s3-q028 ("applying X three
  times"), s3-q033 ("needing no further transpilation" = ISA definition). Kept
  deliberately: s3-q024 "`if_else`" (excludes the `while_loop` near-miss), s3-q037
  basis set (scenario data, not a hint).
- **Generic stems cleared two PRE-EXISTING MEDIUM stem_echo flags** (s3-q017,
  s3-q052): both had descriptive stems re-using the keyed option's vocabulary
  ("list … alphabetical order", "DEFAULT … every shot"); "What angles do the two
  gates in `bound` receive?" / "What outcome (order `c1 c0`) appears on every shot?"
  remove the echo. stem_keyword_overlap 0.242 -> 0.221; 9 low length flags
  unchanged, 0 blockers/warnings.
- Honest re-rating 13/28/8 -> 30/18/1 (2->1 ×16, 3->2 ×6, 3->1 ×1: s3-q051, a
  reused Parameter is one parameter). Only s3-q026 stays at 3. Stem median 22 -> 10
  words, max 41 -> 19. As in s1/s2, hard items must come from R2 adds.

## Realism audit R1 — s4 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

- 19/41 s4 questions are executed; all re-ran PROVEN. The 22 conceptual items were
  re-checked against freshly fetched guides/execution-modes, choose-execution-mode,
  run-jobs-session, run-jobs-batch and initialize-account; all supported except
  s4-q020 (below). s4-q030 gained guides/save-credentials (initialize-account only
  links to `save_account`, it never shows the call).
- **Correctness fix, s4-q020 (key B -> F): `mode=backend` inside an open
  `Session`/`Batch` does NOT force job mode any more.** Runtime release notes 0.34.0:
  passing a backend as the mode while a session context manager is open now runs the
  job INSIDE that session/batch; a backend different from the session's raises.
  Source (0.48, `base_primitive.get_mode_service_backend`): for an `IBMBackend` with
  `get_cm_session()` open it logs a warning and returns the session as the mode, or
  raises `ValueError("The backend passed in to the primitive is different from the
  session backend…")`. A plain `BackendV2` (every fake backend) still goes to job mode
  via `QiskitRuntimeLocalService` — so this is NOT locally provable with fake
  backends and the stem must say "real IBM QPU". The run-jobs-batch Caution ("If you
  set `backend=backend` in a primitive, the program is run in job mode, even if it's
  inside a batch or session context") is about the deprecated `backend=` KEYWORD,
  not `mode=backend` — never cite it for `mode=`. Rated 3 (subtle, doc-misleading).
- **Correctness fix, s4-q046 (pool distractor F): a `(3, 1)` value array on a
  ONE-parameter circuit is three parameter SETS, shape `(3,)`** — a trailing axis of
  size `num_parameters` is consumed (`BindingsArray.coerce`: `(3, 1)` -> `(3,)`,
  `(5, 1)` -> `(5,)`, but `(1, 6)` -> `(1, 6)`, `(1, 4)` -> `(1, 4)`). So
  "`(3, 1)` params x `(3,)` observables" is ZIP (evs `(3,)`), not a product; the
  stored proof scored the RAW array shape and missed the second correct answer
  (its own evidence printed `evs (3,)`). F is now `(2, 3)` x `(3,)` -> `(2, 3)`; the
  proof scores the coerced `BindingsArray` shape. **This corrects the 2026-07-26
  entry above** ("`(3, 1)` x `(3,)` -> `(3, 3)`" is false for a one-parameter
  circuit). `data/study/s4.json` repeats the false claim in its s4-q046 fact
  ("`(3, 1)` against `(3,)` is a product") — outside the audit's write scope,
  flagged to the orchestrator. Rule: broadcasting options that quote shapes must
  avoid a trailing size-1 parameter axis, or say "parameter-value-set shape".
- Self-containedness: s4-q047/q048 stems now state that `circuit` has one parameter
  (the value-array coercion depends on it; the figures' shape captions already
  agreed). Stem-only edits, no re-render.
- **Glosses removed, rated with the hint gone:** s4-q018 ("pads it to the device's
  qubit count"), s4-q044 ("Ideally the Bell state gives +1"), s4-q036 ("skips a
  step"), s4-q012 ("built with abstract gates"). Kept deliberately: s4-q026 device
  size + line topology (option A's refutation), s4-q011 "return separate results"
  (option E's refutation).
- **Stem-echo trap hit once:** "Which execution mode do the best practices recommend
  for a single primitive request?" raised a NEW MEDIUM `stem_echo_tell` on s4-q035
  (key repeats "single primitive request"); reworded to "one small, standalone
  experiment". stem_keyword_overlap 24.7 % -> 21.6 %; 7 low length flags (was 8:
  s4-q020's keeper flag vanished with the re-key), 0 blockers/warnings.
- Honest re-rating 13/22/6 -> 29/11/1. Stem median 26 -> 14 words, max 59 -> 26.

## Realism audit R1 — s5 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

- 29/34 s5 questions are executed; all re-ran PROVEN with the stored keys (before and
  after edits). The five conceptual items were re-checked against freshly fetched
  pages: guides/sampler-noise-management (Sampler supports exactly dynamical
  decoupling + Pauli twirling — supports s5-q021/q034/q037), guides/primitives
  ("Sampler samples the output register" — s5-q030),
  guides/error-mitigation-and-suppression-techniques (TREX/ZNE/PEC/PEA are
  expectation-value techniques reached through Estimator resilience options — q037
  distractors C/E). No key changes.
- **Citation gaps fixed:** s5-q038 (1/sqrt(N) shot error) cited guides/primitives and
  sampler-input-output, neither of which states the scaling; added guides/estimator-options
  (default precision 0.015625 = 1/sqrt(4096)). s5-q021/q037 (do-it-yourself readout
  correction) gained tutorials/readout-error-mitigation-sampler (M3 on Sampler counts),
  which the old citations never mentioned.
- **Display-letter references removed (process-rule violations):** s5-q022's CODE comment
  said `obs` was "only used by option C" — the obs-using option is stored key A, and the
  site shuffles letters anyway; now "(used only by the Estimator-style tuple)". s5-q034's
  explanation said "(A)"/"(B)" for keys C/E. s5-q027's explanation named `readout` as a
  non-field; it now names the actual pool distractors (`readout_symmetrization`,
  `shots_per_twirl`).
- **Preflight hazard:** `question_flags(q)` on the raw question returned no flags for the
  trimmed s5-q023, yet the section audit raised a NEW MEDIUM `stem_echo_tell` — the audit
  evaluates every `display_variants(q)` subset (dc=5 here, the variant without the
  high-overlap distractor D tripped it: key C overlap 4 vs 2, all from the CODE tokens).
  Preflight over display variants, not the stored question. Fixed by a stem using the
  term "broadcast" (shared with distractors A/E), not by touching code.
- **Glosses removed, rated with the hint gone:** s5-q019 (in-stem DD definition), s5-q014
  ("hoping to turn on error mitigation" framing), s5-q023 ("when `get_counts()` is called
  with no index"), s5-q042 ("binds three angles … in a single PUB"). Kept deliberately:
  s5-q018 "2 free parameters" and s5-q029 "2-qubit" (distractor refutations depend on
  them), s5-q041 "one of the four outcomes never occurs" (figure alt texts and option E
  depend on it), s5-q011 `measure_all()` (the `meas` field name depends on it).
- Honest re-rating 9/18/7 -> 22/12/0 (19 changes; 3->1 on s5-q026: PUB shots beating
  `default_shots` is one recalled fact). No genuinely 3-level item remains; as in s1-s4,
  hard items must come from R2 adds. Stem median 23 -> 11 words, max 39 -> 18.
  Meta-audit unchanged: the same 6 low `length_tell` keepers, 0 blockers/warnings,
  stem_keyword_overlap 26.0 % -> 26.8 %.
- **Future drift (runtime 0.50, NOT re-keyed):** live docs now import
  `qiskit_ibm_runtime.executor_sampler.Sampler` ("client-side primitive introduced in
  0.50.0"), label `SamplerV2` "legacy server-side", and state "The Executor primitive does
  not support local testing mode" (every s5 proof runs on fake backends). guides/primitives
  already links SamplerV2 to `executor-sampler-sampler`. When the bank re-pins, re-verify
  the options tree (s5-q019/q020/q027/q031/q033), `run()` signature (q001/q022) and the
  fake-backend figure items (q040-q042).

## Realism audit R1 — s6 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

- 22/33 s6 questions are executed; all re-ran PROVEN with the stored keys before and
  after edits. The 11 conceptual items were re-checked against freshly fetched
  guides/estimator-noise-management (level table 0/1 [default] TREX/2 = level 1 + ZNE +
  gate twirling, "higher levels … more accurate … longer processing times", manual
  options "applied in addition to" the level base set — supports s6-q028/q029/q034),
  guides/error-mitigation-and-suppression-techniques (DD suppresses on idle qubits;
  ZNE amplify-then-extrapolate, "not guaranteed to produce an unbiased result"; PEC
  "returns an unbiased estimate … generally incurs a greater overhead";
  `zne_mitigation = True`, `dynamical_decoupling.enable = True` — supports
  q019/q021/q026/q032/q039), guides/estimator-options (precision resolution order PUB >
  `run()` > options, `default_precision` 0.015625 = 1/sqrt(4096) — supports q038) and
  guides/primitive-input-output (Estimator PUB "at most four values", precision fourth;
  `apply_layout` usage — q018/q036). No key changes, no correctness fixes.
- **Citation gap fixed, s6-q036:** neither cited guide says WHAT `apply_layout` does
  (specify-observables-pauli never mentions it; primitive-input-output only calls it).
  Added api/qiskit/qiskit.quantum_info.SparsePauliOp ("Apply a transpiler layout to
  this SparsePauliOp").
- **Proof-scoring note (no fix needed, verified by hand):** several predict-output
  proofs write evidence for their SHAPE/TYPE pool distractors without scoring them
  (q011 F, q015 E/F, q022 E/F, q023 F, q035 E/F — the `proven` list can never contain
  them). Re-executed independently: evs shapes `()`, `(2,)`, `()` float64, `(3,)`
  (a `(3, 1)` value list on the one-parameter q023 circuit coerces to 3 sets, so F
  `[[1.0], [0.0], [-1.0]]` is correctly wrong). A future proof-hardening wave should
  score these from the observed shape, as the s4-q046 fix did.
- **Glosses removed, rated with the hint gone:** s6-q017 ("precision is the target
  standard error" handed over the 1/sqrt(N) step), s6-q037 ("computes exact
  expectation values" also echoed key A), s6-q011 (Bell state), s6-q015 (X on qubit 0
  only), s6-q027 (Z on qubit 0 plus Z on qubit 1), s6-q019 (ensemble post-processing
  definition; "bias" kept, it refutes the shots option). Kept deliberately: s6-q013
  "5-qubit backend" (options D/F refute against the width), s6-q023 "one-parameter
  circuit" (option F's coercion depends on the parameter count), s6-q042 figure
  legend/axes carry the group/bar description the trimmed stem dropped (alt text
  unchanged).
- **Stem-echo trap hit once:** s6-q025 trimmed to "Meant as a precision of 0.01, this
  PUB raises …" raised a NEW MEDIUM `stem_echo_tell` (key C overlap 4 vs 2:
  precision/PUB/0.01) in one dc=4 variant. Fixed by describing the intent in words no
  option uses ("Intended as a target standard error, the `0.01` here …").
- Honest re-rating 8/18/7 -> 20/12/1 (17 changes; 3->1 on s6-q034: the documented
  cost/accuracy trade-off is one recalled fact). Only s6-q042 (broadcasting +
  one-parameter coercion + SparsePauliOp-is-one-observable, read from a figure) stays
  at 3. Stem median 21 -> 10 words, max 47 -> 26. Meta-audit unchanged: the same 7
  low `length_tell` keepers, 0 blockers/warnings, stem_keyword_overlap 24.5 % -> 21.7 %.
- **Future drift (runtime 0.50, NOT re-keyed):** every fetched s6 guide now imports
  `qiskit_ibm_runtime.executor_estimator.Estimator` (client-side, 0.50.0) and labels
  `from qiskit_ibm_runtime import Estimator` "legacy server-side"; options come from
  `qiskit_ibm_runtime.options_models`; PEA/PEC on the client-side Estimator need a
  separate noise-learning job (`resilience.layer_noise_model`). When the bank re-pins,
  re-verify the options-path items (q014/q016/q020/q026/q031/q039/q041), the
  `run()` keyword surface (q012/q016), the level/default claims (q028/q029/q034) and
  the fake-backend figure item q041 (Executor primitives do not support local mode).

## Realism audit R1 — s7 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

- 23/29 s7 questions are executed; all re-ran PROVEN with the stored keys before and
  after edits. The six conceptual items were re-checked against freshly fetched
  guides/save-jobs (`service.jobs(created_after=…)` filters, Workloads page lists IDs,
  `service.job(job_id).result()`, RuntimeEncoder/`json.dump` + RuntimeDecoder/`json.load`;
  example `j.status() == "DONE"` — supports s7-q026/q027/q033), guides/monitor-job
  (`job.result()` "blocking call until complete", `job.cancel()` for queued or running
  jobs, "cannot be resumed" — q028/q033) and api/qiskit-ibm-runtime/session (details()
  key list, `state` open/active/inactive/closed, status() wording — q030/q035). The
  session page now renders the stable/0.50 source; the installed 0.48 `Session.details`
  returns the same 14 keys and `status()` derives its wording from `state` +
  `accepting_jobs` (it also maps server states `pending_inactive`/`pending_closed`,
  undocumented). 0.48 `RuntimeJobV2.result()` on a CANCELLED job raises
  `RuntimeInvalidStateError` and there is no `stop()` / `QiskitRuntimeService.cancel` —
  q028 distractors confirmed from source. No key changes.
- **Correctness fix (displayed code), s7-q036:** the stem code used `QuantumCircuit`
  without importing it, so the snippet "whose output you predict" raised `NameError`
  (the proof had its own import and passed). Added `from qiskit import QuantumCircuit`;
  re-executed the shown code: `True PrimitiveResult SamplerPubResult` (key F). Rule:
  for predict-output items, exec the DISPLAYED code, not only the proof — a proof can
  be complete while the stem code is not.
- **"What does this code print?" can misstate a float key:** s7-q020's code prints
  `0.9999999999999998`, so a print stem would make key `1.0` wrong; kept "What does
  `result[0].data.evs` hold?". s7-q011 prints `2000 3` while options read
  `num_shots=2000, num_bits=3`, so its stem names the attributes instead. Check the
  literal stdout before converting any stem to a "print" question.
- **Proof scoring check:** q022's non-numeric branch can never prove an option, but all
  five refuted paths raise (AttributeError/KeyError) — no hidden second answer. Every
  other s7 proof scores all keys, pool distractors included.
- **Glosses removed, rated with the hint gone:** s7-q012 ("raw packed"), s7-q014 ("X to
  qubit 0 only"), s7-q015 ("outcomes are only 000 and 111"), s7-q017 ("qubits 1 and 2
  stay |0>"), s7-q025 (H/CX/measure_all recipe). Kept deliberately: s7-q013 "actually
  achieved" (refutes `target_precision`), s7-q016 "new BitArray … keeping every bit"
  (refutes the list comprehension and `slice_bits`), s7-q019 256/3-bit/5-qubit (options
  A/C/E), s7-q021 "one-parameter" (the `(4, 1)` coercion), s7-q029 the `a`/`b` counts
  definition (options use them), s7-q030 "live service" (`details()` is None locally),
  s7-q033 "0.4x" (string status is version-specific). Figure items q037/q038: stem-only
  edits, alt texts never depended on the dropped wording, no re-render.
- Honest re-rating 5/18/6 -> 18/10/1 (18 changes, no 3->1). Only s7-q021 (one-parameter
  `(4, 1)` coercion) stays at 3. Stem median 28 -> 15 words, max 35 -> 21. Meta-audit
  unchanged: the same 6 low `length_tell` keepers (q015/q020/q023/q024/q028/q036),
  0 blockers/warnings, stem_keyword_overlap 26.4 % -> 26.2 %. Pre-existing, unchanged:
  `position_C` 40.9 % EV (36.6 % est.) is below the verdict threshold but the highest
  position bias in the section — an R2 add should not key C.
- **Overlap (kill/merge candidates, not removed):** q033 & q034 both hinge on
  "RuntimeJobV2.status() is a string, not a JobStatus enum"; q022 & q038 test the same
  `result[0].data.evs` path (q038 is the figure wrapper); q023, q024 & q037 all test
  "index the PUB before `.data`".
- **Future drift (runtime 0.50, NOT re-keyed):** monitor-job now compares
  `str(job.status()) == "DONE"` (the str() hints the 0.50 executor jobs may not return a
  bare string) — re-verify q033/q034 on re-pin. Executor primitives do not support local
  testing mode, so every fake-backend/StatevectorSampler proof stays a 0.48/SDK fact;
  q013 (EstimatorV2 on FakeManilaV2, `default_precision`) is the most exposed.

## Realism audit R1 — s8 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

- 13/20 s8 questions are executed; all re-ran PROVEN with the stored keys before and
  after edits. Displayed code was exec'd too: every non-fragment snippet runs as shown
  (q013/q021 raise exactly the error their stems/comments name; q011/q012/q015 are
  deliberate `...`/comment fragments). Every proof scores all six keys.
- The seven conceptual items were re-checked against freshly fetched pages:
  guides/qasm-feature-table (Qiskit SDK column = parse via `qasm3.loads` +
  represent + export; `bit` ✅ note 3 -> `ClassicalRegister`; `int`/`angle`/`complex`/
  `const`/`duration` ❌; note 6 duration/stretch unparseable; note 9 unbound
  `Parameter` -> `input float[64]` — supports q022, q020's explanation),
  guides/cloud-setup-rest-api (IAM `POST https://iam.cloud.ibm.com/identity/token`,
  apikey grant, `expires_in: 3600`, `authorization: Bearer` + `Service-CRN` — q023/q025),
  guides/sampler-rest-api (`POST /api/v1/jobs`, `'program_id': 'sampler'`,
  `GET …/jobs/{id}/results` — q024/q028), api/qiskit-runtime-rest/tags/jobs, and the
  OpenQASM spec types.rst via raw.githubusercontent (angle[size], `complex[float[n]]`,
  const widths, bit[n]->uint[m] only n==m, bool/bit interchangeable, no casts to/from
  duration, float->angle = nearest mod 2pi ties-to-even, lesser operand promoted; no
  char/string/real/unsigned — q026/q027). All supported; no key changes.
- **Display-letter references removed (process-rule violations):** both multis'
  `explanation.correct` cited stored keys in parentheses — s8-q022 "(B)/(D)/(F)",
  s8-q025 "(C)/(E)". Removed; the prose already names each fact.
- **Glosses removed, rated with the hint gone:** s8-q019 ("built from a named
  sub-circuit and appended with `to_gate()`" — visible in code), s8-q016 ("2 qubits and
  3 classical bits" — kept in the code comment), s8-q028 ("no Qiskit installed",
  "kept the `id`"). Kept deliberately: s8-q015 "begins `OPENQASM 3.0;`" (refutes the
  header-accepted/parse-later distractor), s8-q013 "same conditional circuit" (refutes
  `str(qc)`/`decompose`), s8-q021 qiskit-installed/extension-missing premise, s8-q022 a
  compressed definition of the table's Qiskit SDK column (option D's "neither parse
  nor represent" leans on it), s8-q028 "has finished" (option A's "once the job is
  done"). s8-q010 became "What does this code print?" — literal stdout matches key C
  except the trailing newline (invisible in a code block; proof compares rstrip).
- Honest re-rating 6/11/3 -> 12/7/1 (9 changes: 2->1 q012/q013/q016/q020/q021/q026,
  3->2 q019/q022). Only s8-q017 (silent global-phase drop + `__eq__` includes phase)
  stays at 3. Stem median 27 -> 14 words, max 52 -> 22. Meta-audit unchanged: the same
  4 low `length_tell` keepers (q010/q013/q020/q021), 0 blockers/warnings,
  stem_keyword_overlap 15.2 % -> 16.2 %. Keys A5/B4/C4/D4/E1 single-answer — an R2
  add should not key A.
- **Future drift (NOT re-keyed):** the jobs REST reference now lists Executor and
  NoiseLearnerV3 `params` schemas next to SamplerV2/EstimatorV2 — re-verify q024
  (`program_id` values) on re-pin. Feature-table notes are dated "as of July 2025,
  qiskit-qasm3-import v0.6.0"; if the venv ever gains that package (or Qiskit's native
  `qasm3.loads_experimental` becomes the default loader), q021 (and q012's option E,
  q015's D-wording) must be re-proven. **Verified 2026-10-01 in the pinned venv:
  `qiskit.qasm3.load_experimental`/`loads_experimental` EXIST in 2.5.0, are native
  (no extension needed), emit `ExperimentalWarning`, and parse a simple
  `qubit`/`bit`/`h`/`measure` program.** So "qiskit ships no OpenQASM 3 importer" is
  false as a blanket claim — only `load`/`loads` need the extension. q021 stays correct
  (its code calls `loads`); never key or write a distractor saying Qiskit cannot read
  OpenQASM 3 at all without the extension. sampler-rest-api's own sample uses OpenQASM 3
  with `qreg`/`creg`, which is not q010/q016 territory (those are exporter output).

## R2 expansion — s1 (2026-10-01, qiskit 2.5.0)

Twelve adds s1-q055..q066 (d1 ×2, d2 ×5, d3 ×5; 5 figure items). Measured in the pinned venv:

- **`Operator(qc).dim` is the tuple `(2^n, 2^n)`** — `(8, 8)` for a 3-qubit circuit even
  when one qubit is idle; `input_dims()` is the per-qubit `(2, 2, 2)`. Safe d1 distractor pair.
- **`SparsePauliOp(["X","Z"]) @ itself`** is the operator product (not tensor): raw terms
  `['I','Y','Y','I']` coeffs `[1, -1j, +1j, 1]`; `.simplify()` -> `['I']` coeff `2`. The
  anticommuting cross terms cancel; `a.tensor(a)` is the 2-qubit `XX+XZ+ZX+ZZ` distractor.
- **`qc.inverse()` of `h; s` is `sdg; h`** (gate list), drawn S† then H.
- **`circuit.compose(circuit.inverse())` keeps the parameter count**: `inverse()` reuses the
  same `Parameter` objects (`real_amplitudes(3, reps=2)` -> 9 before and after).
- **`XGate().control(1, ctrl_state=0)` appended on `[1, 0]`** = control q1 (drawn as an
  OPEN circle), target q0; renders 5779 B vs 5786 B for the control-on-q0 variants.
- **`real_amplitudes(3, reps=1, entanglement=...)` CX lists**: full `[(0,1),(0,2),(1,2)]`,
  circular `[(2,0),(0,1),(1,2)]` (same as `sca` at reps=1), linear `[(0,1),(1,2)]`
  (= `pairwise` for 3 qubits — never offer both), reverse_linear `[(1,2),(0,1)]`.
  mpl sizes 20699 / 20694 / 18655 / 18655 B: keyed `full` is the strict-largest at 0.02 %.
- **`probabilities_dict(qargs=[2, 0])`: `qargs[0]` is the RIGHTMOST key bit.** For x(0) on
  3 qubits: `[2, 0]` -> `'10'`, `[0, 2]` -> `'01'`. Raw value 0.9999999999999998 — say
  "rounded" in stems.
- **`PauliEvolutionGate(op, time=t)` = exp(−i t op), no ½.** XX at t = π/6 on |00⟩ ->
  `{00: 0.75, 11: 0.25}`; `RXXGate(π/6)` (the ½ convention) -> 0.933/0.067; RX(π/3) on
  each qubit -> 0.5625/0.1875/0.1875/0.0625. `cx(0,1); rz(π/3, 1); cx(0,1)` is EXACTLY
  (`Operator.__eq__`) `PauliEvolutionGate(SparsePauliOp("ZZ"), time=π/6)`; ZZ π/3, ZI, IZ,
  XX at π/6 are all not equivalent.
- **`Operator(b).compose(Operator(a))` runs b first**; with b = `x(0); cx(0,1)`, a = `h(0)`
  from |00⟩ -> `{'10': .5, '11': .5}`; reversed order gives a Bell pair.
- **Phase kickback** `x(1); h(1); h(0); cx(0,1); h(0); h(1)` -> `{'11': 1.0}` exactly.
- **Audit lists cross-question duplicate option texts with their roles** — a value keyed
  correct in one item and wrong in another (two dict-output items sharing
  `{'01': .5, '11': .5}`) is reported even with 0 flags. Re-pick the answer space instead
  (s1-q063 moved to a deterministic `{'11': 1.0}` circuit).

## R2 expansion — s3 (2026-10-01, qiskit 2.5.0)

Fourteen adds s3-q059..q072 (d1 ×1, d2 ×6, d3 ×7; 6 figure items — 5 option-image,
1 stem-figure). Measured in the pinned venv:

- **`QuantumCircuit.depth()` filters directives but they still SYNCHRONISE** (source
  comment: "it still functions as a data synchronisation point"): `h(0); barrier; h(1)`
  -> 2, not 1. `h;cx(0,1);barrier;x(2);cx(1,2);measure_all()` -> 5; barriers removed -> 4;
  `depth(lambda i: True)` -> 7 (== `size()` here, a coincidence); `len(data)` -> 9.
- **`switch(creg)` compares the whole register value, `c[0]` = LSB**: q0=1 measured into
  `c[1]`, q1=0 into `c[0]` -> value 2 -> `case(2)` (Aer). `switch` on a register builds fine.
- **`while_loop((clbit, 1))` repeat-until-success** (`h; measure` body) ends every shot on
  0; the same body under `if_test` gives ~75/25 — a measured misconception pair.
- **`assign_parameters({theta: 2*phi})` substitutes**: rx/ry(theta+phi) become `2*phi` /
  `3*phi` (symengine simplifies), `num_parameters` 2 -> 1. No error.
- **`a.compose(b)` with two distinct `Parameter("theta")` objects -> `CircuitError: name
  conflict adding parameter 'theta'`**; one shared object composes fine (1 parameter).
- **`decompose()` expands EVERY instruction one level** (swap -> 3 cx, x -> u, custom
  `to_gate()` -> its body), not just custom gates; `reps=2` turns the inner `h` into
  `U(π/2, 0, π)`. `append(gate, [2, 0])` maps gate qubit 0 -> q2.
- **Barrier at level 1** (`cx; barrier; cx; h(1); h(1)`, basis rz/sx/x/cx) ->
  `{'cx': 2, 'barrier': 1}`; level 0 -> `{'rz': 4, 'cx': 2, 'sx': 2, 'barrier': 1}`;
  without the barrier level 1 -> `{}`.
- **`cx; z(control); cx`: level 1 keeps 2 CX, level 2 -> 0 CX** (`{'rz': 1}`), stable over
  seeds 0-4. Level-1 optimization stage has `InverseCancellation` (adjacent only); level 2
  has `CommutativeCancellation` + `TwoQubitPeepholeOptimization` instead. Standalone
  `CommutativeCancellation` -> `{'z': 1}`. CAUTION: X on the CONTROL (`cx; x(0); cx`) at
  level 2 becomes `{'x': 2}` (X⊗X) — never key "X on the control blocks/cancels" naively.
- **`InverseCancellation([CXGate()])` cancels only CX**; with NO argument it uses a
  built-in self-inverse set (CX, ECR, CY, CZ, X, Y, Z, H, SWAP, CH, CCX, ...) and removes
  H/X pairs too (API page fetched 2026-10-01).
- **Routed-drawing trap (s3-q067):** with layout `[2,1,0]` on a 3-line, an input that
  already CONTAINS the routing swap (`h(0); cx(0,1); swap(1,2); cx(0,1)`) reproduces the
  routed drawing exactly — never offer "qc contained the SWAP" as a distractor on a
  reverse-engineer-the-input item.
- mpl if/else drawing: one box with If / Else sections, condition printed `c_0=0x1`;
  two separate `if_test`s with inverted conditions draw two If boxes (`0x1`, `0x0`).
- Craft: `must` is an absolute word (q060/q062 hit medium `absolute_distractor_tell`;
  "has to be" fixed it). q070 dc=4 needed two long distractors (high length_tell at 1.56
  until `{}` was replaced by a 34-char misconception dict). Image sizes: keyed figures
  are mid-pack or tied (q064 four-way 8415 B tie); s3 `smallest_image_option` stays
  low (6.2%) — a future figure wave should key a strict-smallest drawing.
- Answer keys of the adds: A3 B3 C3 D3 E2. Section meta-audit after: 0 blockers /
  0 warnings, same 9 pre-existing low length flags, no flag on any add.
- **s3-q066 reworked (orchestrator anti-duplication scan, 0.487 token-Jaccard vs an
  official sample item):** the `h(0); measure; if_test((clbit, 1)) as else_: X / H`
  shape is the canonical docs example and converges on the official item — avoid it in
  any wave. New shape: `QuantumCircuit(3, 1)`, `ry(π/3, 1)`, `measure(1, 0)`,
  `if_test((c0, 0)) as else_: cx(0, 2)` / `else_: swap(0, 2)`; key C. Renders: correct
  21605 B tied with the swapped-bodies variant, D 22388 B, B 18848 B (no image tell).

## R2 expansion — s4 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

Eleven adds s4-q050..q060 (d2 ×5, d3 ×6; 4 figure items — 3 stem-figure, 1 option-image;
8 executed, 3 conceptual). Measured in the pinned venv:

- **Primitive mode is resolved in the CONSTRUCTOR** (`BasePrimitiveV2.__init__` ->
  `get_mode_service_backend`). A `SamplerV2()` built inside `with Session(...)` / `with
  Batch(...)` stores that session; `run()` after the block exits raises
  `IBMRuntimeError: 'The session is closed.'` (the `_active_session` guard on
  `Session._run`; `__exit__` calls `close()`). Same message for a `Batch` (subclass).
  Locally provable with fake backends — the guard fires before the local service (s4-q052).
  Corollary for the s4-q020 entry: the "mode=backend joins the open session" check also
  happens at construction, so a primitive built BEFORE the `with` block keeps job mode
  (read from source, not executable locally — needs a real IBMBackend).
- **Broadcasting with a TWO-parameter circuit:** values `(4, 2)` = 4 sets; against
  observables `(3, 1)` -> `evs.shape (3, 4)`. Raw `np.broadcast_shapes((4, 2), (3, 1))`
  raises — the "not broadcastable" distractor is the raw-array misconception (s4-q050).
- **Sampler side of the one-parameter coercion:** `StatevectorSampler(seed=1).run([(qc,
  np.zeros((2, 3, 1)), 50)], shots=1000)` -> `meas.shape (2, 3)`, `num_shots 50` (PUB
  shots win, per set), `sum(get_counts().values()) == 300` (no-`loc` `get_counts` merges
  every set); `get_counts(loc=(0, 0))` sums to 50 (s4-q051).
- **GenericBackendV2 reproducibility needs TWO seeds:** `seed=` fixes the randomly drawn
  noise properties (e.g. cx error), `options.simulator.seed_simulator` fixes shot sampling.
  Backend seed alone -> counts differ run to run; sim seed alone on unseeded backends ->
  differ (0/15 identical at 4000 shots, new error rates every construction); both -> byte-
  identical. Proofs repeat each call 3x (s4-q053).
- **Runtime ISA check scope (`utils.is_simulator`):** validation runs only for
  non-simulator backends. `SamplerV2(mode=AerSimulator())` runs an untranspiled H/CX
  circuit; `AerSimulator.from_backend(FakeManilaV2())` passes the runtime check but Aer
  raises `AerError: unknown instruction: h`; FakeManilaV2 and GenericBackendV2 raise
  `IBMInputValueError`; `StatevectorSampler` has no target (s4-q059). The check is
  DIRECTIONAL on a directed coupling map: `GenericBackendV2(3, coupling_map=[[0,1],[1,2]])`
  rejects `cx(2, 1)`; it also rejects an un-translated `swap` (s4-q055).
- **Cross-device ISA:** an ISA built for FakeManilaV2 (line) with `initial_layout=[2, 3]`
  is rejected on FakeLimaV2 (T: 0-1, 1-2, 1-3, 3-4) with `cx on qubits (2, 3)`, but runs on
  FakeAthensV2 (line) — the check is structural, never a device-name check (s4-q054).
  Small fake backends (<=7 q) are ALL `cx` devices; lines: Athens/Bogota/Manila/Rome/
  Santiago; T: Belem/Burlington/Essex/Lima/London/Ourense/Quito/Valencia/Vigo;
  H (7 q): Casablanca/Jakarta/Lagos/Nairobi; Yorktown is the bow-tie.
- **`apply_layout(isa.layout)` uses the FINAL layout:** 3-line, level 0, coupling map only,
  `initial_layout=[1, 0, 2]`, `h(1); cx(1,0); cx(1,2)` -> `h[0], cx[0,1], swap[1,2],
  cx[0,1]`, final `[2, 0, 1]`; `SparsePauliOp("XYZ")` -> `ZXY` (initial-only `XZY`).
  **Physics cross-check hazard:** a probe state built from ry/rx/rz gave `<XYZ> = 0` for
  EVERY candidate label (degenerate, proves nothing) — use generic `u(θ, φ, λ)` product
  probes and assert the reference value is non-zero (s4-q056).
- Hand-drawn gate map (Graphviz absent): draw from `backend.coupling_map.get_edges()`
  and assert the undirected edge literal in both generator and proof (s4-q054).
- Craft: `must` inside a quoted error message ("A backend or session must be specified")
  tripped a MEDIUM `absolute_distractor_tell` — paraphrase error messages that carry
  absolute words. Three new low `length_tell` keepers (q053/q054/q058) moved
  `longest_option` 18.9% -> 20.7% (still below chance); `shortest_option` 32.0% -> 29.1%.
  0 blockers / 0 warnings, no high/medium flags, no cross-question duplicate options.
  q055 option renders 22.2-23.2 KB (keyed E second-largest, 2 B under A).
- Conceptual adds cite guides/execution-modes-faq (session usage = wall-clock commitment
  incl. interactive-TTL idle time and compilation; batch = quantum time only; execution
  lanes fill with batch jobs, no exclusivity) and guides/execution-modes + max-execution-time
  (interactive-TTL lapse DEACTIVATES, job must re-queue to reactivate within max TTL).
  s4-q060 uses different numbers from the FAQ's lanes example on purpose.
- Answer keys of the adds: A2 B2 C2 D1 E3 + multi {B, D}.

## R2 expansion — s5 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

Eight adds s5-q044..q051 (d2 ×3, d3 ×5; 3 figure items — 2 option-image histograms,
1 stem-figure histogram; 7 executed, 1 conceptual). Measured in the pinned venv:

- **`SamplerPubResult.join_data()` puts the FIRST-declared register on the LOW (right)
  end.** `QuantumCircuit(q, out[2], anc[1])`, q1 = q2 = 1, q0 -> out[0], q1 -> out[1],
  q2 -> anc[0]: `join_data()` -> `{'110': 50}` (anc + out); `join_data(["anc", "out"])`
  -> `'101'`. Same layout as `BitArray.concatenate_bits([out, anc])` and as Aer's legacy
  `'1 01'` counts minus the space. **Docstring hazard:** it says the first name "is placed
  to the left of" the next — that means lower bit INDEX, which PRINTS on the right. Key on
  execution, explain via bit indices (s5-q044). `names=None` is legal (no error).
- **`BitArray.postselect(indices, selection)`**: indices are bit indices (`meas[i]`, same
  as `slice_bits`), `selection` lists the values to KEEP, result keeps `num_bits` (3 -> 3)
  and is flattened to shape `()`. Seeded `StatevectorSampler(seed=3)` 400 shots of
  `h0; cx01; h2; measure_all` -> `{'000': 96, '111': 92, '100': 117, '011': 95}`;
  `postselect([2], [0])` -> `{'000': 96, '011': 95}` (s5-q045).
- **`slice_bits([1, 2, 3])` on `1101`** -> `'110'`; character slicing gives `101`,
  list-order string `011`, `slice_shots([1, 2, 3])` -> `{'1101': 3}` (s5-q050).
- **Shot precedence is per PUB, then multiplied by the set count:** FakeManilaV2,
  `default_shots = 300`, `run([(a, None, 100), (b_2param, zeros((3, 2)))], shots=200)` ->
  PUB 1 `num_shots 100`, PUB 2 shape `(3,)` x 200; total 700. Without `shots=` PUB 2 takes
  300 per set — `default_shots` IS honored locally as the last fallback (s5-q046).
- **Twirling allocation (TwirlingOptions 0.48 API page, fetched 2026-10-01):** with
  `num_randomizations` fixed and `shots_per_randomization="auto"` -> `ceil(shots /
  num_randomizations)`; both auto -> `max(64, ceil(shots/32))` then num = ceil(shots/spr);
  PUB/run shots are "always obeyed", twirling product outranks only `default_shots`.
  guides/sampler-options (0.50 docs) adds: the job FAILS if the twirling product is smaller
  than PUB/run shots — a future d3 candidate. The live guide now lists Sampler
  `twirling.enable_gates`/`enable_measure` default False and `default_shots` default None
  (0.50 drift; the 0.48 API page agrees on the twirling False defaults) (s5-q047, conceptual).
- **Crossed measure mapping:** `QuantumCircuit(3, 3); x(0); h(1); measure(0, 2);
  measure(1, 0)`, `StatevectorSampler(seed=5)` 400 shots -> `{'101': 191, '100': 209}`;
  the unwritten `c[1]` prints 0, keys stay 3 bits (s5-q048).
- **Readout inversion check in Aer:** `ReadoutError([[0.95, 0.05], [0.10, 0.90]])` on a
  state with true P(1) = 0.300 reads raw 0.305 (200k shots, `seed_simulator=42`, within
  0.004) — `SamplerV2(mode=AerSimulator(noise_model=...))` runs untranspiled `ry` fine
  (s5-q051).
- Marginal from a histogram: `ry(2π/3, 0); ry(π/3, 1)`, `StatevectorSampler(seed=1)` 1000
  shots -> `{'00': 175, '01': 555, '10': 73, '11': 197}`; P(q0 = 1) = 0.752 via
  `slice_bits([0])` (s5-q049).
- Craft: histogram option families with 2 bars each render 12.7-13.7 KB (2-bit-key and
  1-bar variants are the smallest); keyed s5-q048 ties two distractors at 12858 B. All-tie
  bare-value options (dict literals, numbers) are free length ballast. Adds moved
  `numeric_middle` 49.5% -> 44.1%, `largest_image_option` 56% -> 44%,
  `smallest_image_option` 25% -> 17% (6 image questions — a later wave should key a
  strict-smallest drawing). Same 6 low `length_tell` keepers, 0 blockers/warnings, no
  cross-question duplicates, no flag on any add. Answer keys of the adds: A1 B2 C1 D2 E2.

## R2 expansion — s6 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

Nine adds s6-q043..q051 (d2 ×4, d3 ×5; 3 figure items — 2 stem-figure, 1 option-image;
7 executed, 2 conceptual). Every executed proof scores EVERY option key (string/print
claims compared to captured stdout, raise-claims scored from the observed run). Measured:

- **`SparsePauliOp(["ZI","IZ"]).compose(itself).simplify()` = `2·II + 2·ZZ`** — commuting
  cross terms ADD (contrast the s1 anticommuting `["X","Z"]` case where they cancel). On a
  Bell state `[H, H2]` prints `[0. 4.]`; `H.tensor(H)` in the same observables list raises
  `ValueError: The number of qubits must be the same for all observables` (s6-q043).
- **`BackendEstimatorV2` circuit count = Σ over parameter sets of qubit-wise-commuting
  groups of the Paulis that set needs.** It merges every Pauli the broadcast assigns to a
  set, then `group_commuting(qubit_wise=True)`. Observables `(2,)` × one-parameter values
  `[[0.3],[1.2]]` (2 sets, shape `(2,)`) ZIP: set 0 gets `ZZ/XX/YY` (3 groups), set 1 gets
  `ZI/IX` (1 group) -> AerSimulator.run receives **4** circuits in one call (s6-q044).
  Counting hook: wrap `backend.run` on an `AerSimulator(seed_simulator=7)`.
- **Runtime `EstimatorV2(mode=AerSimulator())` (local mode) -> BackendEstimatorV2:**
  `precision=0.05` -> `metadata['shots'] == 400` (`ceil(1/p²)`), `target_precision 0.05`;
  `stds = Σ|c_i|·sqrt(1 − <P_i>²) / sqrt(shots)`. On |+⟩: Z stds ≈ 0.0499–0.0500 over seeds
  1–3, X stds exactly 0.0 (eigenstate). Untranspiled `h` runs (simulator: no ISA check) (s6-q045).
- **ZNE result fields (ZneOptions docstring, identical in installed 0.48.0 source and the
  live 0.50 API page):** `evs_noise_factors`/`stds_noise_factors`/`ensemble_stds_noise_factors`
  shape `(*pub_shape, num_noise_factors)`; `evs_extrapolated` `(*shape, num_extrapolators,
  num_evaluation_points)`; `extrapolated_noise_factors` defaults to `[0, *noise_factors]`;
  `"fallback"` returns the lowest-noise-factor raw value; default extrapolators
  `("exponential", "linear")`, `evs` = first successful. `zne.noise_factors = (1, 3, 5, 7)`
  is accepted in 0.48 (s6-q046, s6-q050 — both conceptual: ZNE is server-side).
- guides/estimator-input-output (fetched 2026-10-01) is a good s6 citation: commuting
  observables in one PUB grouped via `group_qubit_wise_commuting`, different PUBs never share
  a measurement; stds vs `ensemble_standard_error`; ZNE stds = fit uncertainty at factor 0.
- **`from_sparse_list([("ZX", [0, 2], 0.5)], num_qubits=3)` -> `XIZ`** (characters pair with
  indices left to right) (s6-q048). **Dict and str observables are coerced**:
  `[{"ZI": 2.0, "IX": 1.0}, "XZ"]` -> `evs` shape `(2,)`, the dict is ONE weighted
  observable (s6-q049).
- **3-qubit reversed-label hazard:** reading `IXX` qubit-0-first probes qubits 1 and 2, not
  "the same pair" — the first draft of s6-q047's endianness distractor was mis-derived by
  hand; the proof's assert caught it. Always compute reversed-label variants by executing
  `label[::-1]`, never by hand.
- `np.round(evs, 3)` print forms used as options: `[-1.  0. -1.  0.]`, `[ 0. -1.]`,
  `[-0.333  0.   ]` (numpy pads); compare the captured stdout, not the floats.
- Craft: s6-q051 option renders 21888–21892 B (keyed E tied with B/C at 21890; A smallest)
  — no image tell, but the "strictly smallest correct drawing" wish was NOT met (byte
  sizes move by 2 B with bar heights; not worth a contrived variant). A first q049 draft
  shared `[0. 0.]` with q043 (both wrong) — replaced by the weighted-average
  misconception. Bare numeric options `3`/`2` on s6-q044 coincide with s3-q031 (benign).
  Section audit after: 0 blockers / 0 warnings, the same 7 pre-existing low `length_tell`
  keepers, no flag on any add; `shortest_option` 20.2% -> 21.1%, `position_C`
  36.6% -> 34.7%. Answer keys of the adds: A2 C2 D2 E3 (B avoided — it led s6 with 9).

## R2 expansion — s7 (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

Six adds s7-q039..q044 (d2 ×2, d3 ×4; no figures; 5 executed, 1 conceptual; 2 session-
concept items q039/q042). Measured in the pinned venv:

- **The REAL `QiskitRuntimeService.jobs()/job()` can be executed offline:** the harness
  patch replaces the class, but `importlib.reload(qiskit_ibm_runtime.qiskit_runtime_service)`
  restores it; `object.__new__(cls)` + `_active_api_client = <in-memory stub with
  jobs_get/job_get and _instance=None>` + `_api_clients = {}` runs the library's own paging
  and `_decode_job` (omit `"backend"` from raw job dicts). Server-side filters
  (`session_id`, `pending`, `descending`) are the stub's — cite the API docstring for those.
- **Default `limit=10` truncates silently:** 14 session jobs -> `jobs(session_id=sid)` 10
  (newest), `descending=False` 10 (oldest), `pending=False` 10; `limit=None` pages to all 14.
  **`limit=0` ALSO returns all 14** (`limit or 20` and `if limit:` treat 0 as no limit) —
  never offer it as a distractor. `service.job(session_id)` -> `RuntimeJobNotFound`.
- `RuntimeJobV2.session_id`, `creation_date`, `tags`, `primitive_id`, `inputs` are
  PROPERTIES; `job_id()`, `status()`, `backend()`, `metrics()`, `logs()`,
  `error_message()` are methods. Local-mode `LocalRuntimeJob.session_id` returns the JOB id
  and `Session(backend=fake).session_id`/`details()`/`status()` are None — never prove
  session-ID facts with local mode.
- **Errored job (subclass-pin trick, add `_result_decoders = []`, `_reason = None`,
  `_reason_code = None`):** `result()` returns control at once (no poll) and raises
  `RuntimeJobFailureError("Unable to retrieve job result. <msg>")`; `error_message()` returns
  the stored reason; CANCELLED raises `RuntimeInvalidStateError`. (Reason code 1305 maps a
  CANCELLED server state to ERROR and raises `RuntimeJobMaxTimeoutError` — unused.)
- **RuntimeEncoder/Decoder round trip is lossless for a multi-PUB Sampler result:**
  `PrimitiveResult`/`SamplerPubResult`/`DataBin`/`BitArray` types, shape `(3,)`, per-PUB
  `num_shots`, per-set counts and `metadata` (`{'shots': 50, 'circuit_metadata': {}}`,
  top-level `{'version': 2}`) all survive; Runtime EstimatorV2 local metadata
  (`target_precision`, `shots`) survives too (decodes as `PubResult`).
- **`BitArray.expectation_values` broadcasts against the bit array's shape:** bits `(2,)`
  with `["ZI", "IZ"]` ZIPS (`[-1. -1.]` for `ry(t,0); x(1)`, t ∈ {0, π}); `[["ZI"], ["IZ"]]`
  -> `(2, 2)`. Accepts `0`/`1` projector labels (`"1I"` = P(bit 1 = 1)).
- Estimator `(2, 1)` observables × `(3, 1)` one-parameter values -> `evs (2, 3)`
  (observables axis first). Proof hazard: angles 0.2/0.9/1.6 made sin 1.6 ≈ cos 0.2 within
  0.02 — the uniqueness assert caught it; use 0.5/1.0/2.5.
- Craft: a backticked `None` in an option counts as the absolute word "none" (medium
  `absolute_distractor_tell` on q043's first draft; a hedged second distractor did NOT fix it
  because pool variants drop it) — reword. An evidence string with `limit=20` (page size)
  tripped `lint_proof_drift`; describe internals in prose. Section after: 0 blockers /
  0 warnings, the 6 pre-existing low `length_tell` keepers + 1 new (q044, tied-longest
  `evs[1, 2]`/`evs[2, 1]`), no cross-question duplicate options, `position_C` 36.6% -> 33.5%,
  `longest_option` 19.2%, `shortest_option` 23.5%. Answer keys of the adds: A1 B1 D2 E2.

## R2 expansion — s2 + s8 (2026-10-01, qiskit 2.5.0)

Two d3 adds: s2-q047 (option-image, 5 Bloch-multivector renders, dc=4, key B) and
s8-q030 (mcq, dc=4, key E). Both executed. Measured in the pinned venv:

- **`plot_bloch_multivector` draws REDUCED-state vectors, shortened for entangled
  qubits.** `ry(2π/3, 0); cx(0, 1); h(1)` -> qubit 0 (0, 0, −0.5), qubit 1 (−0.5, 0, 0)
  (`_bloch_multivector_data` and `partial_trace` agree); probabilities 0.125/0.375 each
  on 00/01/10/11. The half-length arrows are clearly visible in the render. Variants:
  swapped roles `ry(T,1); cx(1,0); h(0)`; pure-state look-alike `x(0); x(1); h(1)`
  (full-length −z / −x); CX dropped `ry(T,0); h(1)` (q0 (0.87, 0, −0.5), q1 +x); sign
  error `... cx; x(1); h(1)` (q1 +0.5 x, q0 unchanged). Renders 216507–216509 B (keyed
  tied smallest with the swap variant). Avoided the s1-q051 "state from a product-state
  Bloch figure" shape on purpose.
- **qasm2 exporter accepts exactly one condition form:** an `if_test((register, int))`
  with no `else`, emitted `if (c == 1) x q[1];`. `(c[0], 1)`, `expr.equal(c, 1)`,
  `expr.logic_not(c)`, `expr.lift(c[0])` all raise `QASM2ExportError: 'OpenQASM 2 only
  supports register-equality conditions'`; an `else` raises `"OpenQASM 2 does not support
  'else' statements"`. `qasm3.dumps` exports all: `if (c == 1) {` for BOTH the tuple and
  `expr.equal(c, 1)` (identical line), `if (c[0]) {`, `if (!c) {`, `} else {`.
- **Tuple conditions skip the width check:** `if_test((c, 5))` on a 2-bit register builds
  and qasm2 exports `if (c == 5)`; `(c, True)` exports `if (c == 1)`. Never offer
  "value wider than the register" or a bool value as a refused distractor. By contrast
  `expr.equal(c, 7)` raises `TypeError: integer literal '7' is wider than the other
  operand`. `(c, 1.0)` / `(1, c)` / bare `c` raise `CircuitError` at construction.
- **Spec-vs-exporter hazard (do NOT build an item on it):** `expr.equal(a, b)` with
  `a` 2-bit and `b` 3-bit promotes `a` (explicit `Cast` to `Uint(3)`) and qasm3 emits
  `if (uint[3](a) == b)` — but the OpenQASM 3 spec (types.rst) only allows
  `bit[n] -> uint[m]` when n == m. Relational ops promote unequal widths;
  `expr.bit_and` of widths 2 and 3 raises `TypeError` ("same width"). `expr.logic_not(c)`
  carries an IMPLICIT bool cast that the exporter omits (`!c`).
- Craft: s8-q030 first draft had the keyed option strictly shortest in every pool
  variant (`shortest_option` 25.8% -> 29.7%); shortening the else-distractor to a tie
  brought it to 27.8%. Section audits after: s2 0/0, same 8 low length keepers; s8 0/0,
  same 4 low length keepers; no flag on either add.

## R3 proof hardening (2026-10-01, qiskit 2.5.0 / runtime 0.48.0)

- **Unscored pool distractors now scored (closes the R1 s6 deferral):** s6-q011 (F),
  s6-q015 (E/F), s6-q022 (E/F), s6-q023 (F) score EVERY option through one
  `printed_match(claim)` — the claim's array shape, complex-ness and values against the
  real `evs` (what `print()` shows is fixed by those three). Observed: q011 `()` vs F
  `(2,)`; q015 `(2,)` vs E `()` / F `(2, 1)`; q022 `()` float64 vs E `(1,)` / F
  complex128; q023 `(3,)` vs F `(3, 1)` (the one-parameter coercion, as in s4-q046).
  s6-q035 now wraps the call in try/except and scores E as "raised `QiskitError`"
  (nothing raises) and F as label == `'Z'` (stored `'IIZ'`). All five re-proved with
  the stored keys (C, B, D, A, D) — no disagreement, every `match=` flag computed.
- **Drift-lint findings (13 in s5/s6/s7) were all execution-derived false positives,
  not stale text:** every evidence string still describes its current option. The
  anchors were proof inputs or measured values the question never quotes (s5-q013
  ISA run total, s5-q025 `shots=200`, s5-q028 kept/total/DD-leak shot counts, s5-q033
  the local fallback shot count, s6-q017 shot budgets `BASE * m`, s6-q020 the
  `ZneOptions` repr `amplifier=Unset`, s7-q016/q018 BitArray shot/width numbers,
  s7-q024 the fixed counts). Cleared WITHOUT touching evidence wording, options or
  explanations: each proof now records those raw values in `observed`, which the lint
  treats as legitimate corpus. Trap hit once: adding a >=3-digit number to `observed`
  ARMS the lint's number check for that question — s5-q025's `shots_passed: 200`
  surfaced the B counts (`109`); recording `c_counts` too cleared it.
- Gates: verify_bank s5 36/36, s6 29/29, s7 28/28 PROVEN (exit 0, keys unchanged);
  audit_meta_patterns s5/s6/s7 0 blockers / 0 warnings, only the pre-existing low
  flags (6/7/7). Drift lint 19 -> 6 findings; the 6 left are outside R3 scope
  (s1-q027 C, s3-q021 A-D, s3-q025 D).

## Adversarial review R2 — s1+s2 (2026-10-02)

Scope: s1-q055..q066 (12) + s2-q047. Every distractor got a good-faith second-answer
attack, re-executed in the pinned venv (qiskit 2.5.0); all six figure items were
rasterized and inspected. **0 second-answer attacks stuck, 0 key changes, 0 kills.**

- **Proof weakness (figure items): the option-image proofs compared gate lists, not
  drawings.** s1-q060's tested fact — `ctrl_state=0` is drawn as an OPEN circle — is in
  no cited page, so the proof was adjacent to the claim. s1-q055/q060/q061 now render
  every variant AND the stem code with `draw("mpl")` to SVG text in-process
  (`matplotlib.rcParams["svg.hashsalt"]` fixed, `metadata={"Date": None}`) and require
  byte-identity with the stem's rendering for a match. Identical circuits render
  identically within one process; each keyed variant matches, every distractor differs.
  Adds ~1-3 s per proof. Reusable recipe for any "which diagram does this draw" item.
- **s2-q047 proof now cross-checks the drawer's own data:** each sphere vector from
  `partial_trace` is asserted equal to
  `qiskit.visualization.state_visualization._bloch_multivector_data` (the private helper
  `plot_bloch_multivector` plots) for all 5 variants. Private-API dependence is
  deliberate: if it moves, the proof fails loudly instead of drifting.
- **Citation failures (4), all replaced with pages verified to state the fact:**
  s1-q061 `api/qiskit/circuit_library` (no entanglement definitions; `real_amplitudes`
  delegates to `n_local`) -> `qiskit.circuit.library.n_local`; s1-q064 and s1-q065
  `guides/operators-overview` (never mentions PauliEvolutionGate, exp(-iHt) or the RZ
  half angle) -> `RXXGate` (exp(-i θ/2 XX), distractor A) and `RZGate`
  (RZ(φ) = exp(-i φ/2 Z)); s2-q047 `api/qiskit/visualization` (one-line listing) ->
  `qiskit.visualization.plot_bloch_multivector` ("each component of the sphere labeled
  'qubit i' is the expected value of the Pauli acting only on that qubit").
  Partial support kept, noted: s1-q060 citations support ctrl_state semantics and
  controls-first ordering but not the open-circle glyph (the proof now carries it).
- **Docs-reading trap:** the Statevector `probabilities([1, 0])` example confirms
  s1-q066 (`qargs[0]` = least-significant bit: `'+0'` -> `[0.5, 0.5, 0, 0]`), but an
  LLM summary of that page claimed the opposite. Read the example's numbers yourself.
  Same for `guides/operator-class` "A.compose(B) returns the operator with matrix B.A"
  (= A runs first, as s1-q062 keys) — summaries paraphrase it backwards.
- **Figure checks:** s1-q055/q060/q061 renders match their alt texts exactly;
  s2-q047 −x vs +x is readable from the x-axis label, half vs full length obvious. Quick
  Look (`qlmanage -t`) thumbnails crop wide SVGs to a square — the right-hand Bloch
  sphere looked clipped; the SVG itself is fine (clip rects inside the viewBox).
- **Difficulty:** all 13 ratings kept. Borderline noted: s1-q066 (d3) rests on one
  subtle semantic (qargs order) plus marginalization; kept under "subtle semantics".
- **s1-q027 option C drift finding:** execution-derived false positive (`phase=0.506`
  is the seeded run's measured P(1)). Cleared the R3 way: `p1_gp`/`p1_ref`/`p1_ry`
  recorded in `observed`; no claim or evidence text changed. Drift lint 6 -> 5 (left:
  s3-q021 A-D, s3-q025 D, out of scope).
- Gates: verify_bank s1 55/55, s2 37/37 (+1 conceptual) PROVEN, exit 0;
  audit_meta_patterns s1 0/0 (9 pre-existing low flags), s2 0/0 (8), none on the
  reviewed items; render_figures OK for all six figure qids.

## Adversarial review R2 — s3+s4 (2026-10-02)

Scope: s3-q059..q072 (14) + s4-q050..q060 (11), plus the two leftover drift-lint items
(s3-q021, s3-q025). Every distractor got a good-faith second-answer attack, re-executed
in the pinned venv (qiskit 2.5.0 / runtime 0.48.0); all ten figures were rasterized
(generator re-run with savefig -> PNG) and inspected. **0 second-answer attacks stuck,
0 key changes, 0 kills.**

- **Image-option proofs now pin the drawing (s1+s2 recipe):** s3-q063/q064/q065/q066/q068
  render every variant (with its draw kwargs, e.g. `reverse_bits=True` for q063 D) and
  the stem code with `draw("mpl")` to SVG in-process (`svg.hashsalt` fixed, no Date) and
  require byte-identity with the stem's rendering on top of the old structural match.
  s3-q067 (stem figure) renders every candidate's level-0 output and compares with the
  figure circuit's rendering. Observed: exactly the keyed variant renders identically
  in each of the six. Routing-SWAP trap re-checked: no option except D reproduces the
  q067 drawing; "which three gates" excludes a SWAP-containing input.
- **s3-q070 mechanism wording:** a pass-callback trace shows the H·H pair is removed by
  level 1's `InverseCancellation` (init stage, before translation), not by single-qubit
  merging. `correct` + distractor D reworded (meaning/key unchanged); proof records
  `observed.h_pair_removed_by`. s3-q072's mechanism verified: at level 2 the CX pair
  is removed by `CommutativeCancellation` in the INIT stage (level 2 init also runs
  ConsolidateBlocks/Split2QUnitaries); level 1 has only adjacent `InverseCancellation`.
- **Alt-text leak (s4-q054):** the stem alt ended "There is no line between qubits 2 and
  3" — the exact pair the key turns on; removed (edge list stays complete).
- **Citation failures replaced (all new pages fetched; quotes read in the page source):**
  s3-q066 visualize-circuits (no control flow) -> QuantumCircuit API (if_test/else);
  s3-q069 construct-circuits (no name clash) -> QuantumCircuit API ("forbids having
  multiple parameters of the same name"); s4-q054 sampler-v2 (no ISA content) removed;
  s4-q055 sampler-v2 -> `qiskit.transpiler.CouplingMap` ("directed edges correspond to
  permitted CNOT gates"); s4-q059 sampler-v2 + local-testing-mode (neither mentions the
  simulator exemption) -> `api/qiskit/primitives`. Upgrades for partial support:
  s3-q060/q063 + `guides/bit-ordering`; s3-q070 + `api/qiskit/circuit` (Barrier blocks
  optimizations from crossing); s4-q050 estimator-v2 -> `BindingsArray` ("the last axis
  is over parameters"); s4-q051 + `api/qiskit/primitives` (PUB shots take precedence);
  s4-q053 + `options-simulator-options`; s4-q056 transpiler-stages -> `TranspileLayout`.
- **Docs-only gaps (claims carried by execution, no page states them):** depth() keeps
  a filtered barrier as a sync point (s3-q059); `apply_layout` uses the FINAL layout
  (s4-q056); the runtime ISA check skips simulators (s4-q059, `is_simulator` guard);
  the primitive's mode is fixed at construction + 'The session is closed.' (s4-q052).
  Docs trap: the guides/primitive-input-output broadcasting example's comments quote
  (100, 2)/(3, 100)/300 while its code builds (10, 2) -> (3, 10); never reuse its numbers.
- **Conceptual items:** s4-q057 fully backed by guides/execution-modes "Basic workflow"
  (deactivated, normal job selection resumes, job must go through the normal queue to
  reactivate, max TTL never pauses). s4-q058 by the FAQ usage answer (interactive-TTL
  idle time counts in session; batch = quantum time only) — distractor D survives the
  "whichever happens last" wording because closing stops the TTL wait. s4-q060 by the
  FAQ lanes answer + execution-modes batch notes. FAQ proximity of s4-q060: same
  scenario shape as the FAQ's lanes example with different numbers (1 busy lane / 8
  jobs vs 2 / 6) and original distractors — kept, but do not add a second lanes item.
- **Determinism attacks:** s4-q053 key A re-run in two separate processes -> byte-
  identical counts; s3-q070/q072 have no coupling map, so no layout randomness.
- **Difficulty:** all 25 ratings kept. Borderline: s4-q060 (d2) is close to a one-fact
  read of the FAQ; s3-q063 (d1) correctly easy.
- **Drift lint s3-q021 (A-D), s3-q025 (D):** q021 = execution-derived false positive
  (4-dp angles) -> `rx_4dp`/`rz_4dp` recorded in observed. q025 = genuinely stale label:
  evidence said `x(0, condition=...)`, now quotes option D's call
  `qc.x(0, condition=(cr, 1))` (same call executed); D's outcome also in observed.
  Drift lint 5 -> 0.
- Gates: verify_bank s3 58/58 (+5 conceptual), s4 27/27 (+25 conceptual) PROVEN, exit 0;
  audit_meta_patterns s3 0/0 (9 pre-existing low length flags), s4 0/0 (10 low, incl. the
  known q053/q054/q058 keepers), no high/medium; render_figures OK for s3-q063..q068 and
  s4-q054 (SVGs unchanged).

## Adversarial review R2 — s5-s8 (2026-10-02)

Scope: s5-q044..q051 (8), s6-q043..q051 (9), s7-q039..q044 (6), s8-q030 (1). Every
distractor got a good-faith second-answer attack (proofs re-run, independent re-execution
for s5-q046/s6-q043/s7-q041/s7-q044 in the pinned venv, qiskit 2.5.0 / runtime 0.48.0); all
six figure items rasterized (generator re-run with savefig -> PNG) and inspected; every
cited page fetched and grepped for the claimed fact. **0 second-answer attacks stuck on
execution, 0 key changes, 0 kills.** Two docs-reader attacks are real (the docs read the
other way) and are now answered in the explanations; keys stay execution-proven.

- **Docs-reader traps (wording hardened, keys unchanged):** s5-q044 — the `join_data`
  reference says the first name is "placed to the left of" the next; a reader picks A
  (`101`). Execution: the join keeps `out` at bits 0-1 and `anc` at bit 2, and low
  indices print RIGHT (BitArray `slice_bits` note: index 0 = right-most `get_counts()`
  character). `correct` + distractor A now say so; the proof slices the join by bit index
  (`slice_bits([0, 1])` == out's counts, `slice_bits([2])` == anc's). s7-q039 — the 0.48
  docstring says `session_id` "All jobs in the session will be returned" and
  guides/monitor-job has a commented `jobs(session_id="<session id>")` "to retrieve all
  jobs in a Session" — both read as option C. They describe filter membership; the
  default `limit=10` still caps. Distractor C now names both sources.
- **s7-q039 stub-method scrutiny:** read the real `jobs()` source — the truncation is
  client logic (`if limit: ... break` once `len >= limit`; `limit or 20` page size), the
  stub only slices `[skip:skip+limit]` and reports `count`, as a server does. Proof now
  asserts the reloaded class is the library module's with its own paging loop, records
  `inspect.signature(jobs)` default limit (10) and the page sizes the LIBRARY requested
  (C/A/E `[10]`, B `[20]`). Residual assumption (noted, not provable offline): the real
  server honours the requested page limit with `session_id` set.
- **Figure proofs pinned to the drawing:** s5-q045/q048 (option histograms) now render each
  variant and the stem's own `plot_histogram` call to SVG text in-process (fixed
  `svg.hashsalt`, no Date) and require byte-identity on top of the bars read off the axes;
  only the key is identical. s6-q051: the stem code's plain `ax.bar` render is NOT styled
  like the option images (grey bars, fixed y-range) — stem reworded "Which bar chart shows
  the values this code plots?"; the proof executes the code's `ax.bar`, reads heights by
  tick slot, and requires SVG identity of the generator-styled render. s5-q049/s6-q047/
  s6-q050 (stem figures) kept: q049 reads bars back off the drawing, q047 asserts the same
  GATES literal in generator and proof, q050 is conceptual with a collinearity assert.
- **s6-q044 server-count caveat:** a guide reader can get 6 (PUB-wide grouping, 3 bases,
  times 2 sets) — execution gives 4 (grouping per parameter set). Distractor B now names
  that path. The per-set grouping is execution-carried; the BackendEstimatorV2 page only
  documents `abelian_grouping`. The stem pins BackendEstimatorV2 on AerSimulator.
- **Citation failures replaced (2) + upgrades:** s8-q030 guides/interoperate-qiskit-qasm2
  (no if/else/condition content at all) -> guides/composer (its OpenQASM 2 statement
  table: `if(creg==int) qop;` is the only conditional form, `if(c==5) CX q[0],q[1];`);
  s6-q049 guides/primitive-input-output (lists Pauli/SparsePauliOp/PauliList/str, never
  dicts) -> api ObservablesArray (`coerce_observable` takes `Mapping[str | Pauli, float]`
  and returns one observable). s6-q051 + SparsePauliOp API (`XIIZI` = Z_1 X_4).
  Verified as supporting: s5-q047 (TwirlingOptions 0.48: "Otherwise ... ceil(shots/
  num_randomizations)", `max(64, ceil(shots/32))` only when both auto, PUB/run shots
  "always obeyed"; sampler-options precedence list), s5-q045 (BitArray `postselect`:
  `creg[i]` as in slice_bits, selection = values kept, `num_bits` unchanged), s5-q051
  (M3 tutorial: p̃ = M p; Sampler has no built-in mitigation), s6-q046/q050 (ZneOptions:
  `(*shape, num_noise_factors)`, default `[0, *noise_factors]`, "fallback" = lowest-
  factor raw data, linear = polynomial_degree_1), s7-q042/q043 (0.48 API: pending
  semantics, default limit=10; `result()` raises RuntimeJobFailureError / Invalid-
  StateError for cancelled; `error_message()`).
- **Docs-page trap:** guides/bit-ordering now says BitArray's default is "big (endian)"
  and the Runtime primitives "return big-endian results" (it means the packed byte
  storage); its "Strings" paragraph (bit n-1 leftmost) is the citable part. Don't cite
  that page for printed-key order without quoting the Strings section.
- **Difficulty:** all 24 ratings kept (d3 items each combine >= 2 interacting rules).
- **Minor:** s8-q030 distractor C no longer mentions the proof's `z(1)` else body as if
  it were in the stem.
- Gates: verify_bank s5 35/35 (+6 conceptual), s6 29/29 (+13), s7 27/27 (+6), s8 13/13 (+7)
  PROVEN, exit 0, keys unchanged; audit_meta_patterns s5/s6/s7/s8 0 blockers / 0 warnings,
  no high/medium flags, none on the reviewed items; render_figures OK for s5-q045/q048/q049,
  s6-q047/q050/q051 (generators untouched); drift lint 0 findings.

## Figure wave — s1+s3+s4 (2026-10-02)

Nine figure adds toward the official ~19 % figure share: s1-q067/q068, s3-q073..q076,
s4-q061..q063 (d1 ×1, d2 ×7, d3 ×1; 5 option-image items, 4 stem-figure items; all executed).
Every option-image proof renders each variant AND the stem code's own drawing to SVG
in-process (`svg.hashsalt` fixed, no Date) and requires byte-identity on top of a structural
match; every stem-figure generator asserts a TARGET literal that its proof asserts too.
Measured in the pinned venv (qiskit 2.5.0 / runtime 0.48.0):

- **`plot_state_paulivec` draws ONLY the non-zero Pauli expectations** (x ticks = those
  labels, axis labels `Pauli` / `Coefficients`, no title). Bars read back via
  `ax.get_xticklabels()` + `ax.patches` (no zero bars, so zip pairing is safe here, unlike
  `plot_histogram`). `x(1); h(0); s(0)` -> `{II: 1, IY: 1, ZI: -1, ZY: -1}`; the
  qubit-swapped preparation prints YI/IZ/YZ — a clean endianness distractor (s1-q067).
  `qc.h(0); qc.s(0)` is already an s2-q035 option text — the first draft collided.
- **`TGate().power(3)` returns `PhaseGate(3π/4)`** (drawn as one P box); `SGate().power(2)`
  -> P(π), `SdgGate().power(3)` -> P(−3π/2), `RZGate(0.4).power(3)` -> RZ(1.2),
  `RXGate(π/2).power(2)` -> RX(π); `XGate/HGate/SXGate/CXGate.power(...)` fall back to
  a `UnitaryGate` labelled `"<name>^<exp>"` (drawn `sx^2`). `annotated=True` is ignored
  where a closed form exists. Gate.power docstring states the closed-form rule (s1-q068).
- **switch drawing:** `case(1, 2)` is ONE region labelled `1, 2`; `case.DEFAULT` is a
  region labelled `default` inside the box; the target prints `0x3` under the register.
  `op.cases_specifier()` yields `(values, body)`; body qubits are LOCAL — map through the
  switch instruction's qubits before comparing (first proof draft printed `x` on q1).
  The control-flow guide states "There is no fallthrough" (s3-q073).
- **Routed final layout (s3-q074):** 4-line, layout `[0,1,2,3]`, level 0, seed 42:
  `h(3); cx(3,1); cx(3,0)` -> `h[3], swap[2,3], cx[2,1], swap[1,2], cx[1,0]`,
  `final_index_layout() == [0, 2, 3, 1]` (inverse `[0, 3, 1, 2]` — pick 3-cycles so final !=
  inverse; a 2-swap disjoint routing gave an involution). Avoid `h(0); cx(0,1); cx(0,2)`
  -> `[2, 0, 1]`: that is the `final_index_layout` docstring's own example.
- **One-wire barrier at level 1 (no target):** `h(0); x(1); barrier(0); h(0); x(1); cx`
  -> `h, barrier(0), h, cx` (X pair cancelled, H pair fenced); identical at levels 1-3;
  no layout, so hand-built variants draw byte-identically to the real output (s3-q075).
- **`reverse_ops()`** = reversed order only (no adjoint, wires kept, CX roles kept);
  the inverse()/reverse_bits() distractor variants are asserted equal to those methods'
  outputs inside the proof (s3-q076).
- **Gate-map option images (s4-q061):** FakeLimaV2 / FakeManilaV2 / FakeYorktownV2 maps
  asserted in the generator; a `GenericBackendV2(5, basis_gates=[cx,rz,sx,x],
  coupling_map=<both directions>, seed=1)` per map runs an already-ISA circuit under
  runtime `SamplerV2` (only the map with all three CX pairs) and raises
  `IBMInputValueError: 'The instruction cx on qubits (1, 3) is not supported ...'`
  otherwise. Proof re-renders each map from the backend's own coupling map (byte-identical).
- **FakeNairobiV2 / FakeJakartaV2 / FakeLagosV2 share the H map** `0-1,1-2,1-3,3-5,4-5,5-6`.
  Star of 3 CX from q_0: layout `[1, 0, 2, 3]` -> 0 SWAPs / 3 CX at level 1; `[3,1,5,4]`,
  `[0,1,2,3]`, `[5,4,6,1]` -> 1 SWAP / 6 CX each (s4-q062).
- **ISA drawing -> counts (s4-q063):** `x(2); cx(2,1); measure_all()`, FakeManilaV2 level 1,
  `initial_layout=[3, 0, 1]`, seed 7 -> no routing; `draw(idle_wires=False)` hides the
  ancillas. `SamplerV2` with `options.simulator.seed_simulator = 11`, 1000 shots ->
  `{'110': 905, '100': 46, '010': 38, '111': 10, '011': 1}` (byte-stable across runs);
  noiseless `StatevectorSampler` -> `{'110': 200}`.
- Image sizes (keyed vs distractors): s1-q068 key 9408 B, 2nd of 5 (7581-9874); s3-q073 key
  26579 B mid (22615-28109); s3-q075 key 7414 B mid (5786-10749); s3-q076 key 8358 B 2nd of
  4 (8351-8892, near-tie); s4-q061 key 8168 B TIED smallest with D (8204/8579 others).
  No `image_size_tell`. s3 `smallest_image_option` stays low (4.5 %) — still no strictly
  smallest keyed s3 drawing (the "only CX" barrier-ignored distractor is the natural minimum).
- Craft: stem figures hide what the figure must carry (s4-q063 code omits the source
  circuit; s3-q074 shows qc but the SWAP choice is only in the drawing). Alt texts list
  complete gate/edge lists with equal specificity; none singles out the key pair.
- Gates: verify_bank s1 57/57, s3 62/62 (+5 conceptual), s4 30/30 (+25 conceptual) PROVEN,
  exit 0; audit_meta_patterns s1/s3/s4 0 blockers / 0 warnings, no flag on any add
  (pre-existing low flags 9/9/10); drift lint 0; no cross-question duplicate option
  texts. Answer keys of the adds: A2 B2 C2 D2 E1.

## Figure wave — s2+s5-s8 (2026-10-02)

Twelve figure adds toward the official ~19 % figure share: s2-q048, s5-q052/q053,
s6-q052..q054, s7-q045..q048, s8-q031/q032 (d1 ×1, d2 ×9, d3 ×2; 5 option-image items,
7 stem-figure items; all executed). Option-image proofs render every variant AND the stem
code's own call to SVG in-process (`svg.hashsalt` fixed, no Date) and require byte-identity
on top of a structural match (bars read off the axes by tick slot, density matrices,
instruction lists); stem-figure generators assert a TARGET/COUNTS/GATES/LAYOUT literal the
proof asserts too. Measured in the pinned venv (qiskit 2.5.0 / runtime 0.48.0):

- **`StatevectorSampler` refuses dynamic circuits**: `QiskitError 'StatevectorSampler cannot
  handle ControlFlowOp'` (if_test) and `'... cannot handle mid-circuit measurements'` (reset
  / measure-then-gate). Use runtime `SamplerV2(mode=AerSimulator())` with
  `options.simulator.seed_simulator` — byte-stable across processes (s5-q052 seed 21, 400
  shots, `if_test((c[0], 0))` feed-forward -> `{'10': 195, '01': 205}`).
- **Mid-circuit measure + reset on a Bell pair (s5-q053):** `h(0); cx(0,1); measure(1,0);
  reset(1); measure(1,2); measure(0,1)` -> only `000`/`011`; without the reset `000`/`111`;
  resetting both `000`/`001`. The mpl drawer layers the independent `measure(0,1)` BEFORE
  the reset box — semantics unchanged, but say so if a stem ever leans on drawn order.
- **`plot_state_city` of a ONE-qubit DensityMatrix** draws 2x2 panels at ~39-45 KB (vs ~68 KB
  for two qubits) and auto-ranges the z axis: the pure RY(2π/3) state's axis starts near
  0.25 so its 0.25 diagonal bar looks clipped — honest render, kept. Reduced state of
  `ry(2π/3,0); cx` = diag(0.25, 0.75), no coherences; `partial_trace` accepts a Statevector.
  A non-unit-trace `DensityMatrix(np.diag([0.5, 0.866]))` plots without complaint (s2-q048 D).
- **qasm3 export of a single-bit, value-0 condition** is `if (!c[0]) {` (value 1 -> `if (c[0])
  {`, register-wide `(creg, 0)` -> `if (c == 0) {`), measurements as `c[0] = measure q[0];`.
  The mpl drawing shows `c_0=0x0` with an OPEN circle on the classical wire (s8-q031).
  `IfElseOp.condition` returns `(Clbit, int)` — usable in a GATES signature.
- **qasm2 `gate` definitions load as custom `Instruction`s named after the gate** (NOT inlined;
  `.definition` holds the body). `mix q[2], q[0];` draws one box labelled `Mix` spanning
  q0..q2 with the argument indices printed inside (0 at q2, 1 at q0); q1 passes through
  (s8-q032). Box drawings tie at 6663 B, inlined H+CX drawings 7632-7634 B.
- **DataBin supports `data["out"]`** (mapping access) as well as `data.out` — never offer the
  subscript form as a distractor. Unnamed `ClassicalRegister(n)` auto-names `c0`, `c1`, …
  (counter), so "positional names" distractors must say "only for unnamed registers" (s7-q045).
- **BitArray 2-D indexing (s7-q046):** a `(2, 3, 1)` grid on a 1-parameter circuit -> BitArray
  shape `(2, 3)`; `bits[1]` = row (3 locations, pooled by `get_counts()`), `bits[:, 1]` =
  column, `bits.reshape(6)[1]` = one location. Angles 0/π give exact counts (no sampling noise).
- **`plot_histogram` accepts integer keys** (`get_int_counts()`), sorting them numerically and
  printing them as tick labels `1`, `4`, `6` (s7-q047).
- **`apply_layout` on a routing-free ISA (s6-q053):** FakeManilaV2, level 1,
  `initial_layout=[2, 3]`, seed 42 -> `final_index_layout() == [2, 3]`; `SparsePauliOp("ZX")
  .apply_layout(isa.layout).paulis[0]` prints `IZXII`; `apply_layout(None, 5)` -> `IIIZX`.
  `draw("mpl", idle_wires=True)` shows all five `ancilla_i -> p` / `q_i -> p` labels.
- **Two-qubit correlator sweep (s6-q052):** `ry(θ,0); cx` -> <XX> = sin θ, <YY> = −sin θ,
  <IX> = 0 everywhere (sin θ without the CX), <IZ> = cos θ, <ZZ> = 1.
- **Noisy "which circuit" histogram (s7-q048):** `x(2); h(0); measure_all()`, FakeManilaV2,
  level 1 seed 42, simulator seed 17, 1000 shots -> `{'100': 443, '101': 429, '001': 58,
  '000': 62, '111': 2, '011': 1, '110': 5}`; every distractor circuit with the same seeds sits
  at total-variation distance ≥ 0.23 (the RY(π/3) bar-ratio distractor is the closest).
- Image sizes (keyed vs distractors): s2-q048 key 42489 B, 2nd of 4 (39217-44696); s5-q052 key
  12710 B tied with B/D (others 12739); s7-q046 key 11911 B tied with D (11046-13875);
  s7-q047 key 14795 B mid (14326-15232); s8-q032 key 6663 B tied smallest with B (7632/7634).
  No strict extreme on any keyed image, no `image_size_tell`.
- Gates: verify_bank s2 38/38 (+1 conceptual), s5 37/37 (+6), s6 32/32 (+13), s7 31/31 (+6),
  s8 15/15 (+7) PROVEN, exit 0; audit_meta_patterns s2/s5/s6/s7/s8 0 blockers / 0 warnings,
  no flag of any severity on the twelve adds (pre-existing low flags only: s6-q031/q032);
  render_figures double-render OK for all twelve; drift lint 0 findings; no cross-question
  duplicate option text introduced (the pre-existing s6-q026/q039 pair is untouched).
  `numeric_middle` (ungated) s6 35.9 % — s6-q054's key 0.616 is one of two middle values of
  four; s5 44.1 % is pre-existing (no numeric adds in s5). Answer keys of the adds:
  A2 B2 C2 D3 E3.
- Process trap: re-keying by swapping option dicts in place left the options list out of
  key order -> verify_bank schema FAIL "option keys must be in alphabetical order". Sort
  options by key after any re-key.

## Study absorption (2026-10-02)

Folded 22 newly proven facts from the R2 / adversarial / figure waves into `data/study/`
(append-only: no primer, existing fact or checklist item touched; per-fact
`fact_checked: true`, a one-line provenance note per file). Every fact cites an EXECUTED
qid and was re-verified by re-executing its logic in the pinned venv (qiskit 2.5.0 /
runtime 0.48.0 / aer 0.17.2); s7-q039/q043 re-verified against the installed
`QiskitRuntimeService.jobs` / `RuntimeJobV2.result` source plus the stored proof verdicts.

- Adds: s1 3 (s1o1: PauliEvolutionGate no ½ vs RXX/RZZ, cx·rz·cx = ZZ evolution at θ/2,
  `@` is the operator product), s2 2 (s2o3: shortened reduced Bloch arrows, paulivec draws
  only non-zero Paulis), s3 4 (depth/barrier sync, expression substitution in
  `assign_parameters`, same-name Parameter compose CircuitError, barrier fences level-1
  cancellation), s4 3 (constructor-bound mode + 'The session is closed.', simulator backends
  skip the ISA check, directional coupling map), s5 3 (join_data order, StatevectorSampler
  rejects dynamic circuits, postselect bit indices), s6 2 (dict = one weighted observable,
  precision → ceil(1/p²) shots with eigenstate stds 0), s7 2 (jobs() silent limit=10,
  ERROR vs CANCELLED result() exceptions), s8 3 (qasm2 one condition form, qasm3 bare-bit
  conditions, qasm2 custom gates load un-inlined).
- Caps after: s1o2, s4o2, s5o3, s7o1 now at 6 core / 5 trap; s2o3, s4o1 (trap), s6o2
  (trap), s5o1 (trap) at one limit. A further absorption pass there must merge, not append.
- Prose totals now s1 1125, s2 1147, s3 1255, s4 1077, s5 1135, s6 1197, s7 1108, s8 797
  (contract target ~900-1100; s3/s6 are the ones to trim if a rewrite pass runs).
- **Not absorbed, deliberately:** `mode=backend` inside an open batch/session runs IN it on a
  real IBM QPU (s4-q020 is conceptual, not locally provable) — the s4o1 primer still says it
  "silently puts you back in job mode", the stale pre-0.34 claim the R1 s4 audit corrected;
  adding the right fact beside it would contradict the primer on the same page. **Primer fix
  needed (out of append-only scope).** Also skipped: Gate.power closed form and inverse()
  keeping Parameters (s1o2 at cap), final_index_layout reading (deep), per-parameter-set
  commuting-group counts (BackendEstimatorV2 internal, docs-unbacked), shot-precedence counts
  math (s5o1 primer table + s5-q026/q035 facts already cover it), DataBin `data["out"]` (s7o1
  primer row already lists `db['meas']`; s7o1 at cap), level-1 vs level-2 CX cancellation
  (primer level table already names InverseCancellation vs CommutativeCancellation).
- Gates: `build_study.py` exit 0 (8 cram pages), `build_epub.py` exit 0.

## 2026-10-10 — Study concision pass (s1–s3, s5–s7)

- Claim-preserving trim toward the contract's ~900–1100 prose-word target. Prose words:
  s1 1125→999, s2 1147→1002, s3 1255→1120, s5 1135→932, s6 1197→955, s7 1108→915
  (s4 1095 and s8 797 untouched). Total 8859→7815.
- 8 facts deleted, each verified by the orchestrator as fully covered elsewhere in its file
  (primer table row, primer sentence or code comment): s1-q017, s1-q010, s1-q042, s1-q040,
  s2-q011, s2-q017, s3-q024, s5-q029. The agent also deleted s7-q012 and s7-q019;
  the orchestrator restored both verbatim, because their worked examples carry exam-style
  "not X" contrasts the table rows lack.
- Invariants checked by the orchestrator: every code fence byte-identical, no `source` changed or added,
  `fact_checked` kept true. Gates: build_study, build_epub, meta-audit --gate, npm build — all green.

## 2026-10-10 — Runtime 0.50 impact check (no re-pin; report only)

- Scratch env: the lock with only qiskit-ibm-runtime 0.48.0 → 0.50.0 (released 2026-09-24).
  Its dependencies came along: ibm-quantum-schemas 0.12, samplomatic 0.21, and new transitive
  installs qiskit-mitigation and qiskit-qasm3-import. qiskit 2.5.0 and aer 0.17.2 unchanged.
- `verify_bank.py --check`: 302/302 proven, 0 failures. **No answer key changes under 0.50.**
- Each proof was run under both versions with `PYTHONWARNINGS=always` and the outputs compared:
  - **54 executed questions now emit DeprecationWarnings.** `SamplerV2` (44) and `EstimatorV2`
    (11) are deprecated as of 0.50, with removal no sooner than 3 months after release (so
    ≥2026-12-24). The successors are `qiskit_ibm_runtime.executor_sampler.Sampler` and
    `executor_estimator.Estimator`. The bank mentions V2 classes in 85 question files, plus
    study s2/s4/s5/s6. Affected executed qids:
    s2-q022 s4-q012 q013 q016 q018 q021 q023 q026 q028 q032 q034 q036 q038 q044;
    s5-q001 q010 q011 q013 q014 q015 q017 q018 q019 q020 q022 q023 q024 q025 q026 q027 q028
    q029 q031 q032 q033 q035 q036 q039 q040 q041 q042 q043 q046 q051 q052 q053;
    s6-q012 q013 q016 q041 q045; s7-q013 q038 q048.
  - One question's evidence changed in meaning: in s8-q012, distractor E (`qasm3.loads` on a
    QASM2 string) now raises `QASM3ImporterError`, not `MissingOptionalLibraryError`, because
    runtime 0.50 pulls in qiskit-qasm3-import. The key is unaffected; the explanation's
    "raises MissingOptionalLibraryError" holds only for a bare-qiskit install. s8-q021 is
    robust because it blocks the module. s8-q026/q027/q029 notes ("not installed in the pinned
    env") would go stale at the re-pin. The s8o3 primer claim (import needs the separate
    package) stays true of qiskit itself.
  - All other observed and evidence diffs are shot noise from unseeded fake-backend
    sampling (s4-q018/q036/q038/q044/q053, s5-q001/q010/q024/q025/q039, s6-q012/q013)
    or install-path strings in error messages (s2-q014/q029).
- Re-pin trigger: when IBM moves the exam to the executor primitives, or when 0.5x removes the V2
  classes. Until then, 0.48 stays pinned. The exam blueprint is written against the V2 primitives.

## Adversarial review A3 — s1a (2026-10-16)

Scope: s1-q001, s1-q010, s1-q012..q032 (23). Every option including pool distractors was
re-executed in an independent script (pinned venv, qiskit 2.5.0); every cited page fetched
and grepped. **0 second-answer attacks stuck, 0 key changes, 0 kills.** All 23 edited
(citations), 3 hardened in options, 4 explanation fixes.

- **Incoherent distractors (option + proof rewritten, keys unchanged):**
  s1-q019 E (`−1.0`, "bit 0 maps to the −1 eigenvalue of Z") was unreachable: under that
  misconception ⟨Z⊗Z⟩ on |00⟩ = (−1)(−1) = +1, i.e. the key's value. Now `1.25` = 1² + 0.5²,
  the second moment; executed `⟨00|O·O|00⟩ = 1.25`, `⟨O⟩ = 1.0`, recorded as
  `observed.second_moment`. s1-q028 C (`[i, 0]`, "phase applied to |0⟩") could not arise
  from P acting on |1⟩ (a |0⟩-slot phase leaves `[0, 1]`); now the conjugate-phase sign
  error `[0, −i]` (= P(−π/2)|1⟩ = S†|1⟩); executed P(π/2)|1⟩ = `[0, 1j]` ≠ `[0, −1j]`.
  s1-q018 D's rationale ("from_list merges by default, so simplify does nothing") contradicted
  its own 3-term repr; now the zero-pruning-only misconception (docstring: "combining
  duplicates and removing zeros").
- **False explanation:** s1-q025 distractor D said SX|0⟩'s magnitudes are 0.5; executed
  `|0.5±0.5j| = 0.7071`. Rewritten: SX|0⟩ = e^{iπ/4}·[0.7071, −0.7071j] (relative phase −i).
- **Stem:** s1-q018 "What does this code print?" — the literal print is
  `SparsePauliOp(['Z', 'X'],\n coeffs=[3.+0.j, 1.+0.j])`, not the options' `[3, 1]`; stem
  now "What does `op.simplify()` return?" (the returned op equals the keyed constructor).
  q001/q019/q022/q031 ask for the state/value/return, not the print (q031 prints
  `{np.str_('01'): np.float64(1.0)}` under numpy 2.x — equal to `{'01': 1.0}`).
- **Citation failure (all 23):** `api/qiskit/quantum_info` (module index; only a
  little-endian note) and `guides/operators-overview` (no label endianness, no dot/tensor
  semantics, no simplify, no gate matrices) stated none of the tested facts; q001's
  `construct-circuits` has no S gate. Replaced with pages that state each fact: Pauli API
  ("qubit-0 corresponds to the right-most Pauli character … 'XYZ' … 'Z' on qubit-0";
  `dot` = "self * other"; `tensor` a⊗b, `expand` b⊗a; `commutes`) for q010-q017/q020;
  SparsePauliOp (`simplify`) q018/q019; Statevector (`from_label` table, `expectation_value`)
  q019/q030/q031; gate pages (S, Sdg, SX, T, RZ, Z, P, Y, CX matrices) q001/q022-q029/q032;
  operator-class ("A.compose(B) returns the operator with matrix B.A") + Operator note
  q021; guides/bit-ordering ("bit n−1 is the leftmost", `from_label("0+")`, "this CX-gate
  performs |01⟩ ↔ |11⟩") q030-q032; learning "Limitations on quantum information" (global
  phase: "precisely the same probabilities") + QuantumCircuit q027. operators-overview kept
  only where it supports a distractor (phase-prefixed labels, legal 'I').
- **Docs-reader traps answered:** TGate page calls T "the π/8 gate" (exp(iπ/8 Z) up to global
  phase) → q022 E; QuantumCircuit "global_phase … can have some impact on its output, if
  the circuit is used to describe a Gate that may be controlled" → q027 correct; CXGate
  "textbook matrix" (control q_1, |10⟩↔|11⟩) → q032 C.
- **Survived attacks (executed):** q020 A `Pauli(['Z','I'])` raises QiskitError "Invalid input
  data for Pauli."; q013 `X.compose(Y)` = `-iZ`, `X.dot(Y)` = `iZ`; q017 commutes
  T/F/T/T/F/F; q024 tdg = [0.7071, 0.5−0.5j], p(−π) = [0.7071, −0.7071]; q025 sxdg|0⟩ =
  [0.5−0.5j, 0.5+0.5j]. Noted, not changed: q024 F's snippet uses `np` (not imported in the
  displayed code) — it is a wrong option on the angle anyway.
- **Difficulty:** all 23 kept (q013/q025 borderline d2, one recalled fact plus a phase step).
- Gates: verify_bank s1 57/57 PROVEN, exit 0; audit_meta_patterns s1 0/0 (9 pre-existing
  low length flags, none new); lint_proof_drift 0 findings.

## Adversarial review A3 — s1b (2026-10-16)

Scope: s1-q033..q037, q039..q045, q047..q054, q067, q068 (22; q055..q066 were R2 adds,
reviewed 2026-10-02). Every option including pool distractors re-executed in independent
scripts (pinned venv, qiskit 2.5.0); every cited page fetched as text and grepped; all six
figure items re-rendered and inspected. **0 second-answer attacks stuck, 0 key changes,
0 kills.** 20 edited (citations), 7 with content or proof fixes, 2 survived unchanged
(q067, q068).

- **Literal-print mismatch (stem attack):** s1-q049 "What does this code print?" keyed
  `{'h': 4, 'cp': 6, 'swap': 2}`, but `count_ops()` orders by count, so the displayed code
  prints `{'cp': 6, 'h': 4, 'swap': 2}`. All option dicts re-ordered to print order; the
  proof now compares each option string with the executed `str(dict(...))` literally.
- **Tell in displayed code:** s1-q033's code comment ("a: e.g. … z(0); b: with rz(pi, 0)")
  named a keyed pair as its example. Replaced by a runnable neutral pair (S vs P(π/2),
  prints `True`), not among the options.
- **False explanations (keys unchanged):** s1-q033 F argued "determinants differ in sign,
  so no global phase can bridge them" — wrong for 2×2 (det(iH) = +1 = det RY(π/2));
  now the entry comparison H = (1/√2)[[1,1],[1,−1]] vs RY(π/2) = (1/√2)[[1,−1],[1,1]]
  (executed `equiv` False; RY(π/2)·Z == H True). s1-q053 B said the drawn S–X–S† "= Y";
  executed `Operator` of the drawing is S†XS = −Y (`[[0, i], [−i, 0]]`), and the learning
  page's "S X S† = Y" is the reversed order — rationale now answers that trap. s1-q051 B
  said `sdg` "adds a phase" to |0⟩ (Sdg|0⟩ = |0⟩). s1-q052 D rationale aligned with its
  alt (16 nonzero cells split 8 real / 8 imaginary, executed).
- **Display letters:** s1-q044 `explanation.correct` cited "(statements C and E)" /
  "(statement B)" on a shuffled 5-of-6 pool; rewritten letter-free.
- **Proof weakness ("which drawing" items):** s1-q052 and s1-q054 compared density
  matrices / Bloch vectors only; s1-q051 compared vectors to a literal TARGET. All three
  now render every variant and the verbatim stem state in-process (`svg.hashsalt` fixed,
  `metadata={"Date": None}`) and require SVG byte-identity (only B / C / D match); q051
  and q054 also cross-check `_bloch_multivector_data`. Finding: for the Bell state
  `plot_bloch_multivector` still adds one zero-length `Arrow3D` per sphere; q054's proof
  rasterizes each figure with and without its arrow patches — Bell spheres are
  pixel-identical to arrow-free spheres (alt "drawn empty" holds), every distractor arrow
  changes pixels (control: 2511 px).
- **Citation failure (20 of 22):** `api/qiskit/quantum_info` and
  `guides/operators-overview` (SparsePauliOp/Pauli/Operator intro; no evolve, tensor
  order, probabilities, expectation values or gate matrices) were cited on q033-q047;
  `api/qiskit/circuit_library` (index) on q048-q050; `guides/visualize-circuits` (circuit
  drawing only, no Bloch/city plots) on q051/q052; `api/qiskit/visualization` (index) on
  q054. Replaced with pages verified to state each fact: Operator (`equiv` "up to global
  phase"), ZGate ("RZ(π) = −iZ"), XGate ("RX(π) = −iX") q033; Statevector (`evolve`,
  `tensor` = self ⊗ other / `expand` = other ⊗ self, `from_instruction` raises on
  instructions invalid for statevector simulation, `probabilities([0])` qubit-0 example,
  `probabilities_dict`, `expectation_value`, `from_label` eigenstate table) q034-q047;
  operator-class ("A.tensor(B) … B on subsystem 0, A on subsystem 1") q035/q037; gate
  pages (RY, Z, T, SX, H, X, S, Sdg matrices) q039-q047/q051/q052; efficient_su2 (reps,
  `skip_final_rotation_layer`, 3-qubit drawing ending θ[17]) + EfficientSU2 ("deprecated
  as of Qiskit 2.1") q048; QFTGate (num_qubits only) + QFT ("Hadamard gates on each
  qubit, … controlled … gates and a layer of Swap gates", `do_swaps`) q049;
  real_amplitudes ("alternating layers of Y rotations and CX"), pauli_two_design (random
  axes, CZ) q050; plot_bloch_multivector (per-qubit Pauli expectations) q051/q054;
  plot_state_city ("real and imaginary part of the density matrix") q052; learning
  "Stabilizer codes" ("HXH† = Z, HZH† = X", "SXS† = Y") q053. Kept (verified):
  plot-quantum-states (q054), q067 (plot_state_paulivec, Pauli "qubit-0 … right-most"),
  q068 (TGate/PhaseGate/Gate.power "returned directly").
- **Docs-reader traps noted:** the QFT class page says "controlled-U1" — `QFTGate`'s
  definition decomposes to `cp` (no option uses cu1). TGate page "equivalent to
  exp(iπ/8 Z) up to a global phase" has the sign of RZ(−π/4); T = e^{iπ/8}·RZ(π/4)
  (executed `rz(π/4)` equiv `t` True) — q033 E stays correct. TGate's "π/4 rotation about
  the Z axis" is answered by q068 D (RZ only up to phase; `power(3)` returns PhaseGate).
- **Survived attacks (executed):** q036 all three entry points (`from_instruction`,
  `Statevector(qc)`, `DensityMatrix.from_instruction`) raise "Cannot apply instruction
  with classical bits: measure"; `save_statevector` raises "Cannot apply Instruction";
  `backend=` is a TypeError. q050 only `real_amplitudes(3)` is {ry, cx}. q048 24 / 16
  (skip final) / real_amplitudes 12. q067 every candidate's nonzero Pauli set matches
  its rationale (A ZI=+1, B YI/IZ/YZ, C IY=−1, E IX/ZX). q068 `TGate.power` returns
  `PhaseGate(0.25·π·exponent)`; `HGate().power(3)` is a `UnitaryGate` labelled `h^3`.
- **Figures:** all six re-rendered (`render_figures --only`, 0 failures) and inspected;
  renders match their alts. q052 A vs B differ only in which off-diagonal imaginary cell
  is positive — readable from the axis labels, kept.
- **Difficulty:** all 22 kept (q052, q067 borderline d3: phase sign through ρ / endianness
  plus S vs S†; kept at d2, each is one concept with a twist).
- Gates: verify_bank s1 57/57 PROVEN, exit 0; audit_meta_patterns s1 0 blockers /
  0 warnings (9 pre-existing low length flags, none new); lint_proof_drift 0 findings.

## Adversarial review A3 — s2a (2026-10-16)

Scope: s2-q010..q028 (19; no figure items in this range). Every option including pool
distractors re-executed in independent scripts (pinned venv, qiskit 2.5.0); every cited
page fetched as text and grepped; drawer/plot source read where docs were silent.
**0 second-answer attacks stuck, 0 key-letter changes, 0 kills.** All 19 edited
(citations); 2 items rebuilt around a broken premise (q019, q024), 8 explanation fixes.

- **Distractor misconception landed on the key (option values + code rebuilt, key letter
  kept):** s2-q024 RY(2π/3): the full-angle error gives cos²(2π/3) = 0.25 / sin² = 0.75
  = the key, so the item's own twist (θ/2) did not discriminate, and A's rationale ("full
  angle gives 0.933/0.067") was false. Now RY(π/4): key `{'0': 0.854, '1': 0.146}`, A full
  angle 0.5/0.5, B swapped, C linear-in-angle 0.75/0.25, E amplitudes 0.924/0.383
  (self-labelling glosses like "the amplitudes, not their squares" dropped); proof computes
  each model and asserts the full-angle model ≠ key. s2-q019 x(0), x(2) on 3 qubits is
  endianness-symmetric (`reverse_bits()` also gives '101'), so A/C "reverse convention"
  rationales were unreachable. Now 4 qubits: key '0101', A '1010' (q0 leftmost), C '11'
  (idle qubits dropped), D '0b101' (`bin()` of index 5; replaces '0x5' to keep widths
  equal), E int key; proof computes each model.
- **Literal-print mismatch:** q019/q024 "What does this print?" — the prints are
  `{np.str_('0101'): np.float64(1.0)}` / `{np.str_('0'): np.float64(0.854), ...}`; stems
  now ask for the return / computed probabilities (q010's two class names do print as
  keyed).
- **False explanations (keys unchanged), executed or source-read:** q011 A "idle_wires=True
  is the default" — default is `"auto"` (signature None → docstring "Default is auto").
  q015 D "pylatexenc is a dependency of the LaTeX renderer, not mpl" — `MatplotlibDrawer` is
  decorated `_optionals.HAS_PYLATEX.require_in_instance`; rewritten (missing lib =
  MissingOptionalLibraryError; here the string fails first). q025 E "`sort="desc"` applies
  to values, not keys" — `desc` keeps ascending ticks but `ax.invert_xaxis()`, drawing
  '11','10','01','00' = E's order; proof now reads labels in drawn order. q013 B/C "nothing
  is added" — `qc.x(0)` appends an unconditional X before `.c_if`/`.condition` raises (data
  h, measure, x). q023 B: the error is VisualizationError "Length of legend (2) doesn't match
  number of input executions (1)", not figsize. q010 F (notebooks use `_repr_html_`), q022 B
  (`SamplerPubResult`), q015 E (draw() delegates to circuit_drawer) tightened.
- **Displayed code:** s2-q017 option F used `plt` with no import in the displayed code;
  `import matplotlib.pyplot as plt` added (F runs, returns None).
- **Citation failure (19 of 19):** `api/qiskit/visualization` (index) was cited on 17;
  `guides/visualize-circuits` on q011/q013/q016 states none of idle_wires, if_test,
  initial_state; `guides/visualize-results` on q020/q024/q027 has no plot_distribution, RY or
  Bloch content; plot-quantum-states on q024. Replaced with pages verified to state each fact:
  circuit_drawer API (Returns TextDrawing/Figure/PIL.Image/str, valid outputs "text, mpl,
  latex, latex_source", VisualizationError, idle_wires "auto", reverse_bits, initial_state,
  ax "no returned Figure") q010-q018; QuantumCircuit API (draw kwargs, reverse_ops, if_test
  tuple signature) q011/q012/q013/q016; guides/qiskit-2.0 ("Removal of legacy c_if
  conditions", no condition attribute) q013; plot_histogram API (number_to_keep 'rest',
  sort values + "Defaults to asc", legend length, Returns Figure) q020-q023/q025;
  plot_distribution API q020; BitArray API (get_counts/get_bitstrings/get_int_counts) q022;
  bit-ordering ("bit n−1 is the leftmost bit") + Statevector (probabilities_dict keys,
  from_label table) q019/q024/q028; RYGate matrix q024; SGate diag(1, i) q027;
  plot_bloch_multivector API ("Plot a Bloch sphere for each qubit") q026/q027.
- **Docs-only gap:** no page states that plot_distribution normalizes (its API says only
  "Plot a distribution from input sampled data"); q020 rests on execution (ylabels 'Count' vs
  'Quasi-probability', heights sum 1024 vs 1.0).
- **Docs-reader traps answered:** visualize-circuits calls the text return a "TextDrawer"
  (class is `TextDrawing`) → q010 correct; circuit_drawer "latex: High-quality images" →
  q018 E (PIL Image: `save`, no `savefig`).
- **Proof strengthening:** q027 now asserts its Bloch vector equals
  `_bloch_multivector_data` (the drawn vector, (0, 1, 0)); q025 reads tick labels in drawn
  order.
- **Survived attacks (executed):** q014 only `qiskit.visualization.circuit_drawer(...,
  output=)` runs (tools: ModuleNotFoundError; top-level / draw_circuit: ImportError;
  format=: TypeError); q016 only `initial_state=True` draws |0> (style dict ignored, typos
  TypeError); q021 labels ['00','11','rest'] heights [500,500,24]; q022 only get_counts()
  plots; q026 3 spheres titled qubit 0..2; q028 only '-' at (−1,0,0).
- **Difficulty:** all 19 kept (q024 stays d2: half angle then square; q019 d1: one convention).
- Gates: verify_bank s2 38/38 PROVEN + 1 conceptual, exit 0; audit_meta_patterns s2
  0 blockers / 0 warnings, 7 low flags (pre-existing q010/q018/q022/q023 among them; q024's
  pre-existing low flag cleared; none new); lint_proof_drift 0 findings.

## Adversarial review A3 — s2b (2026-10-16)

Scope: s2-q029..q046, s2-q048 (19; s2-q047 was an R2 add). Every option including pool
distractors re-executed in independent scripts (pinned venv, qiskit 2.5.0); every cited page
fetched as text and grepped; drawer source read where docs were silent; all eight figure items
re-rendered (`render_figures --only`, 0 failures), rasterized (generator re-run with PNG
savefig) and inspected. **0 second-answer attacks stuck, 0 key-letter changes, 0 kills.**
All 19 edited (citations / proofs / notes); none survived fully unchanged.

- **Option text contradicted the drawing (key letter kept):** s2-q032 B claimed "the |01>
  branch carries phase π while |10> has phase 0". `plot_state_qsphere` removes a global phase
  by zeroing the phase of the largest amplitude (`argmax` after rounding picks |01> of the tied
  pair), so the drawn figure is the reverse: `show_state_phases=True` labels |01> `0`, |10> `π`
  (executed). B now states only the π difference; explanation teaches the normalisation; proof
  reads marker sizes/colours and the drawer's own phase labels.
- **False explanations (keys unchanged):** s2-q038 correct said qubits are shaded by "readout
  and single-qubit gate errors" — source: `q_colors` come from the max single-qubit gate error
  only; readout error is the side bar chart. s2-q037 D "a CouplingMap does not carry the qubit
  count" — executed error is `'CouplingMap' object has no attribute 'num_qubits'`. s2-q036 C had
  a false clause ("never gets far enough … when the circuit has no layout") although option C
  passes `isa`. s2-q043 E said phase π is "the opposite side of the colour wheel from the
  quarter turn shown" (π is a quarter turn from π/2; it is opposite phase 0).
- **Figure alt texts:** s2-q040 C/D/E described an "'If-1' region"; the mpl box is labelled
  `If` and the tested value appears as `0x1` under the condition dot — all five alts rewritten
  at equal specificity (D's "the qubit that was measured" gloss dropped). s2-q046 B–E quoted
  marker magnitudes (0.5/0.87/0.25/0.43/0.75) the drawing never prints (A had none) — dropped.
  Noted, kept: s2-q048 A (pure RY state) renders with an auto z-axis starting near 0.25, so its
  bars run below the panel floor — genuine `plot_state_city` output, distractor only.
  s2-q043 T (π/4, purple) vs S (π/2, magenta) is distinguishable but close; the stem alt states
  π/2 (color_essential).
- **Proof weakness ("which drawing" items):** q040, q041, q042, q044, q045, q046 compared
  circuits / bar tuples / Bloch vectors / markers, and each took the keyed variant from the same
  function as its target (C/B/D/A/D/E compared with themselves). All six now run the DISPLAYED
  stem code verbatim, render it and the generator's variants in-process (`svg.hashsalt` fixed,
  `metadata={"Date": None}`) and require SVG byte-identity plus the structural match; q043
  (image-to-code) renders the stem code with each option's sequence against the figure render.
  q042 also asserts `_bloch_multivector_data`; q030 now cross-checks its (0,0,0) pair against
  `_bloch_multivector_data` and counts 2 sphere axes. q048 already pinned (kept).
- **Citation failure (18 of 19):** `api/qiskit/visualization` (index) on 13 items,
  `api/qiskit/quantum_info` on q030, `guides/visualize-results` on q031/q035/q039/q041/q045 and
  `guides/visualize-circuits` on q040/q044 stated none of the tested facts. Replaced with pages
  verified to state each fact: Statevector (draw "Valid choices … qsphere …", sample_counts
  "Return type Counts", sample_memory, seed) q029/q039; plot_bloch_multivector ("Plot a Bloch
  sphere for each qubit", Pauli expectations, `state` parameter) q030/q033/q034/q035/q042;
  plot_bloch_vector (three-element `bloch`, coord_type) q033/q034; plot_state_qsphere ("the
  color represents the phase") q032/q043/q046; bit-ordering ("bit n−1 is the leftmost bit")
  q031/q041; SGate / RYGate matrices q035/q042/q043/q046; plot_circuit_layout + QuantumCircuit
  `layout` ("typically set on the output from transpile()") q036; plot_gate_map q037/q038;
  BitArray `get_int_counts` q039; QuantumCircuit `if_test` ("chainable context manager … else
  blocks") q040; circuit_drawer `reverse_bits` q044; plot_histogram (number_to_keep "single bar
  called 'rest'", sort "Defaults to asc", bar_labels) q041/q045; quantum_info `partial_trace`
  q048. Kept (verified): plot-quantum-states ("psi.draw("qsphere")", "the color represents the
  phase", "can't show correlations"), qpu-information (quoted), plot_error_map, transpile guide,
  classical-feedforward guide, plot_state_city.
- **Docs-reader traps noted:** plot_circuit_layout API lists `VisualizationError` for a missing
  layout; the executed raise is `QiskitError: 'Circuit has no layout. Perhaps it has not been
  transpiled.'` (q036's explanation already says QiskitError). plot_state_qsphere API says point
  size is "proportional to the probability", plot-quantum-states says "thickness … represents
  the amplitude"; source: `markersize = sqrt(prob)·30` (diameter ∝ |amplitude|) — q046's
  "sized by magnitude" stands. Docs gap: no page states that plot_error_map shades by
  calibration; q038 rests on the executed colour arrays.
- **Survived attacks (executed):** q029 only `draw("qsphere")` returns a Figure (q_sphere
  ValueError, plot_qsphere ImportError). q033/q034 bmv([0,0,1]) VisualizationError, list of
  vectors QiskitError "not a square matrix", bv(2-qubit state) silently draws one sphere,
  spherical ValueError, ptrace → 1 sphere. q035 drawer vectors A (1,0,0), D (0,1,0), C z=0.5,
  F north. q036 every level 0-3 sets `isa.layout`, `qc.layout` stays None; A/C/E
  AttributeError. q039 Counts {'00': 999, '11': 1049}. q048 reduced diag(0.25, 0.75).
- **Difficulty:** all 19 kept.
- Gates: verify_bank s2 38/38 PROVEN + 1 conceptual, exit 0; audit_meta_patterns s2
  0 blockers / 0 warnings, 7 low length flags (q030/q036/q037 pre-existing, options untouched;
  none new); lint_proof_drift 0 findings; render_figures OK for all eight figure qids.

## A3 rework — s2-q040 (2026-10-16)

- **Why:** the item still used the canonical docs shape (`h(0); measure(0, 0); with
  if_test((cr, 1)): x(1)` on 2 qubits) that the s3-q066 entry bans (anti-duplication vs
  official sample material). Same objective (reading an `if_test` block in `mpl` output),
  same difficulty (1), `display_count` 4 kept.
- **New circuit:** `QuantumRegister(3, "q")`, `ClassicalRegister(2, "m")`; `sx(0)`,
  `cx(0, 2)`, `measure([0, 2], cr)`, `with qc.if_test((cr, 2)): z(1)`. Deliberately also
  away from the guide's 3-qubit register example (`h([q0, q1])`, contiguous measures,
  `0b001`, X on q2) and from s3-q066 (RY, single-clbit value 0, CX/SWAP else). Key C -> D.
- **Distractors (all rendered, inspected as PNG):** A `if_test((cr[1], 1))` (register test
  read as a single-bit test; dot labelled `m_1=0x1`), B bare `z(1)` (conditional ignored;
  the drawer pulls it into the first column), C `if_test((cr, 1))` (bit-order slip on the
  tested integer; `0x1`), E Z on q2 (target misread onto the measured qubit).
- **Drawer facts (qiskit 2.5.0, default `cregbundle`):** a register condition draws ONE dot
  on the bundled `m` wire labelled with the hex value only (`0x2`); a single-clbit
  condition on the same register draws the dot labelled `m_1=0x1`. Docs-reader trap: the
  feedforward guide describes solid/outlined circles per classical bit — that is the
  unbundled drawing, not this default render.
- **Image sizes:** A 18624, B 13940, C 17978, D (key) 17978, E 17989 B — key tied with C,
  never the strict extreme in any displayed sample.
- **Proof:** copies the generator's five variants, renders the verbatim stem code and every
  variant in-process (`svg.hashsalt` fixed, `metadata={"Date": None}`), requires SVG
  byte-identity plus a structural signature that now includes the `if_else` condition
  (register name/clbit index + value); only D matches.
- **Citations (fetched):** classical-feedforward guide ("conditionally perform operations
  based on the value of a classical bit or register"; "condition on the value of a
  classical register composed of multiple bits"); QuantumCircuit `if_test` ("a tuple of a
  `ClassicalRegister` to be tested for equality with a given `int`", or "a `Clbit` to be
  compared to either a `bool` or an `int`").
- Gates: render_figures --only s2-q040 0 failures; verify_bank --only s2-q040 PROVEN;
  --section s2 38/38 proven + 1 conceptual, exit 0; audit_meta_patterns s2 0 blockers /
  0 warnings, no flag on s2-q040; lint_proof_drift 0 findings.

## Adversarial review A3 — s3a (2026-10-16)

Scope: s3-q010..q036 (27). Every option incl. pool distractors re-executed in independent
scripts (pinned venv, qiskit 2.5.0 / aer 0.17.2); every cited page fetched as text and
grepped. **0 second-answer attacks stuck on the keys as written, 0 key-letter changes, 0 kills.**
24 edited, 3 survived unchanged (q012, q013, q032).

- **Anti-dup reworks (canonical `h(0); measure(0, 0); if_test(...)` + X shape, s3-q066 /
  s2-q040 ban):** q023 (exact canonical) -> `sx(2); measure(2, 1); if_test((cr[1], 1)): x(0);
  measure(0, 0)` on 3 qubits, key D kept (executed {'00': 2000, '11': 2000}); A rewritten as
  "body never fires" (executed no-X variant {00,10}), C as "√X read as a full X" (only 11).
  q026 (h/measure/if_test as else_) -> `sx(1); measure(1, 0); if_test((cr[0], 0)) as else_:
  x(2) / z(2)`, key B kept ({'10': 2000, '01': 2000}). q024 (same context as comment) ->
  `ry(0.6, 2); measure(2, 1)`, Z on qubit 0 conditioned on `cr[1]`, same six syntax forms,
  key C kept; proof now also asserts the if_else condition (clbit 1, 1) and body [z on q0].
  q025 (c_if legacy, same skeleton) -> `sx(1); measure(1, 0); z(0).c_if(cr, 1)`, key A kept.
  Not reworked, noted: q028 is close to the feedforward guide's own `for_loop(range(5))` X
  example (range(3) here); not the banned shape.
- **False explanations (keys unchanged):** q015 D "the H and the first CX share a layer"
  (they are sequential; DAG layers show `measure(0, 0)` shares a layer with `cx(1, 2)`).
  q016 B "|100> would appear if the CX gates did nothing" (H-only state is |000>+|001>; B
  now names the big-endian misread). q018 E suggested `sorted(qc.parameters, reverse=True)`
  — raises TypeError (Parameter defines no `<`); now `qc.parameters[::-1]`. q030 E "scheduling
  runs an empty pass set" — executed stage without scheduling_method = ContainsInstruction
  ('delay') + conditional TimeUnitConversion. q031/q036 "level 1 was transpile()'s default in
  Qiskit 1.x" -> "older releases" (2 was already the default before 2.0).
- **Display-letter references:** q014 correct ("Option D creates"), q027 correct ("Option D
  is exactly that pattern") — reworded.
- **Code not runnable as displayed:** q030 and q031 used an undefined `backend` -> stem code
  now defines `GenericBackendV2(num_qubits=5, seed=42)`; q030 proof captures the literal
  `print(pm.stages)` output and compares option reprs to it.
- **Stem underspecification:** q035 "qc ... containing an h gate" admitted an h-only circuit
  for which F (basis_gates only, no coupling map) is also ISA -> comment now "h and cx gates
  on arbitrary qubit pairs" (proof circuit already had non-adjacent CX).
- **Proof weakness:** q018 D was hard-coded False -> runs the stem in 3 processes
  (PYTHONHASHSEED 0/1/12345), one output. q031 first-match count_ops comparison could tie
  across levels -> pins the stem pm's full pass structure (stage + pass names) to explicit
  level 2 only. q033 hand-written ISA checker -> cross-checked with GatesInBasis(target) +
  CheckMap (+ width); all six agree.
- **Docs-reader trap:** guides/set-optimization ("one required positional argument,
  optimization_level") and guides/transpiler-stages ("a positional argument that must be
  specified") contradict the 2.5 signature (`optimization_level=2`) and the API page ("By
  default optimization level 2 is used if this is not specified"). Answered in q031 E.
- **Citation failures replaced (all fetched, quotes grepped):** Parameter page (no ordering
  statement) -> QuantumCircuit API ("sorted alphabetically"; list "assigned ... in the order
  of parameters") q017/q018/q019/q020; construct-circuits (silent on the fact) ->
  QuantumCircuit API / CXGate / Statevector / bit-ordering / api/qiskit/circuit
  "Compile-time parametrization" / ParameterVector / ZGate / SXGate on q016/q021/q022/q023/
  q026/q028/q027(dropped); quantum_info index -> Statevector q016; bit-ordering added q010;
  QuantumCircuit API measure_all (add_bits) added q011; Qiskit v2.0 migration guide ("This
  legacy method has been removed in Qiskit v2.0; you should use the if_test method") added
  q024/q025/q029; set-optimization / transpile-with-pass-managers -> generate_preset_pass_manager
  API + compiler (transpile "If None, level 2 will be chosen") q031/q035/q036; transpile /
  set-optimization -> transpiler-stages layout ("one-to-one mapping ... is necessary") +
  Layout API q034; QuantumCircuit decompose ("one level") added q033.
- **Survived attacks (executed):** q014 A/B/C/F CircuitError, E adds `meas` (4 clbits);
  q019 ValueError "Mismatching number of values and parameters", bind_parameters
  AttributeError, ParameterVector {pv:[0.7]} CircuitError; q020 bound/qc distinct data;
  q024 A AttributeError, B/E TypeError, D CircuitError, F while_loop; q025 D TypeError
  "unexpected keyword argument 'condition'"; q032 level 0 10 CX / level 1 1 CX for seeds
  0-4; q034 level 3 "More virtual qubits (4) exist than physical (3).", initial_layout still
  fails, 4-qubit backend OK; q035 C "'str' object has no attribute 'target'", E list has no
  build_coupling_map.
- **Difficulty:** all 27 kept (q023 stays d1 after the rework: one SX fact + one copy).
- Gates: verify_bank s3 62/62 PROVEN + 5 conceptual, exit 0; audit_meta_patterns s3
  0 blockers / 0 warnings, 9 low length flags (same pre-existing set; q024's option lengths
  shifted equally, 44 vs 42 as before); lint_proof_drift 0 findings.

## Adversarial review A3 — s3b (2026-10-16)

Scope: s3-q037..q058, s3-q073..q076 (26; 7 figure items). Every option incl. pool distractors
re-executed in independent scripts (pinned venv, qiskit 2.5.0 / aer 0.17.2); every cited page
fetched as text and grepped; all figure items re-rendered, rasterized and inspected.
**0 second-answer attacks stuck on the keys, 0 key-letter changes, 0 kills.** 20 edited,
6 survived unchanged (q037, q038, q044, q048, q074, q075).

- **Anti-dup reworks (key letters, objectives, difficulty kept):** s3-q056 used the canonical
  GHZ fan-out (`h(0); cx(0, 1); cx(0, 2)`, highest token overlap in the bank) -> `cx(1, 2);
  t(0); cx(2, 0)` on the 3-line, level 0, layout `[0, 1, 2]`, seed 42: router swaps physical
  0-1, last CX drawn control q_2 -> physical 1 (key B). Variants regenerated (A full map, C
  layout `[2, 1, 0]`, D + basis_gates (T -> Rz, SWAP -> 3 CX), E `cx(0, 2)` routed on the 1-2
  edge); the other valid routing (SWAP 1-2) is in no option. s3-q073 matched the
  `QuantumCircuit.switch` API example (`h`, measure, `case(1, 2): z(1)`, DEFAULT) and the
  feedforward guide's register switch -> `ry(1.2, 0); sx(1)`, bodies Y on q_0 / S on q_1 (key C).
  s3-q057 checked against the cached guides: no docs circuit with the CX/Z redundant pairs —
  circuit kept. Noted, not reworked: s3-q058's `for_loop(range(3))` with `cx(0, 1)` in the body
  is near the for_loop API example (`range(5)`, `h(0); cx(0, 1)`), body and framing differ.
- **Image-size tell:** s3-q057's keyed "nothing removed" figure (16012 B) was the strictly
  busiest SVG in every displayed sample. D (only the CX pair removed, a mirror of B) replaced by
  the same level-0 run with `basis_gates=['rz', 'sx', 'cx']` (31111 B; "translation without a
  target"); all five shown (`display_count` dropped).
- **Drawer facts wrong in text:** s3-q058 explanation/alts said the box reads
  `For-0 range(0, 3)`; executed SVG text is `For` + `r(0, 3)` (and `r(0, 2)` for E). B's alt said
  the region spans both wires; its body touches q_1 only and the box is drawn on q_1 only.
- **False explanations (keys unchanged):** s3-q052 E "DEFAULT may appear anywhere" — executed:
  DEFAULT before `case(0)` raises `CircuitError: 'cases after the default are unreachable'`
  (DEFAULT must be last). s3-q055: "SWAPs are inserted downstream" of SabreLayout and
  "scheduling is present but empty" — executed with a pass callback on a 5-line backend at
  levels 1-3: SabreLayout inserts all SWAPs and the routing stage's SabreSwap never executes;
  scheduling holds ContainsInstruction('delay') + TimeUnitConversion. Stem "Which pass does the
  routing stage run?" -> "is part of"; proof records the observation
  (`line_run_first_swap_inserted_by: SabreLayout`).
- **Code not runnable as displayed:** q040 (undefined `backend`, `qc`; `transpile` in option D
  not imported), q043 (undefined `qc`, `backend`), q054 (no imports), q055 (no import, undefined
  `backend`) — all now define a `GenericBackendV2(num_qubits=5, seed=42)` / circuit, and the
  proofs run the displayed code. q040 stem now "Which line sets `isa` to the ISA circuit …"
  (E `pm.run([qc])` transpiles but assigns a list).
- **Proof weakness:** "which drawing" items q056/q057/q058 compared gate lists with the key built
  by the same function as the target -> now run the verbatim stem code and require SVG
  byte-identity (`svg.hashsalt` fixed, `metadata={"Date": None}`); q073 updated in step.
  Hard-coded False claims replaced by attempts: q039 C/D (`'4'` and even `'3'` -> ValueError;
  seed_transpiler + level 4 -> ValueError), q043 A (`optimization_level=[2, 3, 4]` ->
  ValueError), q046 F, q047 D (measure before the CX still CircuitError), q052 E.
- **Docs-reader traps answered:** transpiler-stages "the hardware may execute up to six CNOT
  gates" per Toffoli (unrouted) vs executed 9 on the 3-line -> q041 E; transpiler-stages
  "Scheduling … does not run by default" vs `pm.stages` listing it -> q042; transpiler-stages
  "By default, SabreLayout runs both layout and routing" -> q055 A; `QuantumCircuit.if_test`
  signature lists only the tuple form, the feedforward guide uses `if_test(parity)` -> q053 C.
  Noted: assign_parameters "keys should be Parameter instances" yet string keys are
  "permissible" (q049 F already says so).
- **Citation failures replaced (fetched, quotes grepped):** transpile-with-pass-managers /
  transpile / set-optimization stated none of q039's range, q043's initial_layout semantics,
  q040's run return -> generate_preset_pass_manager API ("This can be 0, 1, 2, or 3", "Raises
  ValueError", "Initial position of virtual qubits on physical qubits"), compiler API
  (transpile initial_layout), StagedPassManager ("Returns The transformed circuit(s)");
  construct-circuits (silent on tensor, bit order, measure errors, reverse_ops) -> QuantumCircuit
  API (tensor "leftmost operation will be at the bottom", measure cbit, assign_parameters "sorted
  alphabetically" / string keys / CircuitError / ValueError, reverse_ops "does not invert") +
  bit-ordering on q045/q046/q047/q049/q050/q051/q076; Parameter page ("Bases:
  ParameterExpression", "atom of ParameterExpression") q054; visualize-circuits (no control flow)
  -> QuantumCircuit for_loop on q058; transpile guide ("six fundamental stages") on q042;
  set-optimization (level-0 "inserts SWAPs … using SabreSwap") on q055; generate_preset_pass_manager
  API on q056/q057. Kept (verified): transpiler-stages (routing SWAPs, translation, Toffoli),
  transpile (ISA), get-started-with-sampler (ISA), measure-qubits ("Measure qubit 1 into the
  classical bit 0"), feedforward guide (default case, "There is no fallthrough"),
  circuit_classical (expr.equal lifting), TranspileLayout (final_index_layout), api/qiskit/circuit
  (barrier blocks optimizations), InverseCancellation.
- **Survived attacks (executed):** q037 every level emits rz/sx/cx only; q041 level-1 count 9 for
  seeds 0-19 (levels 2/3: 7); q045 Aer {'10'}, Sampler get_int_counts {2}; q049 `{'q': 1.0}` binds
  too, a short list raises ValueError; q051 a fresh `Parameter('th')` key raises CircuitError
  "Cannot bind parameters (th) not present in the circuit."; q053 {'1 11': all}; q074
  `final_index_layout()` = routing_permutation = [0, 2, 3, 1]; q075 X pair cancelled in init,
  a merged 1q run with no target becomes `u2` (D holds); q076 reverse_ops = t, cx(0,1), s, h.
- **Figures:** q056/q057/q073 regenerated; all seven rendered (`render_figures --only`, 0
  failures; `--check` 69/0) and inspected as PNG; alts match. Sizes: q056 A 10520 / B (key)
  11544 / C 11452 / D 25224 / E 11515; q057 A 10806 / B 14841 / C (key) 16012 / D 31111 / E 13535;
  q073 A 29644 / B 27483 / C (key) 28114 / D 24150.
- **Difficulty:** all 26 kept.
- Gates: verify_bank s3 62/62 PROVEN + 5 conceptual, exit 0; audit_meta_patterns s3 0 blockers /
  0 warnings, 9 low length flags (same pre-existing set; q037/q039/q052 options untouched);
  lint_proof_drift 0 findings; render_figures --check 69 questions, 0 failures.

## Adversarial review A3 — s4a (2026-10-16)

Scope: s4-q001, s4-q010..q030 (22; 8 executed, 14 conceptual). Every executable option incl.
pool distractors re-run in independent scripts (pinned venv, qiskit 2.5.0 / runtime 0.48.0);
runtime behavior not runnable offline read from the INSTALLED 0.48 source; every cited page
fetched as text and grepped. **0 key changes, 0 kills.** 18 edited, 4 survived unchanged
(q014, q017, q027, q030).

- **Second-answer / premise fixes (keys unchanged):** s4-q015 stem had no "real QPU", so E
  ("Open Plan users can open a session, but only in local testing mode") was literally true:
  `Session.__init__` sends any non-IBMBackend `BackendV2` to `QiskitRuntimeLocalService`, for
  every plan. Stem now "submits jobs to a real QPU"; E rewritten to the batch-TTL confusion
  (the Open Plan 10-minute max TTL is batch's, run-jobs-batch table). s4-q025 "which channel
  does `QiskitRuntimeService()` use" had a saved-account reading (`AccountManager.get` loads a
  saved default of any channel) -> "use by default"; E's "raises unless a saved account or
  `channel=` supplies one" was half true (a bare call with nothing saved does raise
  AccountNotFoundError) -> clean "no default channel". Executed in an isolated HOME:
  `save_account(token=, instance=)` writes `default-ibm-quantum-platform` with channel
  `ibm_quantum_platform`; `channel="ibm_quantum"` -> ValueError. s4-q001 "30 independent
  circuits": the FAQ/best practices say to combine sub-minute jobs into one larger job, an
  answer outside the options -> "30 independent jobs". s4-q029 "Besides shorter queuing ...
  over one giant job": a single job queues once too; the FAQ credits batch with parallel
  classical processing -> "Besides parallel classical processing".
- **False rationales:** s4-q021 A said "construction succeeds; the failure happens at run
  time", contradicting the key and its own proof (`SamplerV2()` raises `ValueError: A backend or
  session must be specified.` in the constructor). s4-q019 C/D: 0.48 `backend(self, name, ...)`
  requires `name`, so `service.backend()` and `backend(least_busy=True)` raise TypeError
  (signature bind). s4-q010 F: fair-share balances across instances by allocation, not "users
  and projects" (fair-share-scheduler guide). s4-q024 E said "nothing is cached client-side in
  the primitive", but the noise-learning guide passes a learned model into `EstimatorV2` via
  `options.resilience.layer_noise_model` (with `mode=backend`); F ignored the standalone
  `NoiseLearner(mode=...)` program. s4-q001 F rebuilt from execution: nested
  `with Session(fake): with Batch(fake):` -> `SamplerV2()._mode is batch`; after the inner block
  exits, `SamplerV2()` raises "A backend or session must be specified." (one ContextVar, reset
  to None by `Batch.__exit__`), so modes never stack.
- **s4-q020 key (F) re-checked against installed code, executed:** `get_mode_service_backend`
  called with stub `IBMBackend` objects and `set_cm_session(batch)`: the batch's own backend
  object -> mode is the batch (warning "will run inside this session/batch instead of in job
  mode"); another `IBMBackend` object -> ValueError "The backend passed in to the primitive is
  different from the session backend". `IBMBackend`/`BackendV2` define no `__eq__`, so "the
  backend object the batch was opened on" (F's wording) is exactly identity.
- **Code not runnable as displayed:** q023 (no imports, undefined `pm`/`backend`) and q026 (no
  imports) now self-contained; their proofs exec the verbatim stem code. q013/q020/q028
  fragments now say where `backend`/`isa`/`service` come from; q028's comment states `isa` is a
  `measure_all()` circuit (the `data.meas` key and option E both depend on the register name).
- **Proof weakness:** q023 B/C/D and q016 B/C were flags inferred from the key's success
  (`not fix_works`, `not mode_works`) -> now attempted: `job.result().counts` AttributeError,
  Bell counts returned, `from qiskit.primitives import SamplerV2` ImportError, `SamplerV2(isa)`
  ValueError. q028 now execs the six displayed option snippets verbatim (the old proof
  re-typed them under swapped function names). Install paths and raw shot counts kept out of
  evidence strings.
- **Docs-reader traps answered:** choose-execution-mode "Job ... Might run sooner than batch
  mode" (q001 C, q010 C); run-jobs-batch comment "earlier than 0.24.0, change `mode=` to
  `batch=`" (q013 B: TypeError in 0.48); execution-modes "To run in job mode, specify
  mode=backend" (q020 B, assumes no open context); QiskitRuntimeService API "ibm_cloud ... points
  to the same path as ibm_quantum_platform" (q025 A); current SamplerV2 API lists
  `run(..., dry_run=False)` (0.50) — q016 E now scoped to 0.48 (`pubs`, `shots`). Noted:
  execution-modes "Any job currently running won't run to completion if doing so would exceed
  the instance's cost limit" — q027 D ("running jobs finish") kept, it is the TTL rule.
- **Citation failures replaced (fetched, quotes grepped):** execution-modes (silent on ISA,
  observables, close semantics, the missing-mode error) dropped/replaced on q012 (->
  get-started-with-sampler "transformed to only use instructions supported by the QPU"), q018
  (-> get-started-with-estimator `apply_layout`), q022 (-> execution-modes-faq "Session.close()
  ... existing jobs run to completion. Session.cancel() cancels all pending"), q023/q028 (->
  primitive-input-output "'meas', which is the default name of the classical register when this
  is added by the measure_all method"), q026; run-jobs-batch -> FAQ on q029 ("If some jobs fail,
  you still get results"), dropped on q001/q011, added on q015 (TTL table); hello-world ->
  SamplerV2 API (`mode` Backend/Session/Batch) q016/q021, -> QiskitRuntimeService API on q025
  ("set to ibm_quantum_platform by default"); run-jobs-session -> QiskitRuntimeService API on
  q019 ("The backend with the fewest number of pending jobs"); + fair-share-scheduler q010,
  noise-learning q024, SamplerV2 API q013. Docs-only gap: the `ValueError` for no mode (q021)
  and the observable-size `ValueError` (q018, builtin type, not the `IBMInputValueError`
  subclass) are execution-carried.
- **Survived attacks (executed):** q012 IBMInputValueError naming `h` at `run()`; q013
  session=/batch=/backend= TypeError, `mode="batch"` and `mode=batch.backend()` ('fake_manila')
  ValueError; q016 `run([isa], backend)` / `run(..., mode=)` TypeError; q018 evs after
  apply_layout ~0.87; q026 cx (0, 4) rejected; q028 A/D invalid pub-like, C TypeError, E/F
  AttributeError; q030 `save_account(api_key=)` TypeError, no `login`/`save`.
- **Difficulty:** all 22 kept.
- Gates: verify_bank s4 30/30 PROVEN + 25 conceptual, exit 0; audit_meta_patterns s4 0 blockers /
  0 warnings, 10 low length flags (q015's only option change lengthened a distractor, so no new
  variant); lint_proof_drift 0 findings.

## Adversarial review A3 — s4b (2026-10-16)

Scope: s4-q031..q049, s4-q061..q063 (22; 13 executed, 9 conceptual; figure items q047, q048,
q049, q061, q062, q063 rendered, rasterized and read). Every executable option, pool distractors
included, re-run in independent scripts (pinned venv, qiskit 2.5.0 / runtime 0.48.0); runtime
behavior read from the INSTALLED 0.48 source; every cited page fetched as text and grepped.
**0 key changes, 0 kills.** 17 edited, 5 survived unchanged (q033, q041, q049, q062, q063).

- **Second-answer / loose-reading fixes (keys unchanged):** s4-q039 E ("session mode is
  available to Open Plan users") was true under local testing mode (s4-q015 precedent) -> "can
  submit session jobs to a QPU". s4-q035 F ("local testing ... then submitted with
  `mode=backend`") ended in job mode, i.e. the key -> F now claims local testing is a fourth
  execution mode that replaces the QPU run. s4-q061 left CX direction open (CouplingMap API:
  "directed edges correspond to permitted CNOT gates"; a one-way coupling rejects `cx(1, 0)` even
  on the keyed map) -> code comment: every drawn coupling supports cx both ways (FakeLimaV2's
  target has cx on (0,1) and (1,0); the proof's GenericBackendV2 is bidirectional).
- **False rationales, rebuilt from execution/source:** s4-q043 DC said the second list "is
  interpreted as shots" (0.48 `run(pubs, *, shots=None)`: TypeError "takes 2 positional arguments
  but 3 were given"); DA said the PUB's first element is a list of circuits (the inner list IS the
  pub: `isa2` lands in the parameter-values slot -> ValueError). s4-q038 DE "Session exposes close,
  cancel, status, details and backend, and nothing else" (0.48 also has usage, session_id,
  service, from_id). s4-q035 DE "a primitive never picks a mode by itself" (`get_mode_service_backend`
  adopts `get_cm_session()` when `mode` is None). s4-q037 DF "a single job has no service-side
  classical processing" -> rewritten; DE "opening one costs nothing" trimmed. s4-q046 correct:
  dropped "the one pattern where adding observables does not multiply the work".
- **Display letters:** s4-q031 correct cited "(A)"/"(B)" for keys B/C (wrong letters too);
  s4-q039 correct cited "(A)(B)(C)" -> letter-free.
- **Code not runnable as displayed:** q036, q044, q045 had no imports -> added; their proofs now
  exec the verbatim stem code (q036 also each option as a literal edit of it; q036 A now says `pm`
  is a preset pass manager for `backend`). q038/q043/q047/q048 fragments now say where
  `backend`/`isa1`/`estimator`/`circuit` come from.
- **Proof weakness:** hard-coded / never-attempted flags now attempted: q032 A (a
  `QiskitRuntimeLocalService` initialized first, string still ValueError; resolver takes only
  `mode`), q042 D (verbatim code, scored by whether it raised; printed literal `fake_manila`),
  q044 E (`resilience_level=1` on the fake backend: "The resilience_level option has no effect in
  local testing mode.", value unchanged). Keys now check the property asked, not just success:
  q034 `sampler.mode is None` (job mode), q038 `estimator.mode is session`, q043 two pub results.
  q036 D was attempted with the ISA circuit -> literal `run([(qc, obs)], backend)` (TypeError).
  q044 (shot noise): options scored on a `seed_simulator=42` run (0.8765); the verbatim unseeded
  stem run is used only as a (0.7, 1.0) band check, no raw unseeded value in evidence.
  q047 proof scores the coerced BindingsArray shape and asserts the figure captions.
- **Docs-example duplication:** s4-q047 used the primitive-input-output guide's own outer/product
  example shapes ((4, 1) observables x (1, 6) values, four single Paulis) -> reworked to (3, 1) x
  (1, 5) in code, generator, options, alt and proof; re-rendered and read. s4-q048 kept at 5 rows:
  its `reshape(5, 1)` one-parameter coercion twist is not the guide's zip example.
- **Docs-reader traps answered:** EstimatorV2 API/0.48 signature annotate `mode` with `| str`
  (q038 DC: any string -> ValueError); run-jobs-batch caution "If you set backend=backend ... run
  in job mode" (q034 DB: deprecated keyword, TypeError in 0.48); initialize-account "free plans
  are prioritized by default" (q040 DC: instance choice, not saved-account choice);
  choose-execution-mode "classical computation, such as compilation, is run in parallel" (q037
  DF: service-side, across several jobs); local-testing-mode "mitigation options are implemented
  locally" (q044 DE: 0.50 client-side primitives; 0.48 warns no effect).
- **s4-q040 executed although conceptual:** temp account file, 0.48 `save_account` +
  `AccountManager.get`, both save orders -> `premium_acct` (file written sort_keys; last matching
  channel wins). Confirms D, refutes B/E.
- **Citation failures replaced (fetched, quotes grepped):** hello-world -> SamplerV2 API on q032
  (`mode (BackendV2 | Session | Batch | None)`) and q034 ("A Backend if you are using job mode");
  execution-modes -> get-started-with-estimator on q036 ("circuit and observable need to be
  transformed", apply_layout); run-jobs-batch -> execution-modes-faq on q037 ("other jobs in that
  batch essentially jump to the front of the queue"); run-jobs-session/execution-modes -> Session
  API (`backend()` returns `str | None`) + local-testing-mode on q042; execution-modes/hello-world
  -> SamplerV2 API + primitive-input-output on q043; execution-modes -> local-testing-mode on q044
  ("noise model from the snapshot is automatically applied"); estimator-v2 API /
  get-started-with-estimator (no broadcasting content) dropped on q045-q048, primitive-input-output
  carries the pattern table.
- **Survived attacks (executed):** q033/q041 TTL definitions vs execution-modes ("When the first
  job starts running, the maximum TTL timer starts"); q045 evs (3, 4); q046 six pairings (only E
  equal non-scalar shapes; D ValueError); q048 (5,) x (5,) -> evs (5,); q061 only A runs, B/C/D
  IBMInputValueError; q062 only [1, 0, 2, 3] 0 SWAPs / 3 CX; q063 '110' (noiseless 200/200), each
  distractor reproduced by its misreading. Figures: all renders match alt texts.
- **Difficulty:** all 22 kept.
- Gates: verify_bank s4 30/30 PROVEN + 25 conceptual, exit 0; audit_meta_patterns s4 0 blockers /
  0 warnings, 10 low length flags, all pre-existing (the q035 format tell and q036 length tell my
  rewrites introduced were fixed); lint_proof_drift 0 findings (q038 F evidence trimmed to the
  exception's first line); render_figures OK for q047.

## Adversarial review A3 — s5a (2026-10-16)

Scope: s5-q001, s5-q010, q011, q013..q015, q017..q028 (18; 17 executed, 1 conceptual). Every
option, pool distractors included, re-run in independent scratch scripts (pinned venv, qiskit
2.5.0 / runtime 0.48.0); local-testing behavior read from the INSTALLED 0.48 source; every cited
page fetched as text and grepped. **0 key changes, 0 kills.** 18 edited, 0 survived unchanged.

- **Hollow proof (s5-q028):** C (DD) and E (measurement twirling) were "refuted" by enabling the
  options on `SamplerV2(mode=FakeManilaV2())`, but 0.48 `fake_provider/local_service.py` drops them
  (`warnings.warn(f"Options {options_copy} have no effect in local testing mode.")`); executed,
  the counts with DD on, twirling on and neither were byte-identical. Proof now asserts that warning
  and applies each technique explicitly under a readout-only `NoiseModel` (gates noiseless):
  Qiskit's `PadDynamicalDecoupling` inserted 4 X pulses into an idle window, odd parity unchanged
  (13.6%); an emulated 16-randomization measurement twirl (random X before measure, classical flip
  after) still 16.7% odd parity. Stem "Which do-it-yourself correction" echoed only the key
  ("post-selection you code yourself") -> "Which approach removes them from the result?".
- **Second-answer fix (s5-q021, conceptual):** stem asked for "untouched per-shot outcomes ... own
  readout calibration" while E called `meas_type='kerneled'` "the raw per-shot readout"; per-shot IQ
  points are rawer than classified bits and are exactly what a custom discriminator calibrates on.
  Stem now asks for uncorrected outcomes for a readout-error correction; E claims kerneled switches
  off a default readout correction (none exists; 0.48 `meas_type` is a return-format Literal
  classified/kerneled/avg_kerneled). Key quote: readout-error-mitigation-sampler tutorial "Unlike the
  Estimator primitive, the Sampler primitive does not have built-in support for error mitigation."
- **Key text not literally doable (s5-q018):** "Reshape to (5, 2)" — executed, `vals.reshape(5, 2)`
  on the (5, 3) array raises `ValueError: cannot reshape array of size 15 into shape (5,2)` -> "Rebuild
  `vals` as a (5, 2) array"; proof label typo "1-A" -> "1-D".
- **False rationales rebuilt from execution:** s5-q013 DE said `decompose()` gives `u`/`cx` (it gives
  h/t/tdg/u/cx; run rejects `u`), DD now names the constructor ValueError ("A backend or session must be
  specified."); s5-q014 DE "the same validation error" (constructor path is a ValidationError
  "Unexpected keyword argument", assignment is "Object has no attribute"); s5-q010 DD scoped to the
  service `default_shots` (local fake fallback is 1024, not 4096); s5-q019 DA names the
  AttributeError; s5-q026 correct adds the twirling rung of the sampler-options precedence list.
- **Docs-reader traps answered:** bit-ordering guide "the IBM Quantum Compute Service Sampler and
  Estimator primitives return big-endian results" (s5-q015 DB: BitArray layout, `to_bool_array()`
  defaults to `order='big'`; executed key '001' -> bool row [F, F, T]; BitArray reference "index 0 ...
  right-most bitstring entry as returned by get_counts()"); runtime-options-overview "Commonly-used
  options, such as resilience_level, are at the first level" (s5-q014 DB, s5-q020 DB: Estimator
  example, SamplerOptions has no such field); latest SamplerV2 API `run(pubs, *, shots=None,
  dry_run=False)` (s5-q001 DD: dry_run is 0.50, 0.48 has only `shots`); BitArray `get_counts`
  "counts from all positions in this array are unioned together" (s5-q023 DF: tallies added, 2 keys
  holding 2000 shots); error-mitigation TREX "diagonalizing the readout-error transfer matrix"
  (s5-q028 DE: symmetrizes, rescaling is an Estimator step).
- **Code not runnable as displayed:** q001/q010/q011/q017/q018/q022/q023/q026 fragments now say where
  `backend`/`sampler`/`isa` come from (q023 pins a 1-qubit circuit so the distinct-key distractor
  yields its 2); q022/q024/q025/q026 gained their missing imports.
- **Proof hygiene:** display letters removed from evidence strings (q010, q015, q023, q026: "option E
  claims ..."); q010 unseeded raw counts dropped from `observed`; q011 B now checks per-shot storage
  (256 bitstrings = num_shots) and that `get_counts()` sums to num_shots, not just the type name.
- **Citation failures replaced (fetched, quotes grepped):** SamplerV2 API page (no BitArray/DataBin/
  ordering content) replaced on q011/q023 (-> BitArray API), q024/q025 (-> DataBin API "attributes and
  keys are the names of the ClassicalRegister objects"), q015 (-> bit-ordering + BitArray API), q017
  (-> primitive-input-output "the last index is over circuit Parameter objects" + BitArray API
  "preceding axes correspond to the shape of the pub"), q018 (-> primitive-input-output), q014/q020
  (-> SamplerOptions API field list), q027 (-> TwirlingOptions API signature + sampler-options table);
  runtime-options-overview dropped on q014/q020/q027; error-mitigation-and-suppression-techniques
  dropped on q019/q021 (no option fields); q001 -> SamplerV2 API ("An iterable of pub-like objects")
  + sampler-options ("The only values you can pass to run() ... That is, shots"); q021 -> readout
  tutorial + sampler-options (meas_type choices).
- **Survived attacks (executed):** q001 B ValueError (CircuitInstruction pub-like), C/D/E/F TypeError;
  q010 1000; q013 only the preset-PM ISA run succeeds, F fails on cx (0, 2); q017 (3, 4); q019 A
  AttributeError, B/E ValidationError, C TypeError, F leaves enable Unset; q020 A/C/D accepted, F
  rejected by SamplerExecutionOptionsV2 (init_qubits, rep_delay, meas_type); q022 only (isa, vals, 256)
  runs; q024 only `data.alice` (SamplerPubResult exposes data/join_data/metadata); q025 A/F KeyError,
  E AttributeError; q026 50 (bare PUB 1000); q027 0.48 TwirlingOptions = enable_gates, enable_measure,
  num_randomizations, shots_per_randomization, strategy.
- **Difficulty:** all 18 kept.
- Gates: verify_bank s5 37/37 PROVEN + 6 conceptual, 0 failures; audit_meta_patterns s5 0 blockers /
  0 warnings, 4 flagged (q010/q025/q026 low length flags pre-existing, options untouched; the q021
  stem-echo and q018 length tells my rewrites introduced were fixed); lint_proof_drift 0 findings
  (q028 D evidence now quotes a kept fraction, not the shot total).

## Adversarial review A3 — s5b (2026-10-16)

Scope: s5-q029..q043, s5-q052, s5-q053 (17; 13 executed, 4 conceptual: q030/q034/q037/q038;
6 figure items). Run in two sittings: q029..q036 were edited by an
interrupted first run and re-checked here (verify_bank per id, displayed code, notes vs change; A3
notes amended, rounds not re-incremented); q037..q043/q052/q053 fully reviewed. Every option re-run
in independent scratch scripts (pinned venv, qiskit 2.5.0 / runtime 0.48.0); every cited page fetched
as text and grepped; all six figure items rendered, rasterized and inspected.
**0 key changes, 0 kills.** 17 edited, 0 survived unchanged.

- **Second answers closed (first sitting, re-checked):** s5-q036 E `0b11` IS the int 3 (`0b11 == 3`
  -> True) -> E is now the string `'0b11'`; s5-q030 unqualified "the Sampler primitive" let E (V1
  quasi-distributions; primitives guide "V1 primitives are still usable") be right -> stem names
  SamplerV2; s5-q035 "circuit executions" let C (6 bound circuits) be right -> stem counts every
  shot as one execution (executed: shape (6,), 200 per set, 1200).
- **Visual odd-one-out tell (s5-q052):** rasterized, all four distractor histograms put the 195 bar
  on the left and only the key put 205 there (structural: with c[0] the mid-circuit bit, the key
  alone files the c[0]=1 shots under the lexicographically smaller key). Reworked: qubit 0 measured
  into c[1], qubit 1 into c[0], condition on c[1]==0. Executed (AerSimulator, seed 21, 400 shots):
  key `{'01': 195, '10': 205}`; A/B/C circuits executed -> `00/11`, `01/11`, `00/10` with 195 left;
  only the bit-order distractor D swaps sides. Key letter E kept; generator, alts, rationales redone.
- **False rationales:** s5-q037 DF called M3 "a maximum-likelihood fit" (readout tutorial: M3 solves
  `p~ = M p` on a reduced matrix; "equation (2) is not solved by inverting M") -> key text "Solve
  against an assignment matrix ... e.g. with M3", "rigorously" dropped from the stem (M3 ignores
  3rd-order correlations); s5-q042 DA said a count-from-one reading of `get_counts(2)` lands on the
  FIRST angle (it lands on the second, pi/2 = the B drawing) -> DB names the count-from-one slip, DA a
  reversed-sweep reading; s5-q032 DD used the "little-endian" label the key avoids (docs-reader trap).
- **Alt text vs render:** s5-q041 D alt said "Count axis", the render's y label is
  "Quasi-probability" (plot_histogram on float values); s5-q042 E alt singled out "one tally being a
  three-digit number" though A's 146 is three-digit too -> all five alts now give the same detail
  (share of the tall bar, total).
- **Figure proofs compared the key with itself:** q040 (C), q041 (A), q042 (D), q043 (B), q052 (E)
  took the target from the generator's own function/call. All five now execute the DISPLAYED stem
  code verbatim (AST: exec the body, eval the last line to capture the figure), render it and every
  variant to SVG in-process (`svg.hashsalt` fixed, `metadata={"Date": None}`) and require
  byte-identity plus a tick-slot bar/axis match; only the key matches. q043 also asserts the stem's
  counts literal equals the seeded FakeManilaV2 run its comment claims; q041 asserts the premise
  ('10' never sampled); q042 no longer pairs bars with ticks by patch order. s5-q053 (stem figure,
  GATES-pinned) now also runs the displayed code unseeded 3x: same printed key list.
- **Code not runnable as displayed / proof hygiene:** q029/q031/q033/q035/q039 fragments say where
  `sampler`/`isa`/`backend` come from or gained imports; q029/q039 proofs run the displayed code with
  stdout captured; display letters dropped from evidence (q029, q035, q039 "option E/F claims");
  unseeded raw counts dropped from q039 `observed`, q029 seeded.
- **Docs-reader traps answered:** primitives guide "SamplerV2 ... including error mitigation" and
  error-mitigation guide "measurement twirling ... diagonalizing the readout-error transfer matrix"
  (s5-q037 DB/DD: TREX is the Estimator's step); bit-ordering "Sampler and Estimator primitives
  return big-endian results" (s5-q032 key + DD); SamplerV2 API `shots` "total number of shots ... for
  each sampler pub" (s5-q035 DB); plot_histogram "The number of terms to plot" (s5-q043 DD: `rest` is
  extra, "more bars than number_to_keep + 1").
- **Citation failures replaced (fetched, quotes grepped):** s5-q038 none of three pages stated
  1/sqrt(N) -> estimator-input-output ("sigma_O / sqrt(N_shots)") + EstimatorOptions API ("Default:
  0.015625 (1 / sqrt(4096))"); s5-q043 visualization index + primitive-input-output -> plot_histogram
  API ("The rest is made into a single bar called 'rest'"); s5-q039 SamplerV2 API -> PrimitiveResult
  API ("A container for multiple pub results"); s5-q040 primitive-input-output -> bit-ordering;
  s5-q053 measure-qubits (no reset content) -> QuantumCircuit API ("Reset the quantum bit(s) to their
  default state") + bit-ordering; s5-q037 primitives guide dropped; q029/q031/q032/q034/q035/q036
  replacements per their notes (SamplerV2 API page carries no BitArray/seed/ordering content).
- **Survived attacks (executed):** q029 777 (entries = shot rows in order); q031 only
  `simulator.seed_simulator` (A/D/E ValidationError, C/F TypeError); q033 only the options dict
  (D accepted but ignored: 1024); q034 `resilience_level` ValidationError, Sampler twirling defaults
  False (installed TwirlingOptions docstring); q039 `len(result)` 3, PrimitiveResult indexable; q040
  noisy 8-bar key, D 7 bars; q043 rest=42.
- **Anti-tell:** s5-q032 medium absolute_distractor_tell (tokenizer reads `measure_all` as "all", plus
  F "cannot") -> F reworded, key gains a true "always"; s5-q036 low length tell cleared.
- **Difficulty:** all 17 kept.
- Gates: verify_bank s5 37/37 PROVEN + 6 conceptual, 0 failures; audit_meta_patterns s5 0 blockers /
  0 warnings, 3 flagged (q010/q025/q026 low length, pre-existing, outside this batch); lint_proof_drift
  0 findings.

## Adversarial review A3 — s6a (2026-10-16)

Scope: s6-q010..q027 (18; 14 executed, 4 conceptual: q018/q019/q021/q026; no figure items). Every
option re-run in independent scratch scripts (pinned venv, qiskit 2.5.0 / runtime 0.48.0), runtime
claims on `qiskit_ibm_runtime.EstimatorV2(mode=FakeManilaV2())` (local mode), every displayed
predict-output block executed verbatim, every cited page fetched as text and grepped.
**0 key changes, 0 kills.** 14 edited, 4 survived unchanged (q019, q020, q021, q025).

- **Literal-print mismatch (stem attack):** "What does this code print?" keyed values that are not the
  literal output: q011 prints `0.9999999999999998`, q022 `2.999999999999999`, q027
  `1.5000000000000002` (stems now "Up to floating-point rounding, ..."); q015 prints `[ 1. -1.]` and
  q023 `[ 1.00000000e+00  2.22044605e-16 -1.00000000e+00]` (stems now ask which values the printed
  `evs` holds, q023 rounded to three decimals; s1-q018 precedent). All five proofs record the literal
  printed string in `observed`.
- **Stem false about where it fails (s6-q013):** stem and code comment said `result()` raises;
  executed, runtime 0.48 `EstimatorV2.run()` itself raises `ValueError: The number of qubits of the
  circuit (5) does not match ... observable (2)` (job never returned). Stem/comment now say `run()`;
  proof records `raised_at: run()`. Fixes re-run: only `apply_layout` runs; E's pinned layout still
  5 wide, F `TypeError` (no `num_qubits` on `SparsePauliOp.__init__`).
- **False rationales:** s6-q014 E claimed the retired V1 interface used a 0-4 scale (V1 Estimator was
  0-3) -> now the open-ended-dial misconception, PEC via `resilience.pec_mitigation`; s6-q023 F
  claimed an extra observable dimension gives the nested `(3, 1)` shape -> executed `[[obs]]` gives
  `(1, 3)`, a `(3, 1)` observable array `(3, 3)`; only bindings nested as `(3, 1, 1)` give `(3, 1)`
  (rationale rewritten, shape recorded in the proof); s6-q018 B "not equivalent ... under any
  circumstances" overclaimed -> the distribution must be weighted with eigenvalues.
- **Displayed code not runnable / proofs off the displayed API:** s6-q010 `job`/`estimator` were only a
  comment -> fragment now builds them (names defined earlier stated); proof moved from
  StatevectorEstimator to runtime EstimatorV2 local mode (seeded via `simulator.seed_simulator`, which
  local_service passes through) and evaluates each option's literal expression (D was tested as
  `data.quasi_dists`, displayed is `result[0].quasi_dists`); q012/q016 comments now define `backend`;
  q014 proof assigns on `EstimatorV2(mode=...).options` as displayed and quotes the validator
  (`must be <=2`; installed `MAX_RESILIENCE_LEVEL = 2`).
- **Proof strengthened (s6-q017):** it measured shot noise with StatevectorSampler only; now also runs
  runtime EstimatorV2 at precision 0.02 and 0.01 and reads PUB metadata shots (2500 -> 10000, ratio 4)
  — `precision`/`default_precision` are among the few options local mode honors (local_service.py
  pops `default_shots`, `default_precision`, `seed_simulator`; everything else warns "have no effect
  in local testing mode"). s6-q016 evidence shows the key actually tightens (target_precision 0.01 vs
  default 0.015625; shots in `observed`).
- **Citation failures replaced (fetched, quotes grepped):** specify-observables-pauli was cited for
  facts it does not state in q011/q013/q015/q022/q027 -> primitive-input-output ("Estimator returns one
  expectation value estimate for each element of the broadcasted shape"; "a single observable
  represented as a 0-d array"), VQE course ("the weighted sum of expectation values of the constituent
  terms"), Pauli API ("qubit-0 corresponds to the right-most Pauli character"), SparsePauliOp API
  (`apply_layout`: "the number of the transpiler output circuit qubits will be used by default";
  `from_sparse_list(obj, num_qubits, ...)`, also added to q024), RYGate API (q023, q027);
  q014 runtime-options-overview (no level range) -> EstimatorOptions API (levels 0/1/2); q017 +
  estimator-input-output ("sigma_O / sqrt(N_shots)"); q026 error-mitigation-and-suppression (no option
  path) -> estimator-noise-management ("ZNE How to enable : options.resilience.zne_mitigation = True";
  level table 1 = TREX, 2 = Level 1 + ZNE and gate twirling).
- **Survived attacks (executed):** q012 only `[(isa, iobs)]` (A/C ValueError pub-like, D/E TypeError,
  F KeyError 0); q016 installed signature `run(pubs, *, precision=None)`, F ValidationError; q020 only
  `zne.noise_factors` (A/B/C ValidationError, E/F no_such_attribute; `>= 1` validator confirmed);
  q024 only B; q025 displayed error string matches verbatim, raised at `run()`, 0.1 identical error;
  q026 only B sets `resilience.zne_mitigation` True (F silently sets an attribute on the `Unset`
  sentinel, no error, flag stays Unset — as DF says); q019/q021 checked against the
  error-mitigation-and-suppression page (DD "suppressing errors", PEC "unbiased", ZNE "not guaranteed
  to produce an unbiased result").
- **Difficulty:** all 18 kept.
- Gates: verify_bank s6 32/32 PROVEN + 13 conceptual, 0 failures; audit_meta_patterns s6 0 blockers /
  0 warnings (low length_tell on q013/q020/q021 pre-existing, options untouched); lint_proof_drift 0
  findings.

## Adversarial review A3 — s6b (2026-10-16)

Scope: s6-q028..q042, s6-q052..q054 (18; now 12 executed, 6 conceptual: q028/q029/q032/q034/q036/
q039 -- q038 moved from conceptual to executed; 6 figure items: q040 option images,
q041/q042/q052/q053/q054 stem figures). Every option re-run in independent scratch scripts (pinned venv, qiskit 2.5.0 / runtime
0.48.0; runtime claims on `EstimatorV2(mode=FakeManilaV2())` local mode), every displayed block run,
every cited page fetched as text and grepped, all figure items rendered, rasterized and inspected.
**0 key changes, 0 kills.** 14 edited, 4 survived unchanged (q028, q029, q030, q039).

- **Second answer closed (s6-q042):** A ("a single `SparsePauliOp("Z")` with a (2, 3) parameter
  array") reproduces the drawn numbers exactly with a second row (pi/3, 0, pi/3): executed (2, 3)
  `[[0.866, 0, -0.866], [0.5, 1, 0.5]]`; the proof had only tried a strawman row `[0, pi/4, pi/2]`.
  A is now the tiled-angles zip (`[Z, X]` with the angles repeated per observable: `ValueError ...
  shapes (2,) and (2, 3) are not broadcastable`). D re-run: `[[Z, X]]` with (3, 1) rejected
  ((1, 2) vs (3,)); the only (3, 2) route is a (3, 1, 1) array, not an option.
- **Distractor values no misconception produces (s6-q033):** E's rationale said a 1-based reading of
  `[2, 0]` gives Z on qubits {0, 3}; it gives {1, 3} (= B, `ZIZI`); F's "span" reading cannot give
  {1, 2}. With a symmetric `ZZ` all six two-Z labels were in play, so E/F are now the two real
  layout-list misconceptions ("one entry per target qubit", "index 2 does not exist on the 2-qubit
  observable"), executed as non-raising with the true boundaries recorded (`[2]` -> `QiskitError
  Number of qargs does not match (1 != 2)`; `[4, 0]` -> `indices outside the number of qubits`).
  B/C rationales now name big-endian position reading / right-padding.
- **Partly-true distractor (s6-q034):** E "typically noisier" is partly true of mitigated
  estimators (and DE's claim that the service still meets the requested precision is unverifiable)
  -> E "typically less accurate", contradicted verbatim by estimator-noise-management ("Higher levels
  generate more accurate results, at the expense of longer processing times").
- **Displayed code vs figure (s6-q041):** the stem code drew no axis labels while the figure had
  them; code gains `plt.xlabel/ylabel`, the generator now renders the DISPLAYED code verbatim with
  the keyed line inserted (asserting TARGET), and the proof runs the displayed program with each
  option line and reads marker heights and error-bar half-lengths back off the drawn figure. Local
  mode honours `default_precision` + `simulator.seed_simulator`: 0.1 -> 100 shots/point, stds
  0.039-0.095 (match); 0.01 -> 10000 shots, stds 0.002-0.009 (DC now quotes these).
- **Figure proofs off the displayed code:** s6-q040 compared the generator's own series with
  itself -> now execs the displayed sweep and requires SVG byte-identity (fixed hashsalt, no Date)
  plus point match; only B. s6-q052 now substitutes each option line into the displayed code and
  reads the plotted markers back (only XX; YY = -sin, IZ = cos, ZZ = 1, IX = 0). Visual tells: q040
  keyed U-curve is not the odd one out (D is its mirror, E shares both endpoints); all alts match.
- **Proofs on the wrong object / false evidence:** s6-q031 proof validated a bare
  `EstimatorOptions` -> now the displayed lines on `EstimatorV2(mode=...)`, F via the real
  constructor `options=`, plus the installed validator line
  `make_constraint_validator("default_precision", gt=0)`; DB notes 1000 is accepted (stored 1000.0,
  a std error, not shots). s6-q037 F evidence called precision 0.01 "tighter" than the 0.0 default
  -> now 0.1 -> 0.01, stds 0.0 both (installed source: `stds = np.zeros_like(...)`, precision only
  perturbs `evs`).
- **Conceptual -> executed (s6-q038):** local mode shows PUB 0.02 > run() 0.03 > default 0.05
  resolution, shots = ceil(1/p^2) (2500/1112/400), reported stds on |+> Z equal to the target (A),
  `run(shots=)` TypeError.
- **Docs-reader traps answered:** s6-q032 DE (PEA also learns a layer noise model, so "PEC needs a
  learned noise model" is not the difference); s6-q035 DE (SparsePauliOp API "Raises QiskitError - If
  the number of qubits is incompatible with the indices"); s6-q040 DC (RY matrix's cos(theta/2) entry
  is the amplitude, not <Z>).
- **Citation failures replaced (fetched, quotes grepped):** specify-observables-pauli was cited for
  apply_layout / label order / broadcasting it never states (q033, q036, q040, q042, q052, q053) ->
  SparsePauliOp API, Pauli API ("qubit-0 corresponds to the right-most Pauli character"), QAOA
  tutorial (q036: "transform the observable defined on virtual qubits to an observable defined on all
  physical qubits"), RYGate API (q040, q052), primitive-input-output; q037 + StatevectorEstimator API
  ("the error is 0 for this StatevectorEstimator"); q031/q038/q041 + EstimatorOptions API; q038 +
  estimator-input-output (sigma/sqrt(N)); q054 + variational-algorithms course ("Average value of a
  measurement ... weighted by the probability of the outcome"); q035 + SparsePauliOp API.
- **Code not runnable as displayed:** q031 comment defines `backend`; q042 comment marks
  `observables`/`values` as the blanks.
- **Survived attacks (executed):** q028 level 3 -> `ValidationError ... must be <=2`, explicit
  `measure_mitigation=False` at level 1 kept; q029 installed docstrings (DD enable default False,
  measure_mitigation True at levels 1/2); q030 shapes `()`, `(1,)`, `(3, 1)`, `(1, 3)` for the
  distractor nestings; q039 `enabled` -> `no_such_attribute`, `sequence_type` leaves `enable` Unset;
  q053 prints `IZXII`; q054 0.616 (0.808 / 0.106 / 0.380 models).
- **Difficulty:** all 18 kept.
- Gates: verify_bank s6 33/33 PROVEN + 12 conceptual, 0 failures, exit 0; audit_meta_patterns s6
  0 blockers / 0 warnings (low length_tell on q031/q032/q034/q037 are variant-level and pre-existing;
  q034's edit lengthened a distractor, so it eased); lint_proof_drift 0 findings.

## Adversarial review A3 — s7a (2026-10-16)

Scope: s7-q010..q025 (16; all executed, no conceptual, no figure items). Every option re-run in
independent scratch scripts (pinned venv, qiskit 2.5.0 / runtime 0.48.0; runtime claims on
`SamplerV2`/`EstimatorV2(mode=FakeManilaV2())` local mode), every runnable displayed block executed
three times unseeded and compared to the literal output, every cited page fetched as text and grepped.
**0 key changes, 0 kills.** 8 edited, 8 survived unchanged (q011, q012, q014, q016, q019, q023, q024,
q025).

- **Second answer closed (s7-q015):** pool F "`{'111': n}`, but `n` is now a fraction of the shots" is
  literally true (about half the 1000 shots survive; displayed code re-run: 519/488/498). F now claims
  the renormalised `{'111': 1.0}`; proof compares the observed dict (`{'111': 480}`, int values).
- **Literal-print mismatch (s7-q020):** `print(result[0].data.evs)` gives `0.9999999999999998`; stem
  now "Up to floating-point rounding, ..." (s6a precedent), proof records the printed string.
- **Displayed code not runnable:** s7-q018 option F calls `np.concatenate` but the code never imported
  numpy (NameError as shown) -> `import numpy as np` added. s7-q013 and s7-q022 were comment-only
  (`result` undefined) -> live lines on a stated `estimator`.
- **Proofs off the stem's object:** s7-q010 (stem: runtime `sampler.run([isa_circuit])`) and s7-q022
  (stem: Estimator `result`) ran StatevectorSampler/StatevectorEstimator -> now runtime SamplerV2 /
  EstimatorV2 local mode, seeded via `simulator.seed_simulator` (honoured by local_service). q010: A
  only (B `not JSON serializable`, C `unexpected keyword argument 'skipkeys'`, D no `to_json`, E
  `KeyError: 0`, F `dumps() takes 1 positional argument`). q022: DataBin fields `['evs', 'stds']`,
  metadata keys `circuit_metadata/shots/target_precision` (DF now names `shots`).
- **Rationales made exact:** s7-q018 E "far fewer shots" -> executed 200 vs 400 (both GHZ jobs share
  `000`/`111`), evidence prints both; s7-q021 D "single-PUB, single-parameter case" -> values `(1,)`
  give `()`, C: `(1, 1)` give `(1,)` (both executed; E's `(1, 4)` needs `(1, 4, 1)`).
- **Docs-reader trap answered (s7-q017 F):** the BitArray API lists `IndexError` for `slice_bits`;
  DF now quotes the real boundary (`[3]` -> `index 3 is out of bounds for the number of bits 3`,
  `[2]` -> `{'0': 300}`).
- **Citation failures replaced (fetched, quotes grepped):** api/qiskit/primitives states only
  `job.result()[0].data.evs` (kept for q022) -> estimator-input-output in q013 ("populate the stds
  field with a quantity like the standard error of the mean"), q020 ("contains at least an array of
  expectation values (PubResult.data.evs) and associated standard deviations"), q021 ("parameter
  binding sets having shape (100, 2), where 2 is the number of parameters in the circuit"). Kept and
  verified: save-jobs (`json.dump(..., cls=RuntimeEncoder)` / `json.load(file, cls=RuntimeDecoder)`),
  PrimitiveResult API ("does not contain any actual data ... primitive_result[0].data, which is a
  DataBin"), BitArray API ("last axis is over packed bits, the second last axis is over shots";
  postselect returns "num_bits=data.num_bits, num_shots<=data.num_shots"; slice_bits "index 0
  corresponds to the least-significant bit ... right-most bitstring entry"; concatenate_shots "Join a
  sequence of bit arrays along the shots axis"), primitive-input-output ("a single observable
  represented as a 0-d array").
- **Survived attacks (executed):** q011 `2000 3`; q012 `(1024, 2)`; q014 `{'001': 500}`; q016 only
  postselect (E `TypeError ... unexpected keyword argument 'num_bits'`, F width 1); q019 A/B/D
  (shape `(256, 1)`, dtype uint8); q023 len 2, `result.data` / `.get_counts()` paths AttributeError;
  q024 only C; q025 prints `1.0` deterministically (0-d), `ZI` gives ~0.
- **Difficulty:** all 16 kept.
- Gates: verify_bank s7 31/31 PROVEN + 6 conceptual, 0 failures; audit_meta_patterns s7 0 blockers /
  0 warnings (low length_tell on q015/q020/q023/q024 pre-existing; q015's new F is longer than the old
  one); lint_proof_drift 0 findings.

## Adversarial review A3 — s7b (2026-10-16)

Scope: s7-q026 q027 q028 q029 q030 q031 q032 q034 q035 q036 q038 q045 q046 q047 q048 (15; 9 executed,
6 conceptual, 5 figure items). Executed options re-run in independent scratch scripts (pinned venv,
qiskit 2.5.0 / runtime 0.48.0); conceptual items checked against the INSTALLED 0.48 source, and where
possible by executing that source offline (`RuntimeJobV2` / `Session` / `QiskitRuntimeService` objects
with stub API clients, no network); every cited page fetched as text and grepped; all five figures
rendered, rasterized and inspected. **0 key changes, 0 kills.** 14 edited, 1 survived unchanged (q036).

- **Half-true distractor + false rationale (s7-q035 E):** "`usage_time` ... keeps growing while the
  session sits idle between two of its jobs" is TRUE for a session: 0.48 `Session.usage()` defines
  session usage as "the time from when the first job starts until the session goes inactive, is
  closed, or when its last job completes, whichever happens last" (`details()["usage_time"]` is the
  same server field `elapsed_time`), and monitor-job says session usage is elapsed time "regardless
  of whether jobs are actively running". The old rationale ("an idle session accumulates none of it")
  was false. E is now the batch-accounting misconception (summed QPU time, idle gap leaves it
  unchanged) with the quotes. Key B no longer claims a closed four-value state set: 0.48 `status()`
  also maps `pending_inactive` / `pending_closed` (stub-executed: active+accepting -> "In progress,
  accepting new jobs", open/inactive -> "Pending", closed -> "Closed").
- **Local-mode trap (s7-q034):** executed `SamplerV2(mode=FakeManilaV2())` -> `LocalRuntimeJob.status()`
  returns `JobStatus.DONE` and `== "DONE"` is False, i.e. the answer flips on a fake backend. The code
  now picks a real QPU explicitly (`least_busy(operational=True, simulator=False)`), A's rationale
  explains the local-mode habit, the proof records the local contrast. A/C reworded from "ends the
  polling loop" (the displayed loop exits on `in_final_state()`) to "the check for a successful finish".
- **Cancel semantics executed (s7-q028):** 0.48 `RuntimeJobV2` with a stub client: QUEUED -> `cancel()`
  -> `status()` 'CANCELLED' (cancel sets `_status`; terminal states short-circuit polling),
  `in_final_state()` True, `result()` raises `RuntimeInvalidStateError: Unable to retrieve result for
  job <id>. Job was cancelled.`; no `RuntimeJobV2.stop`, no `QiskitRuntimeService.cancel`. E/F/correct
  now state exactly that; monitor-job quoted ("Cancel a job that is queued or running ...").
- **Free elimination removed:** s7-q032 option A was the displayed failing line verbatim -> default
  name `c` misconception (executed `'DataBin' object has no attribute 'c'`); s7-q027 E was a statement,
  not an approach, in a "which approaches" item -> "load the JSON file Runtime saves locally" (0.48
  grep: the only file writes are account credentials in accounts/storage.py).
- **Displayed code not runnable / proof off the stem's object:** s7-q031 comment-only `result` ->
  runnable `QuantumCircuit(2, 2)` circuit (`db.keys()` -> `['c']`, `db.meas` AttributeError asserted).
  s7-q046 was a QPU retrieval whose noisy counts could not be the exact 200/100 bars -> runnable
  `StatevectorSampler` sweep (angles 0/pi, deterministic); proof executes the DISPLAYED code verbatim as
  the SVG byte-identity target (s5-q041 recipe). s7-q047 proof now executes the displayed code with only
  the three service lines bound to a BitArray whose printed `get_counts()` equals the stem comment
  (asserted). s7-q045 proof moved from StatevectorSampler to runtime SamplerV2 seeded local mode
  (ISA circuit keeps cregs `flag`/`out`).
- **Circular figure proof (s7-q048):** the key "reproduced" the figure only because the figure was
  made from it with the same seeds. The proof now re-runs every option under three unrelated
  transpile/simulator seed pairs: B TVD 0.008-0.040, D 0.244-0.274, A/C/E >= 0.451 (scratch sweep of 8
  pairs: B <= 0.049, D >= 0.222).
- **Figure drawn by code the stem does not show (s7-q038):** generator added a y label "expectation
  value" (which by itself rules out `stds`) plus axhline/xlabel absent from the stem code. Generator now
  uses the stem's pyplot calls (plot, axhline, xlabel; no y label), stem code shows them and defines
  `angles`; alt updated; re-rendered and inspected.
- **Rationales made exact:** q026 C (`jobs()`' first positional is `limit`, returns
  `list[RuntimeJobV2]`) and F (literal `TypeError: QiskitRuntimeService.job() missing 1 required
  positional argument: 'job_id'`); q029 A names the Hamming-weight misconception that yields 3;
  q038 A (stds 0.005-0.018, not "two orders of magnitude") and D (metadata keys `shots`,
  `target_precision`, `circuit_metadata`); q030 B (0.48 `details()` builds a fixed 14-key dict,
  stub-executed; local Session details() None).
- **Docs example copied (s7-q026):** job ID literal was the save-jobs example's `d762omnq1anc738d2cj0`
  -> neutral ID.
- **Citation failures replaced (fetched, quotes grepped):** q029/q047 primitive-input-output and
  save-jobs (neither states the int-key rule) -> bit-ordering ("When interpreting bits as a number,
  bit 0 is the least significant bit"); q030 monitor-job (no `details()` content) -> run-jobs-session
  (prints the details dict); q035 + monitor-job (session usage quote). Kept and verified: save-jobs
  ("use the QiskitRuntimeService.job method to retrieve it", Workloads page lists job IDs), monitor-job
  ("use service.job(<job_id>) to retrieve it later", `job.cancel()`), runtime-job-v2 (`status()` Return
  type `Literal['INITIALIZING', ..., 'ERROR']`), session API (details key list, status strings),
  BitArray ("bitstrings are stored as ints"; get_counts loc=None "unioned together"), DataBin ("query
  the available keys with keys()", keys are ClassicalRegister names), primitive-input-output /
  api/qiskit/primitives (PrimitiveResult of SamplerPubResults; "Running a sampler returns a
  BasePrimitiveJob object"), sampler-input-output, visualize-results.
- **Survived attacks:** q036 prints `True PrimitiveResult SamplerPubResult` (displayed code run;
  `join_data` only on SamplerPubResult; RuntimeJobV2 subclasses BasePrimitiveJob); q029 displayed code
  3x unseeded, keys always {0, 7}.
- **Difficulty:** all 15 kept.
- Gates: verify_bank s7 31/31 PROVEN + 6 conceptual, 0 failures; audit_meta_patterns s7 0 blockers /
  0 warnings (new medium absolute_distractor_tell on q027/q035 from the first rewrites fixed; low
  length_tell on q028/q036 pre-existing, options untouched); lint_proof_drift 0 findings.
