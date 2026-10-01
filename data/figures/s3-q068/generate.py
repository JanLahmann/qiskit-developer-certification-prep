# Figures for s3-q068: mpl renderings of the stem circuit and its misconception
# variants. The proof script builds THE SAME variants (copy of the block below)
# and proves which one matches the stem code — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: fixed angles, no sampling, no transpiler randomness.
QID = "s3-q068"
from qiskit import QuantumCircuit

sub = QuantumCircuit(2, name="ent")
sub.h(0)
sub.cx(0, 1)


def build(mapping=(2, 0)):
    qc = QuantumCircuit(3)
    qc.append(sub.to_gate(), list(mapping))
    qc.swap(0, 1)
    return qc


VARIANTS = {
    "A": (lambda: build().decompose(gates_to_decompose=["ent"]), {}),   # only the custom gate opened
    "B": (lambda: build((0, 2)).decompose(), {}),                        # append order ignored
    "C": (lambda: build().decompose(reps=2), {}),                        # two levels deep
    "D": (lambda: build().decompose(gates_to_decompose=["swap"]), {}),  # custom gate left boxed
    "E": (lambda: build().decompose(), {}),                              # the stem code
}

for key, (make, kwargs) in VARIANTS.items():
    fig = make().draw(output="mpl", **kwargs)
    fig.savefig(f"{QID}-{key}.svg")
