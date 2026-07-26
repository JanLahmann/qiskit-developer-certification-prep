# Figures for s2-q046: q-sphere renderings of the stem state and four
# misconception states. The proof script builds THE SAME five states and
# compares the markers each would place on the sphere (bitstring, magnitude,
# relative phase) — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: exact statevectors, no sampling.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere

ANGLE = 2 * np.pi / 3  # cos(ANGLE/2) = 0.5 on |00>, sin(ANGLE/2) = 0.866


def v_even():  # A — angle ignored, an even Bell superposition assumed
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def v_swapped_weights():  # B — cos/sin assignment inverted
    qc = QuantumCircuit(2)
    qc.ry(np.pi / 3, 0)
    qc.cx(0, 1)
    return qc


def v_no_cx():  # C — the entangling gate dropped
    qc = QuantumCircuit(2)
    qc.ry(ANGLE, 0)
    return qc


def v_both_rotated():  # D — rotation applied to both qubits, no entanglement
    qc = QuantumCircuit(2)
    qc.ry(ANGLE, 0)
    qc.ry(ANGLE, 1)
    return qc


def v_correct():  # E — the stem code, verbatim
    qc = QuantumCircuit(2)
    qc.ry(ANGLE, 0)
    qc.cx(0, 1)
    return qc


VARIANTS = {
    "A": v_even,
    "B": v_swapped_weights,
    "C": v_no_cx,
    "D": v_both_rotated,
    "E": v_correct,
}

for key, make in VARIANTS.items():
    fig = plot_state_qsphere(Statevector(make()))
    fig.savefig(f"s2-q046-{key}.svg")
