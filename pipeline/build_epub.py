#!/usr/bin/env python3
"""Build the CertiQ Study Book EPUB — Kindle / e-reader support.

Modern Kindles accept EPUB via Send-to-Kindle; e-ink can't run the site or
Anki, so this is the offline vehicle. One book:

  Part I  — exam facts, how-to-use, per-section study chapters
            (objectives, cram primers + key facts, resource URLs in print form)
  Part II — the full question bank as a quiz book: each question on its own
            page (full option pool, like Anki — static media can't rotate),
            with the answer + explanations on the FOLLOWING page so the answer
            never shows while thinking. Internal links: question -> answer ->
            next question.

E-ink constraints honored: no color-bearing information, no images, <pre>
blocks kept intact (reader font settings apply), pure-black-on-white styling.

Output: site/static/downloads/certiq-study-book.epub
Usage:  python3 pipeline/build_epub.py
"""

from __future__ import annotations

import html
import json
import sys
from datetime import date
from pathlib import Path

from ebooklib import epub

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_anki import code_block, md_inline  # noqa: E402  (Anki-safe HTML == EPUB-safe)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "site" / "static" / "downloads" / "certiq-study-book.epub"

CSS = """
body { font-family: serif; line-height: 1.45; }
h1, h2, h3 { font-family: sans-serif; }
pre { font-family: monospace; font-size: 0.82em; white-space: pre-wrap;
      border: 1px solid #888; padding: 6px; }
code { font-family: monospace; }
.opt { margin: 0.4em 0; }
.opt .k { font-weight: bold; padding-right: 0.4em; }
.correct { font-weight: bold; }
.meta { font-size: 0.85em; color: #444; }
.fact { margin: 0.35em 0; }
.src { font-size: 0.85em; }
.pagebreak { page-break-before: always; }
hr { border: none; border-top: 1px solid #999; margin: 1.2em 0; }
"""

DISCLAIMER = (
    "CertiQ is an unofficial, independent community project — not affiliated "
    "with, endorsed by, or sponsored by IBM. Qiskit is a trademark of IBM. "
    "All practice content is AI-generated from the public exam objectives and "
    "open documentation, executed and verified against a pinned Qiskit 2.x "
    "stack at build time, and adversarially reviewed. It is never derived "
    "from actual exam content. Found a problem? Every question lists its id — "
    "report it at github.com/JanLahmann/qiskit-developer-certification-prep."
)


def esc(t: str) -> str:
    return html.escape(t, quote=False)


def chapter(book: epub.EpubBook, uid: str, title: str, body: str) -> epub.EpubHtml:
    ch = epub.EpubHtml(uid=uid, title=title, file_name=f"{uid}.xhtml", lang="en")
    ch.content = f"<h2>{esc(title)}</h2>\n{body}"
    ch.add_link(href="style/book.css", rel="stylesheet", type="text/css")
    book.add_item(ch)
    return ch


def study_chapter_body(sec: dict, study: dict | None, qcount: int) -> str:
    parts = [
        f"<p><b>{sec['weight_pct']}% of the exam.</b> "
        f"{qcount} practice questions in Part II.</p>",
        "<h3>Objectives</h3><ul>",
    ]
    parts += [f"<li>{md_inline(o['text'])}</li>" for o in sec["objectives"]]
    parts.append("</ul>")

    if study:
        obj_titles = {o["id"]: o["text"] for o in sec["objectives"]}
        facts_by_obj: dict[str, list[dict]] = {}
        for f in study.get("facts", []):
            facts_by_obj.setdefault(f["objective"], []).append(f)
        for oid, otext in obj_titles.items():
            primers = [p for p in study.get("primers", []) if p["objective"] == oid]
            if not primers and oid not in facts_by_obj:
                continue
            parts.append(f"<h3>{md_inline(otext)}</h3>")
            for p in primers:
                parts.append(f"<h4>{md_inline(p['title'])}</h4>")
                parts.append(f"<p>{md_inline(p['body_md'])}</p>")
            facts = facts_by_obj.get(oid, [])
            if facts:
                parts.append("<p><b>Key facts:</b></p>")
                for f in facts:
                    src = f["source"]
                    tag = (
                        f"proven by execution ({esc(src['ref'])})"
                        if src["type"] == "proof"
                        else f"source: {esc(src['ref'].split('//')[-1])}"
                    )
                    parts.append(
                        f'<div class="fact">• {md_inline(f["fact_md"])} '
                        f'<span class="src">[{tag}]</span></div>'
                    )

    resources = [r for r in sec.get("resources", []) if r.get("url")]
    if resources:
        parts.append("<h3>Official resources</h3><ul>")
        for r in resources:
            parts.append(f"<li>{esc(r['title'])}<br/><code>{esc(r['url'])}</code></li>")
        parts.append("</ul>")
    return "\n".join(parts)


