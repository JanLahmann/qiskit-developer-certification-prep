# Figure for s1-q065: the mpl drawing of a CX-RZ-CX circuit. The proof script
# hardcodes the SAME gate list (STEM) and scores five PauliEvolutionGate
# candidates against it — keep the two definitions in sync (ledger rule:
# figure content == proof target). The assert is the sync check: the drawn
# circuit must equal exp(-i*pi/6*ZZ) or the render fails.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Operator, SparsePauliOp

STEM = [("cx", 0, 1), ("rz", np.pi / 3, 1), ("cx", 0, 1)]

qc = QuantumCircuit(2)
for name, *args in STEM:
    getattr(qc, name)(*args)

ref = QuantumCircuit(2)
ref.append(PauliEvolutionGate(SparsePauliOp("ZZ"), time=np.pi / 6), [0, 1])
assert Operator(qc) == Operator(ref)

fig = qc.draw(output="mpl")
fig.savefig("s1-q065-stem.svg")
