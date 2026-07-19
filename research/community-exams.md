# Community Qiskit Developer Certification Practice Exams + Advocate Program 2.0

_Research date: 2026-07-19. Current exam: **C1000-179** (Qiskit v2.x, "IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate", exam page [C9008400](https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400)). Format: 68 questions, 90 min, pass 47/68. Predecessor: **C1000-112** (Qiskit v0.2x)._

---

## 1. Inventory of community practice exams

### v2.x era (C1000-179) — genuine multiple-choice practice exams / quiz tools

| # | Repo / URL | Author | Format | #Qs | Answers+expl? | Code Qs? | License | Updated | Stars | Quality impression |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [vantnprof/Qiskit_v2X_Certificate_Practice](https://github.com/vantnprof/Qiskit_v2X_Certificate_Practice) | vantnprof | Markdown (`Practice.md`) | 68 | Yes (collapsible "Answer and explanation" + key) | Yes | none stated | 2026 | 0 | High. Mirrors real exam exactly (68Q/90min/47 pass, single + select-all). Bell-state Q verified correct (ans C). Original, well-formed. Almost certainly an advocate submission. |
| 2 | [KurianUthuppu/ibm_qiskit_2_x](https://github.com/KurianUthuppu/ibm_qiskit_2_x) (`Practice_Exams/`) | KurianUthuppu | Markdown + solutions folder | 20 (exam 1) | Yes (solutions) | Yes | none stated | 2026 | 0 | High. Exam-accurate; lists official 8-section weights. Sample Q on `EstimatorV2` `resilience_level=2`/ZNE is correct & professional. Exactly meets 20-Q advocate minimum. |
| 3 | [hastikacheddy/qiskit-cert-prep](https://github.com/hastikacheddy/qiskit-cert-prep) ([live app](https://hastikacheddy.github.io/qiskit-cert-prep/)) | hastikacheddy | Browser app (single HTML) | 583 | Yes — per-option "why right/wrong" | Yes | MIT | 2026-07-18 | 0 | Very polished. Flashcards, quiz, timed exam sim, SM-2 spaced repetition, dashboard, localStorage. Covers full syllabus. Strong candidate. |
| 4 | [Luke-J-Miller/Qiskit-v2.X-developer-certification-practice-test](https://github.com/Luke-J-Miller/Qiskit-v2.X-developer-certification-practice-test) | Luke J. Miller | Jupyter notebook | 1000+ | Not clearly stated | Yes ("circuit deconstruction ASCII" items) | none stated | 2026-07-03 | 16 | Largest bank; adaptive study, save progress, study-by-target. Most-starred v2.x exam. Author admits gaps (rare gates omitted); question correctness unverified from README. |
| 5 | [dorakingx/qisquiz](https://github.com/dorakingx/qisquiz) | dorakingx | Next.js quiz app (`questions.ts`) | many (per-section banks) | Yes — explanation + commonMistake + relatedDocsUrl | Yes | none stated | 2026 | 0 | Original items "mapped to IBM C1000-179 objectives", difficulty tags, exam-skill mapping. X/H-gate Qs verified correct. Well-engineered. |
| 6 | [MrRobert91/QuantumComputingGuide](https://github.com/MrRobert91/QuantumComputingGuide) | MrRobert91 | Interactive web app (React) + MockExamPage | mock exam + lessons | Yes | Yes (Aer-executable) | none stated | 2026 | 0 | Full syllabus (10 modules/35 lessons, official section weights), Bloch/circuit widgets, mock exam. Code verified vs Qiskit 2.5 + runtime 0.47. Ambitious. |
| 7 | [quantum-tokyo/qiskit-certification-prep](https://github.com/quantum-tokyo/qiskit-certification-prep) ([web](https://quantum-tokyo.github.io/qiskit-certification-prep/)) | Quantum Tokyo community | Web page practice questions | multiple | Yes | Yes | Apache-2.0 | 2026-05-29 | 6 | Community-maintained (Quantum Tokyo). Unofficial practice questions for v2.x Associate. Credible group. |
| 8 | [0sophy1/qrabbit-hole](https://github.com/0sophy1/qrabbit-hole) | 0sophy1 (Sophy) | watsonx Assistant chat quiz | interactive | Yes | some | none stated | 2026-03 | 0 | Story-based ("Alice & Bob down the quantum rabbit hole") conversational quiz. Novel format; not a static ≥20-Q bank. |

### v2.x era — study material / notebooks with embedded quizzes (adjacent, not pure MCQ exams)

| Repo | Author | Format | Notes |
|---|---|---|---|
| [kibrahim757/qiskit_2x_certification_exam_tutorial](https://github.com/kibrahim757/qiskit_2x_certification_exam_tutorial) | kibrahim757 + alanspace | Jupyter notebooks | **QAMP 2025** project ([qamp-2025 #42](https://github.com/qiskit-advocate/qamp-2025/issues/42)). Comprehensive topic notebooks. |
| [Hannan0107/Qiskit-Certification-Practice-Notebooks](https://github.com/Hannan0107/Qiskit-Certification-Practice-Notebooks) | Hannan0107 | 30 notebooks + live self-check quizzes | MIT. Day-by-day split of kibrahim757's notebooks + added interactive quizzes (derivative, credited). |
| [yusufibrahim0107-create/Qiskit-Certification-Practice-Notebooks](https://github.com/yusufibrahim0107-create/Qiskit-Certification-Practice-Notebooks) | yusufibrahim0107 | 30 notebooks | MIT. Near-duplicate of above. |
| [jvscursulim/study-group-qiskit-2.x-certification](https://github.com/jvscursulim/study-group-qiskit-2.x-certification) | jvscursulim | Weekly notebooks (6 sections) | Study-group curriculum with per-section material (likely a Qiskit v2.X study group — advocate 2-pt activity). |
| [algovista-collab/qiskit_v2_study_materials](https://github.com/algovista-collab/qiskit_v2_study_materials) | algovista-collab | Notebooks | 8-section syllabus theory + code, 2 stars, 2026. |
| [MisterSzled/qiskit_flashcodes](https://github.com/MisterSzled/qiskit_flashcodes) | MisterSzled | Code-snippet flashcards | GPL-3.0, 2025-10. Runnable snippet per exam topic; not MCQ. |
| [NiankSoft/qiskit-v2.x-training](https://github.com/NiankSoft/qiskit-v2.x-training) · [Caraquel/QC_IBM_Qiskit-Cert-CA](https://github.com/Caraquel/QC_IBM_Qiskit-Cert-CA) | — | Training notes | v2.x prep material, 2026, 0 stars. |

### v0.2x era (C1000-112 / older C0010300) — notable older resources

| Repo | Author | Format | #Qs | License | Updated | Stars | Notes |
|---|---|---|---|---|---|---|---|
| [pratjz/IBM-Qiskit-Certification-Exam-Prep](https://github.com/pratjz/IBM-Qiskit-Certification-Exam-Prep) | pratjz | Pointers/resource list | n/a | none | 2026-02 | **33** | Most-starred cert-prep repo overall; curated pointers (spans both eras). |
| [arthurfaria/Qiskit_certificate_prep](https://github.com/arthurfaria/Qiskit_certificate_prep) | Arthur Faria | Jupyter workbook | n/a | MIT | 2025-06 | 24 | Well-regarded workbook; targets old exam (C0010300/C1000-112). |
| [VedDharkar/IBM_QISKIT_EXAM_C1000-112](https://github.com/VedDharkar/IBM_QISKIT_EXAM_C1000-112) | Ved Dharkar | Resources | n/a | Apache-2.0 | 2025-04 | 20 | Explicitly C1000-112. |
| [petr-ivashkov/qiskit-cert-workbook](https://github.com/petr-ivashkov/qiskit-cert-workbook) | Petr Ivashkov | Notebook | n/a | MIT | 2023 | 5 | Prep workbook. |
| [soumya-s3/qiskit_developer_test_notebook](https://github.com/soumya-s3/qiskit_developer_test_notebook) | soumya-s3 | Notebook | n/a | MIT | 2023 | 5 | Test notebook for old exam. |
| [Sidx369/Qiskit-Developer-Exam-C1000-112-Prep](https://github.com/Sidx369/Qiskit-Developer-Exam-C1000-112-Prep) | Sidx369 | Notebooks | n/a | none | 2022 | 0 | C1000-112 prep. |
| [olgOk/qiskit_certificate_preparation](https://github.com/olgOk/qiskit_certificate_preparation) · [peachnuts/Prepare-for-qiskit-developer-certification-exam](https://github.com/peachnuts/Prepare-for-qiskit-developer-certification-exam) | — | Exercises / slides | n/a | MIT | 2022 | 0 | Older prep (exercises, slides). |

_Non-GitHub community note: [schrodinteq.github.io](https://schrodinteq.github.io/) ("Schrodin's Diary") publishes detailed **free** explanations of IBM's official v2.x Sample Test ([Part 1](https://schrodinteq.github.io/ibmcertsamplev2x01/), [Part 2](https://schrodinteq.github.io/ibmcertsamplev2x02/), English + Japanese)._

---

## 2. Qiskit Advocate Program 2.0 — key facts

**Where it lives:**
- Public announcement / apply: IBM Quantum blog "Applications are open for the Qiskit advocate program" (https://www.ibm.com/quantum/blog/qiskit-advocate-program). Coverage: [HPCwire, 2025-07-29](https://www.hpcwire.com/2025/07/29/ibm-launches-qiskit-advocate-program-2-0/).
- Official org: [github.com/qiskit-advocate](https://github.com/qiskit-advocate). Key repos: `qiskit-advocate-library` (**private, advocate-only** — holds the points guide & materials), `qap-eligibility`, `advocate-agreements`, `qamp-2025`, `qamp-general`. The old [application-guide](https://github.com/qiskit-advocate/application-guide) is **archived (May 2025)** — it describes the pre-2.0 (2023) scoring and is now outdated.
- Points claims are submitted via an **Airtable form** (linked in the private points guide).

**Tier structure** (all advocates start at **Tier 0**; level up by crossing a points threshold **AND** holding the Qiskit v2.x certification):
- **Tier 0:** exclusive Discord community; eligible to mentor at IBM Quantum flagship events.
- **Tier 1:** public recognition as official advocate; official swag; participate in **QAMP**.
- **Tier 2:** annual Credly accomplishment badge; beta-test new Qiskit features & courses.
- **Tier 3:** +30 min IBM QPU access per month.
- **The Qiskit SDK v2.x developer certification (C1000-179) is a HARD requirement for progression beyond Tier 0** (i.e. required for Tier 1+). Confirmed in IBM blog + certification blog.

**Full points/activity table** (from the private `qiskit-advocate-library/advocate-information/points_guide.md`, effective dates 7 May 2025 unless noted):

_1 point each:_
- Attended a live Qiskit advocate seminar (or watched recording within 24 h)
- Completed a badged IBM Quantum Learning course (excl. Basics of QI / Foundations of QA)
- Completed the Qiskit advocate training (training video + Quantum Business Foundations)
- Used >8 min of the open-plan 10-min monthly allocation
- Completed the half-yearly advocate feedback survey (eff. 5 Aug 2025)
- Accepted syntax/grammar/small-bug PR to Qiskit SDK or Ecosystem (eff. 28 May 2025)
- **Created a Qiskit v2.x Certification practice exam (min 20 questions)** — _provide a link to the published exam (e.g. public GitHub); must have ≥20 multi-choice questions; questions assessed for quality._ ← the activity driving these repos
- Participated in an approved event

_2 points each:_
- Gave an approved talk using Qiskit advocate materials
- Participated in / organized a Quantum Computing club **or Qiskit v2.X Certification study group** (claim after the 12-week initiative ends)

_4 points each:_
- Actively mentored in an official Qiskit event (QGSS, Qiskit Fall Fest)
- **Completed a project in QAMP 2025** (eff. 5 Aug 2025)
- Accepted code PR to Qiskit SDK/Ecosystem (new feature / major bug fix, eff. 28 May 2025)
- Won first prize in an external hackathon using Qiskit (eff. 5 Aug 2025)
- Completed a user interview (by IBM request, eff. 5 Aug 2025)
- Opted-in & used 180 min in the new open-plan promotion (eff. 16 Mar 2026)

**QAMP relationship:** The **Qiskit Advocate Mentorship Program** — advocates work on Qiskit projects with mentors over ~3 months, runs in the second half of each year. It is a **Tier-1 benefit** (you can participate once at Tier 1) and completing a QAMP project = **4 points**. QAMP 2025 is directly producing cert-prep material (e.g. `kibrahim757/qiskit_2x_certification_exam_tutorial`, qamp-2025 issue #42).

**Note on the specific practice-exam activity value:** it is worth only **1 point** (not a large amount) but requires a quality review — hence the recent wave (mostly 2025–2026) of ≥20-question community exams on GitHub.

---

## 3. Guided prep platforms / courses (competitive landscape)

- **IBM official (free):** Sample Test + downloadable study guide on the [IBM Training C9008400 page](https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400). The de-facto baseline everyone recommends.
- **Udemy (paid) — v2.x:** ["IBM Certified Quantum Computation Qiskit v2.x Practice Exams"](https://www.udemy.com/course/ibm-certified-quantum-computation-qiskit-v2x-practice-exams/) — full mock exams with explanations.
- **Udemy (paid) — v2.x hands-on:** "Qiskit v2.X Quick Start in 60 Min: Hands-On Quantum Computing."
- **Udemy (paid) — older v0.2x:** ["IBM Certified Quantum Computation - Qiskit: Practice Exams"](https://www.udemy.com/course/ibm-certified-quantum-computation-qiskit-practice-exams/).
- **Free blog course:** [schrodinteq.github.io](https://schrodinteq.github.io/) — sample-test walkthroughs + exam experience/study-tips posts (v2.x).
- **Medium:** Ark Rana, ["A Complete Practice Test for Qiskit v.2x Certification"](https://medium.com/@arkrana9/a-complete-practice-test-for-qiskit-v-2x-certification-8188fc32e78b) (Aug 2025); a widely cited "230 practice questions" collection is referenced around this.
- **Avoid:** exam-dump sites (dumpsvalid, etc.) — low-quality "braindump" content, not legitimate practice.

---

## 4. Gaps / uncertainties

- **Licenses:** several of the strongest v2.x exams (vantnprof, KurianUthuppu, Luke-J-Miller, dorakingx, MrRobert91) have **no explicit LICENSE** — reuse rights unclear; worth confirming before building on them.
- **Exact question counts** for the app/notebook-based ones (dorakingx, MrRobert91, jvscursulim) weren't tallied precisely — they're bank/section-based.
- **Which repos are actual advocate submissions** isn't publicly listed; the points guide is private and there's no public registry of approved exams. Inferred from framing/timing (vantnprof, KurianUthuppu, hastikacheddy, Luke-J-Miller, dorakingx all read like advocate submissions; kibrahim757 is confirmed QAMP 2025).
- **Monthly-review cadence:** the task mentioned "monthly reviews"; the points guide shows rolling Airtable claim submission but I did not find an explicit monthly-review statement — treat cadence as unconfirmed.
- **Question correctness** was spot-checked on 3–4 repos only (all correct where checked); no exam was fully audited.
- `gh search` returned 0 for several queries ("qiskit practice exam", "C1000-179", "qiskit quiz/mock exam") due to GitHub's topic/description indexing — code search + varied phrasing was far more productive.

_Report file: `/private/tmp/claude-501/-Users-majl-GitHub-qiskit-developer-certification-prep/c804621c-a4db-4fd1-bc3e-cd7c280c4a88/scratchpad/research/community-exams.md`_