def add_figure(book: epub.EpubBook, q: dict, spec: dict | None) -> str:
    """Embed a figure SVG (grayscale-safe only) and return its <img> HTML.

    Figures whose meaning needs color (figures.color_essential — e.g. the
    q-sphere's phase wheel) are NOT embedded on e-ink; the alt text stands in
    and points the reader at the website.
    """
    if not spec:
        return ""
    if (q.get("figures") or {}).get("color_essential"):
        return (f'<p class="meta"><i>[Color figure — see this question on '
                f"certiq.dev. Description: {esc(spec['alt'])}]</i></p>")
    src = DATA / spec["file"]
    if not src.exists():
        return ""
    name = spec["file"].rsplit("/", 1)[-1]
    uid = f"img-{name}"
    if uid not in _added_images:
        book.add_item(epub.EpubItem(uid=uid, file_name=f"img/{name}",
                                    media_type="image/svg+xml",
                                    content=src.read_bytes()))
        _added_images.add(uid)
    return f'<div><img src="img/{name}" alt="{esc(spec["alt"])}" style="max-width:100%"/></div>'


_added_images: set[str] = set()


def question_pages(book: epub.EpubBook, q: dict, next_uid: str | None) -> list[epub.EpubHtml]:
    qid = q["id"]
    quid, auid = f"q-{qid}", f"a-{qid}"
    multi = q["type"] == "multi"
    figs = q.get("figures") or {}
    opt_figs = figs.get("options") or {}

    qparts = [f'<p class="meta">{esc(qid)} · {esc(q["type"])} · difficulty {q["difficulty"]}/3</p>']
    qparts.append(f"<p>{md_inline(q['stem'])}"
                  + (" <i>(Select all that apply.)</i>" if multi else "") + "</p>")
    if q.get("code"):
        qparts.append(code_block(q["code"]))
    qparts.append(add_figure(book, q, figs.get("stem")))
    for o in q["options"]:
        qparts.append(f'<div class="opt"><span class="k">{esc(o["key"])}.</span>'
                      f"{md_inline(o['text'])}"
                      f"{add_figure(book, q, opt_figs.get(o['key']))}</div>")
    qparts.append(f'<p><a href="{auid}.xhtml">Show answer →</a></p>')
    qch = chapter(book, quid, f"{qid}", "\n".join(qparts))

    ans = ", ".join(q["answer"])
    aparts = [f'<p class="meta">{esc(qid)} — answer</p>',
              f'<p class="correct">Correct: {esc(ans)}</p>',
              f"<p>{md_inline(q['explanation']['correct'])}</p>"]
    wrong = [(k, v) for k, v in sorted(q["explanation"].get("distractors", {}).items())
             if k not in set(q["answer"]) and v]
    if wrong:
        aparts.append("<p><b>Why the others are wrong:</b></p>")
        for k, v in wrong:
            aparts.append(f'<div class="opt"><span class="k">{esc(k)}.</span>{md_inline(v)}</div>')
    cits = q["explanation"].get("citations", [])
    if cits:
        aparts.append("<p class='src'><b>Read more:</b><br/>"
                      + "<br/>".join(f"<code>{esc(u)}</code>" for u in cits[:3]) + "</p>")
    if next_uid:
        aparts.append(f'<p><a href="{next_uid}.xhtml">Next question →</a></p>')
    ach = chapter(book, auid, f"{qid} — answer", "\n".join(aparts))
    return [qch, ach]


