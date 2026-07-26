# Figures for s8-q029: mpl renderings of five OpenQASM 2 programs, each loaded
# with QuantumCircuit.from_qasm_str so that every option is a genuine loader
# output (no hand-built circuits, so the drawer conventions are identical
# everywhere). The proof script loads THE SAME five programs and compares the
# structure the drawer receives — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: parsing only, no sampling.
from qiskit import QuantumCircuit

HEADER = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'

PROGRAMS = {
    # A — the stem program, verbatim.
    "A": HEADER + "qreg a[2];\ncreg m[2];\nh a[0];\ncx a[0], a[1];\n"
                  "measure a -> m;\n",
    # B — register names believed to be discarded in favour of q/c defaults.
    "B": HEADER + "qreg q[2];\ncreg c[2];\nh q[0];\ncx q[0], q[1];\n"
                  "measure q -> c;\n",
    # C — register-wide measure believed to reverse the bit order.
    "C": HEADER + "qreg a[2];\ncreg m[2];\nh a[0];\ncx a[0], a[1];\n"
                  "measure a[0] -> m[1];\nmeasure a[1] -> m[0];\n",
    # D — cx operands read as (target, control).
    "D": HEADER + "qreg a[2];\ncreg m[2];\nh a[0];\ncx a[1], a[0];\n"
                  "measure a -> m;\n",
    # E — register-wide measure believed to measure only the first qubit.
    "E": HEADER + "qreg a[2];\ncreg m[2];\nh a[0];\ncx a[0], a[1];\n"
                  "measure a[0] -> m[0];\n",
}

for key, program in PROGRAMS.items():
    fig = QuantumCircuit.from_qasm_str(program).draw(output="mpl")
    fig.savefig(f"s8-q029-{key}.svg")
