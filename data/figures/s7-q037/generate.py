# Figure for s7-q037: the two-series histogram the stem code draws once the
# counts of BOTH pub results are handed to plot_histogram. The proof script
# rebuilds the same two-pub result locally and compares what each candidate
# expression draws against the TARGET below — keep the two definitions in sync
# (ledger rule: figure content == proof target). The assert is the sync check.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

# What the drawing shows: one bar per outcome per series, in label order.
TARGET = {
    "labels": ("00", "01", "10", "11"),
    "bell": (467, 22, 32, 479),
    "single": (492, 496, 10, 2),
}
SHARES = {"bell": (0.47, 0.02, 0.03, 0.48),
          "single": (0.49, 0.5, 0.01, 0.0)}
LABELS = ["bell", "single"]
SHOTS = 1000

BACKEND = FakeManilaV2()
PM = generate_preset_pass_manager(optimization_level=1, backend=BACKEND,
                                  seed_transpiler=42)

bell = QuantumCircuit(2)
bell.h(0)
bell.cx(0, 1)
bell.measure_all()

single = QuantumCircuit(2)
single.h(0)
single.measure_all()

sampler = SamplerV2(mode=BACKEND)
sampler.options.simulator.seed_simulator = 21
result = sampler.run([PM.run(bell), PM.run(single)], shots=SHOTS).result()

series = [result[i].data.meas.get_counts() for i in range(2)]
for name, counts in zip(LABELS, series):
    got = tuple(counts[k] for k in TARGET["labels"])
    assert got == TARGET[name], (name, got)
    # the proof compares the same series as shares of the shot count
    assert tuple(round(v / SHOTS, 2) for v in got) == SHARES[name], (name, got)

fig = plot_histogram(series, legend=LABELS)
fig.savefig("s7-q037-stem.svg")
