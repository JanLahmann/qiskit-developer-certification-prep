# Adversarial Review Contract (wave A3, 2026-10-16)

Binding for every A3 review agent. Scope: the 303 questions that predate the October
waves plus the 21 figure-wave items. The 62 R2 adds were reviewed on 2026-10-02 (see
`REVIEW_LEDGER.md`, "Adversarial review R2"), and that entry shows the expected depth.
Each agent gets one batch of question ids.

## Your job: try to break every question in your batch

For EACH question, in this order:

1. **Second-answer attack.** For every option, including undisplayed pool distractors
   (`display_count` < number of options), argue in good faith that it is ALSO correct,
   or that the key is wrong. Where the claim is executable, RUN it in the pinned venv
   (`.venv/bin/python`, qiskit 2.5.0 / runtime 0.48.0) with your own independent
   script. Do not just re-read the proof. Proofs can be adjacent to the claim, so check
   that the proof actually tests what the stem asks.
2. **Stem attack.** Is the stem literally answerable as written, from stem + code
   alone? Look for underspecification: unstated backend, version, seed, optimization
   level or default. Look for a second reading, and for code that does not run as
   displayed (missing imports, undefined names). For a "what does this print" stem,
   run the DISPLAYED code and compare its literal output.
3. **Explanation attack.** `explanation.correct` and each `distractors[key]` must be
   true, must name the misconception, and must never reference display letters ("option
   B"), because options are shuffled and sampled. Check that each claim matches execution.
4. **Citation attack.** Fetch every citation (qiskit-docs MCP `get_page_tool` /
   `search_docs_tool`, or the live docs) and confirm the page actually states the
   fact. Replace a citation that does not, using a page you verified. Watch for
   docs-reader traps: docs wording that points at a wrong option. Answer them in the
   distractor explanation, as the s5-q044 and s7-q039 precedents do.
5. **Figure items** (any `figures` block): run
   `.venv/bin/python pipeline/render_figures.py --only <qid>` and inspect the
   rendering. Alt text must describe the drawing without singling out the key's
   distinguishing feature. Proofs of "which drawing" items must pin the drawing by
   SVG byte-identity (recipe in the ledger, Adversarial review R2 s1+s2).
6. **Difficulty sanity** per `REALISM_CONTRACT.md` rubric. Change a rating only with a
   one-line reason.

## Fixing

- **Verified wrong key or second correct answer:** fix the QUESTION, not the verdict.
  Re-key, or rewrite the offending distractor into a clearly wrong misconception.
  Update the proof so it refutes the new distractor, and write a ledger entry with the
  executed evidence. A key change needs execution evidence, or for conceptual items a
  quoted docs/source line. Never change a key on reasoning alone.
- **Unfixable** (the premise itself is wrong or obsolete): do NOT delete. List the
  question as a kill-candidate in your report, with the reason.
- After ANY edit to a question: `adversarial_rounds += 1`, and append to
  `provenance.notes`: `"adversarial A3 2026-10-16: <one line>"`. Untouched questions
  that survived also get `adversarial_rounds += 1` and the note
  `"adversarial A3 2026-10-16: survived, no change"`.
- Stems stay in exam register (official median ~14 words; cap 30). Keep the
  anti-tell properties (`GENERATION_GUIDE.md` §2.5): edits must not make the key
  the longest option, the only hedged one, or the only one that echoes the stem.
- NDA: never copy text from official IBM exam material. You do not have it and do
  not need it.

## Rules

- Do NOT run ANY git command, not even read-only ones.
- Touch only: the question files in your batch, `data/proofs/` via the verifier,
  `data/figures/<qid>/` for your batch (generator + SVGs via render_figures), and appending ONE section to
  `pipeline/REVIEW_LEDGER.md`, titled `## Adversarial review A3 — <batch label> (2026-10-16)`.
- Scratch scripts go in your scratch directory (given in your prompt), never in the repo.
- Allowed commands:
  - `.venv/bin/python` / `python3` scripts and one-liners for investigation
  - `.venv/bin/python pipeline/verify_bank.py --only <qid>`, and
    `--section sX --jobs 2` at the end. Must exit 0.
  - `python3 pipeline/audit_meta_patterns.py --section sX`: 0 blockers / 0 warnings,
    and no new high/medium flag on your items.
  - `.venv/bin/python pipeline/render_figures.py --only <qid>`
  - `python3 pipeline/lint_proof_drift.py`: no new findings on your items.

## Report (final message, compact)

1. Counts: questions reviewed, survived unchanged, hardened, re-keyed, kill-candidates.
2. Every key change and kill-candidate: qid, before→after, and the executed evidence
   in one or two lines.
3. Other fixes grouped by type (stem, explanation, citation, figure, difficulty), with qids.
4. Gate results.
