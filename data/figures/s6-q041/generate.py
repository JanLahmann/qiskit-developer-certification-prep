# Figure for s6-q041: the error-bar plot the stem code draws when the missing
# options line sets default_precision to 0.1. The proof script applies each
# candidate options line to the same seeded run and compares what it gets
# against the TARGET arrays below — keep the two definitions in sync (ledger
# rule: figure content == proof target). The asserts are the sync check.
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

# What the drawing shows: the marker heights and the error-bar half-lengths.
TARGET_EVS = (0.92, 0.48, -0.32, -0.92)
TARGET_STDS = (0.039, 0.088, 0.095, 0.039)

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
estimator.options.simulator.seed_simulator = 7
estimator.options.default_precision = 0.1
pub_result = estimator.run([(isa, obs, ANGLES)]).result()[0]

evs = np.asarray(pub_result.data.evs)
stds = np.asarray(pub_result.data.stds)
assert tuple(np.round(evs, 3)) == TARGET_EVS, tuple(np.round(evs, 3))
assert tuple(np.round(stds, 3)) == TARGET_STDS, tuple(np.round(stds, 3))

fig, ax = plt.subplots(figsize=(6, 4))
ax.errorbar(ANGLES.ravel(), evs, yerr=stds, fmt="o-", capsize=4)
ax.set_xlabel("theta")
ax.set_ylabel("expectation value")
fig.savefig("s6-q041-stem.svg")
