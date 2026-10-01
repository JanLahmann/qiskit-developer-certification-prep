# Figures for s3-q066: mpl renderings of the stem circuit and its misconception
# variants. The proof script builds THE SAME variants (copy of the block below)
# and proves which one matches the stem code — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: fixed angles, no sampling.
QID = "s3-q066"
import numpy as np
from qiskit import QuantumCircuit


def build(kind="if_else"):
    qc = QuantumCircuit(3, 1)
    qc.ry(np.pi / 3, 1)
    qc.measure(1, 0)
    c0 = qc.clbits[0]
    if kind == "if_else":            # the stem code
        with qc.if_test((c0, 0)) as else_:
            qc.cx(0, 2)
        with else_:
            qc.swap(0, 2)
    elif kind == "swapped":          # branch bodies exchanged
        with qc.if_test((c0, 0)) as else_:
            qc.swap(0, 2)
        with else_:
            qc.cx(0, 2)
    elif kind == "no_else":          # else body read as unconditional
        with qc.if_test((c0, 0)):
            qc.cx(0, 2)
        qc.swap(0, 2)
    elif kind == "two_ifs":          # else read as a second, inverted if_test
        with qc.if_test((c0, 0)):
            qc.cx(0, 2)
        with qc.if_test((c0, 1)):
            qc.swap(0, 2)
    return qc


VARIANTS = {
    "A": (lambda: build("swapped"), {}),
    "B": (lambda: build("no_else"), {}),
    "C": (lambda: build("if_else"), {}),
    "D": (lambda: build("two_ifs"), {}),
}

for key, (make, kwargs) in VARIANTS.items():
    fig = make().draw(output="mpl", **kwargs)
    fig.savefig(f"{QID}-{key}.svg")
