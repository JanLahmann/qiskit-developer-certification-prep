# Figures for s8-q032: mpl renderings of four OpenQASM 2 programs, each loaded
# with QuantumCircuit.from_qasm_str so every option is a genuine loader output
# (identical drawer conventions everywhere). The proof script loads THE SAME
# four programs — keep PROGRAMS identical in both files
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude; parsing only.
from qiskit import QuantumCircuit

HEADER = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'
GATE = "gate mix a, b { h a; cx a, b; }\n"

PROGRAMS = {
    # A — gate definition believed to be inlined at load time.
    "A": HEADER + "qreg q[3];\nh q[2];\ncx q[2], q[0];\n",
    # B — operands of the call read in the opposite order.
    "B": HEADER + GATE + "qreg q[3];\nmix q[0], q[2];\n",
    # C — inlined AND formal parameters bound by register order.
    "C": HEADER + "qreg q[3];\nh q[0];\ncx q[0], q[2];\n",
    # D — the stem program, verbatim.
    "D": HEADER + GATE + "qreg q[3];\nmix q[2], q[0];\n",
}

for key, program in PROGRAMS.items():
    QuantumCircuit.from_qasm_str(program).draw(output="mpl").savefig(f"s8-q032-{key}.svg")
