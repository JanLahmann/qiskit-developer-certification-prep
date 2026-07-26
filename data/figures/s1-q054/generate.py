# Figures for s1-q054: plot_bloch_multivector renderings of the stem circuit
# and four misconception circuits. The proof script builds THE SAME five
# circuits and reduces each to the pair of Bloch vectors the drawer receives —
# keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: exact statevectors, no sampling. 3D axes -> the question sets
# platform_sensitive: true (SVG path decimals differ across OSes).
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector


def v_product_plus_zero():  # A — H alone, no entanglement
    qc = QuantumCircuit(2)
    qc.h(0)
    return qc


def v_partially_entangled():  # B — a shallow rotation before the CX
    qc = QuantumCircuit(2)
    qc.ry(np.pi / 3, 0)
    qc.cx(0, 1)
    return qc


def v_correct():  # C — the stem code, verbatim (Bell pair)
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def v_both_plus():  # D — H on each qubit, a product of two |+> states
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.h(1)
    return qc


def v_computational():  # E — a plain computational-basis product state
    qc = QuantumCircuit(2)
    qc.x(1)
    return qc


VARIANTS = {
    "A": v_product_plus_zero,
    "B": v_partially_entangled,
    "C": v_correct,
    "D": v_both_plus,
    "E": v_computational,
}

for key, make in VARIANTS.items():
    fig = plot_bloch_multivector(Statevector(make()))
    fig.savefig(f"s1-q054-{key}.svg")
