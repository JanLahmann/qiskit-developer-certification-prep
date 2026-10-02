# Figure for s5-q053: the circuit the stem code samples (mid-circuit measure,
# reset and reuse of qubit 1). The proof script rebuilds qc from the SAME
# GATES literal and asserts the same structure — keep the two in sync
# (ledger rule: figure content == proof target). The assert is the sync check.
# Runs under pipeline/render_figures.py's deterministic prelude.
from qiskit import QuantumCircuit

GATES = [("h", (0,), ()), ("cx", (0, 1), ()), ("measure", (1,), (0,)),
         ("reset", (1,), ()), ("measure", (1,), (2,)), ("measure", (0,), (1,))]

qc = QuantumCircuit(2, 3)
qc.h(0)
qc.cx(0, 1)
qc.measure(1, 0)
qc.reset(1)
qc.measure(1, 2)
qc.measure(0, 1)

drawn = [(ci.operation.name, tuple(qc.find_bit(q).index for q in ci.qubits),
          tuple(qc.find_bit(c).index for c in ci.clbits)) for ci in qc.data]
assert drawn == GATES, drawn

qc.draw(output="mpl").savefig("s5-q053-stem.svg")
