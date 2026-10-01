# Figures for s3-q063: mpl renderings of the stem circuit and its misconception
# variants. The proof script builds THE SAME variants (copy of the block below)
# and proves which one matches the stem code — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: fixed angles, no sampling, no transpiler randomness.
QID = "s3-q063"
from qiskit import QuantumCircuit, QuantumRegister


def build(anc_first=False, h_on=1, reversed_cx=False):
    data = QuantumRegister(2, "d")
    anc = QuantumRegister(1, "anc")
    qc = QuantumCircuit(anc, data) if anc_first else QuantumCircuit(data, anc)
    qc.h(data[h_on])
    if reversed_cx:
        qc.cx(anc[0], data[h_on])
    else:
        qc.cx(data[h_on], anc[0])
    return qc


VARIANTS = {
    "A": (lambda: build(anc_first=True), {}),        # register order swapped
    "B": (lambda: build(h_on=0), {}),                # d[1] read as the first wire
    "C": (lambda: build(reversed_cx=True), {}),      # control/target swapped
    "D": (lambda: build(), {"reverse_bits": True}),  # highest index drawn on top
    "E": (lambda: build(), {}),                      # the stem code, verbatim
}

for key, (make, kwargs) in VARIANTS.items():
    fig = make().draw(output="mpl", **kwargs)
    fig.savefig(f"{QID}-{key}.svg")
