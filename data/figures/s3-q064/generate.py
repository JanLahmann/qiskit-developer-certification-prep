# Figures for s3-q064: mpl renderings of the stem circuit and its misconception
# variants. The proof script builds THE SAME variants (copy of the block below)
# and proves which one matches the stem code — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: fixed angles, no sampling, no transpiler randomness.
QID = "s3-q064"
from qiskit import QuantumCircuit


def build(front=True, mapping=(1, 0)):
    base = QuantumCircuit(2)
    base.h(0)
    base.cx(0, 1)
    prep = QuantumCircuit(2)
    prep.x(0)
    prep.s(1)
    return base.compose(prep, qubits=list(mapping), front=front)


VARIANTS = {
    "A": (lambda: build(), {}),                                # the stem code
    "B": (lambda: build(front=False), {}),                     # front= ignored
    "C": (lambda: build(mapping=(0, 1)), {}),                  # qubits= ignored
    "D": (lambda: build(front=False, mapping=(0, 1)), {}),     # both ignored
}

for key, (make, kwargs) in VARIANTS.items():
    fig = make().draw(output="mpl", **kwargs)
    fig.savefig(f"{QID}-{key}.svg")
