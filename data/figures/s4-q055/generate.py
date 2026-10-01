# Figures for s4-q055: one OPTION image per candidate circuit. Each option is
# the mpl drawing of a hand-built 3-qubit circuit (all options hand-built, so
# no option carries transpiler layout labels — ledger "q_0 -> 0" tell).
# The proof builds the SAME variants (keep VARIANTS identical in both files)
# and submits each to SamplerV2 on the directed 3-qubit GenericBackendV2 from
# the stem; only the variant that respects basis, connectivity and direction
# runs.
# Runs under pipeline/render_figures.py's deterministic prelude.
# Determinism: fixed circuits, no sampling.
from math import pi

from qiskit import QuantumCircuit

VARIANTS = {
    "A": [("rz", pi / 2, 0), ("sx", 0), ("cx", 0, 1), ("cx", 2, 1)],
    "B": [("rz", pi / 2, 0), ("sx", 0), ("cx", 0, 1), ("swap", 1, 2)],
    "C": [("rz", pi / 2, 0), ("h", 0), ("cx", 0, 1), ("cx", 1, 2)],
    "D": [("rz", pi / 2, 0), ("sx", 0), ("cx", 0, 1), ("cx", 0, 2)],
    "E": [("rz", pi / 2, 0), ("sx", 0), ("cx", 0, 1), ("cx", 1, 2)],
}


def build(ops):
    qc = QuantumCircuit(3)
    for name, *args in ops:
        getattr(qc, name)(*args)
    qc.measure_all()
    return qc


for key, ops in VARIANTS.items():
    fig = build(ops).draw(output="mpl")
    fig.savefig(f"s4-q055-{key}.svg")
