"""Community practice-exam parser + validation helpers (CertiQ).

Parses community-authored Qiskit v2.x practice exams (markdown + notebook
formats) into a normalized question schema so their stated answers can be
checked. This script is READ-ONLY over the community raw files under
``data/community/raw/`` and writes normalized JSON to
``data/community/parsed/``.

Normalized question schema (per question):
    {
      "n": int,                 # question number as printed
      "stem": str,              # prose of the question (no options)
      "code": str | null,       # code block that belongs to the stem, if any
      "options": {key: text},   # option key (A/B/...) -> option text/code
      "stated_answer": [key],   # author's stated correct option key(s)
      "has_code": bool          # stem or any option contains code
    }

Only parsing lives here. Execution of extracted snippets is done separately
through the project's offline harness (pipeline/harness), never by importing
or running the community repos.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "community" / "raw"
PARSED = REPO / "data" / "community" / "parsed"

CODE_HINT = re.compile(r"[`(){}\[\]]|qc\.|import |Sampler|Estimator|Pauli|np\.|=")


def _has_code(*parts: str) -> bool:
    blob = "\n".join(p for p in parts if p)
    return "```" in blob or bool(re.search(r"`[^`]+`", blob)) or "qc." in blob


def _norm_answer(raw: str) -> list[str]:
    """Extract option letters from a stated-answer string like 'A, C' or 'C and D'."""
    return [m.upper() for m in re.findall(r"\b([A-Fa-f])\b", raw)]


# --------------------------------------------------------------------------
# notebook helper
# --------------------------------------------------------------------------
def _nb_cells(path: Path) -> list[dict]:
    nb = json.loads(path.read_text())
    out = []
    for c in nb.get("cells", []):
        out.append({"type": c.get("cell_type"), "src": "".join(c.get("source", []))})
    return out


# --------------------------------------------------------------------------
# 1. clausia — practice-exam-1.md  +  answer-key-1.md
# --------------------------------------------------------------------------
def parse_clausia() -> list[dict]:
    text = (RAW / "clausia-practice-exam-1.md").read_text()
    key = (RAW / "clausia-answer-key-1.md").read_text()
    answers = {int(n): _norm_answer(a) for n, a in re.findall(r"^(\d+)\s*[→-]+\s*([a-dA-D, ]+)", key, re.M)}

    blocks = re.split(r"^####\s+(\d+)\.\s*(.*)$", text, flags=re.M)
    questions = []
    # blocks: [pre, n, title, body, n, title, body, ...]
    for i in range(1, len(blocks), 3):
        n = int(blocks[i])
        body = blocks[i + 2]
        body = body.split("\n---")[0]
        opts, stem, code = _split_opts_letter_paren(body)
        questions.append({
            "n": n, "stem": stem.strip(), "code": code,
            "options": opts, "stated_answer": answers.get(n, []),
            "has_code": _has_code(stem, code, *opts.values()),
        })
    return questions


def _split_opts_letter_paren(body: str):
    """Options marked like 'a)' or 'a.' possibly followed by fenced code."""
    lines = body.splitlines()
    opt_start = None
    for idx, ln in enumerate(lines):
        if re.match(r"^\s*[a-eA-E][\)\.]\s", ln) or re.match(r"^\s*[a-eA-E][\)\.]\s*$", ln):
            opt_start = idx
            break
    if opt_start is None:
        return {}, body.strip(), _extract_code(body)
    stem = "\n".join(lines[:opt_start])
    opt_region = "\n".join(lines[opt_start:])
    opts = {}
    # split on option markers at line starts
    parts = re.split(r"^\s*([a-eA-E])[\)\.]\s?", opt_region, flags=re.M)
    for j in range(1, len(parts), 2):
        key = parts[j].upper()
        val = parts[j + 1].strip()
        opts[key] = val
    return opts, stem.strip(), _extract_code(stem)


def _extract_code(stem: str) -> str | None:
    m = re.search(r"```(?:python|qasm)?\n(.*?)```", stem, re.S)
    return m.group(1).strip() if m else None


# --------------------------------------------------------------------------
# 2. vantnprof — Practice.md  (inline answers)
# --------------------------------------------------------------------------
def parse_vantnprof() -> list[dict]:
    text = (RAW / "vantnprof-Practice.md").read_text()
    blocks = re.split(r"^###\s+Question\s+(\d+)\s+of\s+68\s*$", text, flags=re.M)
    questions = []
    for i in range(1, len(blocks), 2):
        n = int(blocks[i])
        body = blocks[i + 1].split("\n---")[0]
        ans_m = re.search(r"\*\*Correct answers?:\*\*\s*([A-D, ]+)", body)
        stated = _norm_answer(ans_m.group(1)) if ans_m else []
        qpart = body.split("<details>")[0]
        opts, stem, code = _split_opts_bold_letter(qpart)
        questions.append({
            "n": n, "stem": stem.strip(), "code": code,
            "options": opts, "stated_answer": stated,
            "has_code": _has_code(stem, code, *opts.values()),
        })
    return questions


def _split_opts_bold_letter(body: str):
    """Options marked '**A.**' each followed by prose or a fenced block."""
    parts = re.split(r"^\*\*([A-E])\.\*\*\s*$", body, flags=re.M)
    stem = parts[0].strip()
    opts = {}
    for j in range(1, len(parts), 2):
        key = parts[j].upper()
        val = parts[j + 1].strip()
        opts[key] = val
    return opts, stem, _extract_code(stem)


# --------------------------------------------------------------------------
# 3. kurian — practice_exam_1.md  +  solutions/answer_key
# --------------------------------------------------------------------------
def parse_kurian() -> list[dict]:
    text = (RAW / "kurian-practice_exam_1.md").read_text()
    key = (RAW / "kurian-answer_key_1.md").read_text()
    answers = {}
    for n, a in re.findall(r"^Question\s+(\d+):\s*([A-D and,]+?)\s*$", key, re.M):
        answers[int(n)] = _norm_answer(a)

    blocks = re.split(r"^\*\*Question:?\s*(\d+)[:\*]", text, flags=re.M)
    questions = []
    for i in range(1, len(blocks), 2):
        n = int(blocks[i])
        body = blocks[i + 1]
        # strip leading '**' / ':' remnants
        body = re.sub(r"^[:\*]+", "", body).strip()
        opts, stem, code = _split_opts_circle(body)
        questions.append({
            "n": n, "stem": stem.strip(), "code": code,
            "options": opts, "stated_answer": answers.get(n, []),
            "has_code": _has_code(stem, code, *opts.values()),
        })
    return questions


def _split_opts_circle(body: str):
    """Options marked '○ A.' or bare 'A.' (kurian Q11)."""
    lines = body.splitlines()
    opt_start = None
    for idx, ln in enumerate(lines):
        if re.match(r"^\s*(○\s*)?[A-E]\.\s", ln):
            opt_start = idx
            break
    if opt_start is None:
        return {}, body, _extract_code(body)
    stem = "\n".join(lines[:opt_start])
    region = "\n".join(lines[opt_start:])
    opts = {}
    parts = re.split(r"^\s*(?:○\s*)?([A-E])\.\s", region, flags=re.M)
    for j in range(1, len(parts), 2):
        opts[parts[j].upper()] = parts[j + 1].strip()
    return opts, stem, _extract_code(stem)


# --------------------------------------------------------------------------
# 4. algovista — 25_Practice_Questions.md  (inline key + explanations)
# --------------------------------------------------------------------------
def parse_algovista() -> list[dict]:
    text = (RAW / "algovista-25_Practice_Questions.md").read_text()
    body, _, keypart = text.partition("## Complete Answer Key")
    answers = {}
    for n, a in re.findall(r"^###\s+(\d+)\.\s+Correct Answers?:\s*([A-D, ]+)", keypart, re.M):
        answers[int(n)] = _norm_answer(a)

    blocks = re.split(r"^###\s+(\d+)\.\s+(.*)$", body, flags=re.M)
    questions = []
    for i in range(1, len(blocks), 3):
        n = int(blocks[i])
        title = blocks[i + 1]
        rest = blocks[i + 2].split("\n---")[0]
        full = title + "\n" + rest
        opts, stem, code = _split_opts_letter_dot(full)
        questions.append({
            "n": n, "stem": stem.strip(), "code": code,
            "options": opts, "stated_answer": answers.get(n, []),
            "has_code": _has_code(stem, code, *opts.values()),
        })
    return questions


def _split_opts_letter_dot(body: str):
    """Options marked '^A.' each followed by prose or a fenced block."""
    parts = re.split(r"^([A-E])\.\s", body, flags=re.M)
    stem = parts[0].strip()
    opts = {}
    for j in range(1, len(parts), 2):
        opts[parts[j].upper()] = parts[j + 1].strip()
    return opts, stem, _extract_code(stem)


# --------------------------------------------------------------------------
# 5. rishihg — mock_exam.md  (inline grid key)
# --------------------------------------------------------------------------
def parse_rishihg() -> list[dict]:
    text = (RAW / "rishihg-mock_exam.md").read_text()
    body, _, keypart = text.partition("## Answer Key")
    answers = {int(n): [a.upper()] for n, a in re.findall(r"(\d+)\.\s*([A-D])\b", keypart)}

    blocks = re.split(r"^##\s+Question\s+(\d+)\s*$", body, flags=re.M)
    questions = []
    for i in range(1, len(blocks), 2):
        n = int(blocks[i])
        chunk = blocks[i + 1].split("\n---")[0]
        opts, stem, code = _split_opts_dash_letter(chunk)
        questions.append({
            "n": n, "stem": stem.strip(), "code": code,
            "options": opts, "stated_answer": answers.get(n, []),
            "has_code": _has_code(stem, code, *opts.values()),
        })
    return questions


def _split_opts_dash_letter(body: str):
    """Options marked '- A)' (rishihg / algovista list style)."""
    parts = re.split(r"^-\s*([A-E])\)\s*", body, flags=re.M)
    stem = parts[0].strip()
    opts = {}
    for j in range(1, len(parts), 2):
        opts[parts[j].upper()] = parts[j + 1].strip()
    return opts, stem, _extract_code(stem)


# --------------------------------------------------------------------------
# 6. qbees — Qiskit-Practice-Exam.ipynb  (one markdown cell per question)
# --------------------------------------------------------------------------
def parse_qbees() -> list[dict]:
    cells = _nb_cells(RAW / "qbees-Qiskit-Practice-Exam.ipynb")
    questions = []
    for c in cells:
        if c["type"] != "markdown":
            continue
        m = re.match(r"\s*\*\*Q(\d+)\*\*", c["src"])
        if not m:
            continue
        n = int(m.group(1))
        src = c["src"]
        ans_m = re.search(r"\*\*Answer\*\*:\s*([A-D])", src)
        stated = [ans_m.group(1).upper()] if ans_m else []
        qbody = src[: ans_m.start()] if ans_m else src
        qbody = re.sub(r"^\s*\*\*Q\d+\*\*\s*", "", qbody)
        # options are '- A\n text' blocks
        parts = re.split(r"^-\s*([A-D])\s*$", qbody, flags=re.M)
        stem = parts[0].strip()
        opts = {}
        for j in range(1, len(parts), 2):
            opts[parts[j].upper()] = parts[j + 1].strip()
        questions.append({
            "n": n, "stem": stem, "code": _extract_code(stem),
            "options": opts, "stated_answer": stated,
            "has_code": _has_code(stem, *opts.values()),
        })
    return sorted(questions, key=lambda q: q["n"])


# --------------------------------------------------------------------------
# 7. marcobarroca — qiskit_v2_mock_exam.ipynb  (Q cell + answer cell)
# --------------------------------------------------------------------------
def parse_marcobarroca() -> list[dict]:
    cells = _nb_cells(RAW / "marcobarroca-qiskit_v2_mock_exam.ipynb")
    md = [c["src"] for c in cells if c["type"] == "markdown"]
    questions = []
    for idx, src in enumerate(md):
        m = re.match(r"###\s+Question\s+(\d+)\b", src.strip())
        if not m:
            continue
        n = int(m.group(1))
        # find following answer cell
        stated = []
        for k in range(idx + 1, min(idx + 4, len(md))):
            am = re.search(r"\*\*Answer:\*\*\s*([A-F, ]+)", md[k])
            if am:
                stated = _norm_answer(am.group(1))
                break
        qbody = re.sub(r"^###\s+Question\s+\d+\s*", "", src.strip())
        parts = re.split(r"^-\s*(?:\[[ xX]\]\s*)?\*\*([A-F])\.\*\*\s*", qbody, flags=re.M)
        stem = parts[0].strip()
        opts = {}
        for j in range(1, len(parts), 2):
            opts[parts[j].upper()] = parts[j + 1].strip()
        questions.append({
            "n": n, "stem": stem, "code": _extract_code(stem),
            "options": opts, "stated_answer": stated,
            "has_code": _has_code(stem, *opts.values()),
        })
    return questions


# ==========================================================================
# PASS 2 parsers (2026-07-25)
# ==========================================================================

def _strip_fenced(text: str) -> list[tuple[str, bool]]:
    """Yield (line, in_fence) so splitters can ignore code-fence interiors."""
    out, fence = [], False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            out.append((ln, True))
            fence = not fence
            continue
        out.append((ln, fence))
    return out


def _split_numbered(text: str, pat: str) -> list[tuple[int, str]]:
    """Split a markdown blob on top-level numbered question headers."""
    marks = []
    lines = _strip_fenced(text)
    for idx, (ln, in_fence) in enumerate(lines):
        if in_fence:
            continue
        m = re.match(pat, ln)
        if m:
            marks.append((idx, int(m.group(1))))
    blocks = []
    for j, (idx, n) in enumerate(marks):
        end = marks[j + 1][0] if j + 1 < len(marks) else len(lines)
        body = "\n".join(l for l, _ in lines[idx:end])
        body = re.sub(pat, "", body, count=1)
        blocks.append((n, body))
    return blocks


def _split_opts_generic(body: str, marker: str):
    """Split options where each option starts a line, ignoring fenced code."""
    lines = _strip_fenced(body)
    starts = []
    for idx, (ln, in_fence) in enumerate(lines):
        if in_fence:
            continue
        m = re.match(marker, ln)
        if m:
            starts.append((idx, m.group(1).upper(), m.end()))
    if not starts:
        return {}, body.strip(), _extract_code(body)
    stem = "\n".join(l for l, _ in lines[: starts[0][0]])
    opts = {}
    for j, (idx, key, off) in enumerate(starts):
        end = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        chunk = [lines[idx][0][off:]] + [l for l, _ in lines[idx + 1: end]]
        opts[key] = "\n".join(chunk).strip()
    return opts, stem.strip(), _extract_code(stem)


# --------------------------------------------------------------------------
# 8. lkaucic — questions/section*.yaml (structured bank behind a LaTeX generator)
# --------------------------------------------------------------------------
def parse_lkaucic() -> list[dict]:
    import yaml  # noqa: PLC0415

    questions = []
    n = 0
    for path in sorted(RAW.glob("lkaucic-section*.yaml")):
        for item in yaml.safe_load(path.read_text()) or []:
            n += 1
            code = item.get("code")
            opts = {k.upper(): str(v) for k, v in (item.get("choices") or {}).items()}
            ans = item.get("answer")
            if isinstance(ans, (list, tuple)):
                stated = [str(a).upper() for a in ans]
            else:
                stated = [str(ans).upper()] if ans else []
            questions.append({
                "n": n, "qid": item.get("id"), "section": item.get("section"),
                "stem": str(item.get("question", "")).strip(), "code": code,
                "options": opts, "stated_answer": stated,
                "has_code": bool(code) or _has_code(str(item.get("question", "")), *opts.values()),
                "source_file": path.name,
            })
    return questions


# --------------------------------------------------------------------------
# 9. gnietof — exam1/2/3.md (numbered, 'Show answer key' <details> block)
# --------------------------------------------------------------------------
def parse_gnietof() -> list[dict]:
    questions = []
    for path in sorted(RAW.glob("gnietof-exam*.md")):
        exam = int(re.search(r"exam(\d)", path.name).group(1))
        text = path.read_text()
        body, _, keypart = text.partition("<details>")
        answers = {
            int(n): [c.upper() for c in a]
            for n, a in re.findall(r"^\s*(\d+)\.\s*([A-E]+)\s*<br>", keypart, re.M)
        }
        for n, chunk in _split_numbered(body, r"^\s*(\d+)\.\s+"):
            opts, stem, code = _split_opts_generic(chunk, r"^([A-E])\.(?:\s|$)")
            questions.append({
                "n": n, "exam": exam, "stem": stem, "code": code,
                "options": opts, "stated_answer": answers.get(n, []),
                "has_code": _has_code(stem, code, *opts.values()),
                "source_file": path.name,
            })
    return questions


# --------------------------------------------------------------------------
# 10. adrian-panasiewicz — practice_exam.ipynb (Q cell, option cell, answer cell)
# --------------------------------------------------------------------------
def parse_adrian() -> list[dict]:
    cells = _nb_cells(RAW / "adrian-practice_exam.ipynb")
    md = [c["src"] for c in cells if c["type"] == "markdown"]
    questions, cur, buf = [], None, []

    def flush(nxt):
        nonlocal cur, buf
        if cur is None:
            cur, buf = nxt, []
            return
        n, body = cur, "\n\n".join(buf)
        qpart, _, apart = body.partition("***Answer:***")
        qpart = re.sub(r"\*\*\s*$", "", qpart.splitlines()[0]) + "\n" + "\n".join(qpart.splitlines()[1:])
        stated = _norm_answer_paren(apart)
        opts, stem, code = _split_opts_generic(qpart, r"^([A-E])\)(?:\s|$)")
        questions.append({
            "n": n, "stem": stem, "code": code, "options": opts,
            "stated_answer": stated, "answer_note": apart.strip()[:400],
            "has_code": _has_code(stem, code, *opts.values()),
        })
        cur, buf = nxt, []

    for src in md:
        m = re.match(r"\s*\*\*(\d+)\.\s", src)
        if m:
            flush(int(m.group(1)))
            buf = [re.sub(r"^\s*\*\*\d+\.\s*", "", src, count=1)]
        elif cur is not None and src.strip() != "---":
            buf.append(src)
    flush(None)
    return questions


def _norm_answer_paren(text: str) -> list[str]:
    """Answer letters written 'B)' / 'A), B), C)' inside a <Details> block."""
    inner = text.split("<Details>")[-1].split("<details>")[-1]
    inner = inner.split("```")[0]
    return sorted({m.upper() for m in re.findall(r"\b([A-E])\)", inner)})


# --------------------------------------------------------------------------
# 11. bs-ns — 01-easy / 02-harder notebooks ('## Question N', <details> answer)
# --------------------------------------------------------------------------
def parse_bs_ns() -> list[dict]:
    questions = []
    for path in sorted(RAW.glob("bs-ns-*.ipynb")):
        tier = "easy" if "01" in path.name else "harder"
        for c in _nb_cells(path):
            if c["type"] != "markdown":
                continue
            m = re.match(r"\s*##\s+Question\s+(\d+)\s*$", c["src"].strip().splitlines()[0])
            if not m:
                continue
            n = int(m.group(1))
            src = c["src"]
            am = re.search(r"\*\*Answers?:\s*([A-E, and]+)\*\*", src)
            stated = _norm_answer(am.group(1)) if am else []
            qpart = src.split("<details>")[0]
            qpart = re.sub(r"^\s*##\s+Question\s+\d+\s*", "", qpart, count=1)
            opts, stem, code = _split_opts_generic(qpart, r"^([A-E])\.(?:\s|$)")
            questions.append({
                "n": n, "tier": tier, "stem": stem, "code": code,
                "options": opts, "stated_answer": stated,
                "has_code": _has_code(stem, code, *opts.values()),
                "source_file": path.name,
            })
    return questions


# --------------------------------------------------------------------------
# 12. skupisz — questions.ipynb (one cell per question, final answer-key cell)
# --------------------------------------------------------------------------
def parse_skupisz() -> list[dict]:
    cells = _nb_cells(RAW / "skupisz-questions.ipynb")
    key_src = next((c["src"] for c in cells if c["src"].strip().startswith("Answers:")), "")
    answers = {
        int(n): [c.upper() for c in re.findall(r"[A-E]", a)]
        for n, a in re.findall(r"^\s*(\d+)\)\s*([A-E](?:\s*,\s*[A-E])*)\s*$", key_src, re.M)
    }
    questions = []
    for c in cells:
        if c["type"] != "markdown" or c["src"].strip().startswith("Answers:"):
            continue
        m = re.match(r"\s*(\d+)\.\s", c["src"])
        if not m:
            continue
        n = int(m.group(1))
        body = re.sub(r"^\s*\d+\.\s*", "", c["src"], count=1)
        opts, stem, code = _split_opts_generic(body, r"^([A-E])\)(?:\s|$)")
        questions.append({
            "n": n, "stem": stem, "code": code, "options": opts,
            "stated_answer": answers.get(n, []),
            "has_code": _has_code(stem, code, *opts.values()),
        })
    return sorted(questions, key=lambda q: q["n"])


# --------------------------------------------------------------------------
# 13. manuelesparcia — README.md ('# N.' questions + '# Anwers' key)
# --------------------------------------------------------------------------
def parse_manuelesparcia() -> list[dict]:
    text = (RAW / "manuelesparcia-README.md").read_text()
    body, _, keypart = text.partition("# Anwers")
    answers = {int(n): [a.upper()] for n, a in re.findall(r"^\s*(\d+)\.\s*([A-D])\s*$", keypart, re.M)}
    questions = []
    for n, chunk in _split_numbered(body, r"^#\s*(\d+)\s*\.\s*"):
        chunk = chunk.replace("\\\n", "\n")
        opts, stem, code = _split_opts_generic(chunk, r"^([A-D])\)(?:\s|$)")
        questions.append({
            "n": n, "stem": stem, "code": code, "options": opts,
            "stated_answer": answers.get(n, []),
            "has_code": _has_code(stem, code, *opts.values()),
        })
    return questions


# --------------------------------------------------------------------------
# 14. luke-j-miller — necessary_files/question_df.pkl (1035-row bank)
#
# The bank ships as a pandas pickle. Unpickling arbitrary bytes executes code,
# so it is loaded through a RESTRICTED unpickler that whitelists only the
# pandas/numpy container constructors the file actually references (verified
# first with pickletools.genops, which never executes anything).
# --------------------------------------------------------------------------
_PICKLE_ALLOWLIST = {
    ("pandas.core.frame", "DataFrame"),
    ("pandas.core.internals.managers", "BlockManager"),
    ("pandas._libs.internals", "_unpickle_block"),
    ("numpy.core.multiarray", "_reconstruct"),
    ("numpy", "ndarray"),
    ("numpy", "dtype"),
    ("pandas.core.indexes.base", "_new_Index"),
    ("pandas.core.indexes.base", "Index"),
    ("pandas.core.indexes.range", "RangeIndex"),
    ("builtins", "slice"),
}


def _restricted_load(path: Path):
    import pickle  # noqa: PLC0415

    class _Restricted(pickle.Unpickler):
        def find_class(self, mod, name):
            if (mod, name) not in _PICKLE_ALLOWLIST:
                raise pickle.UnpicklingError(f"blocked global {mod}.{name}")
            return super().find_class(mod, name)

    with path.open("rb") as fh:
        return _Restricted(fh).load()


def parse_luke() -> list[dict]:
    df = _restricted_load(RAW / "luke" / "question_df.pkl")
    keys = ["A", "B", "C", "D"]
    questions = []
    for i, row in enumerate(df.to_dict("records"), start=1):
        opts = {k: str(row[f"Choice_{k}"]).strip() for k in keys if row.get(f"Choice_{k}") is not None}
        correct = str(row["Correct_Answer"]).strip()
        stated = [k for k, v in opts.items() if v == correct]
        if not stated and re.fullmatch(r"[A-D]", correct):
            stated = [correct]
        stem = str(row["Question"]).strip()
        questions.append({
            "n": i, "stem": stem, "code": _extract_code(stem), "options": opts,
            "stated_answer": stated, "answer_text": correct,
            "section": str(row.get("Section", "")), "task": str(row.get("Task", "")),
            "has_code": _has_code(stem, *opts.values()),
        })
    return questions


PARSERS = {
    "clausia": parse_clausia,
    "vantnprof": parse_vantnprof,
    "kurian": parse_kurian,
    "algovista": parse_algovista,
    "rishihg": parse_rishihg,
    "qbees": parse_qbees,
    "marcobarroca": parse_marcobarroca,
    # pass 2
    "lkaucic": parse_lkaucic,
    "gnietof": parse_gnietof,
    "adrian-panasiewicz": parse_adrian,
    "bs-ns": parse_bs_ns,
    "skupisz": parse_skupisz,
    "manuel-esparcia": parse_manuelesparcia,
    "luke-j-miller": parse_luke,
}


def main() -> None:
    PARSED.mkdir(parents=True, exist_ok=True)
    for slug, fn in PARSERS.items():
        qs = fn()
        (PARSED / f"{slug}.json").write_text(json.dumps(qs, indent=2, ensure_ascii=False))
        with_code = sum(1 for q in qs if q["has_code"])
        with_ans = sum(1 for q in qs if q["stated_answer"])
        good_opts = sum(1 for q in qs if len(q["options"]) >= 2)
        print(f"{slug:14s} questions={len(qs):3d} options_ok={good_opts:3d} "
              f"answers={with_ans:3d} code={with_code:3d}")


if __name__ == "__main__":
    main()
