# Figures for s5-q052: feed-forward on a mid-circuit measurement, sampled with
# runtime SamplerV2 on a seeded AerSimulator (local testing mode).
# MUST mirror the proof script's variant definitions (ledger rule:
# figure variants == proof variants). COUNTS is asserted in both files so a
# stack bump fails loudly instead of silently redrawing the figure.
# Runs under pipeline/render_figures.py's deterministic prelude.
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2

COUNTS = {"10": 195, "01": 205}

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.measure(0, 0)
with qc.if_test((qc.clbits[0], 0)):
    qc.x(1)
qc.measure(1, 1)

sampler = SamplerV2(mode=AerSimulator())
sampler.options.simulator.seed_simulator = 21
bits = sampler.run([qc], shots=400).result()[0].data.c
assert bits.get_counts() == COUNTS, f"sampler drift: {bits.get_counts()}"
n0, n1 = COUNTS["10"], COUNTS["01"]   # shots where c[0] read 0 / read 1

VARIANTS = {
    # A: condition value ignored — X fires when c[0] is 1.
    "A": {"00": n0, "11": n1},
    # B: the if block read as an ordinary block — X on every shot.
    "B": {"10": n0, "11": n1},
    # C: no feed-forward — the if block believed to be skipped by the Sampler.
    "C": {"00": n0, "01": n1},
    # D: bit order reversed — c[0] printed as the LEFT character.
    "D": {"01": n0, "10": n1},
    # E: the stem's run.
    "E": bits.get_counts(),
}

for key, counts in VARIANTS.items():
    plot_histogram(counts).savefig(f"s5-q052-{key}.svg")
