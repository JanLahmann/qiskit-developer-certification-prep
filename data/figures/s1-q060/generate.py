# Figures for s1-q060: mpl drawings of four single-control X gates that differ
# in control state (filled vs open circle) and in which wire holds the control.
# The proof script builds THE SAME four circuits and compares each with the
# stem circuit (ctrl_state, control wire, target wire, and unitary) — keep the
# two definitions in sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate

# key: (ctrl_state, [control, target])
VARIANTS = {
    "A": (1, [1, 0]),  # ctrl_state ignored: filled dot on q1
    "B": (0, [0, 1]),  # qubit list read target-first: open circle on q0
    "C": (1, [0, 1]),  # both misreadings: filled dot on q0
    "D": (0, [1, 0]),  # the stem code: open circle on q1, target on q0
}


def circuit(ctrl_state, qubits):
    qc = QuantumCircuit(2)
    qc.append(XGate().control(1, ctrl_state=ctrl_state), qubits)
    return qc


for key, (cs, qubits) in VARIANTS.items():
    fig = circuit(cs, qubits).draw(output="mpl")
    fig.savefig(f"s1-q060-{key}.svg")
