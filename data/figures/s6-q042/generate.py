# Figure for s6-q042: the grouped bar chart of a (2, 3) expectation-value array
# produced by one PUB. The proof script submits each candidate pub shape to the
# same estimator and compares the resulting array against the TARGET below —
# keep the two definitions in sync (ledger rule: figure content == proof
# target). The assert is the sync check. Bars are separated by hatch as well as
# shade, so the drawing survives greyscale (color_essential stays false).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

# What the drawing shows: one row of bars per observable, one bar per angle.
TARGET = ((0.866, 0.0, -0.866), (0.5, 1.0, 0.5))

THETA = Parameter("theta")
ANGLES = np.array([[np.pi / 6, np.pi / 2, 5 * np.pi / 6]])
LABELS = ("pi/6", "pi/2", "5pi/6")

qc = QuantumCircuit(1)
qc.ry(THETA, 0)
observables = [[SparsePauliOp("Z")], [SparsePauliOp("X")]]

evs = np.asarray(
    StatevectorEstimator().run([(qc, observables, ANGLES)]).result()[0].data.evs
)
assert tuple(map(tuple, np.round(evs, 3).tolist())) == TARGET, evs.tolist()

fig, ax = plt.subplots(figsize=(6, 4))
x = np.arange(len(LABELS))
width = 0.38
styles = (("0.35", "//"), ("0.75", ".."))
for row, (name, (shade, hatch)) in enumerate(zip(("Z", "X"), styles)):
    ax.bar(x + (row - 0.5) * width, evs[row], width, label=name,
           color=shade, edgecolor="black", hatch=hatch)
ax.set_xticks(x)
ax.set_xticklabels(LABELS)
ax.set_xlabel("theta")
ax.set_ylabel("expectation value")
ax.axhline(0.0, color="black", linewidth=0.8)
ax.legend(title="observable")
fig.savefig("s6-q042-stem.svg")
