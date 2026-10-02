# Figures for s3-q075: mpl drawings of four candidate level-1 outputs for a
# circuit with a ONE-wire barrier between two inverse pairs. No coupling map and
# no basis are given, so the real output carries no layout and draws with plain
# q_0/q_1 labels — the hand-built variants below draw in the same style. The
# proof builds THE SAME four circuits (variant() below), runs the stem pass
# manager, and compares every variant's mpl SVG with the real output's.
# SYNC DUTY: keep variant() identical in the proof script.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate


def variant(key):
    qc = QuantumCircuit(2)
    if key == "A":    # real level-1 output: X pair cancelled, H pair kept by the barrier
        qc.h(0)
        qc.barrier(0)
        qc.h(0)
    elif key == "B":  # barrier ignored: both pairs cancelled
        pass
    elif key == "C":  # barrier taken to freeze the whole circuit: nothing cancelled
        qc.h(0)
        qc.x(1)
        qc.barrier(0)
        qc.h(0)
        qc.x(1)
    elif key == "D":  # kept H gates assumed re-synthesised as U gates
        qc.append(UGate(np.pi / 2, 0, np.pi), [0])
        qc.barrier(0)
        qc.append(UGate(np.pi / 2, 0, np.pi), [0])
    qc.cx(0, 1)
    return qc


for key in "ABCD":
    fig = variant(key).draw(output="mpl")
    fig.savefig(f"s3-q075-{key}.svg")
