# Figure for s6-q054: a 1000-shot two-qubit histogram from a seeded
# StatevectorSampler run. The proof script rebuilds the same run and asserts
# the same COUNTS literal before estimating <ZZ> from it — keep the two in
# sync (ledger rule: figure content == proof target). The assert is the sync check.
# Runs under pipeline/render_figures.py's deterministic prelude.
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram

COUNTS = {"00": 569, "01": 71, "10": 121, "11": 239}

qc = QuantumCircuit(2)
qc.ry(1.2, 0)
qc.cx(0, 1)
qc.ry(0.9, 1)
qc.measure_all()
counts = StatevectorSampler(seed=11).run([qc], shots=1000).result()[0].data.meas.get_counts()
assert counts == COUNTS, counts

plot_histogram(counts).savefig("s6-q054-stem.svg")
