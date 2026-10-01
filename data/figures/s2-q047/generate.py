# Figures for s2-q047: plot_bloch_multivector renderings of the stem state and
# four misconception variants. The proof script builds THE SAME five circuits
# and compares the per-sphere Bloch vectors (direction AND length) — keep the
# two definitions in sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: exact statevectors — nothing is sampled.
import math

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector

T = 2 * math.pi / 3


def state(*gates):
    qc = QuantumCircuit(2)
    for name, *args in gates:
        getattr(qc, name)(*args)
    return Statevector(qc)


VARIANTS = {
    # A — spheres read in printed-ket order: the roles of qubits 0 and 1 swapped.
    "A": state(("ry", T, 1), ("cx", 1, 0), ("h", 0)),
    # B — the stem code, verbatim.
    "B": state(("ry", T, 0), ("cx", 0, 1), ("h", 1)),
    # C — each qubit drawn as a pure state (full-length arrows) despite entanglement.
    "C": state(("x", 0), ("x", 1), ("h", 1)),
    # D — gates read wire by wire, the entangling CX ignored.
    "D": state(("ry", T, 0), ("h", 1)),
    # E — qubit 1's reduced state taken to lean toward |0>, so H sends it to +x.
    "E": state(("ry", T, 0), ("cx", 0, 1), ("x", 1), ("h", 1)),
}

for key, st in VARIANTS.items():
    fig = plot_bloch_multivector(st)
    fig.savefig(f"s2-q047-{key}.svg")
