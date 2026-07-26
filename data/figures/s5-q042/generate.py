# Figures for s5-q042: plot_histogram renderings of a seeded three-angle
# SamplerV2 sweep — one figure per candidate reading of `bits.get_counts(2)`.
# The proof script reruns THE SAME sweep with the same seed and compares the
# drawn bars — keep the two definitions in sync (ledger rule: figure variants
# == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

BACKEND = FakeManilaV2()
PM = generate_preset_pass_manager(optimization_level=1, backend=BACKEND,
                                  seed_transpiler=42)
ANGLES = np.array([[np.pi / 6], [np.pi / 2], [5 * np.pi / 6]])


def swept_bits():
    theta = Parameter("theta")
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    qc.measure_all()
    sampler = SamplerV2(mode=BACKEND)
    sampler.options.simulator.seed_simulator = 55
    result = sampler.run([(PM.run(qc), ANGLES)], shots=2000).result()
    return result[0].data.meas


BITS = swept_bits()

VARIANTS = {
    "A": BITS.get_counts(0),   # the first bound angle
    "B": BITS.get_counts(1),   # the middle bound angle
    "C": BITS.get_counts(),    # no index at all: every parameter set pooled
    "D": BITS.get_counts(2),   # the stem code, verbatim
    # E — the two outcome labels read the wrong way round
    "E": {("1" if k == "0" else "0"): v for k, v in BITS.get_counts(2).items()},
}

for key, counts in VARIANTS.items():
    fig = plot_histogram(counts)
    fig.savefig(f"s5-q042-{key}.svg")
