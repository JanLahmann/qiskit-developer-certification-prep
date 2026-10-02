# Figures for s7-q047: plot_histogram of a retrieved Sampler result's
# get_int_counts(), plus three misconception readings of the same shots
# (retrieval rebuilt offline with a seeded StatevectorSampler run).
# MUST mirror the proof script's variant definitions (ledger rule:
# figure variants == proof variants). COUNTS is asserted in both files.
# Runs under pipeline/render_figures.py's deterministic prelude.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram

COUNTS = {"001": 310, "110": 604, "100": 86}

amp = np.zeros(8)
amp[1], amp[4], amp[6] = np.sqrt(0.3), np.sqrt(0.1), np.sqrt(0.6)
qc = QuantumCircuit(3)
qc.initialize(amp)
qc.measure_all()
bits = StatevectorSampler(seed=2).run([qc], shots=1000).result()[0].data.meas
assert bits.get_counts() == COUNTS, bits.get_counts()

counts = bits.get_counts()
VARIANTS = {
    # A: integer read with the LEFTMOST character as bit 0.
    "A": {int(k[::-1], 2): v for k, v in counts.items()},
    # B: get_int_counts believed to keep the bitstring keys.
    "B": counts,
    # C: integer read as the number of 1 bits in the outcome.
    "C": {w: sum(v for k, v in counts.items() if k.count("1") == w)
          for w in sorted({k.count("1") for k in counts})},
    # D: the stem's call.
    "D": bits.get_int_counts(),
}

for key, c in VARIANTS.items():
    plot_histogram(c).savefig(f"s7-q047-{key}.svg")
