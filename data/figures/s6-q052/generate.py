# Figure for s6-q052: an exact estimator sweep of a two-qubit correlator.
# The proof script runs every candidate observable through the same sweep and
# compares with TARGET — keep the two in sync (ledger rule: figure content ==
# proof target). The assert is the sync check.
# Runs under pipeline/render_figures.py's deterministic prelude.
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

# What the drawing shows: nine marker heights, in angle order.
TARGET = (0.0, 0.707, 1.0, 0.707, 0.0, -0.707, -1.0, -0.707, -0.0)

theta = Parameter("theta")
qc = QuantumCircuit(2)
qc.ry(theta, 0)
qc.cx(0, 1)

angles = np.linspace(0, 2 * np.pi, 9)
obs = SparsePauliOp("XX")
evs = StatevectorEstimator().run([(qc, obs, angles.reshape(-1, 1))]).result()[0].data.evs
assert tuple(np.round(evs, 3)) == TARGET, tuple(np.round(evs, 3))

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(angles, evs, marker="o")
ax.set_xlabel("theta")
ax.set_ylabel("expectation value")
ax.set_ylim(-1.1, 1.1)
ax.axhline(0.0, color="black", linewidth=0.8)
fig.savefig("s6-q052-stem.svg")
