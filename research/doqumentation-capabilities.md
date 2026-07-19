# doQumentation Platform Capabilities — Research Report

Repo: `/Users/majl/GitHub/doQumentation` (READ ONLY, working tree on `i18n/opus-round28`).
Stable state cross-checked via `git show origin/main:<file>`. Live site: https://doqumentation.org.
Date: 2026-07-19.

---

## 1. EXECUTION ARCHITECTURE

### Client library
- **thebelab 0.4.x** (loaded from jsDelivr CDN). Component: `src/components/ExecutableCode/index.tsx` (2108 lines). It swizzles Docusaurus `@theme/CodeBlock` (`src/theme/CodeBlock/index.tsx`) so every code block gets a Run/Back toolbar. All cells on a page share ONE kernel session (variables persist across cells). thebelab uses `@jupyterlab/services` under the hood — kernel objects expose `requestExecute`, `statusChanged`, IOPub messages (see `executeOnKernel`, `executeOnKernelWithOutput`).
- Config/detection lives in `src/config/jupyter.ts` (a ~1287-line "god object").

### Four execution backends (priority: Custom > Code Engine > Binder/github-pages > Local/RasQberry)
Defined in `jupyter.ts` `buildConfigFor()` / `detectJupyterConfig()`:
1. **`github-pages` (Binder — the PUBLIC default on doqumentation.org).** thebelab either reuses a running session via `serverSettings {baseUrl, wsUrl, token}` OR starts its own Binder build with `binderOptions: {repo:'JanLahmann/doQumentation', ref:'notebooks', binderUrl:'https://mybinder.org'}` (`getThebelabOptions`, ExecutableCode ~L1194). The "Open in Lab" path instead launches **`https://mybinder.org/v2/gh/QuBins/qiskit-images/<tag>`** and uses **nbgitpuller** to clone notebooks into the session (`buildNbgitpullerQuery`, `getBinderLabUrl`).
2. **`code-engine`** — IBM Cloud Code Engine pod. User pastes a CE URL+token into Settings (localStorage), or a workshop pool of URLs. Image `ghcr.io/janlahmann/doqumentation-codeengine:latest`, port 8080.
3. **`rasqberry` / local** — direct Jupyter on `localhost:8888` or Docker origin (token `rasqberry`).
4. **`custom`** — any user-supplied Jupyter URL+token.

### QuBins images — what they are
`QuBins/qiskit-images` (GHCR `ghcr.io/qubins/images:{version}-{small,xl}`) is a **third-party, maintained, versioned set of pre-built Qiskit Docker images** used as the mybinder base for the public Binder tier. Only used as the Binder environment (kernel image); notebooks are injected via nbgitpuller (QuBins image ships no notebooks). Exposed tags allow-listed in `jupyter.ts`: `SUPPORTED_QISKIT_TAGS = ['2.5-xl','2.4-xl','2.3-xl']`, `DEFAULT_QISKIT_TAG='2.5-xl'` — kept in **lockstep** with `binder/jupyter-requirements.txt` `qiskit[all]` pin, enforced by a CI guard (`ci.yml` "qiskit-lockstep"). Note: `notebook-sweep-report.md` flags QuBins `2.3-xl` missing `graphviz`, `qiskit-ibm-transpiler`, `qiskit-ibm-ai-local-transpiler`.

### Docker / Code Engine (self-host)
`Dockerfile.jupyter` builds two targets from a shared `quay.io/jupyter/base-notebook:python-3.12` base:
- `jupyter-local` — static site (nginx) + Jupyter + Qiskit; nginx (`nginx.conf`) reverse-proxies `/api/` and `/terminals/` to Jupyter :8888. `docker-compose.yml` maps 8080:80 + 8888.
- `jupyter-codeengine` — Jupyter + Qiskit + an **SSE build server** (`binder/sse-build-server.py`, tornado, port 9091) that mimics the mybinder `/build/` SSE protocol so thebelab's `ensureBinderSession()` works unchanged (image is pre-built, phases resolve instantly). nginx config `binder/nginx-codeengine.conf` with rate-limit zones for workshops. Entry: `binder/codeengine-entrypoint.sh`.

