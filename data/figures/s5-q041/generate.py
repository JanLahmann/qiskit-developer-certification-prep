# Figures for s5-q041: five renderings of the SAME seeded 40-shot SamplerV2
# result — one per reading of what a BitArray hands back. The proof script
# rebuilds THE SAME five drawings and compares their axes content — keep the
# two definitions in sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

SHOTS = 40
BACKEND = FakeManilaV2()
PM = generate_preset_pass_manager(optimization_level=1, backend=BACKEND,
                                  seed_transpiler=42)


def sampled_bits():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    sampler = SamplerV2(mode=BACKEND)
    sampler.options.simulator.seed_simulator = 9
    return sampler.run([PM.run(qc)], shots=SHOTS).result()[0].data.meas


BITS = sampled_bits()
COUNTS = BITS.get_counts()

# A — the stem code, verbatim: one bar per outcome that actually occurred
fig = plot_histogram(COUNTS)
fig.savefig("s5-q041-A.svg")

# B — the sampler's per-shot record plotted as a shot-by-shot trace
fig, ax = plt.subplots(figsize=(7, 5))
values = [int(b, 2) for b in BITS.get_bitstrings()]
ax.step(range(1, SHOTS + 1), values, where="mid")
ax.set_xlabel("shot")
ax.set_ylabel("outcome")
ax.set_yticks([0, 1, 2, 3])
ax.set_yticklabels(["00", "01", "10", "11"])
fig.savefig("s5-q041-B.svg")

# C — get_int_counts(): the same tallies keyed by integer
fig = plot_histogram({str(k): v for k, v in BITS.get_int_counts().items()})
fig.savefig("s5-q041-C.svg")

# D — counts mistaken for a normalized distribution
fig = plot_histogram({k: round(v / SHOTS, 3) for k, v in COUNTS.items()})
fig.savefig("s5-q041-D.svg")

# E — every representable outcome listed, unseen ones at zero
fig = plot_histogram({k: COUNTS.get(k, 0) for k in ("00", "01", "10", "11")})
fig.savefig("s5-q041-E.svg")
