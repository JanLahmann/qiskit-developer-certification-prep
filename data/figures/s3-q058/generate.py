# Figures for s3-q058: mpl renderings of the stem circuit and four
# misconception variants of a `for_loop` dynamic circuit. The proof script
# constructs THE SAME five circuits and proves which one matches the stem code
# structurally — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: fixed angle, no sampling.
import numpy as np
from qiskit import QuantumCircuit

ANGLE = np.pi / 4


def v_unrolled():  # A — imagines the body is repeated at build time
    qc = QuantumCircuit(2)
    qc.h(0)
    for _ in range(3):
        qc.rx(ANGLE, 1)
        qc.cx(0, 1)
    return qc


def v_short_body():  # B — only the first statement treated as the body
    qc = QuantumCircuit(2)
    qc.h(0)
    with qc.for_loop(range(3)):
        qc.rx(ANGLE, 1)
    qc.cx(0, 1)
    return qc


def v_swapped_body():  # C — body statements in the other order
    qc = QuantumCircuit(2)
    qc.h(0)
    with qc.for_loop(range(3)):
        qc.cx(0, 1)
        qc.rx(ANGLE, 1)
    return qc


def v_correct():  # D — the stem code, verbatim
    qc = QuantumCircuit(2)
    qc.h(0)
    with qc.for_loop(range(3)):
        qc.rx(ANGLE, 1)
        qc.cx(0, 1)
    return qc


def v_two_iterations():  # E — loop built over range(2)
    qc = QuantumCircuit(2)
    qc.h(0)
    with qc.for_loop(range(2)):
        qc.rx(ANGLE, 1)
        qc.cx(0, 1)
    return qc


VARIANTS = {
    "A": v_unrolled,
    "B": v_short_body,
    "C": v_swapped_body,
    "D": v_correct,
    "E": v_two_iterations,
}

for key, make in VARIANTS.items():
    fig = make().draw(output="mpl")
    fig.savefig(f"s3-q058-{key}.svg")
