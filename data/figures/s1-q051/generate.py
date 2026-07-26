# Figure for s1-q051: the plot_bloch_multivector rendering of the state the
# question asks the reader to identify. The proof script compares the SAME
# literal Bloch vectors (TARGET below) against the five candidate gate
# sequences — keep the two definitions in sync (ledger rule: figure content ==
# proof target). The assert below is the sync check: if the drawn state ever
# stops matching TARGET, the render fails instead of drifting silently.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, Statevector, partial_trace
from qiskit.visualization import plot_bloch_multivector

# What the drawing shows, one arrow per sphere: (x, y, z).
TARGET = ((0.0, -1.0, 0.0), (0.0, 0.0, -1.0))


def stem_circuit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.sdg(0)
    qc.x(1)
    return qc


def bloch_vectors(state):
    n = state.num_qubits
    out = []
    for q in range(n):
        rho = partial_trace(state, [i for i in range(n) if i != q])
        out.append(tuple(
            round(float(rho.expectation_value(Pauli(p)).real), 6) for p in "XYZ"
        ))
    return tuple(out)


state = Statevector(stem_circuit())
assert bloch_vectors(state) == TARGET, bloch_vectors(state)

fig = plot_bloch_multivector(state)
fig.savefig("s1-q051-stem.svg")
