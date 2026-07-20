#!/usr/bin/env python3
"""Build Anki flashcard decks (.apkg) from the CertiQ verified question bank.

Reads every ``site/src/data/bank/*.json`` file, and for each section that has
at least one question emits an Anki package under ``site/static/downloads/``:

    certiq-<sid>-<kebab-title>.apkg   (one per non-empty section)
    certiq-all-sections.apkg          (every section as sub-decks)

It also (re)generates ``site/docs/flashcards.mdx`` with download links that
always match the packages actually produced, so the page stays correct as the
bank fills in.

Design goals
------------
* Deterministic: model id, deck ids and note GUIDs are derived from stable
  names via SHA-1, so re-running never changes them and re-importing an updated
  deck *updates* cards instead of duplicating them.
* Re-runnable at every site build: works with whatever sections are present,
  silently skipping nothing -- every section is reported in the summary.
* No runtime installs. ``genanki`` must already be in the environment
  (see ``pipeline/requirements-extra.txt``); install it with
  ``.venv/bin/pip install -r pipeline/requirements-extra.txt``.

Usage
-----
    .venv/bin/python pipeline/build_anki.py
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

import genanki

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
BANK_DIR = REPO_ROOT / "site" / "src" / "data" / "bank"
DOWNLOADS_DIR = REPO_ROOT / "site" / "static" / "downloads"
FLASHCARDS_MDX = REPO_ROOT / "site" / "docs" / "flashcards.mdx"

DECK_ROOT = "CertiQ — C1000-179"  # Anki parent deck; sections become sub-decks
GUID_NAMESPACE = "certiq"  # keeps note GUIDs stable & content-independent


# --------------------------------------------------------------------------
# Stable id helpers
# --------------------------------------------------------------------------
def stable_id(name: str) -> int:
    """Deterministic positive int id for a genanki model/deck, from its name."""
    return int(hashlib.sha1(name.encode("utf-8")).hexdigest()[:10], 16)


def stable_guid(*parts: str) -> str:
    """Deterministic note GUID from stable identifiers (not from field text),
    so editing a card's wording still updates the same note on re-import."""
    return genanki.guid_for(GUID_NAMESPACE, *parts)


# --------------------------------------------------------------------------
# Tiny inline-markdown -> HTML converter
# --------------------------------------------------------------------------
_CODE_RE = re.compile(r"`([^`]+)`")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def md_inline(text: str) -> str:
    """Convert the small subset of inline markdown used in the bank
    (``backticks`` and ``**bold**``) into Anki-safe HTML.

    The text is HTML-escaped *first* so that literal ``<``/``>``/``&`` in code
    spans (e.g. ``|0>``, ``diag(1, i)``) survive, then the markdown markers --
    which are not HTML-special -- are replaced.
    """
    if not text:
        return ""
    out = html.escape(text, quote=False)
    out = _CODE_RE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = _BOLD_RE.sub(lambda m: f"<b>{m.group(1)}</b>", out)
    return out


def code_block(code: str) -> str:
    """Render a literal code snippet as an escaped <pre><code> block."""
    if not code:
        return ""
    return f"<pre><code>{html.escape(code, quote=False)}</code></pre>"


