# Figure for s7-q038: the expectation-value curve the stem code draws from a
# retrieved estimator job. The proof script rebuilds the same pub result and
# checks which candidate expression yields the plotted series — keep the two
# definitions in sync (ledger rule: figure content == proof target). The assert
# is the sync check.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

# What the drawing shows: the four marker heights, in angle order.
TARGET = (0.97, 0.532, -0.409, -0.885)

THETA = Parameter("theta")
ANGLES = np.array([[0.0], [np.pi / 3], [2 * np.pi / 3], [np.pi]])

qc = QuantumCircuit(1)
qc.ry(THETA, 0)

backend = FakeManilaV2()
pm = generate_preset_pass_manager(optimization_level=1, backend=backend,
                                  seed_transpiler=42)
isa = pm.run(qc)
obs = SparsePauliOp("Z").apply_layout(isa.layout)

estimator = EstimatorV2(mode=backend)
estimator.options.simulator.seed_simulator = 3
estimator.options.default_precision = 0.02
pub_result = estimator.run([(isa, obs, ANGLES)]).result()[0]

evs = np.asarray(pub_result.data.evs)
assert tuple(np.round(evs, 3)) == TARGET, tuple(np.round(evs, 3))

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(ANGLES.ravel(), evs, marker="o")
ax.set_xlabel("theta")
ax.set_ylabel("expectation value")
ax.axhline(0.0, color="black", linewidth=0.8)
fig.savefig("s7-q038-stem.svg")
