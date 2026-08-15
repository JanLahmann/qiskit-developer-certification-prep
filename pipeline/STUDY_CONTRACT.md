# CertiQ Study Layer Contract v2 (for rewrite/authoring agents)

The study layer (`data/study/s<X>.json`) feeds BOTH the website cram sheets
(`pipeline/build_study.py` → site/docs/cram/) and Part I of the EPUB study
book (`pipeline/build_epub.py`). Its audience is a **human learner cramming
for exam C1000-179** — it must contain the essential minimum for passing,
readably. v1 (2026-07) failed that bar: ~400-word expert-prose primers and
flat walls of up to 24 bullets. v2 fixes it.

## v2 file shape

```json
{
  "section": "s1",
  "version": 2,
  "primers": [{"objective": "s1o1", "title": str,
               "body_md": str, "citations": [url, ...]}],
  "facts":   [{"objective": "s1o1", "group": "core"|"trap",
               "fact_md": str,
               "source": {"type": "citation"|"proof", "ref": url|qid}}],
  "checklist": [str, ...],
  "provenance": {"generated": date, "model": str,
                 "fact_checked": bool, "notes": str}
}
```

`body_md` may contain ``` code fences and markdown pipe tables; both render
on the site and in the EPUB. Inline markdown is limited to `backticks` and
**bold** (the EPUB renderer supports nothing else). A literal `|` inside a
table CELL must be escaped as `\|` (ket notation like `|0>` would otherwise
split the cell); unescaped pipes in cells are a bug in both renderers.

## Hard gates (build_study.py fails otherwise)

- Every objective: >= 1 primer (max 2), >= 2 facts.
- Per objective: <= 6 `core` facts + <= 5 `trap` facts. Fewer is better.
- Primer PROSE <= 180 words (code-fence lines and `|` table rows are free).
  Target ~120-150.
- Section `checklist`: 4-10 items, each <= 25 words.
- Every fact needs a source; `proof` refs must name an existing EXECUTED
  question id; every primer needs >= 1 citation URL.

## Style rules (the point of v2)

1. **Primer = teaching unit, not briefing note.** Lead sentence states the
   one rule plainly. Then a minimal code example (a fence, <= 8 lines) where
   code clarifies. Then a pipe table wherever >= 3 things are compared
   (gates/phases, method pairs, modes, levels, options). One idea per
   paragraph; sentences <= ~25 words; no rhetorical flourishes, no asides.
2. **Facts are triaged, not dumped.** `core` = the handful of rules exam
   points hinge on. `trap` = the specific mistakes the exam baits
   (misconceptions the bank's distractors encode). Delete edge-case trivia;
   merge overlapping facts; never restate in a fact what the primer (or its
   table) already says fully.
3. **Checklist = the pass bar.** 5-8 imperative self-check one-liners a
   learner ticks the night before ("Read a Pauli label right-to-left and
   name each qubit's operator").
4. **Concision target**: ~900-1100 prose words per section TOTAL
   (primers + facts + checklist).

## Integrity rules (non-negotiable)

- **Claim-preserving restructure only.** Every claim must already exist in
  the v1 file (primer or fact) or follow from it by pure condensation. NO
  new factual claims. Moving a fact's content into a primer table is fine —
  then delete the fact and add its citation URL (if citation-type) to the
  primer's citations.
- Keep each kept fact's original `source` unchanged. A merged fact keeps the
  source that covers the surviving claim; if two merged claims have
  different sources, keep both facts instead.
- `provenance`: set `fact_checked: true` only after re-reading every kept
  fact against the v1 text you derived it from; note
  `"v2 claim-preserving rewrite of fact-checked v1"` in `notes`.
- Do NOT run git commands. Touch only `data/study/<your sections>.json`.
- Validation: `python3 pipeline/build_study.py` must exit 0. That command —
  plus reading repo files — is your whole toolbox.
