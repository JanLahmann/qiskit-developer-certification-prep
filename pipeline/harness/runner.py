"""Execute-and-prove runner.

Runs a question's proof_script in an isolated subprocess against the
pinned Qiskit environment and validates the emitted verdict against the
question. The verdict contract for proof scripts:

    emit_verdict({
        "answer": ["C"],                # option keys the execution PROVED correct
        "evidence": {"A": "...", ...},  # per-option: observed proof/refutation
        "observed": {...},              # key observed values (JSON-serializable)
    })

Rules enforced here (not trusted from the generator):
- exactly one verdict, valid JSON;
- verdict.answer == question.answer (order-insensitive);
- evidence covers EVERY option key;
- process exits 0 within the timeout.

The artifact written per question records the verdict, stdout/stderr tails,
wall time, and the exact library versions — that artifact is what the site
shows as the question's proof.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
VERDICT_MARK = "###VERDICT###"

PRELUDE = '''\
import json as _json

_QCS_EMITTED = [False]

def emit_verdict(v):
    if _QCS_EMITTED[0]:
        raise RuntimeError("emit_verdict called twice")
    _QCS_EMITTED[0] = True
    print("###VERDICT###" + _json.dumps(v, default=str))

import os as _os
if _os.environ.get("QCS_PATCH_RUNTIME", "1") == "1":
    try:
        from qcs_patch_runtime import apply_patches as _qcs_apply
        _qcs_apply()
    except Exception as _e:
        print("###PATCHWARN### " + repr(_e))

# ---- proof script follows ----
'''

VERSION_SNIPPET = '''\

# ---- appended by runner: record versions ----
def _qcs_versions():
    import importlib.metadata as _md
    out = {}
    for _p in ("qiskit", "qiskit-aer", "qiskit-ibm-runtime", "numpy"):
        try:
            out[_p] = _md.version(_p)
        except Exception:
            pass
    print("###VERSIONS###" + __import__("json").dumps(out))
_qcs_versions()
'''

VERSIONS_MARK = "###VERSIONS###"


@dataclass
class ProofResult:
    ok: bool
    reason: str
    artifact: dict


def _tail(s: str, n: int = 4000) -> str:
    return s if len(s) <= n else "…" + s[-n:]


def run_proof(question: dict, python_bin: str | Path, timeout: int = 180) -> ProofResult:
    qid = question["id"]
    script = PRELUDE + question["verification"]["proof_script"] + VERSION_SNIPPET

    env = dict(os.environ)
    env.update(
        {
            "PYTHONHASHSEED": "0",
            "MPLBACKEND": "Agg",
            "QCS_PATCH_RUNTIME": "1",
            "PYTHONPATH": str(HARNESS_DIR),
            # Belt and braces: make accidental network use fail fast.
            "QISKIT_IBM_TOKEN": "",
            "NO_PROXY": "*",
        }
    )

    with tempfile.TemporaryDirectory(prefix=f"qcs-{qid}-") as td:
        script_path = Path(td) / f"proof_{qid.replace('-', '_')}.py"
        script_path.write_text(script)
        t0 = time.monotonic()
        try:
            proc = subprocess.run(
                [str(python_bin), str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                cwd=td,
            )
        except subprocess.TimeoutExpired as e:
            return ProofResult(
                False,
                f"timeout after {timeout}s",
                _artifact(qid, None, {}, _tail(e.stdout or ""), _tail(e.stderr or ""), timeout, -1),
            )
        wall = time.monotonic() - t0

    stdout, stderr = proc.stdout, proc.stderr

    verdict = None
    versions: dict = {}
    for line in stdout.splitlines():
        if line.startswith(VERDICT_MARK):
            if verdict is not None:
                return ProofResult(False, "multiple verdicts", _artifact(qid, None, versions, _tail(stdout), _tail(stderr), wall, proc.returncode))
            try:
                verdict = json.loads(line[len(VERDICT_MARK):])
            except json.JSONDecodeError:
                return ProofResult(False, "verdict is not valid JSON", _artifact(qid, None, versions, _tail(stdout), _tail(stderr), wall, proc.returncode))
        elif line.startswith(VERSIONS_MARK):
            try:
                versions = json.loads(line[len(VERSIONS_MARK):])
            except json.JSONDecodeError:
                pass

    artifact = _artifact(qid, verdict, versions, _tail(stdout), _tail(stderr), wall, proc.returncode)

    if proc.returncode != 0:
        return ProofResult(False, f"proof script exited {proc.returncode}", artifact)
    if verdict is None:
        return ProofResult(False, "no verdict emitted", artifact)

    # Validate verdict against the question.
    option_keys = {o["key"] for o in question["options"]}
    v_answer = verdict.get("answer")
    if not isinstance(v_answer, list) or set(v_answer) != set(question["answer"]):
        return ProofResult(
            False,
            f"verdict.answer {v_answer!r} != question.answer {question['answer']!r} — "
            "either the question is wrong or the proof is (both block shipping)",
            artifact,
        )
    evidence = verdict.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != option_keys:
        missing = option_keys - set(evidence or {})
        return ProofResult(False, f"evidence must cover every option; missing {sorted(missing)}", artifact)
    empty = [k for k, val in evidence.items() if not str(val).strip()]
    if empty:
        return ProofResult(False, f"empty evidence for options {empty}", artifact)

    return ProofResult(True, "proven", artifact)


def _artifact(qid, verdict, versions, stdout_tail, stderr_tail, wall, returncode) -> dict:
    return {
        "question": qid,
        "verdict": verdict,
        "versions": versions,
        "wall_seconds": round(wall, 2) if wall >= 0 else None,
        "returncode": returncode,
        "stdout_tail": stdout_tail,
        "stderr_tail": stderr_tail,
        "python": sys.version.split()[0],
    }
