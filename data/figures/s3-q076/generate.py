# Figures for s3-q076: mpl drawings of four rearrangements of the same
# two-qubit circuit (reversed gate order, inverse, reversed wires, flipped CX).
# The proof builds THE SAME four circuits (variant() below) and compares each
# one's mpl SVG with the rendering of the stem code's qc.reverse_ops().
# SYNC DUTY: keep variant() identical in the proof script.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit


def variant(key):
    qc = QuantumCircuit(2)
    if key == "A":    # confused with inverse(): order reversed AND each gate daggered
        qc.tdg(1)
        qc.cx(0, 1)
        qc.sdg(0)
        qc.h(0)
    elif key == "B":  # confused with reverse_bits(): wires flipped, order kept
        qc.h(1)
        qc.s(1)
        qc.cx(1, 0)
        qc.t(0)
    elif key == "C":  # reversal assumed to swap the CX's control and target too
        qc.t(1)
        qc.cx(1, 0)
        qc.s(0)
        qc.h(0)
    elif key == "D":  # what reverse_ops() returns: same gates, reverse order
        qc.t(1)
        qc.cx(0, 1)
        qc.s(0)
        qc.h(0)
    return qc


for key in "ABCD":
    fig = variant(key).draw(output="mpl")
    fig.savefig(f"s3-q076-{key}.svg")
