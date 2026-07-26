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
