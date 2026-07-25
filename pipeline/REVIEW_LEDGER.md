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
