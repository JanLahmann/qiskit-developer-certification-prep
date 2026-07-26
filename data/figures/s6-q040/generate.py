# Figures for s6-q040: five curves of an expectation value against the swept
# RY angle — the exact one the stem code computes plus four misconception
# variants. The proof script recomputes THE SAME five series and compares them
# point by point — keep the two definitions in sync (ledger rule: figure
# variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp, Statevector

THETA = Parameter("theta")
ANGLES = np.linspace(0.0, 2 * np.pi, 9)

QC = QuantumCircuit(1)
QC.ry(THETA, 0)
ESTIMATOR = StatevectorEstimator()


def evs(label, values):
    pub = (QC, SparsePauliOp(label), np.asarray(values).reshape(-1, 1))
    return np.asarray(ESTIMATOR.run([pub]).result()[0].data.evs)


def amplitudes():
    return np.array([
        float(np.real(Statevector(QC.assign_parameters([a])).data[0]))
        for a in ANGLES
    ])


VARIANTS = {
    "A": evs("X", ANGLES),        # the observable read as X
    "B": evs("Z", ANGLES),        # the stem code, verbatim
    "C": amplitudes(),            # the |0> amplitude mistaken for <Z>
    "D": -evs("Z", ANGLES),       # the sign of the observable flipped
    "E": evs("Z", 2 * ANGLES),    # theta mistaken for the half-angle
}

for key, series in VARIANTS.items():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(ANGLES, series, marker="o")
    ax.set_xlabel("theta")
    ax.set_ylabel("expectation value")
    fig.savefig(f"s6-q040-{key}.svg")
