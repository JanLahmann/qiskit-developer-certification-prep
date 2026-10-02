# Figure for s8-q031: a dynamic circuit whose OpenQASM 3 export the question asks
# about. The proof script rebuilds qc from the SAME GATES literal and asserts the
# same structure — keep the two in sync (ledger rule: figure content == proof
# target). The assert is the sync check.
# Runs under pipeline/render_figures.py's deterministic prelude.
from qiskit import QuantumCircuit

# (name, qubits, clbits, condition) in program order
GATES = [("h", (0,), (), None), ("measure", (0,), (0,), None),
         ("if_else", (1,), (0,), (0, 0)), ("measure", (1,), (1,), None)]

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.measure(0, 0)
with qc.if_test((qc.clbits[0], 0)):
    qc.x(1)
qc.measure(1, 1)


def sig(circ):
    out = []
    for ci in circ.data:
        op = ci.operation
        cond = None
        if op.name == "if_else":
            bit, val = op.condition
            cond = (circ.find_bit(bit).index, int(val))
        out.append((op.name, tuple(circ.find_bit(q).index for q in ci.qubits),
                    tuple(circ.find_bit(c).index for c in ci.clbits), cond))
    return out


assert sig(qc) == GATES, sig(qc)
qc.draw(output="mpl").savefig("s8-q031-stem.svg")
