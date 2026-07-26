# Figures for s2-q040: mpl renderings of the stem circuit and four
# misconception variants. The proof script constructs THE SAME five circuits
# and proves which one matches the stem code structurally — keep the two
# definitions in sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


def base():
    qr = QuantumRegister(2, "q")
    cr = ClassicalRegister(1, "c")
    return QuantumCircuit(qr, cr), cr


def v_phantom_else():  # A — imagines if_test always draws an If/Else pair
    qc, cr = base()
    qc.h(0)
    qc.measure(0, 0)
    with qc.if_test((cr, 1)) as else_:
        qc.x(1)
    with else_:
        qc.z(1)
    return qc


def v_unconditional():  # B — drops the conditional box entirely
    qc, _ = base()
    qc.h(0)
    qc.measure(0, 0)
    qc.x(1)
    return qc


def v_correct():  # C — the stem code, verbatim
    qc, cr = base()
    qc.h(0)
    qc.measure(0, 0)
    with qc.if_test((cr, 1)):
        qc.x(1)
    return qc


def v_wrong_target():  # D — X lands on the measured qubit q0
    qc, cr = base()
    qc.h(0)
    qc.measure(0, 0)
    with qc.if_test((cr, 1)):
        qc.x(0)
    return qc


def v_no_h():  # E — forgets the H state preparation
    qc, cr = base()
    qc.measure(0, 0)
    with qc.if_test((cr, 1)):
        qc.x(1)
    return qc


VARIANTS = {
    "A": v_phantom_else,
    "B": v_unconditional,
    "C": v_correct,
    "D": v_wrong_target,
    "E": v_no_h,
}

for key, make in VARIANTS.items():
    fig = make().draw(output="mpl")
    fig.savefig(f"s2-q040-{key}.svg")
