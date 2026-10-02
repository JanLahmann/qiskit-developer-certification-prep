# Figures for s1-q068: mpl drawings of five two-qubit circuits that differ only
# in the single-qubit operation placed between the H and the CX — the picture a
# reader expects for TGate().power(3). The proof builds THE SAME five circuits
# and compares each one's mpl SVG with the rendering of the stem code.
# SYNC DUTY: keep variant() identical in the proof script.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PhaseGate, RZGate, TdgGate, TGate, UnitaryGate
from qiskit.quantum_info import Operator


def variant(key):
    qc = QuantumCircuit(2)
    qc.h(0)
    if key == "A":    # power read as repetition: three T boxes
        for _ in range(3):
            qc.append(TGate(), [0])
    elif key == "B":  # what TGate().power(3) returns: a phase gate P(3*pi/4)
        qc.append(PhaseGate(3 * np.pi / 4), [0])
    elif key == "C":  # T^3 confused with T-dagger (as S^3 = S-dagger)
        qc.append(TdgGate(), [0])
    elif key == "D":  # phase gate confused with RZ of the same angle
        qc.append(RZGate(3 * np.pi / 4), [0])
    elif key == "E":  # the generic Gate.power path: a labelled UnitaryGate
        qc.append(UnitaryGate(Operator(TGate()).power(3), label="t^3"), [0])
    qc.cx(0, 1)
    return qc


for key in "ABCDE":
    fig = variant(key).draw(output="mpl")
    fig.savefig(f"s1-q068-{key}.svg")
