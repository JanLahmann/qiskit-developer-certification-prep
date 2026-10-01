# Figures for s5-q045: postselect on a seeded StatevectorSampler run.
# MUST mirror the proof script's variant definitions (ledger rule:
# figure variants == proof variants). Deterministic: seeded sampler +
# asserted COUNTS; runs under render_figures.py's prelude.
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram

COUNTS = {"000": 96, "111": 92, "100": 117, "011": 95}

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.h(2)
qc.measure_all()
bits = StatevectorSampler(seed=3).run([qc], shots=400).result()[0].data.meas
assert bits.get_counts() == COUNTS, f"sampler drift: {bits.get_counts()}"
kept = bits.postselect([2], [0])

variants = {
    # A: index 2 read as the third character of the printed key (that is c0).
    "A": bits.postselect([0], [0]).get_counts(),
    # B: the stem's call.
    "B": kept.get_counts(),
    # C: selection value read as "discard shots whose bit is 0".
    "C": bits.postselect([2], [1]).get_counts(),
    # D: the post-selected bit believed to be dropped from the keys.
    "D": {k[1:]: v for k, v in kept.get_counts().items()},
}

for key, counts in variants.items():
    plot_histogram(counts).savefig(f"s5-q045-{key}.svg")
