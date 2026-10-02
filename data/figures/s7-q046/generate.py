# Figures for s7-q046: histograms of different slices of a (2, 3)-shaped
# BitArray from a parameter-grid Sampler job (rebuilt offline with a seeded
# StatevectorSampler). MUST mirror the proof script's variant definitions
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram

theta = Parameter("theta")
qc = QuantumCircuit(1)
qc.ry(theta, 0)
qc.measure_all()
grid = np.array([[[0.0], [np.pi], [np.pi]],
                 [[np.pi], [0.0], [0.0]]])
bits = StatevectorSampler(seed=8).run([(qc, grid)], shots=100).result()[0].data.meas
assert bits.shape == (2, 3)

VARIANTS = {
    "A": bits[1].get_counts(),                  # the stem's call: row 1, three locations
    "B": bits[:, 1].get_counts(),               # index read as a column
    "C": bits.get_counts(),                     # index ignored: all six locations pooled
    "D": bits[0].get_counts(),                  # index read as 1-based
    "E": bits.reshape(6)[1].get_counts(),       # index read as a flat location number
}
assert VARIANTS["A"] == {"1": 100, "0": 200}, VARIANTS["A"]

for key, counts in VARIANTS.items():
    plot_histogram(counts).savefig(f"s7-q046-{key}.svg")
