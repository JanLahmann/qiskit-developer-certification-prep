# Figures for s1-q053: mpl drawings of five single-qubit three-gate circuits.
# The proof script builds THE SAME five circuits and scores each one with
# Operator.equiv against XGate — keep the two definitions in sync (ledger rule:
# figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit

VARIANTS = {
    "A": ("h", "x", "h"),    # conjugation run the other way -> Z
    "B": ("s", "x", "sdg"),  # conjugation by the phase gate -> Y
    "C": ("z", "h", "z"),    # not a Pauli at all
    "D": ("h", "s", "h"),    # the square root of X
    "E": ("h", "z", "h"),    # the identity H Z H = X
}


def circuit(names):
    qc = QuantumCircuit(1)
    for n in names:
        getattr(qc, n)(0)
    return qc


for key, names in VARIANTS.items():
    fig = circuit(names).draw(output="mpl")
    fig.savefig(f"s1-q053-{key}.svg")
