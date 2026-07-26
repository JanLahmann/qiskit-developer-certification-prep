# Figures for s2-q042: plot_bloch_multivector renderings of the stem state and
# four misconception variants. The proof script builds THE SAME five states and
# compares the per-sphere Bloch vectors — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.visualization import plot_bloch_multivector


def state(*gates):
    qc = QuantumCircuit(2)
    for name, *args in gates:
        getattr(qc, name)(*args)
    return Statevector(qc)


def stem_state():  # D — the stem code, verbatim
    return state(("h", 0), ("s", 0), ("x", 1))


VARIANTS = {
    "A": state(("h", 0), ("x", 1)),              # the S gate treated as a no-op
    "B": state(("h", 0), ("s", 0)),              # the X gate forgotten
    "C": state(("h", 1), ("s", 1), ("x", 0)),    # spheres read in ket order
    "D": stem_state(),
    "E": partial_trace(stem_state(), [1]),       # one sphere for a 2-qubit state
}

for key, st in VARIANTS.items():
    fig = plot_bloch_multivector(st)
    fig.savefig(f"s2-q042-{key}.svg")
