# Figure for s1-q067: the STEM figure — plot_state_paulivec of the state built by
# the keyed candidate circuit. The options are candidate circuits (text); the
# proof builds EVERY candidate below, plots it with the same call, reads the bars
# back off the axes and compares them (and the SVG rendering) with this figure.
# SYNC DUTY: keep CANDIDATES, STEM_KEY and TARGET identical in the proof script.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: exact statevector, no sampling.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_paulivec

# Candidate circuits, one per option (gate lists exactly as the options print them).
CANDIDATES = {
    "A": [("z", 1), ("h", 0), ("s", 0)],
    "B": [("x", 0), ("h", 1), ("s", 1)],
    "C": [("x", 1), ("h", 0), ("sdg", 0)],
    "D": [("x", 1), ("h", 0), ("s", 0)],
    "E": [("x", 1), ("s", 0), ("h", 0)],
}
STEM_KEY = "D"

# What the figure shows: Pauli label -> bar height (non-zero bars only).
TARGET = {"II": 1.0, "IY": 1.0, "ZI": -1.0, "ZY": -1.0}


def build(ops):
    qc = QuantumCircuit(2)
    for name, q in ops:
        getattr(qc, name)(q)
    return qc


def bars(fig):
    ax = fig.axes[0]
    labels = [t.get_text() for t in ax.get_xticklabels()]
    heights = [round(float(p.get_height()), 6) for p in ax.patches]
    return dict(zip(labels, heights))


fig = plot_state_paulivec(Statevector(build(CANDIDATES[STEM_KEY])))
assert bars(fig) == TARGET, bars(fig)
fig.savefig("s1-q067-stem.svg")
