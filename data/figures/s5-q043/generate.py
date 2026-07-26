# Figures for s5-q043: plot_histogram renderings of one seeded SamplerV2 run,
# drawn once as the real `number_to_keep=3` call and four times from
# misconception count dictionaries. The proof script re-runs THE SAME seeded
# sampler and reads the bars back off the axes for every variant — keep the two
# definitions in sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: options.simulator.seed_simulator makes the fake-backend run
# reproducible across processes (ledger, 2026-07-26); the assert below fails
# loudly if the pinned stack ever produces different counts.
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

KEEP = 3
COUNTS = {"000": 188, "111": 150, "011": 20, "100": 14, "110": 12,
          "101": 6, "001": 6, "010": 4}


def sampled_counts():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure_all()
    backend = FakeManilaV2()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend,
                                      seed_transpiler=42)
    sampler = SamplerV2(mode=backend)
    sampler.options.simulator.seed_simulator = 11
    result = sampler.run([pm.run(qc)], shots=400).result()
    return result[0].data.meas.get_counts()


counts = sampled_counts()
assert counts == COUNTS, f"sampler drift: {counts}"

ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
kept = dict(ranked[:KEEP])
dropped = dict(ranked[KEEP:])
rest = sum(dropped.values())

# A — number_to_keep read as a plain truncation: the discarded outcomes vanish.
v_a = dict(kept)
# C — the rest bar read as "how many outcomes were folded away" (5), not their
#     total count (42).
v_c = {**kept, "rest": len(dropped)}
# D — off-by-one: only k - 1 outcomes kept, the rest bar absorbing one more.
v_d = {**dict(ranked[:KEEP - 1]), "rest": sum(v for _, v in ranked[KEEP - 1:])}
# E — number_to_keep believed to affect only sorting, so nothing is folded.
v_e = dict(counts)

plot_histogram(v_a).savefig("s5-q043-A.svg")
plot_histogram(counts, number_to_keep=KEEP).savefig("s5-q043-B.svg")
plot_histogram(v_c).savefig("s5-q043-C.svg")
plot_histogram(v_d).savefig("s5-q043-D.svg")
plot_histogram(v_e).savefig("s5-q043-E.svg")