### Auth / CORS constraints (CRITICAL for external reuse)
- **doqumentation.org is a static GitHub Pages site with NO execution backend of its own.** It has no API to call. Legal page (`src/pages/legal.tsx`) confirms hosting is GitHub Pages; execution goes to mybinder.org "only when user clicks" or to user-configured CE/local.
- Kernel auth = Jupyter **token** in the URL/serverSettings (XSRF disabled; token is the whole auth boundary — see `nginx-codeengine.conf` log-scrubbing comment).
- **CE CORS is locked to doqumentation.org by default.** `binder/codeengine-entrypoint.sh` L40/88: `CORS_ORIGIN="${CORS_ORIGIN:-https://doqumentation.org}"` → sets Jupyter `c.ServerApp.allow_origin` (single) or `allow_origin_pat` regex (multiple, comma-separated). The SSE server (`sse-build-server.py` L41-53) echoes only allowlisted origins.

### BOTTOM LINE — external-origin reuse feasibility
- **Reusing doqumentation.org itself: nothing to reuse** — it's static, no backend, no public execution API.
- **Reusing the public Binder tier: YES, today, with zero change on their side.** mybinder.org + `QuBins/qiskit-images` are public and CORS-open. Our separate site can copy `ExecutableCode` + `jupyter.ts` + load thebelab and get identical execution, fully origin-independent. This is the clean path. (Caveat: mybinder cold builds are slow, 10-25 min uncached; public Binder is best-effort/rate-limited — a UX risk, not a blocker.)
- **Reusing THEIR Code Engine pod: only with a one-line change on their side** — add our origin to the pod's `CORS_ORIGIN` env (comma-separated). Otherwise the browser CORS-blocks cross-origin kernel calls. We would also need the CE URL+token. Not recommended (their pod, their cost, scale-to-zero cold starts).
- Our own execution options that need NOBODY: (a) same public-Binder pattern; (b) our own CE image (fork of theirs); (c) settings-gated pointer that just deep-links users to doqumentation.org pages (learning material) and lets doqumentation's own thebelab handle execution there.

---

## 2. VERIFICATION HARNESS (the reusable recipe)

### Where
- `ci/ipython_startup_dir/profile_default/startup/00_patch_runtime.py` — the runtime patch.
- `.github/workflows/notebook-ci.yml` — the sweep runner.
- `ci/list-notebooks.sh`, `ci/notebooks-skip.txt` — notebook selection/skip list.
- `notebook-sweep-report.md` — human-readable sweep findings (~291 notebooks).
- Pins: `binder/jupyter-requirements.txt` (`pyproject.toml` is only for the translation-script pytest, NOT notebooks).

### How it works (concrete)
1. **Runs inside the pinned prod image**: `notebook-ci.yml` executes in container `ghcr.io/janlahmann/doqumentation-codeengine:<tag>` — identical Python/Qiskit stack as prod. Test deps added: `pip install nbmake pytest-xdist`.
2. **Version pinning** (`binder/jupyter-requirements.txt`, auto-generated by `scripts/sync-deps.py`, synced from upstream `Qiskit/documentation` nb-tester): `qiskit[all]~=2.5.0`, `qiskit-ibm-runtime~=0.47.0`, `qiskit-aer~=0.17`, plus all addons pinned.
3. **Fake-backend patching** — `00_patch_runtime.py` auto-loaded via `IPYTHONDIR` env at kernel startup, BEFORE any user cell. It monkeypatches `qiskit_ibm_runtime`:
   - `QiskitRuntimeService` → `_FakeService`: `.least_busy()`, `.backend()`, `.backends()` return **FakeBrisbane / FakeFez / FakeMarrakesh** (`_BACKEND_MAP` maps ibm_brisbane→FakeBrisbane, ibm_fez→FakeFez, ibm_pittsburgh/ibm_marrakesh→FakeMarrakesh; ≥128 qubits→FakeFez else FakeBrisbane). `save_account`/`saved_accounts` no-op; `.job()` deliberately raises (surfaces cloud-only deps).
   - `SamplerV2`/`EstimatorV2` wrapped so `mode` defaults to a FakeBrisbane BackendV2, and **shots clamped** to `CI_MAX_SHOTS` (default 1024, `_MAX_SHOTS`).
   - `Session`/`Batch` replaced with a context manager yielding the fake backend.
