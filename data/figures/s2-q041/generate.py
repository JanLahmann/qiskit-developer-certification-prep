# Figures for s2-q041: plot_histogram renderings of the stem counts and four
# misconception variants. The proof script builds THE SAME five counts dicts
# and reads the bar labels/heights back off the rendered figures — keep the two
# definitions in sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: the counts come from Statevector probabilities scaled to a fixed
# shot budget — nothing is sampled.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram


def stem_counts():  # B — the stem code, verbatim
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(2)
    sv = Statevector(qc)
    return {str(k): round(v * 800) for k, v in sv.probabilities_dict().items()}


VARIANTS = {
    "A": {"001": 400, "111": 400},          # bitstrings read big-endian
    "B": stem_counts(),
    "C": {"000": 400, "011": 400},          # the X on qubit 2 forgotten
    "D": {"100": 200, "101": 200,           # the CX correlation dropped
          "110": 200, "111": 200},
    "E": {"100": 566, "111": 566},          # amplitudes used as counts
}

for key, counts in VARIANTS.items():
    fig = plot_histogram(counts)
    fig.savefig(f"s2-q041-{key}.svg")
