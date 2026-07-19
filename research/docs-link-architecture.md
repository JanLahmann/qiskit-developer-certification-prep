# Docs Link Architecture — IBM Qiskit v2.X Developer Certification Prep

_Research date: 2026-07-19. Purpose: map the OFFICIAL learning-resource landscape so a static site can deep-link every exam topic to the best official resource._

## 0. The exam we are mapping to (context)

- **Credential:** IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate
- **Exam code:** **C1000-179** — "Fundamentals of Quantum Computing Using Qiskit v2.X Developer" (this REPLACES the older C1000-112 / Qiskit v0.2X exam).
- **Format:** 68 questions, 90 minutes, pass = 47/68 (~69%). Delivered by Pearson VUE (in-center or OnVUE at-home). Badge via Credly.
- **Section weights (from exam guide):** Perform quantum operations ~16%, Visualize circuits/measurements/states ~11%, Create quantum circuits ~18%, plus sections on running circuits and using primitives (SamplerV2/EstimatorV2). Full weights live on the IBM Training exam page.
- **Official prep (recommended, not required):** the **Watrous "Understanding quantum information & computation"** course series (theory) + the **"In Practice" / Quantum Computing in Practice** course (applied Qiskit). IBM Training exam page hosts a downloadable **Study Guide** + a short **sample test**.
- **Key official URLs:**
  - Exam / IBM Training page: `https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400`
  - Announcement blog: `https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification`

## 1. Canonical domains (verified mid-2026 via redirects)

| Legacy domain | Redirect | Canonical (mid-2026) |
|---|---|---|
| `docs.quantum.ibm.com/guides` | 301 Moved Permanently | `https://quantum.cloud.ibm.com/docs/guides` |
| `learning.quantum.ibm.com` | 301 Moved Permanently | `https://quantum.cloud.ibm.com/learning` |

**Bottom line:** the single canonical host is **`quantum.cloud.ibm.com`**, with three product paths:
- Docs: `https://quantum.cloud.ibm.com/docs` (guides, tutorials, api)
- Learning: `https://quantum.cloud.ibm.com/learning`
- Platform (console/account): `https://quantum.cloud.ibm.com`

Locale note: both `/docs/<path>` and `/docs/en/<path>` resolve (the `/en/` locale segment is optional). Use the shorter no-locale form for deep links; it is what the MCP/live search returns.

## 2. The local clone: what it is and how stale

- Path: `/Users/majl/GitHub/Qiskit-documentation`
- **Remote is NOT upstream:** `git@github.com:JanLahmann/Qiskit-documentation.git` — this is **JanLahmann's fork ("q-docs")**, a derivative of `Qiskit/documentation` that adds Binder interactive-execution wrappers (see `NOTICE`, `00-q-docs--START-HERE.md`). Content itself is a mirror of upstream.
- **Staleness:** last commit `6f006d7a` dated **2026-03-10** (commit msg: "Fix Binder workflow…"). So the content snapshot is **~4 months old** as of 2026-07-19. Treat file listings as authoritative for path→URL structure, but ALWAYS confirm the live URL for anything new (the live catalog already has content this clone lacks — see §4 uncertainty about `use-a-qc-today`).

### Repo structure → live URL mapping

| Repo path | File formats | Live URL prefix |
|---|---|---|
| `docs/guides/<slug>.{mdx,ipynb}` | 86 mdx + 86 ipynb (+ `_toc.json`) | `…/docs/guides/<slug>` |
| `docs/tutorials/<slug>.ipynb` | 43 ipynb + `index.mdx` + `_toc.json` | `…/docs/tutorials/<slug>` |
| `docs/api/qiskit/<page>.mdx` | mdx (module pages + one file per class) | `…/docs/api/qiskit/<page>` |
| `docs/api/qiskit/<version>/…` | versioned snapshots: `0.46,1.0–1.4,2.0–2.2,dev` | `…/docs/api/qiskit/<version>/<page>` |
| `docs/api/{qiskit-ibm-runtime,qiskit-ibm-transpiler,qiskit-c,qiskit-addon-*}` | mdx | `…/docs/api/<pkg>/…` |
| `learning/courses/<course>/[<lesson-group>/]<lesson>.{mdx,ipynb}` | mdx + ipynb | `…/learning/courses/<course>/[<lesson-group>/]<lesson>` |
| `learning/modules/{computer-science,quantum-mechanics}` | mdx/ipynb | `…/learning/modules/…` |

