# Figures for s5-q048: measurement mapping into one register.
# MUST mirror the proof script's variant definitions (ledger rule:
# figure variants == proof variants). Deterministic: seeded sampler +
# asserted COUNTS; runs under render_figures.py's prelude.
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram

COUNTS = {"101": 191, "100": 209}


def build(pairs):
    qc = QuantumCircuit(3, 3)
    qc.x(0)
    qc.h(1)
    for qubit, clbit in pairs:
        qc.measure(qubit, clbit)
    return qc


def support(qc):
    c = StatevectorSampler(seed=5).run([qc], shots=400).result()[0].data.c.get_counts()
    return sorted(c)


bits = StatevectorSampler(seed=5).run([build([(0, 2), (1, 0)])], shots=400).result()[0].data.c
counts = bits.get_counts()
assert counts == COUNTS, f"sampler drift: {counts}"

# Each misconception keeps the SAME shots (same q1 coin flips), relabelled.
variants = {
    # A: mapping ignored, c[i] taken from q[i] (key = c2 c1 c0 = 0, q1, q0).
    "A": {"0" + k[2] + k[0]: v for k, v in counts.items()},
    # B: register printed with c0 on the left.
    "B": {k[::-1]: v for k, v in counts.items()},
    # C: unmeasured c1 believed absent from the key (c2 c0 only).
    "C": {k[0] + k[2]: v for k, v in counts.items()},
    # D: measure(0, 2) read as (clbit, qubit): q2 -> c0, q0 -> c1.
    "D": {"010": sum(counts.values())},
    # E: the stem's counts.
    "E": dict(counts),
}

for key, c in variants.items():
    plot_histogram(c).savefig(f"s5-q048-{key}.svg")
