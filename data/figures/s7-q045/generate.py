# Figure for s7-q045: the circuit a retrieved Sampler job ran; its classical
# register names become the DataBin field names. The proof script builds the
# SAME circuit and asserts the same REGISTERS / GATES literals — keep the two in
# sync (ledger rule: figure content == proof target). The asserts are the sync check.
# Runs under pipeline/render_figures.py's deterministic prelude.
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

REGISTERS = [("flag", 1), ("out", 2)]
GATES = [("h", (0,), ()), ("cx", (0, 1), ()), ("ry", (2,), ()),
         ("measure", (2,), (0,)), ("measure", (0,), (1,)), ("measure", (1,), (2,))]

q = QuantumRegister(3, "q")
flag = ClassicalRegister(1, "flag")
out = ClassicalRegister(2, "out")
qc = QuantumCircuit(q, flag, out)
qc.h(0)
qc.cx(0, 1)
qc.ry(0.6, 2)
qc.measure(2, flag[0])
qc.measure(0, out[0])
qc.measure(1, out[1])

assert [(r.name, r.size) for r in qc.cregs] == REGISTERS
drawn = [(ci.operation.name, tuple(qc.find_bit(x).index for x in ci.qubits),
          tuple(qc.find_bit(c).index for c in ci.clbits)) for ci in qc.data]
assert drawn == GATES, drawn

qc.draw(output="mpl").savefig("s7-q045-stem.svg")