Rule: strip the `docs/`/`learning/` repo prefix and the file extension; prepend `https://quantum.cloud.ibm.com/`. Directory `index.mdx` → the bare directory URL. Course lessons can be nested one level (e.g. `single-systems/quantum-information`), confirmed against `_toc.json`.

## 3. License — link freely, quote carefully

The repo is **dual-licensed** (identical statement in `LICENSE`, `LICENSE-DOCS`, `NOTICE`, `README`):

- **Code** (scripts, source files, **and code snippets inside docs examples**) → **Apache-2.0**.
- **Content** (guides prose, tutorials, courses, media, other non-code assets) → **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. NOTE: it is **BY-SA**, not plain CC-BY — the **ShareAlike** term matters.

**Practical bottom line for the static site:**
- **Linking / deep-linking** to any page: always fine, no obligation. This is the safe default and what this whole architecture is built for.
- **Quoting/excerpting prose** (guide/course/tutorial text): permitted under CC BY-SA 4.0 **only if** you (a) give attribution (credit IBM/Qiskit + link + indicate changes) AND (b) license YOUR derivative excerpt/adaptation under the **same CC BY-SA 4.0**. ShareAlike can "infect" the surrounding page if excerpts are adapted/integrated — so prefer short clearly-attributed blockquotes, or just link.
- **Reusing code snippets:** governed by **Apache-2.0** (permissive; keep the license/attribution notice, no ShareAlike). Safe to copy example code into the site.
- Recommendation: **default to linking**; when you must include content, quote code (Apache-2.0) rather than prose, and attribute.

## 4. IBM Quantum Learning — course catalog (certification-relevant)

Base: `https://quantum.cloud.ibm.com/learning/courses/<course-slug>`
Lesson deep-link pattern: `…/learning/courses/<course-slug>/[<lesson-group>/]<lesson-slug>` (verified live via MCP search, e.g. `…/quantum-computing-in-practice/running-quantum-circuits`). Course landing = bare course slug. Some courses include an `exam.mdx` → `…/<course-slug>/exam`.

13 courses present in the (stale) clone; the **Watrous "Understanding quantum information and computation" series** = the first four below (primary theory prep), and **Quantum computing in practice** = primary applied-Qiskit prep.

| Course | Slug (→ URL) | Cert relevance / coverage |
|---|---|---|
| Basics of quantum information | `basics-of-quantum-information` | States, measurements, unitary ops, single/multiple systems, quantum circuits, teleportation, superdense coding, CHSH. **Core theory.** |
| Fundamentals of quantum algorithms | `fundamentals-of-quantum-algorithms` | Query/circuit models, Deutsch-Jozsa, Grover, phase estimation, Shor. Watrous series. |
| General formulation of quantum information | `general-formulation-of-quantum-information` | Density matrices, channels, measurements (advanced theory). Watrous series. |
| Foundations of quantum error correction | `foundations-of-quantum-error-correction` | Codes, stabilizers. Watrous series. |
| Quantum computing in practice | `quantum-computing-in-practice` | **Applied Qiskit workflow**: mapping problems, running circuits, primitives, utility-scale QAOA. **Primary applied prep.** |
| Variational algorithm design | `variational-algorithm-design` | Ansätze, cost functions, optimization loops, reference states (has `exam`). |
| Utility-scale quantum computing | `utility-scale-quantum-computing` | Large-scale workflow, transpilation, error mitigation. |
| Quantum diagonalization algorithms | `quantum-diagonalization-algorithms` | SQD/Krylov. |
| Quantum chemistry with VQE | `quantum-chem-with-vqe` | VQE application. |
| Quantum machine learning | `quantum-machine-learning` | Kernels, QNNs. |
| Integrating quantum and HPC | `integrating-quantum-and-high-performance-computing` | Runtime, execution modes. |
| Quantum-safe cryptography | `quantum-safe-cryptography` | Context (low cert relevance). |
| Quantum business foundations | `quantum-business-foundations` | Non-technical (low cert relevance). |

Also `learning/modules/computer-science` and `learning/modules/quantum-mechanics` (prerequisite building blocks).

**Is there a certification-specific course/path on the Learning site?** No dedicated "certification" course or pathway is published on `quantum.cloud.ibm.com/learning` (verified: catalog page makes no mention of certification). Certification prep is assembled from the courses above + the **Study Guide/sample test hosted on the IBM Training exam page** (§0).

## 5. IBM Quantum Platform — what a learner needs to run on hardware (2026)

