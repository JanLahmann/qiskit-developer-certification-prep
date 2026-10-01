# Stem figure for s5-q049: histogram of a seeded 1000-shot StatevectorSampler
# run. The proof hardcodes the SAME COUNTS literal (ledger rule: figure content
# == proof target); the assert below fails the render on drift.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram

COUNTS = {"00": 175, "01": 555, "10": 73, "11": 197}

qc = QuantumCircuit(2)
qc.ry(2 * np.pi / 3, 0)
qc.ry(np.pi / 3, 1)
qc.measure_all()
counts = StatevectorSampler(seed=1).run([qc], shots=1000).result()[0].data.meas.get_counts()
assert counts == COUNTS, counts
plot_histogram(counts).savefig("s5-q049-stem.svg")
