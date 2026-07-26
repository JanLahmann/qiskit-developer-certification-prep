# Figures for s5-q040: plot_histogram renderings of the counts the stem's
# seeded SamplerV2 run produces, plus four misconception variants. The proof
# script builds THE SAME five counts dicts (same seeds, same circuits) and
# compares the drawn bars — keep the two definitions in sync (ledger rule:
# figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

BACKEND = FakeManilaV2()
PM = generate_preset_pass_manager(optimization_level=1, backend=BACKEND,
                                  seed_transpiler=42)


def sampled(*gates):
    """Counts from a seeded 2000-shot SamplerV2 run of a 3-qubit circuit."""
    qc = QuantumCircuit(3)
    for name, *args in gates:
        getattr(qc, name)(*args)
    qc.measure_all()
    sampler = SamplerV2(mode=BACKEND)
    sampler.options.simulator.seed_simulator = 123
    result = sampler.run([PM.run(qc)], shots=2000).result()
    return result[0].data.meas.get_counts()


def stem_counts():  # C — the stem code, verbatim
    return sampled(("h", 0), ("cx", 0, 1), ("x", 2))


VARIANTS = {
    # A — a fake backend read as a noiseless simulator
    "A": {"100": 1000, "111": 1000},
    # B — the bitstring read left-to-right as q0 q1 q2
    "B": {k[::-1]: v for k, v in stem_counts().items()},
    "C": stem_counts(),
    # D — cx control and target swapped, so nothing gets entangled
    "D": sampled(("h", 0), ("cx", 1, 0), ("x", 2)),
    # E — the x on qubit 2 forgotten
    "E": sampled(("h", 0), ("cx", 0, 1)),
}

for key, counts in VARIANTS.items():
    fig = plot_histogram(counts)
    fig.savefig(f"s5-q040-{key}.svg")