To exercise Runtime primitives (SamplerV2/EstimatorV2) on real hardware — which the exam's "running circuits / primitives" sections assume — a learner: (1) registers a free account at `https://quantum.cloud.ibm.com/registration`; (2) signs in at `https://quantum.cloud.ibm.com` and creates a free **Open Plan** instance at `https://quantum.cloud.ibm.com/instances` (choose region **us-east** for Open Plan; the Open plan gives a limited monthly allotment of free QPU minutes, historically ~10 min/month, and the fork's README notes "no credit card required for the first 30 days"); (3) creates an **API key** (on the platform dashboard or `https://cloud.ibm.com/iam/apikeys`) and copies the instance **CRN** from the Instances page; (4) saves credentials once via `QiskitRuntimeService.save_account(token=…, instance=<CRN>, overwrite=True)`. Setup guides: `…/docs/guides/cloud-setup`, `…/docs/guides/save-credentials`, `…/docs/guides/hello-world`. Exact free-minute quota is the main value to re-verify on the live plans page.

## 6. Topic → canonical URL table (starter, ~24 rows)

All URLs are prefixed `https://quantum.cloud.ibm.com`. G = guide (prose/how-to), A = API reference. Slugs verified present in the clone and/or via live MCP search; the path→URL rule (§2) applies.

| # | Exam topic area | Type | Canonical URL |
|---|---|---|---|
| 1 | First end-to-end workflow ("Hello world") | G | `/docs/guides/hello-world` |
| 2 | Construct circuits (QuantumCircuit basics) | G | `/docs/guides/construct-circuits` |
| 3 | Circuit library (standard gates/templates) | G | `/docs/guides/circuit-library` |
| 4 | QuantumCircuit class | A | `/docs/api/qiskit/qiskit.circuit.QuantumCircuit` |
| 5 | circuit module (Gate, Instruction, Parameter, control flow) | A | `/docs/api/qiskit/circuit` |
| 6 | Standard gate set (library gates) | A | `/docs/api/qiskit/circuit_library` |
| 7 | Transpilation (overview / how-to) | G | `/docs/guides/transpile` |
| 8 | Transpiler stages (init→layout→routing→translation→opt→sched) | G | `/docs/guides/transpiler-stages` |
| 9 | Transpile with pass managers / preset | G | `/docs/guides/transpile-with-pass-managers` |
| 10 | transpiler module | A | `/docs/api/qiskit/transpiler` |
| 11 | Preset pass managers (generate_preset_pass_manager) | A | `/docs/api/qiskit/transpiler_preset` |
| 12 | Primitives concept (Sampler/Estimator) | G | `/docs/guides/primitives` |
| 13 | Get started with primitives | G | `/docs/guides/get-started-with-primitives` |
| 14 | Primitive input/output (PUBs, results) | G | `/docs/guides/primitive-input-output` |
| 15 | V2 primitives interface | G | `/docs/guides/v2-primitives` |
| 16 | primitives module (SamplerV2/EstimatorV2 base) | A | `/docs/api/qiskit/primitives` |
| 17 | Runtime SamplerV2/EstimatorV2 (execution) | A | `/docs/api/qiskit-ibm-runtime` |
| 18 | Execution modes (job/session/batch) | G | `/docs/guides/execution-modes` |
| 19 | Visualize circuits (draw) | G | `/docs/guides/visualize-circuits` |
| 20 | Visualize results (histogram, Bloch, state) | G | `/docs/guides/visualize-results` |
| 21 | visualization module | A | `/docs/api/qiskit/visualization` |
| 22 | Operators overview (quantum_info) | G | `/docs/guides/operators-overview` |
| 23 | Operator class (Pauli/SparsePauliOp/Statevector) | G | `/docs/guides/operator-class` |
| 24 | quantum_info module | A | `/docs/api/qiskit/quantum_info` |
| 25 | OpenQASM interop (intro + 2/3) | G | `/docs/guides/introduction-to-qasm` |
| 26 | qasm2 / qasm3 modules | A | `/docs/api/qiskit/qasm3` |
| 27 | QPY serialization | A | `/docs/api/qiskit/qpy` |
| 28 | Save/serialize circuits | G | `/docs/guides/save-circuits` |
| 29 | Providers / fake backends | A | `/docs/api/qiskit/providers_fake_provider` |
| 30 | Result / counts | A | `/docs/api/qiskit/result` |
| 31 | Error mitigation & suppression | G | `/docs/guides/configure-error-mitigation` |
| 32 | Account / cloud setup | G | `/docs/guides/cloud-setup` |

## 7. Uncertainties / re-verify against live

