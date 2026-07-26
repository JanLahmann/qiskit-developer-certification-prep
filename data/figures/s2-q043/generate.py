# Figure for s2-q043: the STEM q-sphere. The question runs backwards — the
# figure is given and the options are gate sequences — so only one SVG is
# rendered, the q-sphere of the sequence keyed C. The proof script builds THE
# SAME five sequences and compares the markers each one would put on the sphere
# (bitstring, magnitude, phase); keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere

SEQUENCES = {
    "A": (("h", 0), ("cx", 0, 1), ("t", 0)),   # T instead of S: phase pi/4
    "B": (("h", 0), ("cx", 0, 1)),             # no phase gate at all: phase 0
    "C": (("h", 0), ("cx", 0, 1), ("s", 0)),   # the figure shown in the stem
    "D": (("h", 0), ("s", 0)),                 # product state, no entanglement
    "E": (("h", 0), ("cx", 0, 1), ("z", 0)),   # Z instead of S: phase pi
}


def state(seq):
    qc = QuantumCircuit(2)
    for name, *args in seq:
        getattr(qc, name)(*args)
    return Statevector(qc)


fig = plot_state_qsphere(state(SEQUENCES["C"]))
fig.savefig("s2-q043-stem.svg")
