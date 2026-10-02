# Figure for s7-q048: counts of a noisy 1000-shot Sampler job (rebuilt offline:
# FakeManilaV2, seeded transpile + seeded simulator). The proof script runs the
# SAME circuit with the same seeds and asserts the same COUNTS literal — keep
# the two in sync (ledger rule: figure content == proof target).
# Runs under pipeline/render_figures.py's deterministic prelude.
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

COUNTS = {"100": 443, "101": 429, "001": 58, "000": 62, "111": 2, "011": 1, "110": 5}

qc = QuantumCircuit(3)
qc.x(2)
qc.h(0)
qc.measure_all()

backend = FakeManilaV2()
pm = generate_preset_pass_manager(optimization_level=1, backend=backend, seed_transpiler=42)
sampler = SamplerV2(mode=backend)
sampler.options.simulator.seed_simulator = 17
counts = sampler.run([pm.run(qc)], shots=1000).result()[0].data.meas.get_counts()
assert counts == COUNTS, counts

plot_histogram(counts).savefig("s7-q048-stem.svg")
