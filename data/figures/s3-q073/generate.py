# Figures for s3-q073: mpl drawings of four switch-on-register circuits that
# differ in how the case values and the DEFAULT body are laid out. The proof
# builds THE SAME four circuits (variant() below) and compares each one's mpl
# SVG with the rendering of the stem code.
# SYNC DUTY: keep variant() identical in the proof script.
# A3 2026-10-16: preparation and bodies moved off the feedforward guide's
# switch example shape (H on both qubits, X/Z bodies) to ry/sx and Y/S.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


def variant(key):
    qr = QuantumRegister(2, "q")
    cr = ClassicalRegister(2, "c")
    qc = QuantumCircuit(qr, cr)
    qc.ry(1.2, 0)
    qc.sx(1)
    qc.measure([0, 1], [0, 1])
    if key == "A":    # case(1, 2) split into two separate case blocks
        with qc.switch(cr) as case:
            with case(1):
                qc.y(0)
            with case(2):
                qc.y(0)
            with case(case.DEFAULT):
                qc.s(1)
    elif key == "B":  # case(1, 2) read like range(1, 2): value 1 only
        with qc.switch(cr) as case:
            with case(1):
                qc.y(0)
            with case(case.DEFAULT):
                qc.s(1)
    elif key == "C":  # the stem code: one case block listing 1, 2
        with qc.switch(cr) as case:
            with case(1, 2):
                qc.y(0)
            with case(case.DEFAULT):
                qc.s(1)
    elif key == "D":  # C-style fall-through: default body runs after the switch
        with qc.switch(cr) as case:
            with case(1, 2):
                qc.y(0)
        qc.s(1)
    return qc


for key in "ABCD":
    fig = variant(key).draw(output="mpl")
    fig.savefig(f"s3-q073-{key}.svg")