4. **Execution + pass/fail**: `pytest --nbmake --nbmake-timeout=300 -n 2 --overwrite --junitxml=ci-report.xml <notebooks>`. nbmake executes every cell; a raised exception = test failure. JUnit XML parsed into a GitHub step summary (total/passed/failed/errored/skipped + first-line failure messages). Executed notebooks uploaded as artifacts.
5. **Cells that can't work under fakes** are tagged `nbmake-skip-cell`; whole notebooks in `ci/notebooks-skip.txt`.
6. **Seeding**: no global seed injected by the harness; determinism comes from fake backends + shot clamp. (Individual notebooks set their own seeds where needed.)

### Reusable pattern for our quiz-answer pipeline
Every code-bearing quiz question is executed at build time against the SAME pinned stack + `00_patch_runtime.py` fake-backend patch (FakeBrisbane/Fez/Marrakesh, shots≤1024), via nbmake/pytest. **The correct answer is proven by execution; distractors are proven wrong (executed → confirmed different output or the claimed error).** Freshness-gate it on every Qiskit bump exactly like the notebook sweep, so questions can't silently rot. This exact plan is already written up in `.claude/BUILD_TIME_AI_IDEAS.md` §2.3 (see §4 below).

---

## 3. CONTENT & LINKING

### Organization
- `scripts/sync-content.py` clones upstream `Qiskit/documentation` (tracked as git submodule `upstream-docs/`), converts notebooks→MDX, transforms MDX, parses `_toc.json`→sidebar JSON (`.generated/`), copies notebooks for "Open in Lab". Content types: tutorials, guides, courses, modules.
- `docs/` = generated Docusaurus content: `docs/tutorials/`, `docs/guides/`, `docs/learning/courses/<course>/`, `docs/learning/modules/<module>/`, `docs/qiskit-addons/`.
- `local-content/` = doQumentation's OWN content (custom hello-world tutorial + `use-a-qc-today` course notebooks; the only non-IBM content). `upstream-addons/` = addon tutorial submodules.
- Notebooks live on the auto-built `notebooks` branch (Binder/Colab/CE pull from there).

### Stable deep-link URL patterns (docusaurus.config.ts: `url:'https://doqumentation.org'`, `baseUrl:'/'`, `trailingSlash:false`, docs `routeBasePath:'/'`)
Docs are served at ROOT, so the on-disk path = the URL path:
- Tutorial: `https://doqumentation.org/tutorials/<slug>` (e.g. `/tutorials/hello-world`, `/tutorials/grovers-algorithm`, `/tutorials/shors-algorithm`)
- Guide: `https://doqumentation.org/guides/<slug>` (e.g. `/guides/choose-execution-mode`)
- Course page: `https://doqumentation.org/learning/courses/<course-slug>/<page-slug>` (e.g. `/learning/courses/use-a-qc-today/your-first-quantum-experiment`)
- Module: `https://doqumentation.org/learning/modules/<module>/...`
- **Locale subdomains** (one per language): `https://de.doqumentation.org/...`, `es.`, `fr.`, `ja.`, `uk.`, etc. EN = apex `doqumentation.org`. (Full list in config lines 136-162.)
- GitHub source of any page: `https://github.com/JanLahmann/doQumentation/tree/main/<docs-path>` (`editUrl`).
These slugs are stable (sourced from upstream `_toc.json`); safe to deep-link.

