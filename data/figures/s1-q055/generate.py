# Figures for s1-q055: mpl drawings of four one-qubit two-gate circuits, one
# of which is what `qc.inverse()` returns for the stem circuit (h, then s).
# The proof script builds THE SAME four circuits and compares each with the
# real `qc.inverse()` (gate list AND unitary) — keep the two definitions in
# sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit

VARIANTS = {
    "A": ("h", "sdg"),  # each gate inverted, order NOT reversed
    "B": ("s", "h"),    # order reversed, S NOT inverted (treated as self-inverse)
    "C": ("sdg", "h"),  # the real qc.inverse(): reversed AND inverted
    "D": ("h", "s"),    # unchanged circuit (both gates assumed self-inverse)
}


def circuit(names):
    qc = QuantumCircuit(1)
    for n in names:
        getattr(qc, n)(0)
    return qc


# Sync check: the keyed variant must be exactly what inverse() produces.
stem = QuantumCircuit(1)
stem.h(0)
stem.s(0)
assert tuple(i.operation.name for i in stem.inverse().data) == VARIANTS["C"]

for key, names in VARIANTS.items():
    fig = circuit(names).draw(output="mpl")
    fig.savefig(f"s1-q055-{key}.svg")