def main() -> int:
    syllabus = json.loads((DATA / "syllabus.json").read_text())
    sections = syllabus["sections"]

    bank: dict[str, list[dict]] = {}
    for p in sorted((DATA / "questions").glob("s*/*.json")):
        q = json.loads(p.read_text())
        bank.setdefault(q["section"], []).append(q)

    book = epub.EpubBook()
    book.set_identifier("certiq-study-book")
    book.set_title("CertiQ Study Book — IBM Qiskit v2.x Developer Certification (unofficial)")
    book.set_language("en")
    book.add_author("CertiQ (AI-generated, execution-verified; unofficial)")

    css = epub.EpubItem(uid="css", file_name="style/book.css",
                        media_type="text/css", content=CSS.encode())
    book.add_item(css)

    exam = syllabus["exam"]
    intro_body = (
        f"<p><i>{esc(DISCLAIMER)}</i></p>"
        f"<p>Generated {date.today().isoformat()} from the CertiQ bank: "
        f"{sum(len(v) for v in bank.values())} machine-verified questions.</p>"
        f"<h3>The exam</h3><ul>"
        f"<li>{esc(exam['code'])} — {exam['questions']} questions, "
        f"{exam['minutes']} minutes, pass at {exam['pass_score']}.</li>"
        f"<li>Qiskit SDK v2.x + Runtime primitives (SamplerV2 / EstimatorV2).</li></ul>"
        "<h3>How to use this book</h3>"
        "<p>Part I is the study layer: objectives, background primers, and "
        "key facts (each fact names its source — an official docs page or an "
        "executed proof from the question id shown). Part II is the drill: "
        "read a question, commit to an answer, then turn the page. Options "
        "are printed with their bank keys; on the website the same questions "
        "appear with shuffled positions and rotating wrong answers.</p>"
    )
    intro = chapter(book, "intro", "Start here", intro_body)

    spine: list = ["nav", intro]
    toc: list = [intro]

    # Part I — study chapters
    study_chs = []
    for sec in sections:
        sid = sec["id"]
        study_file = DATA / "study" / f"{sid}.json"
        study = json.loads(study_file.read_text()) if study_file.exists() else None
        ch = chapter(book, f"study-{sid}", f"Section {sid[1:]}: {sec['title']}",
                     study_chapter_body(sec, study, len(bank.get(sid, []))))
        study_chs.append(ch)
        spine.append(ch)
    toc.append((epub.Section("Part I — Study"), study_chs))

    # Part II — quiz book
    for sec in sections:
        sid = sec["id"]
        qs = bank.get(sid, [])
        if not qs:
            continue
        head = chapter(book, f"quiz-{sid}",
                       f"Questions — Section {sid[1:]}: {sec['title']}",
                       f"<p>{len(qs)} questions. Answers follow each question "
                       f'on the next page. <a href="q-{qs[0]["id"]}.xhtml">Start →</a></p>')
        spine.append(head)
        sec_chs = [head]
        for i, q in enumerate(qs):
            nxt = f"q-{qs[i + 1]['id']}" if i + 1 < len(qs) else None
            qch, ach = question_pages(book, q, nxt)
            spine += [qch, ach]
            sec_chs.append(qch)
        toc.append((epub.Section(f"Part II — Drill {sid}"), sec_chs))

    book.toc = toc
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(OUT), book)
    size_kb = OUT.stat().st_size // 1024
    n_q = sum(len(v) for v in bank.values())
    print(f"wrote {OUT.relative_to(ROOT)} ({size_kb} KB, {n_q} questions, "
          f"{len(sections)} study chapters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