### Licensing (dual-license)
- `LICENSE` = **Apache 2.0** (code: scripts, source, config).
- `LICENSE-DOCS` = **CC BY-SA 4.0** (content: tutorials, guides, courses, media, translations).
- `NOTICE`: content is from `Qiskit/documentation` © IBM Corp., CC BY-SA 4.0; addon tutorials Apache 2.0. Translations are CC BY-SA 4.0 adapted material. **Reuse/linking is permitted** under these licenses with attribution + share-alike for content. "IBM, IBM Quantum, and Qiskit are trademarks of IBM Corporation." Linking to pages is unrestricted; copying content requires CC BY-SA attribution + share-alike.

### "Unofficial / not affiliated with IBM" disclaimer — exact wording + locations
- **Site footer** (`docusaurus.config.ts` L447, rendered on every page): *"...doQumentation is part of the [RasQberry](https://rasqberry.org/) project and is not affiliated with, endorsed by, or sponsored by IBM Corporation."* (Also: "IBM, IBM Quantum, and Qiskit are trademarks of IBM Corporation.")
- **NOTICE L46-48**: *"IBM, IBM Quantum, and Qiskit are trademarks of IBM Corporation. doQumentation is part of the RasQberry project (https://rasqberry.org/) and is not affiliated with, endorsed by, or sponsored by IBM Corporation."*
- **Legal/Impressum page** (`src/pages/legal.tsx` L31-37): *"This is a personal, non-commercial open-source project. The content is derived from IBM's open-source Qiskit documentation (CC BY-SA 4.0). IBM, Qiskit, and IBM Quantum are trademarks of International Business Machines Corporation. This project is not affiliated with or endorsed by IBM."*

---

## 4. RELEVANT `.claude` DOCS

**Important**: `.claude/` is byte-identical on `origin/main` and `origin/claude/build-time-ai-ideas-bzrjov` (empty `git diff`). The "build-time-ai-ideas" branch does NOT add anything to `.claude`. Both key docs already live on main.

### `.claude/BUILD_TIME_AI_IDEAS.md` (286 lines, 2026-07-18) — DIRECTLY the cert-prep blueprint
This is essentially the design doc for the exact site we are building. Core pattern: **"Precompute the decision space at build time; personalize by selection at runtime. Intelligence in the build, personalization in the browser."** No backend; works offline on a Pi.
- **§2 Qiskit Certification Studio** — flagship. Targets exam **C1000-179** ("Fundamentals of Quantum Computing Using Qiskit v2.X Developer": 68 Q, 90 min, ≥47 to pass, Pearson VUE). Step 0: ingest the official objective list + section weights like a machine-readable `_toc.json` syllabus.
  - §2.1 `certification-map.json`: objective → doQumentation pages, confidence, gaps; generate "bridge pages" for gaps (marked "Created by doQumentation", reviewed).
  - §2.2 **Cert Mode** localStorage toggle: sidebar filtered to objective order, objective badges, progress = "objectives covered".
  - §2.3 **Machine-verified question bank** (500-1000+ Qs): every code question executed at build time via the §2/harness (FakeBrisbane/Fez/Marrakesh, QuBins image, seeded, shot-clamped); correct answer proven, distractors proven wrong. Adversarial verifier fan-out kills ambiguous Qs. Ships as static JSON; mastery in localStorage `dq-quiz-mastery`.
  - §2.4 Mock exam (68Q/90min, stratified by section weight, real 47/68 pass line). §2.5 exam-drift watchdog (weekly CI hashes the public study guide). §2.6 multilingual via existing translation factory.
- **§5 Compiled Tutor** — precomputed policy tables, persona lenses (math/code/visual/ELI12), spaced-repetition flashcards + `.apkg` export, compiled Q&A (RAG as fallback).
- **Guardrails (§2.3 + §10.6)**: questions generated ONLY from PUBLIC exam objectives + our CC BY-SA content, NEVER actual exam content / no dumps; mark AI-generated + human-reviewed; carry the standard **"unofficial preparation material, not affiliated with or endorsed by IBM"** disclaimer (same site-wide pattern).