def kebab(text: str) -> str:
    """Lower-case, hyphen-separated slug for filenames."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)


# --------------------------------------------------------------------------
# Card model  ("CertiQ QA")
# --------------------------------------------------------------------------
MODEL_CSS = """
.card {
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 17px;
  line-height: 1.5;
  color: #1a1a1a;
  background: #ffffff;
  text-align: left;
  padding: 4px 8px;
}
.stem { margin-bottom: 12px; }
pre {
  background: #f4f4f5;
  border: 1px solid #e2e2e5;
  border-radius: 6px;
  padding: 10px 12px;
  overflow-x: auto;
}
pre code { font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 14px; }
code {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.92em;
  background: #f0f0f2;
  padding: 1px 4px;
  border-radius: 4px;
}
.options { margin: 8px 0; }
.opt { margin: 3px 0; }
.opt .k { font-weight: 700; margin-right: 6px; }
#answer { margin: 14px 0; border: none; border-top: 2px solid #d0d0d5; }
.correct { font-size: 1.05em; margin-bottom: 8px; }
.correct .k { color: #0a7d33; font-weight: 700; }
.explanation { margin-bottom: 10px; }
.citations { font-size: 0.9em; }
.citations ul { margin: 4px 0 0; padding-left: 20px; }
.meta {
  margin-top: 16px;
  padding-top: 8px;
  border-top: 1px solid #ececef;
  font-size: 0.78em;
  color: #6b6b70;
}
.meta .disclaimer { font-style: italic; }
""".strip()

MODEL = genanki.Model(
    stable_id("CertiQ QA model v1"),
    "CertiQ QA",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
        {"name": "Meta"},
    ],
    templates=[
        {
            "name": "Q&A",
            "qfmt": "{{Question}}",
            "afmt": (
                '{{FrontSide}}\n<hr id="answer">\n{{Answer}}'
                '\n<div class="meta">{{Meta}}</div>'
            ),
        }
    ],
    css=MODEL_CSS,
)

DISCLAIMER = (
    "AI-generated, execution-verified — CertiQ. "
    "Unofficial: not affiliated with, endorsed by, or sponsored by IBM."
)


# --------------------------------------------------------------------------
# Field builders
# --------------------------------------------------------------------------
def build_question_field(q: dict) -> str:
    parts = [f'<div class="stem">{md_inline(q.get("stem", ""))}</div>']
    code = q.get("code")
    if code:
        parts.append(code_block(code))
    opts = q.get("options") or []
    if opts:
        rows = [
            f'<div class="opt"><span class="k">{html.escape(str(o.get("key", "")))}.</span>'
            f'{md_inline(o.get("text", ""))}</div>'
            for o in opts
        ]
        parts.append('<div class="options">' + "".join(rows) + "</div>")
    return "\n".join(parts)


def build_answer_field(q: dict) -> str:
    answer_keys = q.get("answer") or []
    keys_txt = ", ".join(html.escape(str(k)) for k in answer_keys) or "—"
    parts = [f'<div class="correct"><span class="k">Correct: {keys_txt}</span></div>']

    explanation = q.get("explanation") or {}
    correct = explanation.get("correct")
    if correct:
        parts.append(f'<div class="explanation">{md_inline(correct)}</div>')

    citations = explanation.get("citations") or []
    if citations:
        links = []
        for url in citations[:3]:
            href = html.escape(str(url), quote=True)
            label = html.escape(str(url).replace("https://", "").replace("http://", ""))
            links.append(f'<li><a href="{href}">{label}</a></li>')
        parts.append(
            '<div class="citations"><b>References</b><ul>' + "".join(links) + "</ul></div>"
        )
    return "\n".join(parts)


def build_meta_field(q: dict) -> str:
    qid = html.escape(str(q.get("id", "")))
    difficulty = q.get("difficulty")
    diff_txt = f"Difficulty {difficulty}/3" if difficulty is not None else ""
    qtype = html.escape(str(q.get("type", "")))
    bits = " · ".join(x for x in [qid, qtype, diff_txt] if x)
    return f'<div>{bits}</div>\n<div class="disclaimer">{html.escape(DISCLAIMER)}</div>'


def make_note(q: dict) -> genanki.Note:
    return genanki.Note(
        model=MODEL,
        fields=[build_question_field(q), build_answer_field(q), build_meta_field(q)],
        guid=stable_guid(str(q.get("id", ""))),
    )


# --------------------------------------------------------------------------
# Bank loading
# --------------------------------------------------------------------------
def load_sections() -> list[dict]:
    """Return every bank section sorted by numeric section id (s1..s8)."""
    sections = []
    for path in sorted(BANK_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  ! skipping {path.name}: {exc}")
            continue
        sec = data.get("section") or {}
        sections.append(
            {
                "sid": sec.get("id") or path.stem,
                "num": sec.get("num"),
                "title": sec.get("title") or path.stem,
                "questions": data.get("questions") or [],
                "path": path,
            }
        )
    sections.sort(key=lambda s: (s["num"] is None, s["num"], s["sid"]))
    return sections


def deck_name_for(sec: dict) -> str:
    num = sec["num"] if sec["num"] is not None else sec["sid"]
    return f"{DECK_ROOT}::{num} · {sec['title']}"


def build_section_deck(sec: dict) -> genanki.Deck:
    name = deck_name_for(sec)
    deck = genanki.Deck(stable_id(name), name)
    for q in sec["questions"]:
        deck.add_note(make_note(q))
    return deck


# --------------------------------------------------------------------------
# flashcards.mdx generation
# --------------------------------------------------------------------------
def human_size(num_bytes: int) -> str:
    kb = num_bytes / 1024
    if kb < 1024:
        return f"{kb:.0f} KB"
    return f"{kb / 1024:.1f} MB"


def cards_label(n: int) -> str:
    return f"{n} card" if n == 1 else f"{n} cards"


def render_flashcards_mdx(rows: list[dict], all_row: dict) -> str:
    """rows: [{sid, num, title, count, filename, size}], all_row same shape."""

    def link(row: dict, label: str) -> str:
        return (
            f'    <li><Download file="{row["filename"]}">{label}</Download>'
            f' <span className="dl-meta">— {cards_label(row["count"])} · {human_size(row["size"])}</span></li>'
        )

    section_items = "\n".join(
        link(r, f'Section {r["num"]} — {r["title"]}') for r in rows
    )

    return f"""---
sidebar_position: 11
title: Flashcards (Anki)
description: Download the CertiQ verified question bank as Anki decks for spaced-repetition study.
---

{{/* GENERATED by pipeline/build_anki.py — do not edit by hand */}}

import useBaseUrl from '@docusaurus/useBaseUrl';

export const Download = ({{file, children}}) => (
  <a href={{useBaseUrl(`/downloads/${{file}}`)}} download>{{children}}</a>
);

# Flashcards (Anki)

Every verified practice question in the CertiQ bank, packaged as [Anki](https://apps.ankiweb.net/) decks you can drill anywhere — phone, laptop, offline. Each card shows the question (with code and options) on the front; the back reveals the correct answer, the worked explanation, and up to three source links.

## Why spaced repetition

Anki schedules each card just before you would forget it, so facts move into long-term memory with the least total review time. That is exactly what a closed-book certification rewards: recall the API shape, the default, the bit-ordering rule *without* looking it up. Drill a few minutes daily and the patterns become reflexive by exam day.

## Download

The decks below regenerate from the question bank at every site build, so **re-downloading always gives you the latest, verified content.** Cards keep stable identities, so re-importing an updated deck *updates* your existing cards instead of creating duplicates (your review history is preserved).

<ul className="download-list">
    <li><Download file="{all_row['filename']}"><b>All sections</b></Download> <span className="dl-meta">— {cards_label(all_row['count'])} · {human_size(all_row['size'])}</span></li>
</ul>

Or grab a single section:

<ul className="download-list">
{section_items}
</ul>

## Import into Anki

1. Install the free [Anki desktop app](https://apps.ankiweb.net/) (or AnkiMobile / AnkiDroid).
2. Download an `.apkg` file above, then in Anki choose **File → Import** and select it.
3. The cards land under the **{DECK_ROOT}** deck (each exam section is its own sub-deck). Click **Study Now** and start drilling.

To refresh later, re-download and import again — updated cards are matched by identity and overwritten in place, so nothing is duplicated.

:::note Unofficial
CertiQ is an independent community project. These cards are AI-generated from the public exam objectives and open documentation, then execution-verified against a pinned Qiskit 2.x stack — they are **not** affiliated with, endorsed by, or sponsored by IBM, and never derived from real exam content.
:::
"""


def write_flashcards_mdx(rows: list[dict], all_row: dict) -> None:
    FLASHCARDS_MDX.write_text(render_flashcards_mdx(rows, all_row), encoding="utf-8")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> None:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    sections = load_sections()

    print(f"CertiQ Anki build — {len(sections)} section file(s) found\n")
    print(f"Model 'CertiQ QA' id: {MODEL.model_id}\n")

    rows: list[dict] = []
    all_decks: list[genanki.Deck] = []
    total_cards = 0

    print("Per-section:")
    for sec in sections:
        count = len(sec["questions"])
        total_cards += count
        name = deck_name_for(sec)
        did = stable_id(name)
        if count == 0:
            print(f"  {sec['sid']}  {count:>3} cards  (empty — no deck)   deck_id={did}")
            continue

        deck = build_section_deck(sec)
        all_decks.append(deck)

        filename = f"certiq-{sec['sid']}-{kebab(sec['title'])}.apkg"
        out_path = DOWNLOADS_DIR / filename
        genanki.Package(deck).write_to_file(out_path)
        size = out_path.stat().st_size

        rows.append(
            {
                "sid": sec["sid"],
                "num": sec["num"],
                "title": sec["title"],
                "count": count,
                "filename": filename,
                "size": size,
                "deck_id": did,
            }
        )
        print(
            f"  {sec['sid']}  {count:>3} cards  -> {filename}"
            f"  ({human_size(size)})  deck_id={did}"
        )

    # Combined package: every non-empty section as a sub-deck.
    all_filename = "certiq-all-sections.apkg"
    all_path = DOWNLOADS_DIR / all_filename
    if all_decks:
        genanki.Package(all_decks).write_to_file(all_path)
    else:
        # No questions anywhere yet: still emit a valid (empty) package so the
        # download page has something to point at and the build never breaks.
        placeholder = genanki.Deck(stable_id(DECK_ROOT), DECK_ROOT)
        genanki.Package(placeholder).write_to_file(all_path)
    all_size = all_path.stat().st_size
    all_row = {"filename": all_filename, "count": total_cards, "size": all_size}

    print("\nCombined:")
    print(
        f"      {total_cards:>3} cards  -> {all_filename}"
        f"  ({human_size(all_size)})"
    )

    write_flashcards_mdx(rows, all_row)

    print("\nOutputs:")
    for r in rows:
        print(f"  {DOWNLOADS_DIR / r['filename']}  ({human_size(r['size'])})")
    print(f"  {all_path}  ({human_size(all_size)})")
    print(f"  {FLASHCARDS_MDX}")

    non_empty = len(rows)
    print(
        f"\nSummary: {total_cards} cards across {non_empty} non-empty section(s); "
        f"{len(sections) - non_empty} empty section(s) skipped; "
        f"{non_empty + 1} package(s) written."
    )


if __name__ == "__main__":
    main()
