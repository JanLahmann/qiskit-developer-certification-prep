# Figures for s2-q044: mpl renderings of the stem call and four misconception
# variants of it. The proof script builds THE SAME five (circuit, draw-kwargs)
# pairs and compares what the drawer lays out (wire order + gates per wire) —
# keep the two definitions in sync (ledger rule: figure variants == proof
# variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit


def stem_circuit():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 2)
    qc.t(2)
    return qc


VARIANTS = {
    # A — the stem call, verbatim: the drawer flips the wire order.
    "A": (stem_circuit(), {"reverse_bits": True}),
    # B — reverse_bits treated as a no-op for the mpl renderer.
    "B": (stem_circuit(), {}),
    # C — "reverse the bits" read as "reverse the instructions".
    "C": (stem_circuit().reverse_ops(), {}),
    # D — "reverse the bits" read as "invert the circuit".
    "D": (stem_circuit().inverse(), {}),
    # E — the draw argument confused with the QuantumCircuit method.
    "E": (stem_circuit().reverse_bits(), {}),
}

for key, (circ, kwargs) in VARIANTS.items():
    fig = circ.draw(output="mpl", **kwargs)
    fig.savefig(f"s2-q044-{key}.svg")
