# Figures for s3-q065: mpl renderings of the stem circuit and its misconception
# variants. The proof script builds THE SAME variants (copy of the block below)
# and proves which one matches the stem code — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: fixed angles, no sampling, no transpiler randomness.
QID = "s3-q065"
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

theta = Parameter("theta")
phi = Parameter("phi")


def build(coef=2):
    qc = QuantumCircuit(2)
    qc.rx(theta, 0)
    qc.ry(coef * phi, 1)
    qc.cx(0, 1)
    return qc


VARIANTS = {
    "A": (lambda: build(coef=1).assign_parameters({phi: np.pi / 4}), {}),   # coefficient lost
    "B": (lambda: build().assign_parameters({phi: np.pi / 4}), {}),         # the stem code
    "C": (lambda: build().assign_parameters({phi: np.pi / 4, theta: np.pi / 4}), {}),  # value spread to all
    "D": (lambda: build(), {}),                                             # nothing substituted
}

for key, (make, kwargs) in VARIANTS.items():
    fig = make().draw(output="mpl", **kwargs)
    fig.savefig(f"{QID}-{key}.svg")
