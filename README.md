# Qiskit v2.x Certification Prep Platform

> Working title: **Qiskit Certification Studio** — an unofficial, free, community-built guided learning platform for the IBM **C1000-179** exam ("Fundamentals of Quantum Computing Using Qiskit v2.X Developer").

**This is an independent community project. It is not affiliated with, endorsed by, or sponsored by IBM. Qiskit is a trademark of IBM. All practice content is generated from public exam objectives and open documentation — never from actual exam content.**

## What makes it different

- **Machine-verified questions**: every code-bearing practice question is executed at build time against a pinned Qiskit 2.x stack — correct answers are *proven*, wrong answers are *disproven*, and the proof ships with the question.
- **Built by AI, served static**: all intelligence (generation, verification, remediation advice, study sequencing) runs at build time. The site itself is fully static — no accounts, no backend, no runtime AI, works offline. Progress lives in your browser (localStorage).
- **Guided, not just quizzed**: official syllabus → curated official resources (IBM Quantum docs & Learning) → drills → mock exam (faithful 68 questions / 90 minutes / pass at 47) → per-section remediation.
- **Community-connected**: directory of advocate-created practice exams (credited & linked), with build-time validation reports; freshness CI re-verifies everything on every Qiskit release.

## Repository layout

| Path | Purpose |
|---|---|
| `PRD.md` | Product requirements & architecture (start here) |
| `data/syllabus.json` | Canonical machine-readable exam syllabus — root build input |
| `data/questions/` | Verified question bank (JSON, one file per question) |
| `pipeline/` | Build-time generation, verification & validation tooling (Python) |
| `site/` | The website (Docusaurus 3) |
| `research/` | Research reports the build is based on (provenance) |

## Status

Early build (started 2026-07-19). See `PRD.md` §8 for the delivery plan.

## License

Code: [Apache-2.0](LICENSE). Original learning content (questions, explanations, guides): CC BY-SA 4.0. Official IBM/Qiskit resources are linked, not copied; community practice exams are linked and credited, never republished.