- **Exam section weights:** only partial weights recovered from secondary sources (16/11/18% + primitives/running sections). Pull the authoritative breakdown + Study Guide PDF from the IBM Training C9008400 page.
- **Open Plan free QPU minutes:** value drifts; confirm on the live plans/pricing page.
- **Clone is ~4 months stale AND a fork:** live catalog already contains at least one course not in the clone — `learning/courses/use-a-qc-today` ("Use a quantum computer today", Olivia Lanes) surfaced via live MCP search. The live Learning landing now advertises "10+ courses" and features Watrous + Lanes. Re-scrape the live catalog before final linking.
- **API "latest" vs pinned version:** unversioned `/docs/api/qiskit/<page>` tracks latest (2.x); pin `/docs/api/qiskit/2.1/…` etc. if the site must match a specific SDK the exam targets.
- **Exact API deep-link for qasm2:** table row 26 links qasm3; qasm2 is `/docs/api/qiskit/qasm2` (both module pages exist).

## 8. Machine-usable JSON

```json
{
  "domains": {
    "docs": "https://quantum.cloud.ibm.com/docs",
    "learning": "https://quantum.cloud.ibm.com/learning",
    "platform": "https://quantum.cloud.ibm.com"
  },
  "certification": {
    "credential": "IBM Certified Quantum Computation using Qiskit v2.X Developer - Associate",
    "exam_code": "C1000-179",
    "format": "68 questions / 90 min / pass 47 of 68",
    "ibm_training_url": "https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400",
    "blog_url": "https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification",
    "recommended_prep": ["basics-of-quantum-information", "fundamentals-of-quantum-algorithms", "quantum-computing-in-practice"]
  },
  "license": {
    "code": "Apache-2.0",
    "content": "CC-BY-SA-4.0",
    "bottom_line": "Link freely (no obligation). Code snippets are Apache-2.0 (safe to copy with notice). Prose/course/tutorial content is CC BY-SA 4.0 - attribution + ShareAlike required if excerpted/adapted, so prefer linking or short attributed quotes."
  },
  "local_clone": {
    "path": "/Users/majl/GitHub/Qiskit-documentation",
    "remote": "github.com/JanLahmann/Qiskit-documentation (fork/derivative of Qiskit/documentation)",
    "last_commit": "2026-03-10",
    "staleness": "~4 months old as of 2026-07-19; read-only; verify new content against live"
  },
  "topics": [
    {"topic": "Hello world / end-to-end workflow", "urls": ["https://quantum.cloud.ibm.com/docs/guides/hello-world"]},
    {"topic": "Construct circuits", "urls": ["https://quantum.cloud.ibm.com/docs/guides/construct-circuits"]},
    {"topic": "Circuit library / gates", "urls": ["https://quantum.cloud.ibm.com/docs/guides/circuit-library", "https://quantum.cloud.ibm.com/docs/api/qiskit/circuit_library"]},
    {"topic": "QuantumCircuit class", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit/qiskit.circuit.QuantumCircuit"]},
    {"topic": "circuit module (gates, instructions, parameters, control flow)", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit/circuit"]},
    {"topic": "Transpilation overview", "urls": ["https://quantum.cloud.ibm.com/docs/guides/transpile"]},
    {"topic": "Transpiler stages", "urls": ["https://quantum.cloud.ibm.com/docs/guides/transpiler-stages"]},
    {"topic": "Pass managers / preset", "urls": ["https://quantum.cloud.ibm.com/docs/guides/transpile-with-pass-managers", "https://quantum.cloud.ibm.com/docs/api/qiskit/transpiler_preset"]},
    {"topic": "transpiler module", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit/transpiler"]},
    {"topic": "Primitives concept", "urls": ["https://quantum.cloud.ibm.com/docs/guides/primitives"]},
    {"topic": "Get started with primitives", "urls": ["https://quantum.cloud.ibm.com/docs/guides/get-started-with-primitives"]},
    {"topic": "Primitive input/output (PUBs)", "urls": ["https://quantum.cloud.ibm.com/docs/guides/primitive-input-output"]},
    {"topic": "V2 primitives interface", "urls": ["https://quantum.cloud.ibm.com/docs/guides/v2-primitives"]},
    {"topic": "primitives module (SamplerV2/EstimatorV2)", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit/primitives"]},
    {"topic": "Runtime SamplerV2/EstimatorV2 execution", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime"]},
    {"topic": "Execution modes (job/session/batch)", "urls": ["https://quantum.cloud.ibm.com/docs/guides/execution-modes"]},
    {"topic": "Visualize circuits", "urls": ["https://quantum.cloud.ibm.com/docs/guides/visualize-circuits"]},
    {"topic": "Visualize results (histogram, Bloch, state)", "urls": ["https://quantum.cloud.ibm.com/docs/guides/visualize-results"]},
    {"topic": "visualization module", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit/visualization"]},
    {"topic": "Operators / quantum_info", "urls": ["https://quantum.cloud.ibm.com/docs/guides/operators-overview", "https://quantum.cloud.ibm.com/docs/guides/operator-class", "https://quantum.cloud.ibm.com/docs/api/qiskit/quantum_info"]},
    {"topic": "OpenQASM interop", "urls": ["https://quantum.cloud.ibm.com/docs/guides/introduction-to-qasm", "https://quantum.cloud.ibm.com/docs/api/qiskit/qasm3", "https://quantum.cloud.ibm.com/docs/api/qiskit/qasm2"]},
    {"topic": "QPY serialization", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit/qpy", "https://quantum.cloud.ibm.com/docs/guides/save-circuits"]},
    {"topic": "Providers / fake backends", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit/providers_fake_provider", "https://quantum.cloud.ibm.com/docs/api/qiskit/providers"]},
    {"topic": "Result / counts", "urls": ["https://quantum.cloud.ibm.com/docs/api/qiskit/result"]},
    {"topic": "Error mitigation & suppression", "urls": ["https://quantum.cloud.ibm.com/docs/guides/configure-error-mitigation"]},
    {"topic": "Account / cloud setup", "urls": ["https://quantum.cloud.ibm.com/docs/guides/cloud-setup", "https://quantum.cloud.ibm.com/docs/guides/save-credentials"]}
  ],
  "courses": [
    {"title": "Basics of quantum information", "url": "https://quantum.cloud.ibm.com/learning/courses/basics-of-quantum-information", "covers": ["states", "measurements", "unitary operations", "quantum circuits", "teleportation", "superdense coding", "CHSH"]},
    {"title": "Fundamentals of quantum algorithms", "url": "https://quantum.cloud.ibm.com/learning/courses/fundamentals-of-quantum-algorithms", "covers": ["query model", "Deutsch-Jozsa", "Grover", "phase estimation", "Shor"]},
    {"title": "General formulation of quantum information", "url": "https://quantum.cloud.ibm.com/learning/courses/general-formulation-of-quantum-information", "covers": ["density matrices", "channels", "generalized measurements"]},
    {"title": "Foundations of quantum error correction", "url": "https://quantum.cloud.ibm.com/learning/courses/foundations-of-quantum-error-correction", "covers": ["codes", "stabilizers", "fault tolerance"]},
    {"title": "Quantum computing in practice", "url": "https://quantum.cloud.ibm.com/learning/courses/quantum-computing-in-practice", "covers": ["mapping problems", "running circuits", "primitives", "utility-scale QAOA", "applied Qiskit workflow"]},
    {"title": "Variational algorithm design", "url": "https://quantum.cloud.ibm.com/learning/courses/variational-algorithm-design", "covers": ["ansaetze", "cost functions", "optimization loops", "reference states"]},
    {"title": "Utility-scale quantum computing", "url": "https://quantum.cloud.ibm.com/learning/courses/utility-scale-quantum-computing", "covers": ["transpilation", "error mitigation", "large-scale workflow"]},
    {"title": "Quantum diagonalization algorithms", "url": "https://quantum.cloud.ibm.com/learning/courses/quantum-diagonalization-algorithms", "covers": ["SQD", "Krylov"]},
    {"title": "Quantum chemistry with VQE", "url": "https://quantum.cloud.ibm.com/learning/courses/quantum-chem-with-vqe", "covers": ["VQE", "chemistry"]},
    {"title": "Quantum machine learning", "url": "https://quantum.cloud.ibm.com/learning/courses/quantum-machine-learning", "covers": ["kernels", "QNN"]},
    {"title": "Integrating quantum and HPC", "url": "https://quantum.cloud.ibm.com/learning/courses/integrating-quantum-and-high-performance-computing", "covers": ["runtime", "execution modes", "HPC"]},
    {"title": "Quantum-safe cryptography", "url": "https://quantum.cloud.ibm.com/learning/courses/quantum-safe-cryptography", "covers": ["post-quantum crypto (context)"]},
    {"title": "Quantum business foundations", "url": "https://quantum.cloud.ibm.com/learning/courses/quantum-business-foundations", "covers": ["non-technical context"]},
    {"title": "Use a quantum computer today (live-only; not in stale clone)", "url": "https://quantum.cloud.ibm.com/learning/courses/use-a-qc-today", "covers": ["first quantum experiment", "beginner applied"]}
  ]
}
```
