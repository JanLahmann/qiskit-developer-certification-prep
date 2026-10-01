# Stem figure for s6-q047: mpl drawing of the 3-qubit circuit `qc`. The proof
# script rebuilds THE SAME circuit (ledger rule: figure content == proof
# target) and the GATES literal below is asserted in both files.
# Runs under pipeline/render_figures.py's deterministic prelude.
from qiskit import QuantumCircuit

GATES = [("h", (0,)), ("cx", (0, 1)), ("z", (0,)), ("x", (2,))]

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.z(0)
qc.x(2)

seen = [(i.operation.name, tuple(qc.find_bit(q).index for q in i.qubits)) for i in qc.data]
assert seen == GATES, seen
qc.draw("mpl").savefig("s6-q047-stem.svg")