### `.claude/AI_FEATURES_BRAINSTORMING.md` (587 lines) — capability layer
- **Budget rule**: build-time AI via existing Claude Code Max ≈ $0; runtime AI limited to IBM Granite (watsonx.ai Lite/Essentials) or Code Engine serverless; strategy = "maximize build-time, minimize runtime."
- **2A metadata** (foundation): per-page `difficulty / prerequisites / leads_to / topics / estimated_time` as static JSON — enables badges, breadcrumbs, recommendations, search facets.
- **2E quizzes**: AI-generate per-section quizzes at build time → static JSON → client-side player, score → recommendation (absorbed/upgraded by BUILD_TIME_AI_IDEAS §2.3).
- **Runtime-AI tiers**: R1 fully-static RAG (~300KB embeddings, client-side cosine, $0); R2 client search + Code Engine LLM synthesis ($0-5/mo); Granite free tier or Claude Haiku (~$0.04/mo/100 queries). watsonx Assistant / multi-turn = over budget.
- **T3/L1 conventions**: AI-generated content MUST be labelled ("Summary created by doQumentation" / "Created by doQumentation") and human-reviewed.

### `.claude/PROJECT_HANDOFF.md` (575 lines) — relevant bits
- Footer has 3 columns + IBM disclaimer (L204). `/admin` is password-gated (SHA-256), AES-256-GCM encrypted URLs at build time, excluded from robots.txt.
- Plan-type disclaimer TODO (L387): warn paid-tier users that credentials sit in localStorage plaintext.
- CE-vs-QuBins image migration analysis (L383) — QuBins `2.3-xl` ~2.98GB vs hand-built CE ~905MB compressed; missing transpiler deps + graphviz.

---

## 5. LIVE SITE CONFIRMATION

- **Homepage** (fetched): explicitly advertises interactive execution — *"Click Run on any code block. The first click starts a Jupyter kernel via Binder or IBM Code Engine. After that, runs are instant."* Lists four backends (Binder default via mybinder.org, IBM Code Engine, Local Jupyter, Custom). Offers **Simulator Mode** (AerSimulator / FakeBackends) to run without an IBM account. Footer disclaimer present.
- **Tutorial page** (`/tutorials/hello-world`, fetched): the Run UI is injected client-side by thebelab/React, so the static HTML shows only the code + Binder references (WebFetch can't run the JS). Confirms execution is client-side-JS-driven.
- **Verdict**: doqumentation.org **DOES offer hosted execution to ordinary visitors** — but the "host" is the **public mybinder.org** service (running the QuBins image), NOT a doqumentation-owned backend. Code Engine / local Jupyter are opt-in (user pastes URL+token) and are what RasQberry/self-host/workshop deployments use. So: public visitors get Binder-backed execution (slow first run, best-effort); doqumentation.org itself hosts no compute.

---

## KEY TAKEAWAYS FOR THE CERT-PREP SITE
1. Execution is **fully copyable and origin-independent** via thebelab + public mybinder.org + `QuBins/qiskit-images` — no dependency on, and no change needed from, doqumentation.org. Copy `src/components/ExecutableCode/index.tsx` + `src/config/jupyter.ts`.
2. To (optionally) reuse THEIR Code Engine pod cross-origin, they must add our origin to the pod's `CORS_ORIGIN` env — otherwise CORS-blocked.
3. The **verification harness** (`ci/ipython_startup_dir/.../00_patch_runtime.py` + nbmake + pinned `binder/jupyter-requirements.txt`) is the exact reusable recipe for proving quiz answers.
4. `.claude/BUILD_TIME_AI_IDEAS.md` §2 is a ready-made spec for the cert-prep site (C1000-179, verified question bank, Cert Mode, disclaimers, guardrails).
5. Deep-link pattern: `https://doqumentation.org/<tutorials|guides|learning/courses/...>/<slug>` (no trailing slash), locale subdomains `https://<locale>.doqumentation.org/...`.
6. License: content CC BY-SA 4.0, code Apache 2.0; carry the exact "not affiliated with, endorsed by, or sponsored by IBM Corporation" disclaimer.
