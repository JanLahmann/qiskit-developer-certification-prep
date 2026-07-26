# Figures for s1-q052: plot_state_city renderings of the stem state and four
# misconception variants. The proof script builds THE SAME five states and
# compares the drawn density matrices cell by cell — keep the two definitions
# in sync (ledger rule: figure variants == proof variants).
# plot_state_city draws on mplot3d axes, so the question sets
# figures.platform_sensitive.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_city


def state(*gates):
    qc = QuantumCircuit(2)
    for name, *args in gates:
        getattr(qc, name)(*args)
    return Statevector(qc)


def stem_state():  # B — the stem code, verbatim
    return state(("h", 0), ("cx", 0, 1), ("s", 1))


VARIANTS = {
    "A": state(("h", 0), ("cx", 0, 1), ("sdg", 1)),  # S mistaken for S-dagger
    "B": stem_state(),
    "C": state(("h", 0), ("cx", 0, 1), ("z", 1)),    # quarter turn read as a half turn
    "D": state(("h", 0), ("h", 1), ("s", 1)),        # entanglement dropped
    "E": state(("h", 0), ("cx", 0, 1)),              # the phase treated as global
}

for key, st in VARIANTS.items():
    fig = plot_state_city(st)
    fig.savefig(f"s1-q052-{key}.svg")
