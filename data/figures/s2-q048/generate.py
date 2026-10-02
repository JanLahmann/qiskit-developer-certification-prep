# Figures for s2-q048: plot_state_city of qubit 0's reduced state after a
# partially entangling preparation, plus three misconception states.
# MUST mirror the proof script's variant definitions (ledger rule:
# figure variants == proof variants) — keep VARIANTS identical in both files.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Deterministic: exact statevector algebra only, no sampling.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Statevector, partial_trace
from qiskit.visualization import plot_state_city

qc = QuantumCircuit(2)
qc.ry(2 * np.pi / 3, 0)
qc.cx(0, 1)
rho0 = partial_trace(Statevector(qc), [1])          # the stem's state

single = QuantumCircuit(1)
single.ry(2 * np.pi / 3, 0)
amps = np.abs(Statevector(qc).data)                  # 0.5 on |00>, 0.866 on |11>

VARIANTS = {
    # A: entanglement ignored — qubit 0 drawn as the pure RY state.
    "A": DensityMatrix(single),
    # B: tracing out read as post-selecting qubit 1 on |0>.
    "B": DensityMatrix.from_label("0"),
    # D: amplitudes put on the diagonal instead of probabilities.
    "D": DensityMatrix(np.diag([amps[0], amps[3]]).astype(complex)),
    # C: the stem's reduced state.
    "C": rho0,
}

# Sync check: the stem state is diag(0.25, 0.75) with no coherences.
assert np.allclose(rho0.data, np.diag([0.25, 0.75])), rho0.data

for key, state in VARIANTS.items():
    plot_state_city(state).savefig(f"s2-q048-{key}.svg")
