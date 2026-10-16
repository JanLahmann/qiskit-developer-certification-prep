# Figures for s2-q040: mpl renderings of the stem circuit and four
# misconception variants. The proof script constructs THE SAME five circuits
# and proves which one matches the stem code (SVG byte-identity + structure) —
# keep the two definitions in sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


def base():
    qr = QuantumRegister(3, "q")
    cr = ClassicalRegister(2, "m")
    qc = QuantumCircuit(qr, cr)
    qc.sx(0)
    qc.cx(0, 2)
    qc.measure([0, 2], cr)
    return qc, cr


def v_single_bit():  # A — reads the register test (cr, 2) as a test of bit m_1
    qc, cr = base()
    with qc.if_test((cr[1], 1)):
        qc.z(1)
    return qc


def v_unconditional():  # B — drops the conditional box entirely
    qc, _ = base()
    qc.z(1)
    return qc


def v_value_one():  # C — bit-order misreading of the tested integer (0x1)
    qc, cr = base()
    with qc.if_test((cr, 1)):
        qc.z(1)
    return qc


def v_correct():  # D — the stem code, verbatim
    qc, cr = base()
    with qc.if_test((cr, 2)):
        qc.z(1)
    return qc


def v_wrong_target():  # E — Z lands on q2, the qubit measured into m_1
    qc, cr = base()
    with qc.if_test((cr, 2)):
        qc.z(2)
    return qc


VARIANTS = {
    "A": v_single_bit,
    "B": v_unconditional,
    "C": v_value_one,
    "D": v_correct,
    "E": v_wrong_target,
}

for key, make in VARIANTS.items():
    fig = make().draw(output="mpl")
    fig.savefig(f"s2-q040-{key}.svg")
