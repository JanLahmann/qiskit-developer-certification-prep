# Option figures for s6-q051: bar charts of `evs` for four observables. The
# proof script builds THE SAME five variants (ledger rule: figure variants ==
# proof variants) — keep the VARIANTS definitions in sync.
# Runs under pipeline/render_figures.py's deterministic prelude.
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

LABELS = ["IZ", "ZI", "ZZ", "IX"]


def evs(theta, flip_q1=True, labels=LABELS):
    qc = QuantumCircuit(2)
    qc.ry(theta, 0)
    if flip_q1:
        qc.x(1)
    obs = [SparsePauliOp(l) for l in labels]
    return np.round(np.asarray(StatevectorEstimator().run([(qc, obs)]).result()[0].data.evs), 3)


VARIANTS = {
    "A": evs(2 * np.pi / 3, labels=[l[::-1] for l in LABELS]),  # labels read q0-first
    "B": evs(np.pi / 3),                                       # half-angle reading of ry
    "C": evs(2 * np.pi / 3, flip_q1=False),                    # x(1) overlooked
    "D": evs(-2 * np.pi / 3),                                  # ry sense reversed
    "E": evs(2 * np.pi / 3),                                   # the stem code
}

for key, values in VARIANTS.items():
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(LABELS, values, color="0.55", edgecolor="black")
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("observable")
    ax.set_ylabel("expectation value")
    fig.savefig(f"s6-q051-{key}.svg")
