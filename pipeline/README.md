# CertiQ build pipeline

Build-time AI factory: agents generate content, deterministic gates verify it,
the site ships static. Nothing here runs at serve time.

## The flow

```
data/syllabus.json  ──►  generation agents (per section, GENERATION_GUIDE.md)
                              │  write data/questions/<sX>/*.json
                              ▼
                    verify_bank.py  ── executes every proof_script in .venv
                              │        (schema gate + execute-and-prove gate,
                              │         stamps freshness, writes data/proofs/)
                              ▼
                    adversarial review agents (kill/fix wave, provenance++)
                              ▼
                    build_site_data.py ── compiles shippable questions + proofs
                              │           into site/src/data/bank/*.json and
                              │           generates site/docs/sections/*.mdx
                              ▼
                    build_anki.py ── .apkg decks into site/static/downloads/
                              ▼
                    site (Docusaurus) → GitHub Pages
```

## Commands (from repo root)

| Command | Purpose |
|---|---|
| `.venv/bin/python pipeline/verify_bank.py` | Verify + freshness-stamp the whole bank (CI gate; `--check` for read-only, `--section sX` to scope, `--only <qid>` for one) |
| `.venv/bin/python pipeline/build_site_data.py` | Compile bank + syllabus into site data and section pages |
| `.venv/bin/python pipeline/build_anki.py` | Build Anki `.apkg` decks |
| `python pipeline/check_links.py` | Liveness-check all official resource links (needs network) |

## Environment

`.venv` is pinned via `pipeline/requirements.lock` (created from the working
set: qiskit 2.5.0 / aer 0.17.2 / runtime 0.48.0 / py 3.12). Every proof
artifact records the exact versions it ran against. The weekly
`weekly-verify.yml` workflow re-proves the bank on the pin AND probes the
latest Qiskit for upcoming breakage, and checks link liveness — failures open
a `drift-watchdog` issue.

## Contracts

- `GENERATION_GUIDE.md` — what generation agents must produce (schema, craft
  rules, NDA rules, proof-script contract, workflow).
- `harness/schema.py` — machine-enforced question schema + invariants.
- `harness/runner.py` — proof execution + verdict validation (the
  "execute-and-prove" core). Proof scripts get `emit_verdict()` from the
  prelude and run offline (`qcs_patch_runtime.py` stubs QiskitRuntimeService
  with fake backends).

## Re-running generation (future sessions)

1. Update `data/syllabus.json` if the exam changed (watchdog will have told you).
2. Launch per-section generation agents per `GENERATION_GUIDE.md` (quota table
   inside; IDs continue from the highest existing qNNN).
3. `verify_bank.py` until clean → adversarial wave → `build_site_data.py` →
   `build_anki.py` → commit.
